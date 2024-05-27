import pandas as pd
import copy
from typing import Union
from scripts.prjct_utls import print_header
import time
import numpy as np



'''
QUESTION CONCERNING DUPLICATE AND NEAR-DUPLICATE RECORDS
'''

def display_interaction_info(df: pd.DataFrame, 
                             genre_dict: dict,
                             unique_ts: Union[pd.Series, None] = None, 
                             m : Union[int, None] = None, 
                             n: Union[int, None] = None,
                             ) -> None:
    '''
    Display info corresponding to the mth distinct timestamp and the nth user for which there is an interaction at that timestamp.
    Typically, max n = 0.
    '''
    if unique_ts is None:
        unique_ts = df['timestamps'].unique() # Presumed already sorted

    if m is None:
        m = 1
    if n is None:
        n = 0
        
    m = min(len(unique_ts) - 1, m)
    ts = unique_ts[m]
    df_tmp = df[df['timestamps'] == ts].copy(deep=True)
    users = sorted(df_tmp['sources'].unique())
    n = min(len(users) - 1, n)
    df_tmp = df_tmp[df_tmp['sources'] == users[n]]
    
    df_tmp['destinations'] = df_tmp['destinations'].map(genre_dict)
    df_tmp['timestamps'] = pd.to_datetime(df_tmp['timestamps'], unit='s').dt.strftime('%A, %Y-%m-%d %H:%M:%S')
    
    print_header(f'User-genre interaction: {df_tmp['timestamps'].values[0]}')
    display(df_tmp)
    
    print('The song is', end = ' ')
    to_print = list(zip(df_tmp['destinations'], df_tmp['edge_feat']))
    for i, (g, ef) in enumerate(to_print):
        if i < len(to_print) - 2: 
            end = ', '
        elif len(to_print) - 2 <= i < len(to_print) - 1:
            end = ', and '
        else: 
            end = '.'
        print(f'{100*ef:.2f}% {g}', end = end)
    
    ef_sum = df_tmp['edge_feat'].sum()
    print('\nNotice that', end = ' ')
    if ef_sum == 1:    
        for i, (g, ef) in enumerate(to_print):
            if i < len(to_print) - 1: 
                end = ' + '
            else: 
                end = f' = '
            print(f'{ef:.4f}', end = end)
    elif ef_sum < 1:
        for i, (g, ef) in enumerate(to_print):
            if i < len(to_print) - 1: 
                end = ' + '
            else: 
                end = f' < '
            print(f'{ef:.4f}', end = end)
    else:
        for i, (g, ef) in enumerate(to_print):
            if i < len(to_print) - 1: 
                end = ' + '
            else: 
                end = f' > '
            print(f'{ef:.4f}', end = end)
            
    print(1, end = '.')  

'''
UNDERSTANDING NODE LABELS DATA
'''

