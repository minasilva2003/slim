import pandas as pd

def average_best_fitness():
    files = [f"results/30_runs/run_{i}.csv" for i in range(15, 31)]  # List of file names
    dfs = []
    
    #get first columns (common to all files)
    param_columns = pd.read_csv(files[0]).iloc[:, :-2]

    for file in files:
        try:
            df = pd.read_csv(file)  # Read CSV file
            dfs.append(df.iloc[:, -2:])  # Select only the last two columns
        except FileNotFoundError:
            print(f"Warning: {file} not found")
    
    if dfs:
        avg_df = sum(dfs) / len(dfs)  # Compute average only for last two columns
        avg_df = pd.concat([param_columns, avg_df], axis=1)
        avg_df.to_csv("results/30_runs/average_run.csv", index=False)  # Save to new CSV file
        print("Averaged results saved to 'average_run.csv'")
    else:
        print("No valid data to average.")

# Example usage
average_best_fitness()
