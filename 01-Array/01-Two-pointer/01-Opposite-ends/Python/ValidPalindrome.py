# 125. Valid Palindrome
# https://leetcode.com/problems/valid-palindrome/description/

class Solution:
    def isPalindrome(self, s: str) -> bool:
        # text = ''.join(ch.lower() for ch in s if ch.isalnum())
        text = ''.join(filter(str.isalnum, s)).lower()
        start = 0
        end = len(text) - 1
        while (start < end):
            if (text[start] != text[end]):
                return False
            start += 1
            end -= 1
        return True
        