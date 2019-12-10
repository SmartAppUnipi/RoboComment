from automaton import machines
#from graphviz import Digraph
import numpy as np

def print_on_exit(old_state, triggered_event):
   print("State was:",old_state)

def print_on_enter(new_state, triggered_event):
   #print("Entered '%s' due to '%s'" % (new_state, triggered_event))
   print("State is:",new_state)

class CommentAutomata():
    def __init__(self):
        """
        Initialize the automata
        """
        #states by Luca
        """The states"""
        states = [
                    'Commento su qualche info',
                    'Commento semplice',
                    'Commento semplice ripetuto',
                    'Commento Random'
                ]
        #dictionaries
        """Dict states to index"""
        self.states2idx = {k:i for i,k in enumerate(states)}
        """Dict index to state"""
        self.id2st = {self.states2idx[k]:k for k in self.states2idx.keys()}
        self.n_states = len(states)

        #transaction defined by Luca :P
        self.transitions = np.zeros((self.n_states,self.n_states))
        self.transitions[0,1] = 1
        self.transitions[1,0] = .25
        self.transitions[1,2] = .5
        self.transitions[1,3] = .25
        self.transitions[2,0] = .25
        self.transitions[2,1] = .5
        self.transitions[2,3] = .25
        self.transitions[3,1] = 1


        #PROBABILISTIC PART
        distributions = np.array(self.transitions)
        distributions = distributions / np.sum(self.transitions,axis=1)
        self.cum_SUM = np.cumsum(distributions,axis=1)

        '''print("self.transitions")
        print(self.transitions)
        print("distributions")
        print(distributions)
        print(self.cum_SUM)
        print()
        '''

        #Defining ASF STATES
        
        self.asf = machines.FiniteMachine()
        for i in range(self.n_states):
            self.asf.add_state(self.id2st[i])#on_exit=print_on_exit)
        #Defining ASF TRANSACTIONS
        for i in range(self.n_states):
            for j,pr in enumerate(self.transitions[i]):
                if pr>0:
                    self.asf.add_transition(self.id2st[i],self.id2st[j], str(round(pr,3))+"_"+self.id2st[j])

        #INITIAL STATE
        self.asf.default_start_state = self.id2st[1]
        self.asf.initialize()

        #print(self.asf.pformat())

    def NextState(self):#RUNNING THE AUTOMATA
        """
        Returns the next state
        """
        current_state = self.states2idx[self.asf.current_state]
        #choose random number
        r = np.random.rand(1)
        #sample the next state from the current distribution
        next_state = np.argmin(self.cum_SUM[current_state]<r)
        #send the right event
        self.asf.process_event(str(round(self.transitions[current_state,next_state],3))+"_"+self.id2st[next_state])
        return next_state

    #Draw the Automata
    def DrawAutomata(self,fn='Commentator Automata.gv'):
        """
        Writes on file fn (default 'Commentator Automata.gv') representation of the Automata
        """
        #sorry for the next lines, i've a windows problem and without the following lines it doesnt work
        import os
        os.environ["PATH"] = os.environ["PATH"]+";C:/Program Files (x86)/Graphviz2.38/bin"
        g = Digraph('G', filename=fn)
        for st in self.asf.states:
            
            for k in self.asf._transitions[st].keys():
                
                label = k.split("_")[0]
                st1 = self.asf._transitions[st][k].name
                g.edge(st,st1,label=label)
                


        g.view()
