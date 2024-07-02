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

prettyPrintDatapoint = {
    'Collab' : 'Cooperation',
    'Sus' : 'Sustainability',
}

dimensions = ['Environmental', 'Social', 'Economic']

counter_1 = Counter()
for dimension in dimensions:
    counts = len(data.loc[
        (data['Sustainability dimension'].str.count(',')+1 == 1) &
        (data['Sustainability dimension'].str.contains(dimension))])
    
    counter_1[dimension] = counts

counter_2 = Counter()
pairs = list(combinations(dimensions, 2))

for pair in pairs:
    counts = len(data.loc[
        (data['Sustainability dimension'].str.count(',')+1 == 2) &
        (data['Sustainability dimension'].str.contains(pair[0])) &
        (data['Sustainability dimension'].str.contains(pair[1]))])
    
    counter_2[pair] = counts

counter_3 = Counter()
counts = len(data.loc[data['Sustainability dimension'].str.count(',')+1 == 3])
counter_3[list(combinations(dimensions, 3))[0]] = counts

def get_pair_count_2(dim1, dim2):
    assert counter_2[(dim1, dim2)] == 0 or counter_2[(dim2, dim1)] == 0
    return counter_2[(dim1, dim2)] + counter_2[(dim2, dim1)]

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
        counter_1['Environmental'],
        counter_1['Social'],
        counter_1['Economic'],
        get_pair_count_2('Environmental', 'Social'),
        get_pair_count_2('Environmental', 'Economic'),
        get_pair_count_2('Social', 'Economic'),
        counter_3[list(combinations(dimensions, 3))[0]]
    ]
)

matplotlib.rcParams["font.size"] = 9
facecolor="#85d4ff"
fig = plt.figure(figsize=(8, 5))
result = plot(numbers, show_counts="{:,}", show_percentages=True, facecolor=facecolor, fig=fig, element_size=None)
result["intersections"].set_ylabel("Joint number")

plt.gcf().tight_layout()
plt.savefig(f'{outputFolder}/upset.pdf')