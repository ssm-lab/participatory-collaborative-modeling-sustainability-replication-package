import numpy as np
import os
import pandas as pd
from collections import Counter
from matplotlib import pyplot as plt
from matplotlib.offsetbox import AnchoredText
from matplotlib.ticker import MaxNLocator

__author__ = "Istvan David"
__copyright__ = "Copyright 2024, Sustainable Systems and Methods Lab (SSM)"
__license__ = "GPL-3.0"

inputFolder = './data'
outputFolder = './output'
data = pd.read_excel(f'{inputFolder}/data.xlsx')

#collection for non-default category thresholds
thresholds = {
    'Publication type' : 0,
    'Application domain' : 0,
    'Publisher' : 1,
    'Publication year' : 0
}

orders = {
    'Publication type' : ['Journal', 'Book chapter', 'Conference', 'Workshop'],
}

bins = {
    'Publication year' : [(0, 2009, '-2009'), (2010, 2014, '2010-2014'), (2015, 2019, '2015-2019'), (2020, 2024, '2020-2024')]
}

#collection for non-default pretty printed categories
prettyPrintCategory = {
    'Publication type' : 'Pub.type',
    'Publication year' : 'Pub.year',
}

def chartData(data, settings):
    for categories, color, fileName in settings:
        
        """
        Preparation of plot data. Required for proportional layouts.
        """
        plotData = {}
        for i in range(len(categories)):
            category = categories[i]
            
            #Counter object containing a dictionary of labels and frequencies
            counter = Counter([str(val).strip() for sublist in data[category].dropna().astype(str).str.split(',').tolist() for val in sublist])
            
            """
            Threshold management. Elements with a frequency below the threshold are placed into the 'Others' bin.
            """
            #Split at threshold. Default 1 is used unless specified otherwise in the #thresholds dictionary.
            threshold = thresholds[category] if category in thresholds.keys() else 1
            counterAboveTreshold = [x for x in counter.items() if x[1]>threshold]
            
            if threshold > 0: #anything not above the threshold goes into the 'Other' category
                counterUpToTreshold = [x for x in counter.items() if x[1]<=threshold]
            
            #Sort non-'Other' categories before adding the 'Other' bin.
            if category in orders.keys():
                counterAboveTreshold = [tuple for x in orders[category] for tuple in counterAboveTreshold if tuple[0] == x]
                counterAboveTreshold.reverse()
            else:
                counterAboveTreshold = sorted(counterAboveTreshold, key=lambda x: x[1])
                
            if category in bins.keys():
                binnedCounter = []
                for b in bins[category]:
                    binCount = 0
                    for c in counter:
                        if int(c)>=b[0] and int(c)<=b[1]:
                            binCount += counter[c]
                    binnedCounter.append((b[2], binCount))
                
                binnedCounter.reverse()
                
                counterAboveTreshold = binnedCounter
            
            #If there's been a meaningful threshold set AND there are elements in the 'Other' bin, append the bin.
            if threshold > 0 and len(counterUpToTreshold) > 0:
                counterAboveTreshold = [('Other', len(counterUpToTreshold))] + counterAboveTreshold

            plotData[category] = counterAboveTreshold

        numCharts = len(plotData.keys())
        rows = [len(p) for p in plotData.values()] #The height ratios of the rows are set proportionally to the rows their display.
        
        #Create subplots
        fig, axs = plt.subplots(nrows=numCharts, sharex=False, gridspec_kw={'height_ratios': rows})
        
        #If only 1 subplot, still manage it as an array for compatibility reasons.
        if len(categories) == 1:
            axs = [axs]

        """
        Plotting
        """
        for i, category in enumerate(plotData):
            counter = plotData[category]
            
            values = [element[1] for element in counter]
            sumFrequencies = sum(values)
            labels = ['{} \u2014 {} ({}%)'.format(element[0], element[1], round((element[1]/sumFrequencies)*100)) for element in counter]
            #Get the regular labels and values by: labels, values = zip(*counter)
            
            #Prepare bar chart
            indexes = np.arange(len(labels))
            width = 0.75
            axs[i].set_xlim([0, sum(values)])   #scales bars to 100% within one subplot
            
            #Create vertical bar chart
            plt.sca(axs[i])
            plt.barh(indexes, values, width, color=color)
            plt.yticks(indexes, labels, rotation=0)

            """
            Title of the chart shown as a rotated Y axis label on the right side, inside of the plot area
            """
            title = prettyPrintCategory[category] if category in prettyPrintCategory.keys() else category.capitalize()
            #left label placement:
            axs[i].yaxis.set_label_position("left")
            plt.ylabel(title, rotation=90, fontsize=12, labelpad=7)
            
            #Remove plot area borders
            axs[i].spines['right'].set_visible(False)
            axs[i].spines['top'].set_visible(False)
            axs[i].spines['bottom'].set_visible(False)
            #Remove X ticks and labels
            plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
            
            """
            Category label settings
            """
            #Y tick labels inside
            axs[i].tick_params(axis="y", direction="out", pad=-10)
            #no Y ticks
            axs[i].yaxis.set_ticks_position('none') 
            #align Y tick labels to the left
            ticks = axs[i].get_yticklabels()
            axs[i].set_yticklabels(ticks, ha = 'left')

            """
            Tick label font management
            """
            ax = plt.gca()
            labels=ax.get_yticklabels()+ax.get_xticklabels()
            for label in labels:
                label.set_fontsize(13)
            
            """
            Sizing and plotting
            """
            figure = plt.gcf()
            #Height proportional to the number of rows displayed
            figure.set_size_inches(8, 0.33*sum(rows))
            plt.gcf().tight_layout()

        plt.savefig('{}/{}.pdf'.format(outputFolder, fileName))
        

chartData(data, [
    (['Publication year', 'Publication type', 'Publisher'], '#85d4ff', 'publications')]
)