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

"""
from slim_gsgp.main_slim import slim  # import the slim_gsgp library
from slim_gsgp.datasets.data_loader import load_ppb  # import the loader for the dataset PPB
from slim_gsgp.evaluators.fitness_functions import rmse  # import the rmse fitness metric
from slim_gsgp.utils.utils import train_test_split  # import the train-test split function
"""

from main_slim import slim
from datasets.data_loader import load_pandas_df
from evaluators.fitness_functions import rmse
from utils.utils import train_test_split
import json
import pandas as pd
import csv
import random

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

for epoch in range(1,31):

    results = [["problem", "slim_version", "n_iter", "p_inflate", "best_fit", "num_correct"]]

    seed_n = random.randint(0,0x7fffffff)

    for benchmark in rmse_problems:

        for problem in rmse_problems[benchmark]:

            if problem != "smallest":
                continue

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

            slim_version_list=["SLIM+SIG1", "SLIM+SIG2", "SLIM*SIG1", "SLIM*SIG2"]
            #slim_version_list=["SLIM*SIG1", "SLIM+SIG1"]
            n_iter_list=[2000]
            p_inflate_list=[0.1, 0.5, 0.7]
            #p_inflate_list=[0.5]

            # Apply the SLIM GSGP algorithm
            for cur_slim_version in slim_version_list:
                for cur_n_iter in n_iter_list:
                    for cur_p_inflate in p_inflate_list:

                        num_correct=0
                        best_fit=10**5

                        final_tree, final_population = slim(X_train=X_train, y_train=y_train,
                                        X_test=X_val, y_test=y_val,
                                        dataset_name=f"{benchmark}/{problem}", slim_version=cur_slim_version, pop_size=100, n_iter=cur_n_iter,
                                        ms_lower=0, ms_upper=1, p_inflate=cur_p_inflate, verbose=0, reconstruct=True, seed=seed_n)

                        # Show the best individual structure at the last generation
                        final_tree.print_tree_representation()

                        #Compute and print the RMSE for the first 1000 test cases
                        
                        final_pop = []
                        for individual in final_population.population:

                            individual.version=cur_slim_version
                        
                            predictions = individual.predict(X[:1000])

                            fit = float(rmse(y_true=y[:1000], y_pred=predictions))
                            
                            #print(fit)

                            #solution is considered correct if fit below certain threshold
                            if(fit<correct_threshold):
                                num_correct+=1

                            if(fit<best_fit):
                                best_fit=fit
                            
                            final_pop.append([individual.get_tree_representation(), fit])
                        
                        
                        results.append([problem, cur_slim_version, cur_n_iter, cur_p_inflate, best_fit, num_correct])
                        write_list_to_csv(results, f"results/run_{epoch}.csv")
                        #write_list_to_json(final_pop, f"results/pop_.json")




        

        


