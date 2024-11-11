import json
import sys

class AFND:
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.initial_state = None
        self.final_states = set()

    def add_transition(self, origin, symbol, destination):
        self.states.add(origin)
        self.states.add(destination)
        if symbol:  # Adiciona ao alfabeto apenas se o símbolo não for vazio
            self.alphabet.add(symbol)
        if origin not in self.transitions:
            self.transitions[origin] = {}
        if symbol not in self.transitions[origin]:
            self.transitions[origin][symbol] = set()
        self.transitions[origin][symbol].add(destination)

    def to_json(self, filename):
        afnd_json = {
            "Q": sorted(list(self.states)),
            "V": sorted(list(self.alphabet)),
            "delta": {state: {symbol: sorted(list(destinations)) for symbol, destinations in transitions.items()} for state, transitions in self.transitions.items()},
            "q0": self.initial_state,
            "F": sorted(list(self.final_states))
        }
        with open(filename, 'w') as file:
            json.dump(afnd_json, file, indent=2)

def process_er(expression, afnd, start_state):
    if "simb" in expression:
        symbol = expression["simb"]
        next_state = f"q{len(afnd.states)}"
        afnd.add_transition(start_state, symbol, next_state)
        return next_state
    elif "op" in expression:
        op = expression["op"]
        args = expression["args"]
        if op == "alt":
            split_start = f"q{len(afnd.states)}"
            afnd.states.add(split_start)
            afnd.add_transition(start_state, "", split_start)
            final_states = set()
            for arg in args:
                final_state = process_er(arg, afnd, split_start)
                final_states.add(final_state)
            new_final_state = f"q{len(afnd.states)}"
            afnd.states.add(new_final_state)
            for state in final_states:
                afnd.add_transition(state, "", new_final_state)
            return new_final_state
        elif op == "seq":
            current_state = start_state
            for arg in args:
                current_state = process_er(arg, afnd, current_state)
            return current_state
        elif op == "kle":
            kleene_start = f"q{len(afnd.states)}"
            kleene_end = f"q{len(afnd.states) + 1}"
            afnd.states.add(kleene_start)
            afnd.states.add(kleene_end)
            afnd.add_transition(start_state, "", kleene_start)
            inner_final_state = process_er(args[0], afnd, kleene_start)
            afnd.add_transition(inner_final_state, "", kleene_start)
            afnd.add_transition(kleene_start, "", kleene_end)
            return kleene_end

def convert_er_to_afnd(expression):
    afnd = AFND()
    start_state = "q0"
    afnd.initial_state = start_state
    afnd.states.add(start_state)
    final_state = process_er(expression, afnd, start_state)
    afnd.final_states.add(final_state)
    return afnd

def main():
    if len(sys.argv) != 4 or sys.argv[2] != "--output":
        print("Uso: python er_main.py er.json --output afnd.json")
        return

    input_filename = sys.argv[1]
    output_filename = sys.argv[3]

    with open(input_filename, 'r') as file:
        expression = json.load(file)

    afnd = convert_er_to_afnd(expression)
    afnd.to_json(output_filename)
    print(f"AFND gerado e guardado como {output_filename}")

if __name__ == "__main__":
    main()
