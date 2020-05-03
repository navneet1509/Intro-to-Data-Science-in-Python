
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.5** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # Assignment 3 - More Pandas
# This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

# ### Question 1 (20%)
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
# 
# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.
# 
# <br>
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# <br>
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This function should return a DataFrame with 20 columns and 15 entries.*

# In[25]:


import pandas as pd
import numpy as np
def answer_one():
    

    energy = pd.read_excel(r"Energy Indicators.xls",skiprows=17, skipfooter=38)

    # print whole sheet data

    energy=energy.drop(['Unnamed: 0','Unnamed: 1'], axis=1)
    energy.rename(columns={'Unnamed: 2':'Country', 'Petajoules':'Energy Supply', 'Gigajoules':'Energy Supply per Capita', '%': '% Renewable'}, inplace=True )
    energy["Energy Supply"]=energy["Energy Supply"]*1000000

    energy['Country'] = energy['Country'].str.replace('1','')
    energy['Country'] = energy['Country'].str.replace('2','')
    energy['Country'] = energy['Country'].str.replace('3','')
    energy['Country'] = energy['Country'].str.replace('4','')
    energy['Country'] = energy['Country'].str.replace('5','')
    energy['Country'] = energy['Country'].str.replace('6','')
    energy['Country'] = energy['Country'].str.replace('7','')
    energy['Country'] = energy['Country'].str.replace('8','')
    energy['Country'] = energy['Country'].str.replace('9','')
    energy['Country'] = energy['Country'].str.replace('0','')
    energy['Country'] = energy['Country'].str.replace(r" \(.*\)","")
    energy["Energy Supply"][energy["Energy Supply"].str.startswith("...",na=False)]=np.NAN
    energy["Energy Supply per Capita"][energy["Energy Supply per Capita"].str.startswith("...",na=False)]=np.NAN  
    energy["Country"]=energy["Country"].replace({"Republic of Korea": "South Korea",
    "United States of America": "United States",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "China, Hong Kong Special Administrative Region": "Hong Kong"}) 

    GDP=pd.read_csv("world_bank.csv",skiprows=4) 

    GDP["Country Name"]=GDP["Country Name"].replace({"Korea, Rep.": "South Korea", 
    "Iran, Islamic Rep.": "Iran",  "Hong Kong SAR, China": "Hong Kong"}) 

    ScimEn= pd.read_excel(r"scimagojr-3.xlsx")
    GDP=GDP[['Country Name','2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013','2014', '2015']]
    ScimEn=ScimEn.iloc[0:15,]
    Merge1=pd.merge(energy,GDP.set_index("Country Name"),how='inner',left_on="Country",right_index=True)
    Mergefinal=pd.merge(ScimEn,Merge1,how='inner',left_on="Country",right_on="Country")

    Mergefinal=Mergefinal.set_index("Country")
    return Mergefinal

answer_one()


# ### Question 2 (6.6%)
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*

# In[1]:


get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')


# In[64]:





# ## Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by `answer_one()`)

# ### Question 3 (6.6%)
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

# In[ ]:


def answer_three():
    Top15 = answer_one()
    Top15["avgGDP"]=Top15[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013','2014', '2015']].mean(axis=1)
    Top15.sort_values(by=['avgGDP'], ascending=False,inplace=True)
    return Top15.avgGDP
answer_three()




# ### Question 4 (6.6%)
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 
# *This function should return a single number.*

# In[ ]:


def answer_four():
    Top15 = answer_one()
    Top15["Avg"]=Top15[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013','2014', '2015']].mean(axis=1)
    Top15.sort_values(by=['Avg'], inplace=True)
    
    Difference=Top15["2015"][9]-Top15["2006"][9]
    return Difference
answer_four()


# ### Question 5 (6.6%)
# What is the mean `Energy Supply per Capita`?
# 
# *This function should return a single number.*

# In[ ]:



def answer_five():
    Top15 = answer_one()
    return float(Top15["Energy Supply per Capita"].mean())
answer_five()


# ### Question 6 (6.6%)
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*

# In[ ]:



def answer_six():
    Top15 = answer_one()
    Max_percentage=Top15["% Renewable"].max()
    Country=Top15["% Renewable"].idxmax()
    Answer=(Country,Max_percentage)
    return Answer
answer_six()


# ### Question 7 (6.6%)
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*

# In[ ]:


def answer_seven():
    Top15 = answer_one()
    Top15["New"]=Top15["Self-citations"]/Top15.Citations
    Max=Top15.New.max()
    Country=Top15.New.idxmax()
    return (Country,Max)
answer_seven()


# ### Question 8 (6.6%)
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return a single string value.*

# In[ ]:


def answer_eight():
    Top15 = answer_one()
    Top15["Population"]=Top15["Energy Supply"]/Top15["Energy Supply per Capita"]
    Top15.sort_values(by=['Population'], inplace=True)
    return Top15.index[12]
answer_eight()


# ### Question 9 (6.6%)
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)*

# In[20]:




def answer_nine():
    Top15 = answer_one()
    Top15["Population"]=Top15["Energy Supply"]/Top15["Energy Supply per Capita"]
    Top15["Citable Documents Per Person"]=Top15["Citable documents"]/Top15["Population"]
    Top15.dtypes
    list(Top15.columns[Top15.dtypes=="object"])
    Top15[Top15.columns[Top15.dtypes=="object"]] = Top15[Top15.columns[Top15.dtypes=="object"]].astype(float)
    Correlation =  Top15["Citable Documents Per Person"].corr(Top15["Energy Supply per Capita"], method="pearson")
    return Correlation 
    
answer_nine()


# In[ ]:


def plot9():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])


