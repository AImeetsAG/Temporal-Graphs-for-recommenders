The numbers presented in the paper are not correct\
1. Baseline: (inference-baseline.ipynb)
             Not the most efficient. Worked with dataframe. Need to create a dictionary of {timestamp:{usr:{genre:weight}}} (Check baseline.ipynb). Pandas is faster because of groupby and merge operations.

| Model   | NDCG @10 (Validation) | NDCG @10 (Test)
| -------- | ------- | ------- |
| Latest node lable  | 0.13992    | 0.1314
| Mean node label | 0.1757    | 0.1674
| Median node label    | 0.1635    | 0.1565
