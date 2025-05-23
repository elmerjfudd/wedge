from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
import argparse
import config
import logging
import os
import pandas as pd
import parser
import stats
import time
import viz

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s [%(levelname)s] %(message)s",
)

def process_techniques(data_path, language):
  """
  Process JSON files for each technique and build in-memory data structures
  """
  technique_data = {}
  for tech, tech_folder in config.TECHNIQUES.items():
    tech_dir = os.path.join(data_path, tech_folder)
    logging.info("Processing technique %s from directory %s", tech, tech_dir)
    rt_data, ic_data = parser.build_data_structure_for_technique(tech_dir, language)
    technique_data[tech] = {"rt": rt_data, "ic": ic_data}
    logging.info("Finished processing technique %s with %d total entries", 
                 tech, len(technique_data[tech]["rt"]))
  return technique_data

def keep_common_entries(technique_data):
  """
  Filter individual (problem id, solution id) entries that 
  **do not** appear in all techniques (NOTE: This indicates one of the 
  strategy did not successfuly generated enough tests for that entry) 
  """
  if not technique_data:
    return {}

  techniques = list(technique_data)
  max_k = max(config.TOP_K_VALUES)

  rt_common = set.intersection(
    *(set(technique_data[tech]["rt"]) for tech in techniques)
  )
  ic_common = set.intersection(
    *(set(technique_data[tech]["ic"]) for tech in techniques)
  )
  common_keys = rt_common & ic_common

  # keep only those with >= max_k tests in both rt & ic
  def has_enough_tests(key: str) -> bool:
    for tech in techniques:
      dt = technique_data[tech]["rt"].get(key, {})
      if len(technique_data[tech]["rt"].get(key, {})) < max_k:
        return False
      if len(technique_data[tech]["ic"].get(key, {})) < max_k:
        return False
    return True

  filtered = {k for k in common_keys if has_enough_tests(k)}
  logging.info("Total number of common keys: %d", len(filtered))

  return {
    tech: {
      "rt": {k: technique_data[tech]["rt"][k] for k in filtered},
      "ic": {k: technique_data[tech]["ic"][k] for k in filtered},
    }
    for tech in techniques
  }

def _aggregate_per_individual_technique(args):
  """
  Aggregate stats for each technique for each top-K value and write 
  per-technique CSV files
  """
  tech, data_rt, data_ic, top_k, output_csv_dir = args

  agg_results = stats.compute_aggregate_stats_for_structure(data_rt, data_ic, top_k)

  csv_filename = f"{tech}-top{top_k}inputs.csv"
  csv_output_path = os.path.join(output_csv_dir, csv_filename)
  parser.write_csv(agg_results["aggregated_stats"], csv_output_path)

  return (top_k, tech, agg_results)

def aggregate_and_write_csv(technique_data, output_csv_dir):
  """
  Aggregate stats for each technique for each top-K value and write 
  per-technique CSV files
  """
  global_stats_by_topk = {k: {} for k in config.TOP_K_VALUES}
  tasks = []
  for top_k in config.TOP_K_VALUES:
    for tech in config.TECHNIQUES:
      data_rt = technique_data[tech]["rt"]
      data_ic = technique_data[tech]["ic"]
      tasks.append((tech, data_rt, data_ic, top_k, output_csv_dir))

  max_workers = max(1, (int)((os.cpu_count() or 2) * 0.75))
  with ProcessPoolExecutor(max_workers=max_workers) as executor:
    jobs = [executor.submit(_aggregate_per_individual_technique, t) for t in tasks]
    for job in as_completed(jobs):
      top_k, tech, agg_results = job.result()
      global_stats_by_topk[top_k][tech] = agg_results

  return global_stats_by_topk

def build_unified_stats(global_stats_by_topk):
  """
  Build a unified dictionary keyed by 'problemID-solutionID' from all techniques.
  Only include solution keys that exist for all techniques
  """
  unified_stats = defaultdict(lambda: defaultdict(dict))
  
  for top_k in config.TOP_K_VALUES:
    common_solution_keys = None
    
    for tech, tech_folder in config.TECHNIQUES.items():
      agg_results = global_stats_by_topk[top_k][tech]
      sol_keys = set(agg_results["aggregated_stats"].keys())
      if common_solution_keys is None:
        common_solution_keys = sol_keys
      else:
        common_solution_keys = common_solution_keys.intersection(sol_keys)
    
    if not common_solution_keys:
      continue
    
    for tech, tech_folder in config.TECHNIQUES.items():
      agg_results = global_stats_by_topk[top_k][tech]
      for solution_key in common_solution_keys:
        stats = agg_results["aggregated_stats"][solution_key]
        unified_stats[solution_key][tech][top_k] = {
          "rt": {
            "avg": stats["running_time"]["avg_of_top_k_means"],
            "median": stats["running_time"]["median_of_top_k_means"],
            "cv": stats["running_time"]["avg_of_top_k_cvs"]
          },
          "ic": {
            "avg": stats["instruction_count"]["avg_of_top_k_means"],
            "median": stats["instruction_count"]["median_of_top_k_means"],
            "cv": stats["instruction_count"]["avg_of_top_k_cvs"]
          }
        }
  
  logging.info("Unified stats structure built with %d solutions", len(unified_stats))
  return unified_stats

