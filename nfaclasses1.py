class global_variables (object):
    state_counter = int
    world_states = dict()
    def __init__(self):
        self.state_counter =0
        self.world_states ={}


class state (object):

    transitions = dict()

    def __init__(self, variables,transitions):

        self.number =variables.state_counter
        self.transitions = transitions
        variables.world_states[variables.state_counter]=self
        variables.state_counter += 1



class nfa (object):
    states = []
    final_states = []
    start_state= state


    def __init__(self,name,states,final_states,start_state):
        self.name = name
        self.states=states
        self.final_states=final_states
        self.start_state=start_state


    @classmethod
    def init_from_min(cls,input_symbol,name,variables):
        name=name
        end_state =state(variables,{})
        start_state =state(variables,{input_symbol:[end_state.number]})
        states = [start_state.number,end_state.number]
        final_states=[end_state.number]
        return cls(name,states,final_states,start_state)




    @classmethod
    def init_or_nfa(cls,name,first_nfa,second_nfa,variables):
        name=name
        end_state =state(variables,{})
        for x in first_nfa.final_states:
            for y in variables.world_states:
                if x == y:
                    variables.world_states[y].transitions["$"] = [end_state.number]

        for x in second_nfa.final_states:
            for y in variables.world_states:
                if x == y:
                    variables.world_states[y].transitions["$"] = [end_state.number]
        final_states = []
        final_states.append(end_state.number)
        trans = {"$": [second_nfa.start_state.number ,  first_nfa.start_state.number] }
        start_state=state(variables  ,trans)

        states = []
        states.append(start_state.number)
        for w in first_nfa.states:
            states.append(w)
        for o in second_nfa.states:
            states.append(o)

        states.append(end_state.number)

        return cls(name,states,final_states,start_state)




    @classmethod
    def init_and_nfa(cls,name,first_nfa,second_nfa,variables):
        name = name
        start_state =first_nfa.start_state
        for x in first_nfa.final_states:
            for y in variables.world_states:
                if y == x:
                    variables.world_states[y].transitions["$"]=[second_nfa.start_state.number]

        final_states = second_nfa.final_states
        states = []
        for w in first_nfa.states:
            states.append(w)
        for o in second_nfa.states:
            states.append(o)
        
        return cls(name,states,final_states,start_state)

    @classmethod
    def init_star_nfa(cls,name,first_nfa,variables):
        name = name
        end_state = state(variables,{})
        for x in first_nfa.final_states:
            for y in variables.world_states:
                if x == y:
                    variables.world_states[y].transitions["$"]=[first_nfa.start_state.number,end_state.number]


        final_states = []
        final_states.append(end_state.number)
        start_state = state(variables, {"$":[first_nfa.start_state.number,end_state.number]} )
        states=[]
        states.append(start_state.number)
        for o in first_nfa.states:
            states.append(o)
        states.append(end_state.number)
        return cls(name, states, final_states, start_state)

    @classmethod
    def init_plus_nfa(cls, name, first_nfa, variables):
        name = name
        end_state = state(variables, {})
        for x in first_nfa.final_states:
            for y in variables.world_states:
                if x == y:
                    variables.world_states[y].transitions["$"] = [first_nfa.start_state.number, end_state.number]

        final_states = []
        final_states.append(end_state.number)
        start_state = state(variables, {"$": [first_nfa.start_state.number]})
        states = []
        states.append(start_state.number)
        for o in first_nfa.states:
            states.append(o)
        states.append(end_state.number)
        return cls(name, states, final_states, start_state)















#############################################################################
#variables = global_variables()
#a = nfa.init_from_min("a","letter",variables)
#b = nfa.init_from_min("b","letter",variables)
#c = nfa.init_from_min("c","letter",variables)
#ab= nfa.init_or_nfa("ab",a,b,variables)
#abc=nfa.init_or_nfa("abc",c,ab,variables)

#x = nfa.init_from_min("x","letter",variables)
#y = nfa.init_from_min("y","letter",variables)

#xy= nfa.init_and_nfa("xy",x,y,variables)
#a = nfa.init_from_min("a","letter",variables)
#aORxy=nfa.init_or_nfa("aORxy",a,xy,variables)



print "\n\tfml"

