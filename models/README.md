Below is the results from our models

1. inference_baseline.ipynb\
        Took latest, mean, median prediction. Not the most efficient I think. Worked with dataframe. Need to create a dictionary of {timestamp:{usr:{genre:weight}}} (Check baseline.ipynb). Pandas is faster because of groupby and merge operations. 
2. rollingaverage.ipynb\
        Took moving average with window =7,14,21
        Don't have hardware to do a proper gridlike hyperparameter tuning. For now window =14 performs best.
3. Exponential_Smoothing.ipynb\
        Took exponential smoothing average with smoothing parameter $\alpha=0.8$ and $0.4$.

| Model   | NDCG @10 (Validation) +- 0.0001 | NDCG @10 (Test) +-0.0001
| -------- | ------- | ------- |
| Latest node label (Baseline)  | 0.18068   | 0.1575
| Mean node label | 0.2310    | 0.2034
| Median node label    | 0.2140    | 0.1888
| Rolling average (Window=7)    | 0.2242    | 0.1951
| Rolling average (Window=14)    | 0.2333   | 0.2008
| Rolling average (Window=21)    | 0.2345   | 0.2014
| Exponential Smoothing ($\alpha=0.8$)    | 0.1941   | 0.1662
| Exponential Smoothing ($\alpha=0.4$)    | 0.1827   | 0.1619
