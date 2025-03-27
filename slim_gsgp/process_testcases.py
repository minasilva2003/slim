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


def write_json_to_csv(json_filename, csv_filename):
    # Read JSON lines and store data
    data = []
    with open(json_filename, "r") as json_file:
        counter=0 #only get 1000 test cases
        for line in json_file:
            entry = json.loads(line.strip())  # Parse JSON line
            data.append(entry)  # Store dictionary
            counter+=1
            if counter==1000:
                break

    # Extract column names dynamically
    fieldnames = list(data[0].keys())  # Use the keys from the first entry

    # Write to CSV file
    with open(csv_filename, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()  # Write column names
        writer.writerows(data)  # Write data rows

    print(f"CSV file '{csv_filename}' successfully created!")



def json_to_csv(json_file, csv_file):
    with open(json_file, 'r') as f:
        lines = f.readlines()
    
    lines=lines[:1000]
    data = [json.loads(line) for line in lines]
    
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Writing header
        N = len(data[0]['input1'])
        header = [f'col{i+1}' for i in range(N)] + ['output']
        writer.writerow(header)
        
        # Writing rows
        for entry in data:
            writer.writerow(entry['input1'] + [entry['output1']])




problems=load_data("datasets/data/my_data/vectors.json")

print(problems)

"""
for problem in problems["PSB1"]:
    print(problem)
    txt_to_csv(f"datasets/data/my_data/test_cases/PSB1/{problem}/Test.txt", f"datasets/data/my_data/test_cases/PSB1/{problem}/cases.csv")


"""
for problem in problems["PSB2"]:
    json_to_csv(f"datasets/data/my_data/test_cases/PSB2/datasets/{problem}/{problem}-random.json", f"datasets/data/my_data/test_cases/PSB2/datasets/{problem}/cases.csv")

