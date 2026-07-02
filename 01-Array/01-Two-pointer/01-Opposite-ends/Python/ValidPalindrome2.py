# 680. Valid Palindrome II
# https://leetcode.com/problems/valid-palindrome-ii/description/
class Solution(object):
    def validPalindrome(self, s):
        if s == s[::-1]:
            return True

        start = 0
        end = len(s) - 1
        while s[start] == s[end] and start < end:
            start += 1
            end -= 1

        if(start > end):
            return True

        check1 = s[start + 1: end + 1]
        check2 = s[start: end]
        return check1 == check1[::-1] or check2 == check2[::-1]