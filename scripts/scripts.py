import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import pandas as pd
import ast
import re
import random
from string import Template
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

inputFolder = './data'
outputFolder = './output'

def loadData():
    df = pd.read_csv(f'{inputFolder}/data.csv')
    return df

def papersPerYear():
    df = loadData()
    
    years = df['Publication year'].value_counts().sort_index().to_frame().reset_index()
    years.columns = ['year', 'papers']

    #print(years)

    bins = [2007, 2009, 2014, 2019, 2024]
    labels = ['-2009', '2010-2014', '2015-2019', '2020-2024']

    years['yearbins'] = pd.cut(years['year'], bins, labels=labels)

    #print(years)

    #print(years.groupby('yearbins').sum()['papers'])

    fig = plt.figure(figsize = (10, 5))
    
    ax = years.groupby('yearbins').sum()['papers'].plot(kind='bar', rot=0, color='#43b82c')
    
    ax.set_ylabel('Papers', fontsize=15)
    ax.set_xlabel('Years', fontsize=15)
    ax.bar_label(ax.containers[0], fontsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.savefig(f'{outputFolder}/papers-per-year.pdf', format='pdf', bbox_inches='tight')
    plt.show()

def worldMap():
    df = loadData()
    
    countries = df['Author country'].to_frame()
    countries.columns = ['countries']
    
    countries['countrylist'] = countries.apply(lambda row: re.split(r',', row['countries']), axis=1)
    
    #print(countries)
    
    countries = countries.explode('countrylist')
    countries.columns = ['countries', 'country']
    
    countries['country'] = countries.apply(lambda row: row['country'].strip(), axis=1)
    
    #print(countries)
    
    papersPerCountry = countries.groupby('country').count().sort_values(by=countries.columns[0], ascending=False).reset_index()
    papersPerCountry.columns = ['country', 'papers']
    
    #print(papersPerCountry)
    
    #papersPerCountry[(papersPerCountry['country'] == 'USA')]['country'] = 'United States of America'
    
    papersPerCountry['country'] = papersPerCountry['country'].str.replace('USA','United States of America')
    papersPerCountry['country'] = papersPerCountry['country'].str.replace('UK','United Kingdom')
    
    #print(papersPerCountry)

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    ax2 = world.plot(figsize=(15,15), edgecolor=u'white', color='gray')
    
    #countries = ['Germany', 'Norway', 'Russia', 'China', 'Japan']
    
    #print('Australia' in papersPerCountry['country'].values)
    
    #print('-----')
    #print(int(papersPerCountry[papersPerCountry['country'] == 'Australia']['papers']))
    #print('-----')
    
    world['papers'] = world.apply(lambda row: int(papersPerCountry[(papersPerCountry['country'] == row['name'])]['papers']) if (row['name'] in papersPerCountry['country'].values) else np.nan, axis=1)
    
    
    #print(world['papers'])
    
    world.plot(column = 'papers', edgecolor=u'white', cmap='plasma', ax=ax2, legend = True, missing_kwds={'color': '#ededed'}, legend_kwds={'shrink': 0.4})
    #.loc[world['name'].isin(papersPerCountry['country'])]
    
    ax2.axis('scaled')
    plt.savefig(f'{outputFolder}/papers-per-country.pdf', format='pdf', bbox_inches='tight')
    #plt.show()    
    
def venuesAndPublishers():
    df = loadData()
    
    df = df[['Publication venue', 'Publication type', 'Publisher']]
    
    papersPerPublisher = df.groupby('Publisher').count().sort_values(by=df.columns[0], ascending=False).reset_index()[['Publisher','Publication type']]
    papersPerPublisher.columns = ['publisher', 'papers']
    
    
    papersPerVenue = df.groupby(['Publication venue', 'Publisher']).count().sort_values(by=df.columns[1], ascending=False).reset_index()[['Publication venue', 'Publisher','Publication type']]
    papersPerVenue.columns = ['venue', 'publisher', 'papers']
    
    papersPerVenue = papersPerVenue[papersPerVenue['papers']>1]
    
    vals = papersPerVenue.astype(str).values
    rows = ''
    
    for val in vals:
        val[0] = val[0].replace('&', '\&')
        rows += f"{val[0]} & {val[1]} & {val[2]} \\\\\n"
        
    templateValues = {'rows' : rows}
    
    result = ""
    
    with open('templates/table-template.tex', 'r') as f:
        src = Template(f.read())
        result = src.substitute(templateValues)
    
    f = open(f'{outputFolder}/venues-table.tex', 'w')
    f.write(result)
    f.close()
    
def wordcloud():
    with open('data/abstracts.txt', 'r', encoding="utf-8") as f:
        text = f.read()
        
        stopwords = set(STOPWORDS)
        stopwords.update(["model", "modeling", "modelling", "models"])
        
        wordcloud = WordCloud(background_color="white", stopwords=stopwords, width=1200, height=600).generate(text)
        
        plt.figure(figsize=[20,10])
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(f'{outputFolder}/wordcloud-abstracts.pdf', format='pdf', bbox_inches='tight')
        plt.show()

def sdgs():
    df = loadData()
    
    df = df[['Sustainability goal / SDG'].isna()]
    
    print(df)

sdgs()