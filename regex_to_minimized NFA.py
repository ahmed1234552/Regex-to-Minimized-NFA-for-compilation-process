

def validate_infix(infix):
    def check_square_brackets(infix):#return false if error
        open_bracket = False
        for char in infix:
            if char =='[':
                if open_bracket == True:
                    return False
                open_bracket = True

            elif char == ']':
                if open_bracket == True:
                    open_bracket = False
                else:
                    return False
        if open_bracket:
          return False
        return True

    def are_parentheses_balanced(s):
        stack = []
        for char in s:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False
                stack.pop()
        # If the stack is empty, all opening parentheses have a matching closing parentheses
        return len(stack) == 0

    def check_range(s):
        in_square_bracket = False

        for i in range(len(s)):
            if s[i] == '[':
                in_square_bracket = True
            elif s[i] == ']':
                in_square_bracket = False
            elif s[i] == '-':
                if i == 0 or i == len(s)-1 or not in_square_bracket:
                    return False
                else:
                    if not(s[i-1].isalnum() and s[i+1].isalnum()): #a true % flase  false
                        return False
        return True

    def alnum_or_operator(s):
        for c in s:
            if not(c.isalnum() or c in ['|','&','.','*','?', '-','+', '(',')','[',']']):#"|&.*?+-[]()"): # _,$ ??????
                return False
        return True
    return (alnum_or_operator(infix) and check_square_brackets(infix) and are_parentheses_balanced(infix) and check_range(infix))

def add_concat(s):
    new_s=""
    in_square_bracket = False
    for i in range(len(s)):
        if i == 0:
            new_s+=s[i]
            if s[i] == '[':#c[ , ][
                in_square_bracket = True
            continue

        if not in_square_bracket:   #should be before make in in_square_bracket = true
            if s[i] not in ['|','&','*','?','+',')',']']:#isalnum [ ( .
                if s[i-1] not in ['|','&','('] :
                    new_s+='&' #i add & before current

        if s[i] == '[':#c[ , ][
            in_square_bracket = True
        elif s[i] == ']':
            in_square_bracket = False


        new_s+=s[i]

    return new_s

def infix_to_postfix(infix):
    # precedence of the operators
    precedence = {
        "|": 1,
        "&": 2,
        ".": 3, #any single character higher priority
        "*": 4,
        "+": 4,
        "?": 4

    }

    # stack to store the operators
    stack = []

    # postfix expression
    postfix = ""

    """
    deal with [a-z] and [0-9] as a single operand
    [a-z0-9A-Z] -> [a-zA-Z0-9]

    """
    in_square_brackets = False

    # iterate through the infix expression
    for char in infix:

        # print("start of loop of char: ", char, "stack: ", stack, "postfix: ", postfix)

        # if the character is an operand "alphanumeric", add it to the postfix expression
        if char.isalnum() or char in ['.', '-', '_','[',']']:
            postfix += char
        elif char == '[':
            postfix += '['
            in_square_brackets = True
        elif char == ']':
            postfix += ']'
            in_square_brackets = False
        # if the character is an opening bracket, push it to the stack
        elif char == "(":
            stack.append(char)
        # if the character is a closing bracket, pop the operators from the stack and add them to the postfix expression until an opening bracket is encountered
        elif char == ")":
            while stack and stack[-1] != "(":
                # postfix += stack.pop()
                postfix += stack[-1]
                stack.pop()
            stack.pop() # pop the opening bracket
        # if the character is an operator, pop the operators from the stack and add them to the postfix expression based on the precedence
        else:
            while stack and precedence.get(stack[-1], 0) >= precedence.get(char, 0):
                # postfix += stack.pop()
                postfix += stack[-1]
                stack.pop()
            stack.append(char)

        # print("end of loop of char: ", char, "stack: ", stack, "postfix: ", postfix)

    # pop the remaining operators from the stack and add them to the postfix expression
    while stack:
        postfix += stack.pop()

    return postfix

class Edge:
    def __init__(self):
        self.symbol = None
        self.target = None

class State:
    def __init__(self):
        self.name = None
        self.edges = []

    def __str__(self) -> str:
        return self.name

