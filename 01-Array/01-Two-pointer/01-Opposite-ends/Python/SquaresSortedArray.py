# 977. Squares of a Sorted Array
# https://leetcode.com/problems/squares-of-a-sorted-array/description/

class Solution:
    def mergeSort(self, nums):
        if len(nums) <= 1:
            return nums

        mid = len(nums) // 2
        left = self.mergeSort(nums[:mid])
        right = self.mergeSort(nums[mid:])

        i = j = 0
        res = []

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                res.append(left[i])
                i += 1
            else:
                res.append(right[j])
                j += 1

        res.extend(left[i:])
        res.extend(right[j:])
        return res

    def sortedSquares(self, nums: list[int]) -> list[int]:
        left = start = 0
        end = len(nums) - 1
        while (start <= end):
            nums[start] = nums[start] ** 2
            start += 1

        nums[:] = self.mergeSort(nums)
        return nums
            
    