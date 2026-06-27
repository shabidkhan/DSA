# 167. Two Sum II - Input Array Is Sorted
# https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/

class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        start = 0 
        end = len(numbers) - 1
        while(start < end):
            if (numbers[start] + numbers[end] == target):
                return [start + 1, end + 1]
            if (numbers[start] + numbers[end] < target):
                start += 1
            else:
                end -= 1
        return -1