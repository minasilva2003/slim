import pandas as pd

def average_best_fitness(max_runs):
    files = [f"results/stats_{i}.csv" for i in range(1, max_runs+1)]  # List of file names
    dfs = []
    
    # Get first columns (common to all files)
    param_columns = pd.read_csv(files[0]).iloc[:, :-2]

    for file in files:
        try:
            df = pd.read_csv(file)  # Read CSV file
            dfs.append(df.iloc[:, -2:])  # Select only the last two columns
        except FileNotFoundError:
            print(f"Warning: {file} not found")
    
    if dfs:
        # Combine all dataframes for calculations
        combined_df = pd.concat(dfs, axis=0)
        
        # Compute average and standard deviation for the last two columns
        avg_df = combined_df.groupby(combined_df.index).mean()
        std_df = combined_df.groupby(combined_df.index).std()
        
        # Rename columns for clarity
        avg_df.columns = [f"avg_{col}" for col in avg_df.columns]
        std_df.columns = [f"std_{col}" for col in std_df.columns]
        
        # Concatenate averages, standard deviations, and parameter columns
        result_df = pd.concat([param_columns, avg_df, std_df], axis=1)
        
        # Save to new CSV file
        result_df.to_csv("results/average_run.csv", index=False)
        print("Averaged results with standard deviations saved to 'average_run.csv'")
    else:
        print("No valid data to average.")

