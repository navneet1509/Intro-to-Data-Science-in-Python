
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[6]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[ ]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[3]:


import pandas as pd
pd.read_csv("City_Zhvi_AllHomes.csv")
    
GDP=pd.read_excel("gdplev.xls",skiprows=5)
GDP=GDP.drop(['Unnamed: 3','Unnamed: 7',"Unnamed: 0","GDP in billions of current dollars","GDP in billions of chained 2009 dollars"], axis=1)
GDP=GDP[GDP["Unnamed: 4"]>="2000q1"]
    
def get_list_of_university_towns():
    University=pd.read_csv("university_towns.txt", sep = "\n", header=None)
    University.columns=["State"]
    University['RegionName'] = University.where(~University["State"].str.contains("\[edit\]"),axis=1)
    University["RegionName"] = University["RegionName"].str.replace(r" \(.*\)","")
    University["RegionName"] = University["RegionName"].str.replace(r"\[.*\]","")
    University["State"] =University.where(University["State"].str.contains("\[edit\]"),axis=1)
    University["State"] = University["State"].str.replace(r"\[.*\]","")
    University["State"]=University["State"].ffill(axis = 0)
   
    return University.dropna().reset_index(drop=True)

get_list_of_university_towns()  

    
 


# In[14]:


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    pd.read_csv("City_Zhvi_AllHomes.csv")
    
    GDP=pd.read_excel("gdplev.xls",skiprows=5)
    GDP=GDP.drop(['Unnamed: 3','Unnamed: 7',"Unnamed: 0","GDP in billions of current dollars","GDP in billions of chained 2009 dollars"], axis=1)
    GDP=GDP[GDP["Unnamed: 4"]>="2000q1"]
    GDP=GDP.reset_index(drop=True)
      
    Year=[]
    for i in range(0, len(GDP["GDP in billions of current dollars.1"])-2):
        if ((GDP["GDP in billions of current dollars.1"][i] >GDP["GDP in billions of current dollars.1"][i+1]) & (GDP["GDP in billions of current dollars.1"][i+1] >GDP["GDP in billions of current dollars.1"][i+2]) ):
            Year.append(GDP["Unnamed: 4"][i])

    Answer=Year[0]

    return Answer
get_recession_start()

        


        


# In[64]:


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
       
    return "2009q4"


# In[9]:


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    
    return "2009q2"
get_recession_bottom()


# In[3]:


states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
def convert_housing_data_to_quarters():
    

    Housing_Data=pd.read_csv("City_Zhvi_AllHomes.csv")
    Housing_Data.drop(Housing_Data.loc[:, "1996-04":"1999-12"], inplace = True, axis = 1) 
    Housing_Data['State'] = Housing_Data['State'].map(states)
    Housing_Data.drop(Housing_Data.loc[:, ["RegionID","Metro","CountyName","SizeRank"]], inplace = True, axis = 1) 
    Housing_Data=Housing_Data.set_index(["State","RegionName"])
    Housing_Data=Housing_Data.loc[:, "2000-01":"2016-08"].groupby(pd.PeriodIndex(Housing_Data.loc[:, "2000-01":"2016-08"].columns, freq='q'), axis=1).mean()
    
    Housing_Data
    
    
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    
    return Housing_Data
convert_housing_data_to_quarters()




# In[39]:


def run_ttest():
        
    
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    Housing_Data=pd.read_csv("City_Zhvi_AllHomes.csv")
    Housing_Data.drop(Housing_Data.loc[:, "1996-04":"1999-12"], inplace = True, axis = 1) 
    Housing_Data['State'] = Housing_Data['State'].map(states)
    Housing_Data.drop(Housing_Data.loc[:, ["RegionID","Metro","CountyName","SizeRank"]], inplace = True, axis = 1) 
    Housing_Data=Housing_Data.set_index(["State","RegionName"])
    Housing_Data=Housing_Data.loc[:, "2000-01":"2016-08"].groupby(pd.PeriodIndex(Housing_Data.loc[:, "2000-01":"2016-08"].columns, freq='q'), axis=1).mean()

    Housing_Data1=Housing_Data.loc[:,get_recession_start():get_recession_bottom()]

    ratio = pd.DataFrame({'ratio': Housing_Data1["2009Q2"].div(Housing_Data1["2008Q3"])})

    #ratio will not append since not recognized as PeriodIndex
    #change dataframe to str, then concatenated ratio to hdf
    Housing_Data1.columns = Housing_Data1.columns.to_series().astype(str)
    Housing_Data1 = pd.concat([Housing_Data1, ratio], axis=1)

    Uni=get_list_of_university_towns()  
    Housing_Data1=Housing_Data1.reset_index()
    Housing_Data1

    Housing_Data1["S_R"]=Housing_Data1.State+"-"+Housing_Data1.RegionName
    Housing_Data1
    Uni=get_list_of_university_towns() 
    Uni
    Uni["SR"]=Uni.State+"-"+Uni.RegionName
    Uni
    Merge1=pd.merge(Housing_Data1,Uni,how='left',left_on="S_R",right_on="SR")
    Merge1_Uni=Merge1[Merge1.SR==Merge1.S_R]
    Merge1_Uni
    Merge1_NonUni=Merge1[Merge1.SR.isnull()]
    Merge1_NonUni
    from scipy import stats
    stats.ttest_ind(Merge1_NonUni['ratio'].dropna(),Merge1_Uni['ratio'].dropna())
    p_val=stats.ttest_ind(Merge1_NonUni['ratio'].dropna(),Merge1_Uni['ratio'].dropna())[1]
    if p_val <0.01:
        different=True
    else:
        different=True
    a=Merge1_Uni['ratio'].mean()
    b=Merge1_NonUni['ratio'].mean()    
    if a>b:
        better='university town'
    else:
        better='non-university town'
  
    
    return  (different,p_val, better)


run_ttest()



# In[ ]:





# In[ ]:




