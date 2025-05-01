# SLIM-GSGP Experiments

## Requirements

Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running Experiments

1. Navigate to the `slim_gsgp` directory:
   ```bash
   cd slim_gsgp
   ```

2. Run the main script:
   ```bash
   python example_slim.py
   ```

   - All experiment parameters (e.g., number of runs, generations, population size) are defined in `example_slim.py`.

## Results

- During execution, results are continuously written to:
  ```
  slim_gsgp/results/stats_{run_number}.csv
  ```

- Once all experiments are completed, the script automatically calculates averages and standard deviations, storing them in the same `results` folder.

## Directory Structure

```
slim_gsgp/
├── example_slim.py
├── results/
│   ├── stats_1.csv
│   ├── stats_2.csv
│   └── ... (per-run results and final stats)
├── ...
```

