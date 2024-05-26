The numbers presented in the paper are not correct\
1. inference-baseline.ipynb\
        Took latest, mean, median prediction. Not the most efficient I think. Worked with dataframe. Need to create a dictionary of {timestamp:{usr:{genre:weight}}} (Check baseline.ipynb). Pandas is faster because of groupby and merge operations. Actually seems like pandas is faster than dictionary lookup.
2. rollingaverage.ipynb\
        Took moving average with window =7,14,21
        Don't have hardware to do a proper gridlike hyperparameter tuning. For now window =14 performs best.

| Model   | NDCG @10 (Validation) +- 0.0001 | NDCG @10 (Test) +-0.0001
| -------- | ------- | ------- |
| Latest node label (Baseline)  | 0.1435   | 0.1300
| Mean node label | 0.1793    | 0.1669
| Median node label    | 0.1676    | 0.1559
| Rolling average (Window=7)    | 0.1789    | 0.1616
| Rolling average (Window=14)    | 0.1972   | 0.1770
| Rolling average (Window=21)    | 0.1972   | 0.1769
