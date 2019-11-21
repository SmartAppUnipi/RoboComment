from fuzzy_logic.fuzzy_set import FuzzySet

class FuzzyRule:

    def __init__(self, antecedent, consequent):
        self._antec = antecedent
        self._conseq = consequent

    def selection(self, x):
        result = 1
        for e in self._antec:
            fuzzy_set = e[0]
            func_name = e[1]
            modifier = e[2]
            result *= fuzzy_set.member(x, func_name, modifier)
        ret = []
        for e in self._conseq:
            fuzzy_set = e[0]
            func_name = e[1]
            modifier = e[2]
            ret.append(fuzzy_set.counter_img(result, func_name, modifier))
        return ret