class NFA:
    def __init__(self, start, accept, states):
        self.start = start
        self.accept = accept
        self.states = states

    def __str__(self) -> str:
        return f"start: {self.start}, accept: {self.accept}, states: {self.states}"

    def is_equal(self, nfa):
        # return self.start == nfa.start and self.accept == nfa.accept and self.states == nfa.states # you need to check names

        def state_match(state1, state2):
            return state1.name == state2.name

        if not state_match(self.start, nfa.start) or not state_match(self.accept, nfa.accept):
            return False

        for state1, state2 in zip(self.states, nfa.states):
            if not state_match(state1, state2):
                return False

            for edge1, edge2 in zip(state1.edges, state2.edges):
                if edge1.symbol != edge2.symbol or not state_match(edge1.target, edge2.target):
                    return False

        return True

def ConstructNFA(symbol, states_counter, stack):
    start = State()
    start.name = f"S{states_counter}"
    accept = State()
    accept.name = f"S{states_counter + 1}"

    edge = Edge()
    edge.symbol = symbol
    edge.target = accept

    start.edges.append(edge)

    stack.append(NFA(start, accept, [start, accept]))

def concatNFA(stack):
    nfa2 = stack.pop()
    nfa1 = stack.pop()

    edge = Edge()
    edge.symbol = "ε"
    edge.target = nfa2.start
    nfa1.accept.edges.append(edge)

    stack.append(NFA(nfa1.start, nfa2.accept, nfa1.states + nfa2.states))

def orNFA(stack, states_counter):
    nfa2 = stack.pop()
    nfa1 = stack.pop()

    start = State()
    start.name = f"S{states_counter}"
    accept = State()
    accept.name = f"S{states_counter + 1}"

    edge1 = Edge()
    edge1.symbol = "ε"
    edge1.target = nfa1.start
    start.edges.append(edge1)

    edge2 = Edge()
    edge2.symbol = "ε"
    edge2.target = nfa2.start
    start.edges.append(edge2)

    edge3 = Edge()
    edge3.symbol = "ε"
    edge3.target = accept
    nfa1.accept.edges.append(edge3)

    edge4 = Edge()
    edge4.symbol = "ε"
    edge4.target = accept
    nfa2.accept.edges.append(edge4)

    stack.append(NFA(start, accept, [start, accept] + nfa1.states + nfa2.states))

def ZeroMoreNFA(stack, states_counter):
    nfa = stack.pop()

    start = State()
    start.name = f"S{states_counter}"
    accept = State()
    accept.name = f"S{states_counter + 1}"

    edge1 = Edge()
    edge1.symbol = "ε"
    edge1.target = nfa.start
    start.edges.append(edge1)

    edge2 = Edge()
    edge2.symbol = "ε"
    edge2.target = accept
    start.edges.append(edge2)

    edge3 = Edge()
    edge3.symbol = "ε"
    edge3.target = start
    nfa.accept.edges.append(edge3)

    edge4 = Edge()
    edge4.symbol = "ε"
    edge4.target = accept
    nfa.accept.edges.append(edge4)

    stack.append(NFA(start, accept, [start, accept] + nfa.states))

def OneMoreNFA(stack, states_counter):
    nfa = stack.pop()

    start = State()
    start.name = f"S{states_counter}"
    accept = State()
    accept.name = f"S{states_counter + 1}"

    edge1 = Edge()
    edge1.symbol = "ε"
    edge1.target = nfa.start
    start.edges.append(edge1)

    edge2 = Edge()
    edge2.symbol = "ε"
    edge2.target = accept
    nfa.accept.edges.append(edge2)

    edge3 = Edge()
    edge3.symbol = "ε"
    edge3.target = start
    nfa.accept.edges.append(edge3)

    stack.append(NFA(start, accept, [start, accept] + nfa.states))

def ZeroOrOneNFA(stack, states_counter):
    nfa = stack.pop()

    start = State()
    start.name = f"S{states_counter}"
    accept = State()
    accept.name = f"S{states_counter + 1}"

    edge1 = Edge()
    edge1.symbol = "ε"
    edge1.target = nfa.start
    start.edges.append(edge1)

    edge2 = Edge()
    edge2.symbol = "ε"
    edge2.target = accept
    start.edges.append(edge2)

    edge3 = Edge()
    edge3.symbol = "ε"
    edge3.target = accept
    nfa.accept.edges.append(edge3)

    stack.append(NFA(start, accept, [start, accept] + nfa.states))

