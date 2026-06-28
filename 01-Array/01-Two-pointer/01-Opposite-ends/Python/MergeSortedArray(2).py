# 88. Merge Sorted Array
# https://leetcode.com/problems/merge-sorted-array/description/

class Solution:
    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        start1 = start2 = 0
        end1 = m + n
        end2 = n
        while (start1 < end1 and start2 < end2):
            if (nums2[start2]<nums1[start1] or (start1 >= m+start2 and nums1[start1] == 0)):
                nums1.insert(start1, nums2[start2])
                nums1.pop()
                start2 += 1
            start1 += 1
            