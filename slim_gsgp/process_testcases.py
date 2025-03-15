import ast
import csv
import json

def load_data(file_name):
    with open(file_name, "r") as f:
        return json.load(f)
    
def txt_to_csv(input_txt_file, output_csv_file):
    with open(input_txt_file, "r") as f:
        lines = f.readlines()

    # Extract `inval` and `outval`
    for line in lines:
        if line.startswith("inval ="):
            inval = ast.literal_eval(line.split("=", 1)[1].strip())  # Convert string to list
        elif line.startswith("outval ="):
            outval = ast.literal_eval(line.split("=", 1)[1].strip())  # Convert string to list

    # Ensure the number of rows match
    assert len(inval) == len(outval), "Mismatch between inval and outval lengths"

    # Write to CSV
    with open(output_csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        
        # Writing header (optional, based on `inval` size)
        header = [f"feature_{i+1}" for i in range(len(inval[0]))] + ["output"]
        writer.writerow(header)

        # Writing rows
        for i in range(len(inval)):
            writer.writerow(inval[i] + [outval[i][0]])  # Assumes outval has a nested structure



problems=load_data("datasets/data/my_data/rmse.json")

print(problems)

for problem in problems["PSB1"]:
    print(problem)
    txt_to_csv(f"datasets/data/my_data/test_cases/PSB1/{problem}/Test.txt", f"datasets/data/my_data/test_cases/PSB1/{problem}/cases.csv")