# In[ ]:


#plot9() # Be sure to comment out plot9() before submitting the assignment!


# ### Question 10 (6.6%)
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

# In[35]:


def answer_ten():
    Top15 = answer_one()
    Median= Top15["% Renewable"].median()
    Top15["HighRenew"]=0
    for i in range(0,len(Top15["% Renewable"])):
            if Top15["% Renewable"][i]<Median:
                Top15["HighRenew"][i]=0
            else:
                Top15["HighRenew"][i]=1
       
    Top15 = Top15.sort_values(by= "HighRenew", ascending = (True))        
    return Top15["HighRenew"]
answer_ten()



# ### Question 11 (6.6%)
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

# In[39]:


ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}

def answer_eleven():
    Top15=answer_one()
    Top15=Top15.sort_index()
    Top15
    dict={}
    for i in sorted(ContinentDict.keys()):
        dict[i]=ContinentDict[i]

    dict
    Top15
    Top15["Continent"]=dict.values()
    Top15
    Top15["Population"]=Top15["Energy Supply"]/Top15["Energy Supply per Capita"]
    Top15['Population'] = Top15.Population.astype(float)
    
    Top15['Country'] = Top15.index
    final1=Top15.groupby(['Continent'], as_index=False).agg({"Country":"count","Population":['sum','mean','std']})
    final =final1.set_index("Continent")
    final.columns = ['size','sum','mean','std']
    final['size'] = final['size'].astype(float)
    
    return final
    
answer_eleven()


# ### Question 12 (6.6%)
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 
# *This function should return a __Series__ with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*

# In[60]:


ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
def answer_twelve():
    Top15 = answer_one()
    Top15=answer_one()
    Top15=Top15.sort_index()
    Top15
    dict={}
    for i in sorted(ContinentDict.keys()):
        dict[i]=ContinentDict[i]
    Top15["Continent"]=dict.values()
    Top15['Country'] = Top15.index
    Top15["New % Ren"]=pd.cut(Top15['% Renewable'],5)
    Answer=Top15.groupby(['Continent',"New % Ren"], as_index=False).Country.count().dropna()
    Answer1=Answer.set_index(['Continent',"New % Ren" ])
    return Answer1.Country.astype(int)
answer_twelve()



# ### Question 13 (6.6%)
# Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
# 
# e.g. 317615384.61538464 -> 317,615,384.61538464
# 
# *This function should return a Series `PopEst` whose index is the country name and whose values are the population estimate string.*

# In[11]:


def answer_thirteen():
    Top15 = answer_one()
    Top15["PopEst"]=Top15["Energy Supply"]/Top15["Energy Supply per Capita"]
    Top15['PopEst'] = Top15['PopEst'].astype(object)  
   
    Top15['PopEst']=Top15.apply(lambda x: "{:,}".format(x['PopEst']), axis=1)
    
    return Top15['PopEst'] 
answer_thirteen()


# ### Optional
# 
# Use the built in function `plot_optional()` to see an example visualization.

# In[ ]:


def plot_optional():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")


# In[ ]:


#plot_optional() # Be sure to comment out plot_optional() before submitting the assignment!