def PostFix_To_NFA(postfix):
    stack = []
    states_counter = 0
    range_group = ""
    in_range = False

    for token in postfix:
        if token == '[':
            range_group = "["
            in_range = True
        elif token == ']': #this should be before the next elif to prevent adding characters to the range_group after the ']'
            range_group += "]"
            ConstructNFA(range_group, states_counter, stack)
            states_counter += 2
            in_range = False
        elif in_range:
            range_group += token
        elif token.isalnum() or token in ['.', '_']:
            ConstructNFA(token, states_counter,stack)
            states_counter += 2
        elif token == '*':
            ZeroMoreNFA(stack, states_counter)
            states_counter += 2
        elif token == '+':
            OneMoreNFA(stack, states_counter)
            states_counter += 2
        elif token == '?':
            ZeroOrOneNFA(stack, states_counter)
            states_counter += 2
        elif token == '|':
            orNFA(stack, states_counter)
            states_counter += 2
        elif token == '&':
            concatNFA(stack)
        else:
            print(f"unknown operator {token}")

    result = stack.pop()
    return result

def printNFA(nfa):
    print("start: ", nfa.start)
    print("accept: ", nfa.accept)
    print("states: ")
    for state in nfa.states:
        print(state, end=", ")
        #edges
        print("edges: ", end="")
        for edge in state.edges:
            print(edge.symbol, edge.target, end=", ")
        print()

def visualizeNFA(nfa):#using graphviz
    import graphviz
    dot = graphviz.Digraph(comment='NFA', graph_attr={'rankdir':'LR'})

    #add arrow to the start state
    dot.node('', shape='none')
    dot.edge('', nfa.start.name, label='start',)    #edge creates a node if it does not exist

    # dot.node(name = nfa.start.name,label = nfa.start.name, shape='circle')     #we create the start state in the loop

    dot.node(nfa.accept.name, nfa.accept.name, shape='doublecircle')
    for state in nfa.states:    #states include start and accept states and other states
        for edge in state.edges:
            dot.edge(state.name, edge.target.name, label=edge.symbol)

    # Render and view the graph
    # dot.render('nfa_graph', format='png', cleanup=True)
    # dot.view()
    display(dot)

def to_json(nfa):
    json = {}
    json["startingState"] = nfa.start.name

    for state in nfa.states:
        state_json = {}
        state_json["isTerminatingState"] = state == nfa.accept

        for edge in state.edges:
            # print(edge.symbol, edge.target.name, end=", ")
            #check if the symbol is already in the json and append the target state to it
            if edge.symbol in state_json:
                if not isinstance(state_json[edge.symbol], list):
                    state_json[edge.symbol] = [state_json[edge.symbol]]
                state_json[edge.symbol].append(edge.target.name)
            else:
                state_json[edge.symbol] = edge.target.name
        json[state.name] = state_json

    return json

def nfa_json_to_nfa(json_nfa):
    start = None
    accept = None
    states = []
    start_name = ""

    for state_name, transitions in json_nfa.items():

        if state_name == "startingState":
            start_name = transitions
            continue  # Skip the starting state

        #check if the state is already in the states by check if the state_name == any state.name in states
        # and get the state if it's already in the states or create a new state

        state = next((state for state in states if state.name == state_name), None)

        if state == None:
            state = State()
            state.name = state_name
            states.append(state)

        if start_name == state_name:
            start = state

        if transitions['isTerminatingState']:#.get('isTerminatingState', False):
            accept = state

        for symbol, target_state in transitions.items():
            if symbol != 'isTerminatingState':
                #if the target state is a list
                if isinstance(target_state, list):
                    for state_name in target_state:
                        edge = Edge()
                        go_to_state = next((s for s in states if s.name == state_name), None)
                        edge.symbol = symbol
                        if go_to_state == None:
                            go_to_state = State()
                            go_to_state.name = state_name
                            states.append(go_to_state)
                        edge.target = go_to_state
                        state.edges.append(edge)
                else:
                    edge = Edge()
                    go_to_state2 = next((s for s in states if s.name == target_state), None) #don't use Next
                    edge.symbol = symbol
                    if go_to_state2 == None:
                        go_to_state2 = State()
                        go_to_state2.name = target_state
                        states.append(go_to_state2)

                    edge.target = go_to_state2
                    state.edges.append(edge)

    return NFA(start, accept, states)


