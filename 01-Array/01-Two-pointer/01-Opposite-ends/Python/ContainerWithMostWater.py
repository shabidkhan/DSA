# 11. Container With Most Water
# https://leetcode.com/problems/container-with-most-water/description/

class Solution:
    def maxArea(self, height: list[int]) -> int:
        left, right = 0, len(height) - 1
        max_amount = 0
        while left < right:
            h = height[right] if height[left] > height[right] else height[left]
            if max_amount < h*(right-left):
                max_amount = h*(right-left)
            if height[left] > height[right]:
                right -= 1
            else:
                left += 1
        return max_amount
        