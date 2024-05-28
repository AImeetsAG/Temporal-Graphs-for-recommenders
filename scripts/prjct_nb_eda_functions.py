import pandas as pd
import copy
from typing import Union
from scripts.prjct_utls import print_header
import time
import numpy as np
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
from datetime import datetime, timezone

'''
This file contains functions for the EDA notebook.
These functions are very specific to that notebook and do not generalize at all.
They are essentially code cells of the EDA notebook.
We've just placed them here to make the presentation of the notebook cleaner, without long code cells.
'''

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

def unnormalized_node_labels(df: pd.DataFrame, test: bool = False) -> pd.DataFrame:
    parent_directory = Path(__file__).resolve().parent.parent
    csv_path = parent_directory / 'data'/ 'tgbn-genre_node_labels_unnormalized.csv'
    if not test and csv_path.is_file():
        print('File already exists. Loading now.')
        print('Originally, the DataFrame took 3973.41 seconds to generate.')
        return pd.read_csv(csv_path)
        
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
    print(f'DataFrame complete. Time taken: {toc - tic:.2f} seconds.')
    if not test:
        print('Saving DataFrame to \'data/tgbn-genre_node_labels_unnormalized.csv\'.')
        tic = time.time()
        df_node.to_csv(csv_path, index=False)
        toc = time.time()
        print(f'Time taken: {toc - tic:.2f} seconds.')
    return df_node

'''
NORMALIZED NODE LABELS
'''

def normalize_node_labels(df_node: pd.DataFrame) -> pd.DataFrame:
    tic = time.time()
    print('Grouping by \'sources\', \'week\' and summing \'week_feat_sum\'.')
    grouped_sum = df_node.groupby(['sources', 'week'])['week_feat_sum'].sum().reset_index()
    
    print('Rename the summed column to \'week_total\'.')
    grouped_sum.rename(columns={'week_feat_sum': 'week_total'}, inplace=True)
    print('Grouped dataframe'.upper())
    display(grouped_sum.head())
    
    print('Merging the \'week_total\' column back to the original DataFrame.')
    df_node = df_node.merge(grouped_sum, on=['sources', 'week'], how='left')
    display(df_node.head())
    
    toc = time.time()
    print(f'Time taken: {toc - tic:.2f} seconds')

    try:
        print('Repeating for version with duplicate records taken into account.')
        tic = time.time()
        print('Grouping by \'sources\', \'week\' and summing \'week_feat_sum_mult\'.')
        grouped_sum = df_node.groupby(['sources', 'week'])['week_feat_sum_mult'].sum().reset_index()
        
        print('Rename the summed column to \'week_total_mult\'.')
        grouped_sum.rename(columns={'week_feat_sum_mult': 'week_total_mult'}, inplace=True)
        print('Grouped dataframe'.upper())
        display(grouped_sum.head())
        
        print('Merging the \'week_total_mult\' column back to the original DataFrame.')
        df_node = df_node.merge(grouped_sum, on=['sources', 'week'], how='left')
        display(df_node.head())
        
        toc = time.time()
        print(f'Time taken: {toc - tic:.2f} seconds')
    except:
        pass

    print('Adding \'weight\' column (\'week_feat_sum\' divided by \'week_total\').')
    tic = time.time()
    df_node['weight'] = df_node['week_feat_sum']/df_node['week_total']
    toc = time.time()
    print(f'Time taken: {toc - tic:.2f} seconds')

    try:
        print('Adding \'weight_mult\' column (\'week_feat_sum_mult\' divided by \'week_total_mult\').')
        tic = time.time()
        df_node['weight_mult'] = df_node['week_feat_sum_mult']/df_node['week_total_mult']
        toc = time.time()
        print(f'Time taken: {toc - tic:.2f} seconds')
    except:
        pass
    
    print('Reordering columns.')
    try:
        column_order = ['sources', 
                        'destinations', 
                        'week', 
                        'week_feat_sum',
                        'week_total',
                        'weight',
                        'week_feat_sum_mult',                  
                        'week_total_mult',                 
                        'weight_mult'
                       ]
        df_node = df_node[column_order]
    except:
        column_order = ['sources', 
                        'destinations', 
                        'week', 
                        'week_feat_sum',
                        'week_total',
                        'weight',
                       ]
        df_node = df_node[column_order] 
    
    display(df_node.head())
    return df_node

'''
VISUALIZATION
'''

def plot_graph(df: pd.DataFrame, 
               fname: Union[None, str] = None,) -> Union[FuncAnimation, str]:
    # Make a deep copy of df so there's no chance anything we do here will affect the input DataFrame.
    # The input DataFrame should be a copy of a small piece of the original edge list DataFrame anyway.
    df_copy = df.copy(deep=True)
    # Let's get rid of 'near-duplicate' records, of there are any: we don't want edges displaying on top of edges (especially with the labels).
    # This is just for a visual so there's no need to worry too much about details like that.
    df_copy = df_copy.drop_duplicates(subset=['sources', 'destinations', 'timestamps'], keep='first')
    # Extract the distinct users U, genres V, and timestamps T among these records
    U = sorted(df_copy['sources'].unique())
    V = sorted(df_copy['destinations'].unique())
    T = sorted(df_copy['timestamps'].unique())

    # Initialize a bipartite graph with U one part and V the other
    B = nx.MultiGraph()
    B.add_nodes_from(U, bipartite=0)
    B.add_nodes_from(V, bipartite=1)

    # Create a figure and axis for the animation
    fig, ax = plt.subplots(figsize=(10, 8))

    # Initialize an empty list to store frames
    frames = []

    # Define the update function for the animation
    def update(ts_idx):
        ax.clear()  # Clear the axis for the new plot
        B.clear_edges() # Also clear the edges
        # Create a smaller DataFrame with just the records corresponding to the timestamp T[ts_idx]
        df_this_frame = df_copy[df_copy['timestamps'] == T[ts_idx]]
        # Run over the records and add an edge for each user-genre pair, with weight given by edge feature column
        for idx in df_this_frame.index:
            s = df_this_frame.loc[idx, 'sources']
            d = df_this_frame.loc[idx, 'destinations']
            w = df_this_frame.loc[idx, 'edge_feat']
            round_w = round(w, 4)
            B.add_edge(s, d, weight=round_w)
        
        pos = nx.bipartite_layout(B, U)

        # Draw the graph with formatting etc.
        options = {"edgecolors": "black", "node_color":"white", "edge_color":"black", "node_size": 800, "alpha": 0.9, "font_size":10}
        nx.draw(B, pos, with_labels=True, **options, ax=ax)
        
        edge_labels = {(u, v): d['weight'] for u, v, d in B.edges(data=True)}
            
        nx.draw_networkx_edge_labels(B, pos, edge_labels=edge_labels, ax=ax)
        # nx.draw_networkx_edge_labels(B, pos, edge_labels={}, ax=ax)
    
        # Convert the timestamp to a human-readable date
        date_time = datetime.fromtimestamp(T[ts_idx], timezone.utc)
        formatted_date_time = date_time.strftime('%A %B %d, %Y, %I:%M:%S %p')
        # Display the date as title
        ax.set_title(f'{formatted_date_time}')
       
    # Create the animation
    animation = FuncAnimation(fig, update, frames=len(T), interval=1000, blit=False)

    if bool(fname):
        # Save the animation to a GIF file
        parent_directory = Path(__file__).resolve().parent.parent
        fname = fname.split('.')[0] + '.gif'
        gif_path = parent_directory / 'presentation'/ fname
        animation.save(gif_path, writer='pillow')

    # Display the animation in the notebook    
    return HTML(animation.to_jshtml())