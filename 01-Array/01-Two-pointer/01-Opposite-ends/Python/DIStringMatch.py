# 942. DI String Match
# https://leetcode.com/problems/di-string-match/description/

class Solution(object):
    def diStringMatch(self, s):
        """
        :type s: str
        :rtype: List[int]
        """
        lower, higher = 0, len(s)
        output = []
        for DI in s:
            if DI == 'I':
                output.append(lower)
                lower += 1
            else:
                output.append(higher)
                higher -= 1
                
        output.append(higher)
        return output