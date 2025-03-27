import ast
import json
import inspect
from radon.complexity import cc_visit
import ast
import re
import csv
import os 
from support_functions import count_nodes, count_sloc, create_folder, load_data, write_list_to_csv, normalize_tree, max_depth

def parse_gp_individual(individual):
    # Find all variables (x0, x1, x2, etc.)
    variables = set(re.findall(r'x\d+', individual))

    # Create the function signature with dynamic arguments
    func_signature = f"def dynamic_function({', '.join(variables)}):"
    
    # Replace 'f(...)' with the expression inside the parentheses to simplify the GP expression.
    expression = re.sub(r'f\((.*?)\)', r'\1', individual)
    
    # Replace operators and constants to make the expression valid in Python
    expression = expression.replace('multiply', '*')
    expression = expression.replace('add', '+')
    expression = expression.replace('subtract', '-')
    expression = expression.replace('divide', '/')
    expression = expression.replace('constant', '')
    
    # Indent the expression for the function body
    func_body = f"    return {expression}"
    
    # Combine the function signature and the body
    full_function = f"{func_signature}\n{func_body}"

    return full_function




if __name__=="__main__":
    
    
    rmse_problems = load_data("datasets/data/my_data/rmse.json")
    

    for benchmark in rmse_problems:

        unique_sol_results = [["PROBLEM", "N_UNIQUE_SOURCE", "N_UNIQUE_ASTS"]] #header

        for problem in rmse_problems[benchmark]:

            if problem=="luhn":
                continue

            print(problem)

            create_folder(f"results/pop_analysis/{benchmark}/{problem}")

            population = load_data(f"results/slim_x_sig1/{problem}_5_pop.json")

            metric_results = [["SLOC", "CYCLOMATIC_COMPLEXITY", "AST_NODES", "AST_DEPTH"]] #header
            unique_source_codes = []
            unique_asts = []
            n_unique_asts = 0
            n_unique_source = 0

            for individual in population:

                func_body = individual[0]

                source_code = parse_gp_individual(func_body)
                
                if source_code.startswith("#"):
                    #print("parsing error")
                    continue

                print(source_code)
                sloc = count_sloc(source_code)
                
                #calculate cyclomatic complexity
                complexity_results = cc_visit(source_code) #get complexity analysis
                cc = complexity_results[0].complexity

                #change name of func to "func" to avoid name conflicts
                match = re.match(r"def (\w+)\(", source_code)
                if match:
                    old_name = match.group(1)
                source_code = source_code.replace(old_name, "func", 1)

                #remove comments from source code
                source_code = "\n".join(line for line in source_code.splitlines() if not re.match(r'^\s*#', line))

                #check whether source code is unique
                if source_code not in unique_source_codes:
                    unique_source_codes.append(source_code)
                    n_unique_source += 1

                #convert to ast tree
                parsed_ast = ast.parse(source_code)

                n_nodes = count_nodes(parsed_ast) #calculate number of nodes in ast
                depth = max_depth(parsed_ast) #calculate max depth in ast

                #check whether ast is unique
                parsed_ast = normalize_tree(parsed_ast)
                
                if parsed_ast not in unique_asts:
                    unique_asts.append(parsed_ast)
                    n_unique_asts += 1

                #append metrics of each function to results
                metric_results.append([sloc, cc, n_nodes, depth])
            unique_sol_results.append([problem, n_unique_source, n_unique_asts])
            write_list_to_csv(unique_sol_results, f"results/pop_analysis/{benchmark}/unique_solutions.csv") 
            write_list_to_csv(metric_results, f"results/pop_analysis/{benchmark}/{problem}/results.csv")

