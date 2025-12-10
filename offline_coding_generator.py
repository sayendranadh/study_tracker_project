import random
import ast
from typing import Dict, Any, List

class OfflineCodingGenerator:
    """Lightweight coding problem generator with built-in canonical solvers for test verification."""
    
    def __init__(self):
        self.is_loaded = True
        self.problems = self._load_coding_problems()
        # Run self-tests to validate test cases using canonical solutions
        self._run_self_tests()

    def load_model(self):
        """Compatibility method - always ready"""
        print("✅ Coding problem generator ready")
        self.is_loaded = True

    def generate_coding_problem(self, topic: str, difficulty: str = 'easy') -> Dict[str, Any]:
        """Generate a coding problem"""
        problems = self.problems.get(difficulty, self.problems['easy'])
        
        # Filter by topic if possible
        topic_lower = topic.lower()
        filtered = [
            p for p in problems 
            if topic_lower in p['title'].lower() or topic_lower in p['description'].lower()
        ]
        
        return random.choice(filtered if filtered else problems)

    def _run_self_tests(self):
        """Run canonical solvers on test_cases to verify correctness of test data."""
        print("Running built-in self-tests for coding problems...")
        for level, plist in self.problems.items():
            for p in plist:
                verifier = p.get('verifier')
                if not verifier or not hasattr(self, verifier):
                    print(f"[WARN] No verifier for '{p['title']}'")
                    continue
                func = getattr(self, verifier)
                for i, tc in enumerate(p.get('test_cases', []), start=1):
                    try:
                        inp = tc['input']
                        expected = tc['expected']
                        result = func(inp)
                        # normalize both to strings for comparison
                        if str(result) == str(expected):
                            status = "PASS"
                        else:
                            status = f"FAIL (expected: {expected}, got: {result})"
                    except Exception as e:
                        status = f"ERROR ({e})"
                    print(f" [{level.upper()}] {p['title']} - test #{i}: {status}")
        print("Self-tests complete.\n")

    # ---------------------------
    # Canonical verifier functions
    # Each takes the test-case input string and returns output in same format as expected
    # ---------------------------
    def _verify_two_sum(self, inp: str):
        # input format: '[2,7,11,15]\n9' OR '[2,7,11,15]' and target on next line
        parts = inp.strip().split("\\n")
        if len(parts) == 1 and ' ' in parts[0]:
            parts = inp.strip().splitlines()
        if len(parts) == 1:
            # maybe both on same line separated by space
            # fallback: parse expecting list and number
            data = parts[0]
            if '],' in data:
                data = data.replace('],', ']\n')
                parts = data.splitlines()
        if len(parts) >= 2:
            nums = ast.literal_eval(parts[0])
            target = int(parts[1])
        else:
            # assume single-line with two values?
            lst = ast.literal_eval(parts[0])
            nums = lst[0]
            target = lst[1]
        seen = {}
        for i, num in enumerate(nums):
            diff = target - num
            if diff in seen:
                return str([seen[diff], i])
            seen[num] = i
        return str([])

    def _verify_reverse_string(self, inp: str):
        s = inp.strip()
        return s[::-1]

    def _verify_is_palindrome(self, inp: str):
        s = inp.strip()
        return str(s == s[::-1])

    def _verify_array_sum(self, inp: str):
        arr = ast.literal_eval(inp.strip())
        return str(sum(arr))

    def _verify_find_max(self, inp: str):
        arr = ast.literal_eval(inp.strip())
        return str(max(arr))

    def _verify_valid_parentheses(self, inp: str):
        s = inp.strip()
        stack = []
        pairs = {')':'(', '}':'{', ']':'['}
        for ch in s:
            if ch in '([{':
                stack.append(ch)
            elif ch in ')]}':
                if not stack or stack[-1] != pairs[ch]:
                    return "False"
                stack.pop()
        return "True" if not stack else "False"

    def _verify_length_of_longest_substring(self, inp: str):
        s = inp.strip()
        last_index = {}
        start = 0
        maxlen = 0
        for i, ch in enumerate(s):
            if ch in last_index and last_index[ch] >= start:
                start = last_index[ch] + 1
            last_index[ch] = i
            maxlen = max(maxlen, i - start + 1)
        return str(maxlen)

    def _verify_max_area(self, inp: str):
        arr = ast.literal_eval(inp.strip())
        i, j = 0, len(arr)-1
        maxarea = 0
        while i < j:
            area = min(arr[i], arr[j]) * (j - i)
            maxarea = max(maxarea, area)
            if arr[i] < arr[j]:
                i += 1
            else:
                j -= 1
        return str(maxarea)

    def _verify_merge_k_lists(self, inp: str):
        lists = ast.literal_eval(inp.strip())
        merged = []
        for lst in lists:
            merged.extend(lst)
        merged.sort()
        return str(merged)

    def _verify_find_median_sorted_arrays(self, inp: str):
        parts = inp.strip().split("\\n")
        nums1 = ast.literal_eval(parts[0])
        nums2 = ast.literal_eval(parts[1])
        merged = sorted(nums1 + nums2)
        n = len(merged)
        if n == 0:
            return "0.0"
        if n % 2 == 1:
            return str(float(merged[n//2]))
        else:
            return str((merged[n//2 - 1] + merged[n//2]) / 2.0)

    def _verify_fibonacci_nth(self, inp: str):
        n = int(inp.strip())
        if n <= 1:
            return str(n)
        a, b = 0, 1
        for _ in range(2, n+1):
            a, b = b, a + b
        return str(b)

    def _verify_binary_search(self, inp: str):
        parts = inp.strip().split("\\n")
        arr = ast.literal_eval(parts[0])
        target = int(parts[1])
        l, r = 0, len(arr)-1
        while l <= r:
            m = (l + r) // 2
            if arr[m] == target:
                return str(m)
            elif arr[m] < target:
                l = m + 1
            else:
                r = m - 1
        return str(-1)

    def _verify_gcd(self, inp: str):
        parts = inp.strip().split()
        if len(parts) == 1 and '\\n' in inp:
            parts = inp.strip().splitlines()
        a = int(parts[0])
        b = int(parts[1]) if len(parts) > 1 else 0
        while b:
            a, b = b, a % b
        return str(a)

    def _verify_merge_sort(self, inp: str):
        arr = ast.literal_eval(inp.strip())
        def merge_sort(a):
            if len(a) <= 1:
                return a
            mid = len(a)//2
            left = merge_sort(a[:mid])
            right = merge_sort(a[mid:])
            res = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    res.append(left[i]); i += 1
                else:
                    res.append(right[j]); j += 1
            res.extend(left[i:]); res.extend(right[j:])
            return res
        return str(merge_sort(arr))

    def _verify_quicksort(self, inp: str):
        arr = ast.literal_eval(inp.strip())
        def quicksort(a):
            if len(a) <= 1:
                return a
            pivot = a[len(a)//2]
            left = [x for x in a if x < pivot]
            mid = [x for x in a if x == pivot]
            right = [x for x in a if x > pivot]
            return quicksort(left) + mid + quicksort(right)
        return str(quicksort(arr))

    def _verify_climb_stairs(self, inp: str):
        n = int(inp.strip())
        if n <= 1:
            return "1"
        a, b = 1, 1
        for _ in range(2, n+1):
            a, b = b, a + b
        return str(b)

    def _verify_coin_change(self, inp: str):
        parts = inp.strip().split("\\n")
        coins = ast.literal_eval(parts[0])
        amount = int(parts[1])
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0
        for c in coins:
            for x in range(c, amount + 1):
                dp[x] = min(dp[x], dp[x - c] + 1)
        return str(dp[amount] if dp[amount] != float('inf') else -1)

    def _verify_lis(self, inp: str):
        arr = ast.literal_eval(inp.strip())
        if not arr:
            return "0"
        dp = [1]*len(arr)
        for i in range(len(arr)):
            for j in range(i):
                if arr[j] < arr[i]:
                    dp[i] = max(dp[i], dp[j]+1)
        return str(max(dp))

    # ---------------------------
    # Problem definitions (with test cases and verifier names)
    # ---------------------------
    def _load_coding_problems(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load curated coding problems by difficulty with verifiers attached."""
        return {
            'easy': [
                {
                    'title': 'Two Sum',
                    'description': 'Given an array of integers nums and an integer target, return indices of the two numbers that add up to target.',
                    'template': '''def two_sum(nums, target):
    # Your code here
    pass''',
                    'test_cases': [
                        {'input': '[2,7,11,15]\\n9', 'expected': '[0, 1]'},
                        {'input': '[3,2,4]\\n6', 'expected': '[1, 2]'},
                        {'input': '[3,3]\\n6', 'expected': '[0, 1]'}
                    ],
                    'verifier': '_verify_two_sum'
                },
                {
                    'title': 'Reverse String',
                    'description': 'Write a function that reverses a string.',
                    'template': '''def reverse_string(s):
    # Your code here
    pass''',
                    'test_cases': [
                        {'input': 'hello', 'expected': 'olleh'},
                        {'input': 'python', 'expected': 'nohtyp'},
                        {'input': 'a', 'expected': 'a'}
                    ],
                    'verifier': '_verify_reverse_string'
                },
                {
                    'title': 'Palindrome Check',
                    'description': 'Check if a string is a palindrome.',
                    'template': '''def is_palindrome(s):
    # Your code here
    pass''',
                    'test_cases': [
                        {'input': 'racecar', 'expected': 'True'},
                        {'input': 'hello', 'expected': 'False'},
                        {'input': 'a', 'expected': 'True'}
                    ],
                    'verifier': '_verify_is_palindrome'
                },
                {
                    'title': 'Sum of Array',
                    'description': 'Calculate the sum of all elements in an array.',
                    'template': '''def array_sum(arr):
    # Your code here
    pass''',
                    'test_cases': [
                        {'input': '[1,2,3,4,5]', 'expected': '15'},
                        {'input': '[10,20,30]', 'expected': '60'},
                        {'input': '[0]', 'expected': '0'}
                    ],
                    'verifier': '_verify_array_sum'
                },
                {
                    'title': 'Find Maximum',
                    'description': 'Find the maximum element in an array.',
                    'template': '''def find_max(arr):
    # Your code here
    pass''',
                    'test_cases': [
                        {'input': '[3,7,2,9,1]', 'expected': '9'},
                        {'input': '[5,5,5]', 'expected': '5'},
                        {'input': '[1]', 'expected': '1'}
                    ],
                    'verifier': '_verify_find_max'
                },
                {
                    'title': 'Fibonacci (Nth)',
                    'description': 'Return the nth Fibonacci number (0-indexed).',
                    'template': '''def fibonacci(n):
    # Your code here
    pass''',
                    'test_cases': [
                        {'input': '0', 'expected': '0'},
                        {'input': '1', 'expected': '1'},
                        {'input': '10', 'expected': '55'}
                    ],
                    'verifier': '_verify_fibonacci_nth'
                },
                {
                    'title': 'Binary Search (sorted array)',
                    'description': 'Return index of target in sorted array or -1 if not found.',
                    'template': '''def binary_search(arr, target):
    # Your code here
    pass''',
                    'test_cases': [
                        {'input': '[1,2,3,4,5]\\n3', 'expected': '2'},
                        {'input': '[1,2,3,4]\\n5', 'expected': '-1'},
                        {'input': '[2,4,6,8]\\n6', 'expected': '2'}
                    ],
                    'verifier': '_verify_binary_search'
                }
            ],
            'medium': [
                {
                    'title': 'Valid Parentheses',
                    'description': "Given a string containing '(){}[]', determine if it is valid.",
                    'template': '''def is_valid(s):
    # Your code here
    pass''',
                    'test_cases': [
                        {'input': '()', 'expected': 'True'},
                        {'input': '()[]{}', 'expected': 'True'},
                        {'input': '(]', 'expected': 'False'}
                    ],
                    'verifier': '_verify_valid_parentheses'
                },
                {
                    'title': 'Longest Substring Without Repeating',
                    'description': 'Length of longest substring without repeating characters.',
                    'template': '''def length_of_longest_substring(s):
    # Your code here
    pass''',
                    'test_cases': [
                        {'input': 'abcabcbb', 'expected': '3'},
                        {'input': 'bbbbb', 'expected': '1'},
                        {'input': 'pwwkew', 'expected': '3'}
                    ],
                    'verifier': '_verify_length_of_longest_substring'
                },
                {
                    'title': 'Container With Most Water',
                    'description': 'Given heights, find max water container capacity.',
                    'template': '''def max_area(height):
    # Your code here
    pass''',
                    'test_cases': [
                        {'input': '[1,8,6,2,5,4,8,3,7]', 'expected': '49'},
                        {'input': '[1,1]', 'expected': '1'},
                        {'input': '[4,3,2,1,4]', 'expected': '16'}
                    ],
                    'verifier': '_verify_max_area'
                },
                {
                    'title': 'Merge K Sorted Lists (flatten)',
                    'description': 'Merge k sorted lists into one sorted list.',
                    'template': '''def merge_k_lists(lists):
    # Your code here
    pass''',
                    'test_cases': [
                        {'input': '[[1,4,5],[1,3,4],[2,6]]', 'expected': '[1, 1, 2, 3, 4, 4, 5, 6]'},
                        {'input': '[[]]', 'expected': '[]'},
                        {'input': '[[1]]', 'expected': '[1]'}
                    ],
                    'verifier': '_verify_merge_k_lists'
                },
                {
                    'title': 'Find Median of Two Sorted Arrays',
                    'description': 'Find median of two sorted arrays.',
                    'template': '''def find_median_sorted_arrays(nums1, nums2):
    # Your code here
    pass''',
                    'test_cases': [
                        {'input': '[1,3]\\n[2]', 'expected': '2.0'},
                        {'input': '[1,2]\\n[3,4]', 'expected': '2.5'},
                        {'input': '[]\\n[1]', 'expected': '1.0'}
                    ],
                    'verifier': '_verify_find_median_sorted_arrays'
                },
                {
                    'title': 'Merge Sort',
                    'description': 'Sort an array using merge sort.',
                    'template': '''def merge_sort(arr):
    # Your code here
    pass''',
                    'test_cases': [
                        {'input': '[5,2,3,1]', 'expected': '[1, 2, 3, 5]'},
                        {'input': '[]', 'expected': '[]'},
                        {'input': '[1]', 'expected': '[1]'}
                    ],
                    'verifier': '_verify_merge_sort'
                },
                {
                    'title': 'Quicksort (return sorted array)',
                    'description': 'Implement quicksort and return sorted array.',
                    'template': '''def quicksort(arr):
    # Your code here
    pass''',
                    'test_cases': [
                        {'input': '[3,6,8,10,1,2,1]', 'expected': '[1, 1, 2, 3, 6, 8, 10]'},
                        {'input': '[1,0]', 'expected': '[0, 1]'},
                        {'input': '[]', 'expected': '[]'}
                    ],
                    'verifier': '_verify_quicksort'
                }
            ],
            'hard': [
                {
                    'title': 'Median of Two Sorted Arrays (hard)',
                    'description': 'Advanced median algorithm (see medium version too).',
                    'template': '''def find_median_sorted_arrays(nums1, nums2):
    # Optimal O(log(min(m,n))) algorithm expected
    pass''',
                    'test_cases': [
                        {'input': '[1,3]\\n[2]', 'expected': '2.0'},
                        {'input': '[1,2]\\n[3,4]', 'expected': '2.5'},
                        {'input': '[]\\n[1]', 'expected': '1.0'}
                    ],
                    'verifier': '_verify_find_median_sorted_arrays'
                },
                {
                    'title': 'Climbing Stairs (DP)',
                    'description': 'Compute number of ways to climb n stairs with 1 or 2 steps.',
                    'template': '''def climb_stairs(n):
    # DP solution
    pass''',
                    'test_cases': [
                        {'input': '1', 'expected': '1'},
                        {'input': '2', 'expected': '2'},
                        {'input': '5', 'expected': '8'}
                    ],
                    'verifier': '_verify_climb_stairs'
                },
                {
                    'title': 'Coin Change (minimum coins)',
                    'description': 'Given coins and amount, return min number of coins or -1 if impossible.',
                    'template': '''def coin_change(coins, amount):
    # DP min coins
    pass''',
                    'test_cases': [
                        {'input': '[1,2,5]\\n11', 'expected': '3'},
                        {'input': '[2]\\n3', 'expected': '-1'},
                        {'input': '[1]\\n0', 'expected': '0'}
                    ],
                    'verifier': '_verify_coin_change'
                },
                {
                    'title': 'Longest Increasing Subsequence (LIS)',
                    'description': 'Return length of LIS in an integer array.',
                    'template': '''def length_of_lis(nums):
    # Dynamic programming or patience sorting
    pass''',
                    'test_cases': [
                        {'input': '[10,9,2,5,3,7,101,18]', 'expected': '4'},
                        {'input': '[]', 'expected': '0'},
                        {'input': '[0]', 'expected': '1'}
                    ],
                    'verifier': '_verify_lis'
                },
                {
                    'title': 'GCD (Euclidean)',
                    'description': 'Compute greatest common divisor of two integers.',
                    'template': '''def gcd(a, b):
    # Euclidean algorithm
    pass''',
                    'test_cases': [
                        {'input': '48 18', 'expected': '6'},
                        {'input': '7 3', 'expected': '1'},
                        {'input': '10 5', 'expected': '5'}
                    ],
                    'verifier': '_verify_gcd'
                }
            ]
        }
