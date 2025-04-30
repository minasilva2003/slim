import pandas as pd

def analyze_best_rows(input_csv, output_csv):
    # Read the input CSV file
    df = pd.read_csv(input_csv)

    # Initialize a list to store the best rows for each problem
    best_rows = []

    # Group by the 'problem' column
    grouped = df.groupby('problem')

    for problem, group in grouped:
        if (group['avg_num_correct'] == 0).all():
            # If all 'avg_num_correct' values are 0, find the row with the lowest 'avg_best_fit'
            best_row = group.loc[group['avg_best_fit'].idxmin()]
        else:
            # Otherwise, find the row with the highest 'avg_num_correct'
            best_row = group.loc[group['avg_num_correct'].idxmax()]

        # Append the relevant information to the best_rows list
        best_rows.append({
            'problem': problem,
            'slim_version': best_row['slim_version'],
            'n_iter': best_row['n_iter'],
            'p_inflate': round(best_row['p_inflate'], 2),
            'best_fitness': round(best_row['avg_best_fit'], 2),
            'std_best_fitness': round(best_row['std_best_fit'], 2),
            'best_num_correct': round(best_row['avg_num_correct']),  # Rounded to unit
            'std_num_correct': round(best_row['std_num_correct'], 2)
        })

    # Create a new DataFrame from the best rows
    result_df = pd.DataFrame(best_rows)

    # Save the result to a new CSV file
    result_df.to_csv(output_csv, index=False)
    print(f"Analysis complete. Results saved to '{output_csv}'.")

