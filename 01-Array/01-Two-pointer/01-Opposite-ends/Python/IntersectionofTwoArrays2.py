# 350. Intersection of Two Arrays II
# https://leetcode.com/problems/intersection-of-two-arrays-ii/description/

class Solution(object):
    def intersect(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """
        output = []
        nums1.sort()
        nums2.sort()
        s1, e1 = 0, len(nums1)
        s2, e2 = 0 , len(nums2)

        while s1<e1 and s2<e2:
            if nums1[s1] == nums2[s2]:
                output.append(nums1[s1])
                s1 += 1
                s2 += 1
            elif nums1[s1] > nums2[s2]:
                s2 +=1
            else:
                s1 +=1
        return output
        