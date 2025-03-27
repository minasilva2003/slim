# MIT License
#
# Copyright (c) 2024 DALabNOVA
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from main_gp import gp  # import the slim_gsgp library
from datasets.data_loader import load_ppb  # import the loader for the dataset PPB
from evaluators.fitness_functions import rmse  # import the rmse fitness metric
from utils.utils import train_test_split  # import the train-test split function
import json
import csv
import pandas as pd
import numpy as np
from datasets.data_loader import load_pandas_df

def load_data(file_name):
    with open(file_name, "r") as f:
        return json.load(f)
    
def write_list_to_csv(data_list, file_name):
    with open(file_name, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data_list)


def write_list_to_json(data, filename):
    """
    Writes a list to a JSON file.

    Parameters:
    - data (list): The list to be written to the file.
    - filename (str): The name of the JSON file.

    Returns:
    - None
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)  # indent=4 makes it more readable


rmse_problems = load_data("datasets/data/my_data/rmse.json")

correct_threshold = 0.1

results = [["problem", "best_fit", "num_correct"]]

for benchmark in rmse_problems:

    for problem in rmse_problems[benchmark]:

        if benchmark=="PSB1":
            df = pd.read_csv(f"datasets/data/my_data/test_cases/{benchmark}/{problem}/cases.csv")
        else:
            df = pd.read_csv(f"datasets/data/my_data/test_cases/{benchmark}/datasets/{problem}/cases.csv")

        print(f"{problem}: {df.shape} test cases")

        # Turning df into X and y torch.Tensors
        X, y = load_pandas_df(df, X_y=True)

        # Split into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, p_test=0.4)

        # Split the test set into validation and test sets
        X_val, X_test, y_val, y_test = train_test_split(X_test, y_test, p_test=0.5)

        # Apply the SLIM GP algorithm
        final_tree, final_population = gp(X_train=X_train, y_train=y_train,
                        X_test=X_val, y_test=y_val,
                        dataset_name=f"{benchmark}", pop_size=100, n_iter=2000, max_depth=None)

        # Show the best individual structure at the last generation
        final_tree.print_tree_representation()

        # Get the prediction of the best individual on the test set
        predictions = final_tree.predict(X_test)

        # Compute and print the RMSE on the test set
        best_fit = float(rmse(y_true=y_test, y_pred=predictions))

        final_pop = []

        for individual in final_population.population:

            predictions = individual.predict(X[:1000])

            fit = float(rmse(y_true=y[:1000], y_pred=predictions))
            
            #print(fit)

            #solution is considered correct if fit below certain threshold
            if(fit<correct_threshold):
                num_correct+=1

            if(fit<best_fit):
                best_fit=fit
            
            final_pop.append([individual.get_tree_representation(), fit])
        
        
        results.append([problem, best_fit, num_correct])
        write_list_to_csv(results, f"results/GP/results.csv")
        #write_list_to_json(final_pop, f"results/GP/{problem}_pop.json")