"""
nfa to dfa
we work on the nfa not the dfa,
we only check when we add a new collection state to the dfa if it's exist append to the edges of it
else add this new collection state and add the edges
1.get the epsilon closure of start
eplsilon closure of state are the states you can go to from this state by edge has symbol epsilon and the state itself
2.make a new collection state new_collection_start(set) includes the epsilon closure of start and mark it as start ot dfa
3.get all possible symbols in the nfa
4.loop on the states in the new collection state and get c_s every time
    5.loop over all these symbols and take s every loop
    collection_state_can_go_to_by_s = ""  #example c_s.name={"S0", "S1", "S2"}
    6.get the original state c_s from the nfa :nfa_state
    7.if s exist in nfa_state edges: nfa_state --s--> distination state d_s
        8.get the epsilon closure of d_s and make a new temp collection state temp_c_s to it
            9.if the temp_c_s exist in the new dfa_collection_states
                10.make a new edge with symbol s from the new_collection_start to original temp_c_s in the dfa states
                else: make a new_c_s includes the closure of d_s and add edge new_collection_start--s-->new_c_s
                    and if it icludes the accept state mark it as accept state
    11.if the new_c_s is not empty add it to the dfa collection states


    we need to do the same thing to all the dfa collection states but every loop we may add a new collection state and we need to do the same thing to it
    so we need to make dfa collection states as a set and we loop over it
"""

class DFAState:
    def __init__(self, states):
        self.states = states
        self.transitions = {}
        self.is_accept = False
        self.name = ''.join(state.name for state in states)

    def add_transition(self, symbol, state):
        self.transitions[symbol] = state #no possibility of having two transitions with the same symbol in dfa

def is_in_dfa_states(dfa_states, state):

    def state_match(dfa_state_name, state_name):
        # S0S1S3 == S0S1S3 even if the order is different S1S0S3 == S0S1S3
        dfa_state_name = ''.join(sorted(dfa_state_name))
        state_name = ''.join(sorted(state_name))
        return dfa_state_name == state_name

    # compare the states.name
    for dfa_state in dfa_states:
        if state_match(dfa_state.name,state.name):
            return True
    return False

def epsilon_closure(nfa, states):
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        for edge in state.edges:
            if edge.symbol == 'ε' and edge.target not in closure:
                closure.add(edge.target)
                stack.append(edge.target)

    return closure

def move(nfa, states, symbol):
    move_states = set()
    for state in states:
        for edge in state.edges:
            if edge.symbol == symbol:
                move_states.add(edge.target)
    return move_states

def subset_construction(nfa):
    dfa_states = set()
    start_state = DFAState(epsilon_closure(nfa, [nfa.start]))

    dfa_states.add(start_state)
    unmarked_states = [start_state]

    alphabet = set()
    for state in nfa.states:
        for edge in state.edges:
            if edge.symbol != 'ε':
                alphabet.add(edge.symbol)

    while unmarked_states:
        current_state = unmarked_states.pop()
        for symbol in alphabet:
            next_states = epsilon_closure(nfa, move(nfa, current_state.states, symbol))
            if next_states:
                next_state = DFAState(next_states)
                if not is_in_dfa_states(dfa_states, next_state):
                    dfa_states.add(next_state)
                    unmarked_states.append(next_state)
                current_state.add_transition(symbol, next_state)

    dfa_accepting_states = {state for state in dfa_states if nfa.accept in state.states}

    #set state.accept
    for state in dfa_states:
        if nfa.accept in state.states:
            state.is_accept = True

    return {
        'startingState': start_state,
        'states': dfa_states,
        'accepting_states': dfa_accepting_states
    }

def dfa_to_json(dfa):
    json = {}
    json["startingState"] = dfa['startingState'].name
    for state in dfa['states']:
        state_json = {}
        state_json["isTerminatingState"] = state.is_accept
        for symbol in state.transitions:
            state_json[symbol] = state.transitions[symbol].name
        json[state.name] = state_json

    return json

def print_dfa(dfa_json):
    print("start: ", dfa_json['startingState'].name)
    print("accepting states: ", end="")
    for state in dfa_json['accepting_states']:
        print(state.name, end=", ")
    print()
    print("states: ", end="")
    for state in dfa_json['states']:
        print(state.name, end=", ")
    print()

def visualize_dfa(dfa):
    import graphviz

    # Create a mapping from original state names to unique identifiers
    state_mapping = {}
    unique_id_counter = 0
    for state in dfa['states']:
        unique_id = 'S{}'.format(unique_id_counter)
        state_mapping[state.name] = unique_id
        unique_id_counter += 1

    dot = graphviz.Digraph(comment='DFA', graph_attr={'rankdir':'LR'})

    # Add arrow to the start state
    dot.node('', shape='none')
    start_state_id = state_mapping[dfa['startingState'].name]
    dot.edge('', start_state_id, label='start')

    for state in dfa['states']:
        state_id = state_mapping[state.name]
        if state in dfa['accepting_states']:
            dot.node(state_id, state_id, shape='doublecircle')
        else:
            dot.node(state_id, state_id, shape='circle')

        for symbol in state.transitions:
            target_state_id = state_mapping[state.transitions[symbol].name]
            dot.edge(state_id, target_state_id, label=symbol)

    # Render and view the graph
    # dot.render('dfa_graph', format='png', cleanup=True)
    # dot.view()
    display(dot)