def discretize(df: pd.DataFrame) -> pd.DataFrame:    
    tic = time.time()
    first_tic = tic
    print('Making a copy df_discrete of edge list dataframe df_[\'edge\'].')
    df_discrete = df.copy(deep=True)
    toc = time.time()
    print(f'Time taken: {toc - tic:.2f} seconds.')
    
    display(df_discrete.head())
    
    print('\nWe will make changes to df_discrete but the changes will not affect original df_[\'edge\'].')
    
    tic = time.time()
    print('\nCreating a \'date\' column in df_discrete that gives, for each record, the date in which each timestamp lies.')
    df_discrete['date'] = pd.to_datetime(df_discrete['timestamps'], unit='s', utc=True).dt.date
    toc = time.time()
    print(f'Time taken: {toc - tic:.2f} seconds.')
    
    display(df_discrete.head())
    
    tic = time.time()
    print('\nCreating dictionary that maps each date to an integer n, where n is the nth day following the date of the earliest record.')
    date_mapping = {date: idx for idx, date in enumerate(sorted(df_discrete['date'].unique()))}
    toc = time.time()
    print(f'Time taken: {toc - tic:.2f} seconds.')
    
    tic = time.time()
    print('\nApplying the map to df_discrete[\'date\'] column and placing the result in a new \'day_idx\' column, then dropping the \'date\' column.')
    df_discrete['day_idx'] = df_discrete['date'].map(date_mapping)
    df_discrete.drop(columns=['date'], inplace=True)
    toc = time.time()
    print(f'Time taken: {toc - tic:.2f} seconds.')
    
    display(df_discrete.head())
    
    tic = time.time()
    print('\nGrouping df_discrete records by \'sources\', \'destinations\', and \'day_idx\', then summing the \'edge_feat\' column for each group.')
    grouped_df = df_discrete.groupby(['sources', 
                                  'destinations', 
                                  'day_idx'], as_index=False)['edge_feat'].sum().rename(columns={'edge_feat': 'day_feat_sum'})
    toc = time.time()
    print(f'Time taken: {toc - tic:.2f} seconds.')
    
    tic = time.time()
    print('\nPlacing results in a new column called \'day_feat_sum\'.')
    df_discrete = pd.merge(df_discrete, grouped_df, on=['sources', 'destinations', 'day_idx'], how='left')
    toc = time.time()
    print(f'Time taken: {toc - tic:.2f} seconds.')
    
    print('\nGrouped dataframe'.upper())
    display(grouped_df.head())
    
    display(df_discrete.head())
    
    tic = time.time()
    print('\nCreating \'edge_feat_mult\' column: the element-wise product of the \'edge_feat\' and \'multiplicity\' columns.')
    df_discrete['edge_feat_mult'] = df_discrete['edge_feat'] * df_discrete['multiplicity']
    toc = time.time()
    print(f'Time taken: {toc - tic:.2f} seconds.')
    
    display(df_discrete.head())
    
    tic = time.time()
    print('\nGrouping df_discrete records by \'sources\', \'destinations\', and \'day_idx\', then summing the \'edge_feat_mult\' column for each group.')
    grouped_df = df_discrete.groupby(['sources', 
                                      'destinations', 
                                      'day_idx'], as_index=False)['edge_feat_mult'].sum().rename(columns={'edge_feat_mult': 'day_feat_sum_mult'})
    toc = time.time()
    print(f'Time taken: {toc - tic:.2f} seconds.')
    
    tic = time.time()
    print('\nPlacing results in a new column called \'day_feat_sum\'.')
    df_discrete = pd.merge(df_discrete, grouped_df, on=['sources', 'destinations', 'day_idx'], how='left')
    toc = time.time()
    print(f'Time taken: {toc - tic:.2f} seconds.')
    
    print('\nGrouped dataframe'.upper())
    display(grouped_df.head())
    
    display(df_discrete.head())
    
    tic = time.time()
    print('\nDropping \'edge_feat\',  \'multiplicity\', and \'edge_feat_mult\' columns.')
    df_discrete.drop(columns=['edge_feat', 'multiplicity', 'edge_feat_mult'], inplace=True)
    toc = time.time()
    print(f'Time taken: {toc - tic:.2f} seconds.')
    
    display(df_discrete.head())
    
    tic = time.time()
    print('\nReordering columns.')
    column_order = ['sources', 
                    'destinations', 
                    'timestamps', 
                    'day_idx',
                    'day_feat_sum',                
                    'day_feat_sum_mult',
                    ]
    df_discrete = df_discrete[column_order]
    toc = time.time()
    print(f'Time taken: {toc - tic:.2f} seconds.')
    
    display(df_discrete.head())
    
    print(f'\nTotal time taken: {toc - first_tic:.2f} seconds.')

    return df_discrete

'''UNNORMALIZED NODE LABELS'''

def unnormalized_node_labels(df: pd.DataFrame) -> pd.DataFrame:
    print('Creating unnormalized node labels.')
    
    tic = time.time()
    
    data_list = []
    df_node_columns=['sources', 'destinations', 'week_feat_sum', 'week_feat_sum_mult', 'week']
    df_node = pd.DataFrame(data_list, columns=df_node_columns)
    
    i = 0
    week_idx = 0
    window_start_day = df.loc[i]['day_idx'].astype(int)
    next_day_idx = df.loc[i + 1]['day_idx'].astype(int)
    window_duration = 7
    week_cumulative_sums = {}
    
    while window_start_day + window_duration - 1 <= df['day_idx'].max():
        previous_week_cumulative_sums = copy.deepcopy(week_cumulative_sums)
        next_day_idx = df.loc[i + 1]['day_idx'].astype(int)
        while next_day_idx < window_start_day + window_duration:
            user = df.loc[i]['sources'].astype(int)
            genre = df.loc[i]['destinations'].astype(int)
            w = df.loc[i]['day_feat_sum'].astype(float)
            wm = df.loc[i]['day_feat_sum_mult'].astype(float)
            
            week_cumulative_sums[(user, genre)] = week_cumulative_sums.get((user, genre),np.array([0,0])) + np.array([w,wm])
            
            try:
                next_day_idx = df.loc[i + 1]['day_idx'].astype(int)
                i += 1
                guaranteed_full_week: bool = True
            except KeyError:
                guaranteed_full_week: bool = False
                break
    
        if guaranteed_full_week:
            week_sums = {}
            for (user, genre) in week_cumulative_sums.keys():
                increment = week_cumulative_sums[(user, genre)] - previous_week_cumulative_sums.get((user, genre),np.array([0,0]))
                if increment[0] != 0 or increment[1] != 0:
                    week_sums[(user, genre)] = increment
            
            data_list = [(user, genre, w, wm) for (user, genre), [w,wm] in week_sums.items()]
            
            df_week = pd.DataFrame(data_list, columns=df_node_columns[:-1])
            df_week['week'] = week_idx
            week_idx += 1
            
            if df_node.empty:
                df_node = df_week
            else:
                df_node= pd.concat([df_node, df_week], ignore_index=True)
                
        window_start_day += 1
    
    column_order = ['sources',
                    'destinations',
                    'week',
                    'week_feat_sum',
                    'week_feat_sum_mult',
                   ]
    df_node = df_node[column_order]
    
    toc = time.time()
    print(f'Time taken: {toc - tic:.2f} seconds.')
    return df_node