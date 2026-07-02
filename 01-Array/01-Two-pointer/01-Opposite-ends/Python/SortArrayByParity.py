# 905. Sort Array By Parity
# https://leetcode.com/problems/sort-array-by-parity/description/

class Solution(object):
    def sortArrayByParity(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        start, even, end = 0, 0, len(nums) 
        while(start < end):
            if not nums[start]%2:
                nums[start], nums[even] = nums[even], nums[start]
                even += 1
            start += 1
        return nums
