import json
import sys
from graphviz import Digraph

class AFD:
    def __init__(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            afd_definition = json.load(file)

        mandatory_keys = ["Q", "V", "delta", "q0", "F"]
        for key in mandatory_keys:
            if key not in afd_definition:
                raise ValueError(f"Chave '{key}' em falta no ficheiro JSON")

        self.states = afd_definition["Q"]
        self.alphabet = afd_definition["V"]
        self.transitions = afd_definition["delta"]
        self.initial_state = afd_definition["q0"]
        self.final_states = afd_definition["F"]

        if self.initial_state not in self.states:
            raise ValueError("O estado inicial não pertence ao conjunto de estados")

        for final_state in self.final_states:
            if final_state not in self.states:
                raise ValueError("O estado final não pertence ao conjunto de estados")

        for origin, transitions in self.transitions.items():
            if origin not in self.states:
                raise ValueError(f"O estado de origem '{origin}' não pertence ao conjunto de estados")
            for symbol, destination in transitions.items():
                if symbol != "Ɛ" and symbol not in self.alphabet:
                    raise ValueError(f"O símbolo '{symbol}' não pertence ao alfabeto da linguagem")
                if destination not in self.states:
                    raise ValueError(f"O estado de destino '{destination}' não pertence ao conjunto de estados")

    def generate_graphviz(self):
        output_file_name = "grafo_afd" 
        dot = Digraph()
        
        for state in self.states:
            if state in self.final_states:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state)

        dot.node('initial', shape='point')
        dot.edge('initial', self.initial_state)

        for origin, transitions in self.transitions.items():
            for symbol, destination in transitions.items():
                if symbol != "Ɛ":
                    dot.edge(origin, destination, label=symbol)
                else:
                    dot.edge(origin, destination, label="ε")

        dot.render(output_file_name, format='png', cleanup=True)
        print(f"Representação Graphviz gerada: {output_file_name}")

    def recognize_word(self, word):
        current_states = [self.initial_state]
        path = [self.initial_state]
        error_message = ""

        for symbol in word:
            if symbol not in self.alphabet:
                error_message = f"O símbolo '{symbol}' não pertence ao alfabeto da linguagem"
                return False, path, error_message

            next_states = [self.transitions.get(state, {}).get(symbol) for state in current_states]

            if not next_states:
                error_message = f"Transição inválida de '{current_states}' para '{next_states}' com símbolo '{symbol}'"
                return False, path, error_message

            path.append(symbol)
            path.extend(next_states)
            current_states = next_states

        if any(state in self.final_states for state in current_states):
            return True, path, "Palavra reconhecida."
        else:
            error_message = f"Nenhum dos estados {current_states} é final"
            return False, path, error_message

def main():
    if len(sys.argv) < 3:
        print("Uso: python afd_main.py <filename.json> [-graphviz | -rec <word>]")
        return

    file_name = sys.argv[1]
    operation = sys.argv[2]

    try:
        afd = AFD(file_name)

        if operation == "-graphviz":
            afd.generate_graphviz()
            print("Grafo gerado com sucesso.")
        elif operation == "-rec":
            if len(sys.argv) < 4:
                print("Uso: python afd_main.py <filename.json> -rec <word>")
                return
            word = sys.argv[3]
            recognized, path, message = afd.recognize_word(word)
            if recognized:
                print(f"'{word}' é reconhecida")
                print(f"[caminho {'->'.join(path)}]")
            else:
                print(f"'{word}' não é reconhecida")
                print(f"[{message}]")
        else:
            print("Operação inválida. Por favor, use -graphviz ou -rec")
    except ValueError as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
