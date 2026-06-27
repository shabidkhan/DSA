# 345. Reverse Vowels of a String
# https://leetcode.com/problems/reverse-vowels-of-a-string/description/

class Solution:
    def reverseVowels(self, s: str) -> str:
        start = 0
        end = len(s) - 1
        vowels = 'AaEeIiOoUu'
        arrayStr = list(s)
        while (start < end):
            if (s[start] not in vowels and s[end] not in vowels):
                start += 1
                end -= 1
                continue
            if(s[start] not in vowels):
                start += 1
                continue
            if(s[end] not in vowels):
                end -= 1
                continue
            arrayStr[start], arrayStr[end] = arrayStr[end], arrayStr[start]
            start += 1
            end -= 1
        return ''.join(arrayStr)
        