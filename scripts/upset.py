from upsetplot import from_memberships
from upsetplot import plot
from matplotlib import pyplot
import matplotlib
from itertools import combinations

import numpy as np
import os
import pandas as pd
from collections import Counter
from matplotlib import pyplot as plt
from matplotlib.offsetbox import AnchoredText
from matplotlib.ticker import MaxNLocator

'''
Quick and dirty implementation code for the UpSet chart
'''
__author__ = "Istvan David"
__copyright__ = "Copyright 2024, Sustainable Systems and Methods Lab (SSM)"
__license__ = "GPL-3.0"

inputFolder = './data'
outputFolder = './output'
data = pd.read_excel(f'{inputFolder}/data.xlsx')
column = 'Sustainability dimension'


columnFilename = {
    'Sustainability dimension' : 'sustainability_dim',
    'Sustainability goal / SDG' : 'sdg',
}

list_all = data[column].dropna().astype(str).str.split(',').dropna()
l = [y.strip() for x in list_all for y in x]
dimensions = list(set(l))

counter = Counter()

for length in range(0, len(dimensions)):
    combos = list(combinations(dimensions, length+1))
    
    data_slice_1 = data.loc[data[column].str.count(',')+1 == length+1]
    
    #print(f'COMBOS:{combos}')
    for combo in combos:
        data_slice = data_slice_1
        #print(f'COMBO: {combo}')
        if len(combo) == 1:
            #print('combo of 1')
            #print(combo[0])
            data_slice = data_slice.loc[data_slice[column].str.contains(combo[0])]
            counter[combo[0]] = len(data_slice)
        else:
            #print('combo of N')
            for dim in combo:
                #print(f'..........slicing for dim {dim}')
                data_slice = data_slice.loc[data_slice[column].str.contains(dim)]
            counter[combo] = len(data_slice)

def get_pair_count_2(dim1, dim2):
    assert counter[(dim1, dim2)] == 0 or counter[(dim2, dim1)] == 0
    return counter[(dim1, dim2)] + counter[(dim2, dim1)]


numbers = from_memberships(
    [
        ['Environmental'],
        ['Social'],
        ['Economic'],
        ['Environmental', 'Social'],
        ['Environmental', 'Economic'],
        ['Social', 'Economic'],
        ['Economic', 'Social', 'Environmental'],
    ],
    data=[
        counter['Environmental'],
        counter['Social'],
        counter['Economic'],
        get_pair_count_2('Environmental', 'Social'),
        get_pair_count_2('Environmental', 'Economic'),
        get_pair_count_2('Social', 'Economic'),
        counter[list(combinations(dimensions, 3))[0]]
    ]
)

matplotlib.rcParams["font.size"] = 10
#facecolor="#85d4ff"
#facecolor="#bdbdbd"
facecolor="#ffc569"
fig = plt.figure(figsize=(8, 5))
result = plot(numbers, show_counts="{:,}", show_percentages=True, facecolor=facecolor, fig=fig, element_size=None, sort_categories_by='-cardinality', sort_by='input')
result["intersections"].set_ylabel("Joint number")

plt.gcf().tight_layout()
plt.savefig(f'{outputFolder}/upset-{columnFilename[column]}.pdf', bbox_inches='tight')