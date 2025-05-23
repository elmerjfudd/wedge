# Case Studies

We provide a list of the top 25 most complex (combined \# tokens in the LLM plain-language description and checker LoCs) performance-characterizing constraints synthesized by WEDGE. To read the entire LLM conversation and inspect the plain-language pc-constraints as well as the C++ generated checkers, users should navigate to each directory path individually.

### 1. 63_B/metadata/synthesized_constraints/solutions_0331/private_tests_011_private_tests_016/conversations.txt
* **"Equal rank values** invariant: "If the number of soldiers `n` approaches the upper constraint and their ranks start off as the minimal possible rank, redundant set operations and data updates amplify the program’s execution time."
```cpp
void check_minimal_ranks_with_large_n_invariant(int n, const vector<int>& ranks) {
    int uniqueRanks = std::set<int>(ranks.begin(), ranks.end()).size();
    if (n == 100 && uniqueRanks == 1 && ranks.front() == 1) {
        cerr << "Warning: Performance bottleneck condition triggered - minimal ranks with maximum soldiers." << endl;
        abort();
    }
}
```

### 2. 546_C/metadata/synthesized_constraints/solutions_0567/private_tests_052_generated_tests_012/conversations.txt
* **Cycles** invariant:
```cpp
// Check if the queue configurations have repeated, indicating a cycle
void check_cycle_invariant(const queue<int>& r1, const queue<int>& r2, unordered_set<string>& seenConfigurations) {
    string config;
    auto copy1 = r1, copy2 = r2;
    while (!copy1.empty()) {
        config += to_string(copy1.front()) + ",";
        copy1.pop();
    }
    config += "|";
    while (!copy2.empty()) {
        config += to_string(copy2.front()) + ",";
        copy2.pop();
    }
    
    if (seenConfigurations.find(config) != seenConfigurations.end()) {
        cerr << "Warning: Cycle detected - potential infinite loop!" << endl;
        abort();
    }
    seenConfigurations.insert(config);
}
```

* **Cards balanced** invariant:
```cpp
// Check if neither player can win quickly due to balanced card strength
void check_balance_invariant(const queue<int>& r1, const queue<int>& r2) {
    int max1 = *max_element(r1.front(), r1.back());
    int max2 = *max_element(r2.front(), r2.back());
    if (abs(max1 - max2) <= 1) { // Arbitrarily chosen threshold for similar max strength
        cerr << "Warning: Balanced card strength - prolonged game possible!" << endl;
        abort();
    }
}
```

### 3. 1182_E/metadata/synthesized_constraints/solutions_0029/private_tests_025_generated_tests_020/conversations.txt
* **Factorization** invariant:
```cpp
void check_factorization_invariant(long long num) {
    // Check for large prime factors or the number itself being a large prime
    for (long long i = 2; i * i <= num; i++) {
        if (num % i == 0) {
            int factor_count = 0;
            while (num % i == 0) {
                num /= i;
                factor_count++;
            }
            if (factor_count > 10) { // Arbitrary threshold for "complex" factorization
                std::cerr << "Warning: Factorization invariant triggered - too many factors for a number!" << std::endl;
                abort();
            }
        }
    }
    if (num > 1) { // num is a prime greater than sqrt of the original number
        if (num > 1e9) { // Arbitrary threshold for large primes
            std::cerr << "Warning: Factorization invariant triggered - number has large prime factor!" << std::endl;
            abort();
        }
    }
}
```

### 4. 731_F/metadata/synthesized_constraints/solutions_0179/generated_tests_003_generated_tests_010/conversations.txt
* **Divisors composition** invariant:
```cpp
// Check if many cards share small common divisors
void check_divisibility_invariant(const unordered_map<int, int>& cardPowers) {
    int commonDivisorCount = 0;
    for (const auto& power : cardPowers) {
        if (power.second > 5) { // Threshold for common frequency
            commonDivisorCount++;
        }
    }
    if (commonDivisorCount > 10) { // Threshold for number of common divisors
        cerr << "Warning: Performance bottleneck condition triggered due to many shared divisors!" << endl;
        abort();
    }
}
```

### 5. 1165_F1/metadata/synthesized_constraints/solutions_0204/generated_tests_013_generated_tests_068/conversations.txt
* **Special and remaining offers** invariant:
```cpp
// Checker for the invariant related to special offers usage
void check_special_offers_invariant(const std::vector<long long>& reqd, long long cur) {
    long long unmet = 0;
    for (auto r : reqd) {
        unmet += r;
    }
    if (unmet > cur) {
        std::cerr << "Warning: Performance bottleneck condition triggered due to inefficient use of special offers!" << std::endl;
        abort();
    }
}

// Checker for the invariant related to remaining transactions
void check_remaining_transactions_invariant(const std::vector<long long>& reqd) {
    long long total_unmet = 0;
    for (auto r : reqd) {
        total_unmet += r;
    }
    if (total_unmet > 500) { // Assuming half the total maximum sum as a rough threshold
        std::cerr << "Warning: Performance bottleneck condition triggered due to high number of remaining transactions!" << std::endl;
        abort();
    }
}
```

### 6. 1209_B/metadata/synthesized_constraints/solutions_0328/private_tests_012_public_tests_001/conversations.txt
* **Small values** invariant:
```cpp
void check_small_a_values(const vector<pair<int, int>>& p) {
    int small_a_count = 0;
    for (const auto& pair : p) {
        if (pair.first <= 2) {  // Assume 'small' a_i values are <= 2
            small_a_count++;
        }
    }
    if (small_a_count > 50) {  // Arbitrary threshold, adjust as needed
        cerr << "Warning: Performance bottleneck condition triggered - many lights have small 'a' values!" << endl;
        abort();
    }
}
```

* **Synchronized values** invariant:
```cpp
void check_synchronized_b_values(const vector<pair<int, int>>& p) {
    map<int, int> b_count;
    for (const auto& pair : p) {
        b_count[pair.second]++;
    }
    for (const auto& [b_value, count] : b_count) {
        if (count > 30) {  // Arbitrary threshold for synchronization
            cerr << "Warning: Performance bottleneck condition triggered - synchronized 'b' values!" << endl;
            abort();
        }
    }
}
```

### 7. 1260_D/metadata/synthesized_constraints/solutions_0253/generated_tests_033_generated_tests_026/conversations.txt
* **Range overlap** invariant:
```cpp
void check_trap_overlap_invariant(const vector<trap>& Traps, int x) {
    int count = 0;
    for (const auto& tr : Traps) {
        if (tr.d > x) {
            count++;
            if (count > 100) {
                cerr << "Warning: trap_overlap_invariant triggered - too many overlapping traps with high danger level" << endl;
                abort();
            }
        }
    }
}
```

* **High-density** invariant:
```cpp
void check_high_density_traps(const vector<trap>& Traps, int n) {
    vector<int> coverage(n + 2, 0);
    for (const auto& tr : Traps) {
        for (int i = tr.l; i <= tr.r; ++i) {
            coverage[i]++;
        }
    }
    for (int i = 0; i <= n; ++i) {
        if (coverage[i] > 10) {
            cerr << "Warning: high_density_traps invariant triggered - high trap coverage at position " << i << endl;
            abort();
        }
    }
}
```

### 8. 513_C/metadata/synthesized_constraints/solutions_0200/private_tests_010_generated_tests_054/conversations.txt
* **Overlapping Bid Ranges** invariant:
```cpp
// The program may enter a slow path if multiple companies have overlapping bid ranges, causing the nested loops to iterate extensively over possible bid values
void check_overlap_invariant(const vector<pair<int, int>>& ranges) {
    bool overlap_detected = false;
    int n = ranges.size();
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (!(ranges[i].second < ranges[j].first || ranges[j].second < ranges[i].first)) {
                overlap_detected = true;
                break;
            }
        }
        if (overlap_detected) break;
    }
    if (overlap_detected) {
        cerr << "Warning: overlap_invariant triggered - overlapping bid ranges" << endl;
        abort();
    }
}
```

### 9. 633_A/metadata/synthesized_constraints/solutions_0622/private_tests_039_generated_tests_036/conversations.txt
* **GCD** invariant:
```cpp
// Check if the greatest common divisor of a and b does not divide c
void check_gcd_invariant(int a, int b, int c) {
    if (c % __gcd(a, b) != 0) {
        cerr << "Warning: gcd_invariant triggered - gcd(a, b) does not divide c" << endl;
        abort();
    }

```

### 10. 583_D/metadata/synthesized_constraints/solutions_0083/private_tests_026_generated_tests_018/conversations.txt
* **Non-Reducing Dynamic Array Update** invariant:
```cpp
void check_dynamic_array_update_invariant(long long cur, long long prevCur, long long stabilityThreshold) {
    if (abs(cur - prevCur) < stabilityThreshold) {
        cerr << "Warning: Performance bottleneck due to unstable dynamic array updates triggered!" << endl;
        abort();
    }
}
```

### 11. 559_C/metadata/synthesized_constraints/solutions_0243/private_tests_002_private_tests_001/conversations.txt
* **Path enumeration** invariants:
```cpp
// Check for expensive path enumeration in specific arrangements
void check_complex_obstacle_arrangement(int h, int w, int n, int* blackCellRows, int* blackCellCols) {
    // An arbitrary check for a clustered arrangement in the center of a large board
    if (h * w > 5000000 && n < 20) {
        for (int i = 0; i < n; ++i) {
            if (blackCellRows[i] > h / 3 && blackCellRows[i] < 2 * h / 3 &&
                blackCellCols[i] > w / 3 && blackCellCols[i] < 2 * w / 3) {
                cerr << "Warning: Performance issue due to central clustered obstacles on large board!" << endl;
                abort();
            }
        }
    }
}
```

### 12. 469_B/metadata/synthesized_constraints/solutions_0328/generated_tests_010_private_tests_005/conversations.txt
* **Interval overlapping** invariant:
```cpp
// Check if there is a significant overlap potential due to wide shifts
void check_overlap_potential(const vector<pair<int, int>>& v, const vector<pair<int, int>>& v1, int l, int r) {
    for (const auto& intervalX : v1) {
        for (const auto& intervalZ : v) {
            if ((intervalX.first + r >= intervalZ.first && intervalX.second + l <= intervalZ.second) || 
                (intervalX.first + l <= intervalZ.second && intervalX.second + r >= intervalZ.first)) {
                cerr << "Warning: High overlap potential detected!" << endl;
                abort();
            }
        }
    }
```

### 13. 16_B/metadata/synthesized_constraints/solutions_0034/private_tests_025_generated_tests_017/conversations.txt
* **Match box** invariants:
```cpp
// Function to check the invariant where n is much larger than available matchboxes
void check_large_n_invariant(int n, int m, const vector<pair<int, int>>& v) {
    long long totalBoxes = 0;
    for (const auto& container : v) {
        totalBoxes += container.first;
    }
    if (n > 10 * totalBoxes) {
        cerr << "Warning: Performance bottleneck condition triggered - n is much larger than available matchboxes!" << endl;
        abort();
    }
}

// Function to check the invariant where there are insufficient matchboxes compared to n
void check_small_total_boxes_invariant(int n, int m, const vector<pair<int, int>>& v) {
    long long totalBoxes = 0;
    for (const auto& container : v) {
        totalBoxes += container.first;
    }
    if (totalBoxes < n / 10) {
        cerr << "Warning: Performance bottleneck condition triggered - insufficient matchboxes compared to n!" << endl;
        abort();
    }
```

### 14. 1003_A/metadata/synthesized_constraints/solutions_0871/generated_tests_002_generated_tests_037/conversations.txt
* **Repeating elements** invariant:
```cpp
void check_repeated_element_count(int n, const vector<int>& v) {
    unordered_map<int, int> frequency;
    for (int coin : v) {
        frequency[coin]++;
        if (frequency[coin] > n / 2) {
            cerr << "Warning: Performance bottleneck condition triggered due to high frequency of duplicate elements!" << endl;
            abort();
        }
    }
}
```

### 15. 543_A/metadata/synthesized_constraints/solutions_0017/generated_tests_013_generated_tests_015/conversations.txt
* **Input distribution** invariant:
```cpp
void check_bug_distribution(const vector<int>& V, int b) {
    int high_bug_programmers = 0;
    for (int bugs : V) {
        if (bugs > b / 4) {
            high_bug_programmers++;
        }
    }
    if (high_bug_programmers > V.size() / 3) {
        cerr << "Warning: Performance bottleneck condition triggered - high bug rates per line" << endl;
        abort();
    }
```

### 16. 1210_A/metadata/synthesized_constraints/solutions_0160/private_tests_028_generated_tests_054/conversations.txt
* **Graph structure** invariants:
```cpp
void check_high_degree_invariant(const vector<vector<int>>& graph, int n) {
    for (int i = 1; i <= n; ++i) {
        if (graph[i].size() > 4) {  // Consider a high degree to be greater than 4 for n ≤ 7
            cerr << "Warning: Performance bottleneck condition triggered - high degree of vertices!" << endl;
            abort();
        }
    }

void check_symmetrical_configurations_invariant(const vector<vector<int>>& graph, int n) {
    // Check for symmetrical configurations, e.g., multiple identical subgraphs
    // This is a simplistic check; for illustration, assume symmetry if each vertex connects to the same number of other vertices
    int common_degree = graph[1].size();
    for (int i = 2; i <= n; ++i) {
        if (graph[i].size() != common_degree) {
            return;  // Not symmetrical, skip further check
        }
    }
    cerr << "Warning: Performance bottleneck condition triggered - symmetrical configurations!" << endl;
    abort();
}
```

### 17. 889_B/metadata/synthesized_constraints/solutions_0072/private_tests_029_private_tests_016/conversations.txt
* **Distinct characters** invariant:
```cpp
void check_string_start_invariant(const vector<string>& strings) {
    unordered_set<char> starting_chars;
    for (const auto& str : strings) {
        starting_chars.insert(str[0]);
        if (starting_chars.size() > 26) {  // More unique initial characters than possible
            cerr << "Warning: Performance bottleneck condition triggered - too many distinct starting characters!" << endl;
            abort();
        }
    }
}
```

### 18. 1384_B1/metadata/synthesized_constraints/solutions_0035/generated_tests_068_generated_tests_092/conversations.txt
* **Tide depth** invariant:
```cpp
void check_tide_depth_invariant(const std::vector<int>& depths, int k, int l) {
    for (int i = 0; i < depths.size(); ++i) {
        int maxTideEffect = k;
        if (depths[i] + maxTideEffect > l) {
            cerr << "Warning: Tide and depth interaction invariant triggered - depth with tide exceeds limit" << endl;
            abort();
        }
    }
}
```

### 19. 787_A/metadata/synthesized_constraints/solutions_0325/generated_tests_074_generated_tests_036/conversations.txt
* **GDC** invariant:
```cpp
void check_common_divisor(int a, int c) {
    int gcd = std::__gcd(a, c);
    if (gcd > 1) {
        cerr << "Warning: Performance bottleneck due to common divisor of step sizes!" << endl;
        abort();
    }
}
```

### 20. 351_E/metadata/synthesized_constraints/solutions_0031/generated_tests_008_generated_tests_043/conversations.txt
* **Frequent sign changes** invariant:
```cpp
void check_frequent_sign_changes(const vector<int>& x) {
    int sign_change_count = 0;
    for (size_t i = 1; i < x.size(); ++i) {
        if (x[i] * x[i - 1] < 0) {
            ++sign_change_count;
        }
    }
    if (sign_change_count > (x.size() / 2)) { // Arbitrary threshold to indicate frequent changes
        cerr << "Warning: Performance bottleneck due to frequent sign changes!" << endl;
        abort();
    }
}
```

### 21. 1067_B/metadata/synthesized_constraints/solutions_0196/private_tests_009_generated_tests_010/conversations.txt
* **Vertex imbalance** invariant:
 ```cpp
   void check_vertex_degree_mismatch(const vector<int>& degrees) {
       int inconsistencies = 0;
       for (int degree : degrees) {
           if (degree != 1 && degree != 3) {  // Assumes expected degrees.
               inconsistencies++;
           }
       }
       if (inconsistencies > degrees.size() / 10) {  // Arbitrary threshold for mismatch.
           cerr << "Warning: Performance bottleneck condition triggered - vertex degree mismatches detected!" << endl;
           abort();
       }
   }
```

### 22. 1370_C/metadata/synthesized_constraints/solutions_0988/generated_tests_021_generated_tests_003/conversations.txt
* **Is prime** invariant:
   ```cpp
   void check_large_prime_invariant(int n) {
       // If n is a large prime, it will take longer to confirm it has no divisors
       // Check if n is larger than a typical threshold for being "large"
       if (n > 1000000 && is_prime(n)) {
           cerr << "Warning: Performance bottleneck condition triggered - large prime!" << endl;
           abort();
       }
   }

   bool is_prime(int n) {
       if (n <= 1) return false;
       for (int i = 2; i * i <= n; ++i) {
           if (n % i == 0) return false;
       }
       return true;
   }
   ```

### 23. 1334_E/metadata/synthesized_constraints/solutions_0136/generated_tests_005_generated_tests_042/conversations.txt
* **Factorial** invariant:
```cpp
void check_factorial_calculation_complexity(const vector<int>& diffs) {
    int sum = 0;
    for (int d : diffs) {
        sum += abs(d);
    }
    if (sum > 100) {  // Arbitrary threshold for complexity
        cerr << "Warning: Factorial calculation complexity triggered - high sum of exponent differences" << endl;
        abort();
    }
}
```

### 24. 1107_E/metadata/synthesized_constraints/solutions_0106/generated_tests_044_generated_tests_060/conversations.txt
* **Input composition** invariant: If the input string has long contiguous segments of identical characters that result in frequent recursive calls with high branching in the `calc` function, the program may slow down significantly.
```cpp
void check_input_composition(const string& s) {
    int max_segment_length = 0;
    char last_char = s[0];
    int current_length = 1;
    
    for (size_t i = 1; i < s.size(); ++i) {
        if (s[i] == last_char) {
            ++current_length;
        } else {
            max_segment_length = max(max_segment_length, current_length);
            current_length = 1;
            last_char = s[i];
        }
    }
    max_segment_length = max(max_segment_length, current_length);
    
    if (max_segment_length > 10) {  // Assuming a threshold based on problem constraints
        cerr << "Warning: Performance bottleneck condition triggered - long segment of identical characters!" << endl;
        abort();
    }
}
```

### 25. 1447_E/metadata/synthesized_constraints/solutions_0121/generated_tests_052_generated_tests_035/conversations.txt
```cpp
// LLM-synthesized checker function
void check_recursion_depth(int currentDepth, int maxDepth) {
    if (currentDepth > maxDepth) {
        cerr << "Warning: Performance bottleneck condition triggered - excessive recursion depth!" << endl;
        abort();
    }
}

// LLM-synthesized checker function
void check_imbalance(size_t size1, size_t size2) {
    if (size1 > 2 * size2 || size2 > 2 * size1) {
        cerr << "Warning: Performance bottleneck condition triggered - imbalanced set partitions!" << endl;
        abort();
    }
}

// LLM-synthesized checker function
void check_dense_bits(size_t denseCount, size_t threshold) {
    if (denseCount > threshold) {
        cerr << "Warning: Performance bottleneck condition triggered - dense bit pattern distribution!" << endl;
        abort();
    }
}

int dfs(set<int> s, int t, int currentDepth) {
    // Check for recursion depth
    check_recursion_depth(currentDepth, 30);
    ...
    // Check for set imbalance
    check_imbalance(sd[0].size(), sd[1].size());
    ...
}

int main() {
    ...
    // Check for dense bit distribution in the input set
    size_t denseCount = 0;
    for (int b : s) {
        if (__builtin_popcount(b) > 15) {
            ++denseCount;
        }
    }
    check_dense_bits(denseCount, n / 4);
    ...
}
```