def generate_histograms(unified_stats, output_plot_dir):
  """
  For each top-K value and each overlay technique, generate histograms 
  comparing techniques
  """
  baseline = config.BASELINE_TECHNIQUE

  for top_k in config.TOP_K_VALUES:
    for overlay in list(config.TECHNIQUES):
      if overlay == config.REFERENCE_TECHNIQUE or overlay == config.BASELINE_TECHNIQUE:
        continue
      data_dict = {}
      for tech in (baseline, overlay):
        data_dict[tech] = {
          sol_key: sol_data[tech][top_k]["ic"]["avg"]
          for sol_key, sol_data in unified_stats.items()
          if tech in sol_data and top_k in sol_data[tech]
        }

      if set(data_dict) == {baseline, overlay}:
        scheme = None
        colors = config.CUSTOM_2_COLOR_SCHEME
        pdf = os.path.join(output_plot_dir, 
                            f"histogram_{baseline}_vs_{overlay}_top{top_k}.pdf")
        viz.generate_histogram(
          data_dict,
          baseline_label=baseline,
          overlay_label=overlay,
          output_pdf_name=pdf,
          legend=False,
          x_label="Normalized Ratio (%)",
          y_label="# of programs (log scale)",
          **({"color_scheme": scheme} if scheme else {"custom_colors": colors})
        )
        logging.info("Histogram: %s", pdf)
      else:
        logging.error("Skipping histogram %s vs %s @ top-%d", baseline, overlay, top_k)

def main():
  parser_arg = argparse.ArgumentParser()
  parser_arg.add_argument("--data-path", required=True,
        help="Directory with JSON files organized by technique subdirectories.")
  parser_arg.add_argument("--summaries-out-path", required=True,
        help="Directory to stat summaries (plots, tables, CSVs).")
  parser_arg.add_argument("--language", default="cpp",
        help="Programming language filter (default: cpp).")
  args = parser_arg.parse_args()

  # Create output directories
  summary_tables_path = os.path.join(args.summaries_out_path, "tables/")
  os.makedirs(summary_tables_path, exist_ok=True)
  summary_plots_path = os.path.join(args.summaries_out_path, "plots/")
  os.makedirs(summary_plots_path, exist_ok=True)
  summary_csvs_path = os.path.join(args.summaries_out_path, "csvs/")
  os.makedirs(summary_csvs_path, exist_ok=True)

  t0 = time.perf_counter()
  # Parse JSON files for all problems and all teqhnicues
  technique_data = process_techniques(args.data_path, args.language)
  logging.info("[TIMING] JSON parsing: %.2fs", time.perf_counter() - t0)

  t0 = time.perf_counter()
  # Keep only those entries for which all techniques successfully generated enough tests
  common_data = keep_common_entries(technique_data)
  logging.info("Number of solutions where all techniques generate inputs: %d", 
         len(common_data[config.BASELINE_TECHNIQUE]["rt"]))

  # Aggregate statistics and write CSV files
  global_stats_by_topk = aggregate_and_write_csv(common_data, summary_csvs_path)
  logging.info("[TIMING] In-memory data structure generation and CSV write out: %.2fs", 
         time.perf_counter() - t0)

  # Compute slowdown relative to the reference technique
  slowdown = stats.compute_slowdown_stats_for_topk(
    global_stats_by_topk, 
    config.REFERENCE_TECHNIQUE, 
    config.TECHNIQUES, 
    max(config.TOP_K_VALUES)
  )
  
  t0 = time.perf_counter()
  # Build unified stats structure.
  unified_stats = build_unified_stats(global_stats_by_topk)
  logging.info("[TIMING] In-memory unified data structure for statistics: %.2fs", 
         time.perf_counter() - t0)

  # Generate histogram plot
  generate_histograms(unified_stats, summary_plots_path)

  # Generate tables
  table_file = os.path.join(summary_tables_path, "table_efficiency_baselines.tex")
  viz.generate_efficiency_tables(global_stats_by_topk, unified_stats, config.BASELINES, table_file)
  logging.info("Generated efficiency tables (baselines): %s", table_file)
  table_file = os.path.join(summary_tables_path, "table_efficiency_ablations.tex")
  viz.generate_efficiency_tables(global_stats_by_topk, unified_stats, config.ABLATIONS, table_file)
  logging.info("Generated efficiency tables (ablations): %s", table_file)
  table_file = os.path.join(summary_tables_path, "table_histogram.tex")
  viz.generate_histogram_table(unified_stats, table_file)
  logging.info("Generated histogram table: %s", table_file)
  viz.generate_slowdown_tables(slowdown)
  logging.info("Generated slowdown table")

if __name__ == "__main__":
  main()
