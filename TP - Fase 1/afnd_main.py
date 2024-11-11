import json
import sys
from graphviz import Digraph

class AFND:
    def __init__(self, afnd_json):
        self.Q = afnd_json["Q"]
        self.V = afnd_json["V"]
        self.delta = afnd_json["delta"]
        self.q0 = afnd_json["q0"]
        self.F = afnd_json["F"]

    def epsilon_closure(self, states):
        closure = set(states)
        new_states = True
        while new_states:
            new_states = False
            for state in list(closure):
                if "" in self.delta.get(state, {}):
                    for next_state in self.delta[state][""]:
                        if next_state not in closure:
                            closure.add(next_state)
                            new_states = True
        return closure
    
    def move(self, states, symbol):
        next_states = set()
        for state in states:
            if symbol in self.delta.get(state, {}):
                next_states.update(self.delta[state][symbol])
        return next_states

    def convert_to_afd(self):
        initial_closure = self.epsilon_closure([self.q0])
        dfa_states = {frozenset(initial_closure): 'q0'}
        dfa_transitions = {}
        dfa_final_states = set()
        unmarked_states = [initial_closure]

        while unmarked_states:
            current_closure = unmarked_states.pop()
            current_state = frozenset(current_closure)
            dfa_transitions[dfa_states[current_state]] = {}

            for symbol in self.V:
                move_result = self.move(current_closure, symbol)
                new_closure = self.epsilon_closure(move_result)

                if new_closure:
                    new_state = frozenset(new_closure)
                    if new_state not in dfa_states:
                        new_state_name = f'q{len(dfa_states)}'
                        dfa_states[new_state] = new_state_name
                        unmarked_states.append(new_closure)
                    else:
                        new_state_name = dfa_states[new_state]

                    dfa_transitions[dfa_states[current_state]][symbol] = new_state_name

                    if any(s in self.F for s in new_closure):
                        dfa_final_states.add(new_state_name)

        return {
            "Q": list(dfa_states.values()),
            "V": list(self.V),
            "delta": dfa_transitions,
            "q0": dfa_states[frozenset(initial_closure)],
            "F": list(dfa_final_states)
        }

    def generate_graphviz_afnd(self, output_file_name):
        dot = Digraph()

        for state in self.Q:
            if state in self.F:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state)

        dot.node('initial', shape='point')
        dot.edge('initial', self.q0)

        for origin, transitions in self.delta.items():
            for symbol, destinations in transitions.items():
                for destination in destinations:
                    if symbol != "":
                        dot.edge(origin, destination, label=symbol)
                    else:
                        dot.edge(origin, destination, label="ε")

        dot.render(output_file_name, format='png', cleanup=True)
        print(f"Representação Graphviz gerada: {output_file_name}.png")

def main():
    if len(sys.argv) < 3:
        print("Uso: python afnd_main.py <filename.json> [-graphviz | -output afd.json]")
        return

    file_name = sys.argv[1]
    operation = sys.argv[2]

    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            afnd_json = json.load(file)

        afnd = AFND(afnd_json)

        if operation == "-graphviz":
            afnd.generate_graphviz_afnd("grafo_afnd")
            print("Grafo gerado com sucesso.")
        elif operation == "-output":
            output_file = sys.argv[3]
            afd = afnd.convert_to_afd()
            with open(output_file, 'w') as file:
                json.dump(afd, file, indent=2)
            print(f"AFD gerado e guardado como {output_file}")
        else:
            print("Operação inválida. Por favor, use -graphviz ou -output")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
