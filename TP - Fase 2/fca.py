from FCAGrammar import parse, functions
from FCAEval import evaluate
import sys

def main():
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            contents = file.read()
            try:
                tree = parse(contents)
                variables = {}
                last_result = None
                for node in tree:
                    last_result = evaluate(node, variables, functions)
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
    else:
        variables = {}
        last_result = None
        while True:
            try:
                expr = input(">> ")
                if expr == "":
                    break
                tree = parse(expr)
                for node in tree:
                    last_result = evaluate(node, variables, functions)
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
