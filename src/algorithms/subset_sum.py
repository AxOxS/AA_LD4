"""
Subset Sum Problem Algorithms Module

This module provides implementations of different algorithms to solve the Subset Sum problem,
which is an NP-complete problem.

The Subset Sum problem: Given a set of integers, determine if there exists a subset
whose sum equals a given target value.
"""
from typing import List


def subset_sum_backtracking(nums: List[int], target: int) -> bool:
    """
    Solve the Subset Sum problem using backtracking.
    Returns True if there exists a subset of nums that sums to target, False otherwise.
    
    Time Complexity: O(2^n) - exponential, where n is the length of nums
    Space Complexity: O(n) for the recursion stack
    
    Args:
        nums: List of integers to search within
        target: Target sum to find
        
    Returns:
        bool: True if a subset with the target sum exists, False otherwise
    """
    def backtrack(index: int, current_sum: int) -> bool:
        # Base cases
        if current_sum == target:
            return True
        
        if index >= len(nums) or current_sum > target:
            return False
        
        # Include the current element
        if backtrack(index + 1, current_sum + nums[index]):
            return True
        
        # Exclude the current element
        if backtrack(index + 1, current_sum):
            return True
        
        return False
    
    # Sort and filter numbers for optimization
    nums = [n for n in nums if n <= target]
    nums.sort()
    
    return backtrack(0, 0)


def subset_sum_exhaustive(nums: List[int], target: int) -> bool:
    """
    Subset Sum with exhaustive search - guaranteed worst-case performance.
    This version always checks ALL possible subsets (2^n) by design.
    
    For impossible targets, this forces the algorithm to explore the entire search space.
    
    Time Complexity: O(2^n) - exponential
    Space Complexity: O(n) for the recursion stack
    
    Args:
        nums: List of integers to search within
        target: Target sum to find
        
    Returns:
        bool: True if a subset with the target sum exists, False otherwise
    """
    def backtrack(index, current_sum):
        if index == len(nums):
            return current_sum == target
        
        # Always explore both branches (include and exclude)
        # to ensure we explore the entire search space
        include = backtrack(index + 1, current_sum + nums[index])
        exclude = backtrack(index + 1, current_sum)
        
        return include or exclude
    
    return backtrack(0, 0)


def subset_sum_dynamic(nums: List[int], target: int) -> bool:
    """
    Solve the Subset Sum problem using dynamic programming.
    Returns True if there exists a subset of nums that sums to target, False otherwise.
    
    Time Complexity: O(n * target) - pseudo-polynomial
    Space Complexity: O(target)
    
    Args:
        nums: List of integers to search within
        target: Target sum to find
        
    Returns:
        bool: True if a subset with the target sum exists, False otherwise
    """
    # Filter out numbers that are greater than target
    nums = [n for n in nums if n <= target]
    
    # Create a DP table
    dp = [False] * (target + 1)
    dp[0] = True  # Empty subset sums to 0
    
    for num in nums:
        for i in range(target, num - 1, -1):
            dp[i] = dp[i] or dp[i - num]
    
    return dp[target] 