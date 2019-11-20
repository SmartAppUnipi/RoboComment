import math


class MembershipFunction:
    def __init__(self, range, not_member, member, other = None): 
        self._range = range
        self._func = None
        if other:
            if member > not_member: # LHL
                self._func = _LHL(not_member, member, other)
                print("LHL")
            else: # HLH
                self._func = _HLH(member, not_member, other)
                print("HLH")
        else:
            if member > not_member: # LH
                self._func = _LH(not_member, member)
                print("LH")
            else: # HL
                self._func = _HL(member, not_member)
                print("HL")

        self._degrees = {
            'a little': 1.3, 
            'slightly': 1.7,
            'very': 2,
            'extremely': 3,
            'very very': 4,
            'more or less': 0.5,
            'somewhat': 0.5
        }

    def img(self, x, modifier = None):
        if x not in self._range:
            raise "XNotInDomainException"
        degree = None
        if modifier:
            degree = self._degrees[modifier]
            if not degree:
                print("FUZZY LOGIC: unknown modifier")
                degree = 1

        if degree:
            return self._func.img(x, degree)
        else:
            return self._func.img(x, 1)


class _LHL:
    def __init__(self, low_1, high, low_2): 
        self._low1 = low_1
        self._low2 = low_2
        self._high = high
    
    def img(self, x, degree):
        
        if x <= self._low1 or x >= self._low2:
            return 0
        elif x == self._high:
            return 1
        else:
            if x in range(self._low1, self._high):
                return math.pow((x - self._low1), degree) / (self._high - self._low1)
            else: 
                return math.pow((self._low2 - x), degree) / (self._low2 - self._high)

class _HLH:
    def __init__(self, high_1, low, high_2): 
        self._low = low
        self._high1 = high_1
        self._high2 = high_2
    
    def img(self, x, degree):
        if x <= self._high1 or x >= self._high2:
            return 1
        elif x == self._low:
            return 0
        else:
            if x in range(self._high1, self._low):
                return (self._low - x) / (self._low - self._high1)
            else: 
                return (x - self._low) / (self._high2 - self._low)


class _LH:
    def __init__(self, low, high): 
        self._low = low
        self._high = high
    
    def img(self, x, degree):
        if x <= self._low:
            return 0
        elif x >= self._high:
            return 1
        else:
            return (x - self._low) / (self._high - self._low)


class _HL:
    def __init__(self, high, low): 
        self._low = low
        self._high = high
    
    def img(self, x, degree):
        if x < self._high:
            return 1
        elif x > self._low:
            return 0
        else:
            return (self._low - x) / (self._low - self._high)