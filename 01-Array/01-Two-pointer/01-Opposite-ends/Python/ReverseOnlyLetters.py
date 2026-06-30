# 917. Reverse Only Letters
# https://leetcode.com/problems/reverse-only-letters/description/
class Solution:
    def reverseOnlyLetters(self, s: str) -> str:
        start = 0
        end = len(s) - 1
        s = list(s)
        while (start < end):
            if not s[start].isalpha():
                start += 1
            if not s[end].isalpha():
                end -= 1
            if (s[start].isalpha() and s[end].isalpha()):
                s[start], s[end] = s[end], s[start]
                start +=1
                end -=1

        return ''.join(s)

# Example 1:
# Input: s = "ab-cd"
# Output: "dc-ba"

# Example 2:
# Input: s = "a-bC-dEf-ghIj"
# Output: "j-Ih-gfE-dCba"

# Example 3:
# Input: s = "Test1ng-Leet=code-Q!"
# Output: "Qedo1ct-eeL=gnit-seT"

# Constraints:

# 1 <= s.length <= 100
# s consists of lowercase and uppercase English letters.
# s does not contain any symbols or digits.
