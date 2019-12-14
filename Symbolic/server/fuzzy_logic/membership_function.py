import math


class MembershipFunction:
    def __init__(self, range, not_member = None, member = None, other = None, list = None): 
        self._range = range
        if list:
            self._func = _GenericFunction(list)
        else:
            self._func = None
            if other:
                if member > not_member: # LHL
                    self._func = _LHL(not_member, member, other)
                else: # HLH
                    self._func = _HLH(member, not_member, other)
            else:
                if member > not_member: # LH
                    self._func = _LH(not_member, member)
                else: # HL
                    self._func = _HL(member, not_member)

        self._degrees = {
            'a little': 1.3, 
            'slightly': 1.7,
            'very': 2,
            'extremely': 3,
            'very very': 4,
            'more or less': 0.5,
            'somewhat': 0.5
        }
        self._neg_degrees = ['somewhat', 'more or less']
        self._pos_degrees = ['a little', 'slightly', 'very', 'extremely', 'very very']

    def best_fit(self, x, thresh):
        img = self._func.img(x, 1)
        if img == 0:
            return None
        elif img == 1:
            return 'very very'
        else:
            return self._func.best_fit(x, thresh, self._degrees, self._pos_degrees, self._neg_degrees)

    def img(self, x, modifier = None):
        if x not in self._range:
            raise ValueError("XNotInDomainException")
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
                return math.pow((x - self._low1) / (self._high - self._low1), degree)
            else: 
                return math.pow((self._low2 - x) / (self._low2 - self._high), degree)

    def best_fit(self, x, thresh, degrees, pos_degrees, neg_degrees):
        if x in range(self._low1, self._high):
           return _best_fit_LH(self._low1, self._high, pos_degrees, neg_degrees, degrees, thresh, x)
        else: 
            return _best_fit_HL(self._low2, self._high, pos_degrees, neg_degrees, degrees, thresh, x)
        return None

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
                return math.pow((self._low - x) / (self._low - self._high1), degree)
            else: 
                return math.pow((x - self._low) / (self._high2 - self._low), degree)

    def best_fit(self, x, thresh, degrees, pos_degrees, neg_degrees):
        if x in range(self._high1, self._low):
            return _best_fit_HL(self._low, self._high1, pos_degrees, neg_degrees, degrees, thresh, x)
        else: 
            return _best_fit_LH(self._low, self._high2, pos_degrees, neg_degrees, degrees, thresh, x)


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
            return math.pow((x - self._low) / (self._high - self._low), degree)

    def best_fit(self, x, thresh, degrees, pos_degrees, neg_degrees):
        return _best_fit_LH(self._low, self._high, pos_degrees, neg_degrees, degrees, thresh, x)


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
            return math.pow((self._low - x) / (self._low - self._high), degree)

    def best_fit(self, x, thresh, degrees, pos_degrees, neg_degrees):
        return _best_fit_HL(self._low, self._high, pos_degrees, neg_degrees, degrees, thresh, x)

class _GenericFunction:
    def __init__(self, member_list): 
        self._elem = [a for (a,b) in member_list]
        self._img = [b for (a,b) in member_list]

    def img(self, x, degree):
        if degree != 1:
            raise ValueError("NotAbleToBeDegreedException")
        if x in self._elem:
            return self._img[self._elem.index(x)]
        else:
            return 0

    def best_fit(self, x, thresh, degrees, pos_degrees, neg_degrees):
        raise ValueError("NotAbleToBeDegreedException")

def _best_fit_LH(low, high, pos_degrees, neg_degrees, degrees, thresh, x):
    if ((x - low) / (high - low)) >= thresh:
        best_fit = ""
        for deg in pos_degrees:
            degree = degrees[deg]
            img = math.pow((x - low) / (high - low), degree)
            if img < thresh:
                return best_fit
            else:
                best_fit = deg
        return best_fit
    else:
        for deg in neg_degrees:
            degree = degrees[deg]
            img = math.pow((x - low) / (high - low), degree)
            if img >= thresh:
                return deg
        return None

def _best_fit_HL(low, high, pos_degrees, neg_degrees, degrees, thresh, x):
    if ((low - x) / (low - high)) >= thresh:
        best_fit = ""
        for deg in pos_degrees:
            degree = degrees[deg]
            img = math.pow((low - x) / (low - high), degree)
            if img < thresh:
                return best_fit
            else:
                best_fit = deg
        return best_fit
    else:
        for deg in neg_degrees:
            degree = degrees[deg]
            img = math.pow((low - x) / (low - high), degree)
            if img >= thresh:
                return deg
        return None