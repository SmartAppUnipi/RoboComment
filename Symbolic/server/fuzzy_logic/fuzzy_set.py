import matplotlib.pyplot as plt
import numpy as np

from fuzzy_logic.membership_function import MembershipFunction as MembFunc

class FuzzySet:
    def __init__(self, begin, end, step):
        """Model of a fuzzy set
         - begin is the 0 on the x axis of the universe
         - end is the right extreme
         - step is the discrete step"""
        self._universe =  np.arange(begin, end, step)
        self._memberships = {}

    def new_membership_func(self, name, not_member, member, other = None):
        """Add a membership function
        - name is the name assigned to the function
        - not_member is the membership threshold
        - member is the absolute membership certainty threshold
        - other is optional, and is used in order to get functions that are HighLowHigh or LowHighLow """
        self._memberships[name] = MembFunc(self._universe, not_member, member, other)

    def plot_membership(self, name, modifier = None):
        memb = self._memberships[name]
        if memb:
            plt.plot(self._universe, self._fill_list_for_plot(memb, modifier), 'b', linewidth=1.5, label=name)
            plt.show()
        
    def _fill_list_for_plot(self, memb_f, modifier):
        ret_list = []
        for i in self._universe:
            ret_list.append(memb_f.img(i, modifier))
        return ret_list

    def member(self, x, name, modifier = None):
        memb = self._memberships[name]
        return memb.img(x, modifier)

