import random
import re

# Função principal para avaliar nós da AST
def evaluate(node, variables, functions):
    if isinstance(node, tuple):
        op = node[0]
        if op == '+':
            return evaluate(node[1], variables, functions) + evaluate(node[2], variables, functions)
        elif op == '-':
            return evaluate(node[1], variables, functions) - evaluate(node[2], variables, functions)
        elif op == '*':
            return evaluate(node[1], variables, functions) * evaluate(node[2], variables, functions)
        elif op == '/':
            return evaluate(node[1], variables, functions) // evaluate(node[2], variables, functions)
        elif op == 'concat':
            return str(evaluate(node[1], variables, functions)) + str(evaluate(node[2], variables, functions))
        elif op == 'assign':
            value = evaluate(node[2], variables, functions)
            variables[node[1]] = value
            return value
        elif op == 'escrever':
            value = evaluate(node[1], variables, functions)
            if isinstance(value, str):
                value = interpolate_string(value, variables)
            print(value)
            return value
        elif op == 'entrada':
            value = int(input("Introduza um num: "))
            return value
        elif op == 'aleatorio':
            if len(node) == 2:
                value = random.randint(0, evaluate(node[1], variables, functions))
            else:
                value = random.randint(0, 10)
            return value
        elif op == 'call':
            func_name = node[1]
            args = [evaluate(arg, variables, functions) for arg in node[2]]
            arg_count = len(args)
            if func_name == 'map':
                func_to_apply = args[0][1]  # 'var', 'function_name'
                list_to_apply = args[1]
                return [evaluate(('call', func_to_apply, [elem]), variables, functions) for elem in list_to_apply]
            elif func_name == 'fold':
                func_to_apply = args[0][1]  # 'var', 'function_name'
                list_to_apply = args[1]
                initial_value = args[2]
                result = initial_value
                for elem in list_to_apply:
                    result = evaluate(('call', func_to_apply, [elem, result]), variables, functions)
                return result
            else:
                if func_name in functions and arg_count in functions[func_name]:
                    func_params, func_body = functions[func_name][arg_count]
                    local_vars = {param: arg for param, arg in zip(func_params, args)}
                    return evaluate(func_body, {**variables, **local_vars}, functions)
                else:
                    raise Exception(f"Undefined function '{func_name}' with {arg_count} arguments")
        elif op == 'num':
            return node[1]
        elif op == 'string':
            return node[1]
        elif op == 'list':
            return [evaluate(elem, variables, functions) for elem in node[1]]
        elif op == 'var':
            if node[1] in variables:
                return variables[node[1]]
            elif node[1] in functions:
                return ('func', node[1])
            else:
                raise Exception(f"Undefined variable or function '{node[1]}'")
    else:
        return node

# Função para interpolar variáveis dentro de uma string
def interpolate_string(string, variables):
    def replace_var(match):
        var_name = match.group(1)
        return str(variables.get(var_name, f'#{var_name}'))
    return re.sub(r'#{(\w+[\?\!]*)}', replace_var, string)

