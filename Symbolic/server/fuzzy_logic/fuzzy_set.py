import matplotlib.pyplot as plt
import numpy as np

from fuzzy_logic.membership_function import MembershipFunction as MembFunc

class FuzzySet:
    def __init__(self, begin, end, step, universe_descr = None):
        """Model of a fuzzy set
         - begin is the 0 on the x axis of the universe
         - end is the right extreme
         - step is the discrete step
         - a string identifying the universe for clarity"""
        self._universe =  np.arange(begin, end, step)
        self._memberships = {}
        self._univ_desc = "universe"
        if universe_descr:
            self._univ_desc = universe_descr

    def new_membership_func(self, name, not_member, member, other = None):
        """Add a membership function
        - name is the name assigned to the function
        - not_member is the membership threshold
        - member is the absolute membership certainty threshold
        - other is optional, and is used in order to get functions that are HighLowHigh or LowHighLow """
        self._memberships[name] = MembFunc(self._universe, not_member = not_member, member = member, other = other)

    def plot_membership(self, name, modifier = None):
        """ plots the function by name, by applying its modifier
        - name: the name of the function to plot
        - modifier: optional modifier to be chosen from the list """
        memb = self._memberships[name]
        if memb:
            plt.plot(self._universe, self._fill_list_for_plot(memb, modifier), 'b', linewidth=1.5)
            title = "plotting " + name
            if modifier:
                title = "plotting " + modifier + " " + name
            plt.title(title)
            plt.xlabel(self._univ_desc)
            plt.ylabel("membership degree")
            plt.show()
        
    def _fill_list_for_plot(self, memb_f, modifier):
        ret_list = []
        for i in self._universe:
            ret_list.append(memb_f.img(i, modifier))
        return ret_list

    def member(self, x, name, modifier = None):
        """ compute the membership function of x w.r.t function with name "name" and with the given modifier
         - x: the point of the domain on which to compute the membership function
         - name: the name of the function
         - modifier: the optional modifier to apply"""
        memb = self._memberships[name]
        return memb.img(x, modifier)

    def containment(self, subset, superset, subset_modifier = None, superset_modifier = None):
        """ returns true if subset is a subset of superset, false otherwise (all according to the given modifiers)
         - subset: the name of the function that we assume to be the subset
         - superset: the name of the function that we assume to be the superset
         - subset_modifier: an optional modifier to be applied to the subset
         - superset_modifier: an optional modifier to be applied to the superset"""
        subs = self._memberships[subset]
        super = self._memberships[superset]
        for i in self._universe:
            if subs.img(i, subset_modifier) > super.img(i, superset_modifier):
                return False
        return True

    def intersection(self, func_a, func_b, a_modifier = None, b_modifier = None):
        """ returns the set of couples <element, membership over the interseption> (all according to the given modifiers)
        - func_a: name of the first function
        - func_b: name of the second function
        - a_modifier: optional modifier for the first function
        - b_modifier: optional modifier for the second function"""
        a = self._memberships[func_a]
        b = self._memberships[func_b]
        interc = []
        for i in self._universe:
            minim = min(a.img(i, a_modifier), b.img(i, b_modifier))
            if minim > 0:
                interc.append((i, minim))
        return interc

    def union(self, func_a, func_b, a_modifier = None, b_modifier = None):
        """ returns the set of couples <element, membership over the union> (all according to the given modifiers)
        - func_a: name of the first function
        - func_b: name of the second function
        - a_modifier: optional modifier for the first function
        - b_modifier: optional modifier for the second function"""
        a = self._memberships[func_a]
        b = self._memberships[func_b]
        res = []
        for i in self._universe:
            maxim = max(a.img(i, a_modifier), b.img(i, b_modifier))
            if maxim > 0:
                res.append((i, maxim))
        return res

    def new_membership_func_from_list(self, list, name):
        """Create a membership function over the given domain from a list. The list can be the one provided by the function intersection/union
        - list: the list of couples <x, f(x)>
        - name: a name to assign to the function"""
        self._memberships[name] = MembFunc(self._universe, list = list)