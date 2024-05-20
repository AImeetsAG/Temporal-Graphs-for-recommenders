The numbers presented in the paper are not correct\
1. inference-baseline.ipynb\
        Took latest, mean, median prediction. Not the most efficient I think. Worked with dataframe. Need to create a dictionary of {timestamp:{usr:{genre:weight}}} (Check baseline.ipynb). Pandas is faster because of groupby and merge operations. Actually seems like pandas is faster than dictionary lookup.
2. rollingaverage.ipynb\
        Took moving average with window =7,14,21
        Don't have hardware to do a proper gridlike hyperparameter tuning. For now window =14 performs best.

| Model   | NDCG @10 (Validation) | NDCG @10 (Test)
| -------- | ------- | ------- |
| Latest node lable  | 0.13992    | 0.1314
| Mean node label | 0.1757    | 0.1674
| Median node label    | 0.1635    | 0.1565
| Rolling average (Window=7)    | 0.1635    | 0.1565
| Rolling average (Window=14)    | 0.1798   | 0.1684
| Rolling average (Window=21)    | 0.1798   | 0.1681