def minimize_dfa(dfa_json):
    """
    {
    'startingState': 'S4S0S2',
    'accepting_states': ['S7'],
    'S3S6S5': {'isTerminatingState': False, 'c': 'S7'},
    'S1S6S5': {'isTerminatingState': False, 'c': 'S7'},
    'S7': {'isTerminatingState': False}
    }
    if we have a state that has the same transitions to the same states and has the same teminating state
    the two dictionaries are the same so
    we can merge them by removing one of them and changing the transitions of the other to the transitions of the removed one
        and we can do this in loops until we can't merge any two states

    """

    items_list = list(dfa_json.items())
    for state1, value1 in items_list:
        if state1 == 'startingState':
            continue
        for state2, value2 in list(dfa_json.items()):
            if state2 == 'startingState':
                continue
            if state1 != state2 and value1 == value2:
                for state, state_value in dfa_json.items():
                    if state == 'startingState':
                        continue
                    for symbol, target_state in state_value.items():
                        if symbol == 'startingState':
                            continue
                        if target_state == state2:
                            dfa_json[state][symbol] = state1
                del dfa_json[state2]
                items_list.remove((state2, value2))  # Remove the item from the list
                # break  # Exit the inner loop after deleting state2

    return dfa_json

def visualize_minimized_dfa(dfa_json):
    import graphviz

    dot = graphviz.Digraph(comment='DFA', graph_attr={'rankdir':'LR'})

    # Create a mapping from original state names to unique identifiers
    state_mapping = {}
    unique_id_counter = 0
    for state in dfa_json:
        if state == 'startingState':
            continue
        state_mapping[state] = 'S{}'.format(unique_id_counter)
        unique_id_counter += 1

    # Add arrow to the start state
    dot.node('', shape='none')
    dot.edge('', state_mapping[dfa_json['startingState']], label='start')

    for state in dfa_json:
        if state == 'startingState':
            continue

        # Check if the state is terminating
        if dfa_json[state]['isTerminatingState']:
            dot.node(state_mapping[state], state_mapping[state], shape='doublecircle')
        else:
            dot.node(state_mapping[state], state_mapping[state], shape='circle')

        # Add edges for transitions
        for symbol, target_state in dfa_json[state].items():
            if symbol == 'isTerminatingState':
                continue
            dot.edge(state_mapping[state], state_mapping[target_state], label=symbol)

    # Render and view the graph
    # dot.render('minimized_dfa', format='png', cleanup=True)
    # dot.view()
    display(dot)

def main(infix):
    # infix = input("Enter the infix expression: ")
    #!----input----
    # infix = "(A*|B+)C?D"

    if not validate_infix(infix):
        print("inavalid regex")
        return

    infix = add_concat(infix)
    # print("infix after concatenation : ",infix)

    if not (infix[0].isalnum() or infix[0] == '[' or infix[0]=='(' or '.'):
        print("inavalid regex")
        return

    postfix = infix_to_postfix(infix)
    # print("Postfix expression: ", postfix)

    nfa = PostFix_To_NFA(postfix)#symbol may be repeated with different targets

    #?part 1

    visualizeNFA(nfa)

    json_nfa = to_json(nfa)

    import json
    with open('nfa.json', 'w', encoding='utf-8') as f:
        json.dump(json_nfa, f, indent=4, ensure_ascii=False)

    #?part 2

    with open('nfa.json', 'r', encoding='utf-8') as f:
        json_nfa_read = json.load(f) #json_nfa is a dictionary

    n_nfa = nfa_json_to_nfa(json_nfa_read)

    dfa = subset_construction(n_nfa)

    visualize_dfa(dfa)
    json_dfa = dfa_to_json(dfa)

    minimized_dfa_json = minimize_dfa(json_dfa)
    visualize_minimized_dfa(minimized_dfa_json)

    with open('minimized_dfa.json', 'w', encoding='utf-8') as f:
        json.dump(minimized_dfa_json, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    infix = "[a-z]*[0-9]+[A-Z]?"
    main(infix)
