#!/usr/bin/env python
# coding: utf-8

# # Investigate a TMDb_Movies Dataset
# 
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# To complete this Data Analysis project I'm using TMDb movies dataset.
# 
# This dataset contains information about 10,000 movies collected from The Movie Database (TMDb), including user ratings and revenue. It consist of 21 columns such as (imdb_id, revenue, budget, original_title,...etc).
# 
# 
# #### **Question that can analyised from this data set**
# 
#  1. Movies with largest and lowest budgets.
#  2. Movies with most and least earned revenue
#  3. Movies with longest and shortest runtime values.
#  4. Average runtime of all the movies.
#  5. Year of release vs Revenue.
# 

# In[34]:


# Use this cell to set up import statements for all of the packages that you
#   plan to use.

# Remember to include a 'magic word' so that your visualizations are plotted
#   inline with the notebook. See this page for more:
#   http://ipython.readthedocs.io/en/stable/interactive/magics.html

import pandas as pd
import numpy as np
import csv
from datetime import datetime
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# > After observing the dataset and suggest questions for the analysis I'll keep only relevent data and removing the unsued data. 
# > .
# 
# ### General Properties

# In[35]:


#loading the csv file
tmdb_data = pd.read_csv('tmdb-movies.csv')


# In[36]:


#printing first six rows
tmdb_data.head(6)


# ## Data Cleaning
# 
# ### (Removing the unused information from the dataset )¶
# 
# **Important observation regarding this process**
# 
# 
#  1. We need to remove unused column such as id, imdb_id, vote_count, production_company, keywords, homepage etc.
#  2. Removing the duplicacy in the rows(if any).
#  3. Some movies in the database have zero budget or zero revenue, that is there value has not been recorded so we     will be discarding such entries
#  4. Changing release date column into date format.
#  5. Replacing zero with NAN in runtime column.
#  6. Changing format of budget and revenue column.
# 

# > **1. Removing Unused columns**
# 
#  **Columns that we need to delete are**  -  id, imdb_id, popularity, budget_adj, revenue_adj, homepage, keywords, overview, production_companies, vote_count and vote_average.

# In[37]:


# Remove unused column 
del_col=[ 'id', 'imdb_id', 'popularity', 'budget_adj', 'revenue_adj', 'homepage', 'keywords', 'overview', 'production_companies', 'vote_count', 'vote_average']
tmdb_data= tmdb_data.drop(del_col,1)

#previewing the new dataset
tmdb_data.head(6)


# > **2. Removing the duplicacy in the rows(if any).**
# >
# >Lets see how many entries I have in the database

# In[38]:


# Reduce the count of rows.
rows, col = tmdb_data.shape
print('There are {} total entries of movies and {} no.of columns in it.'.format(rows-1, col))


# > Now removing the duplicate rows if any!

# In[39]:


# Removing the duplicate rows
tmdb_data.drop_duplicates(keep ='first', inplace=True)
rows, col = tmdb_data.shape
print('There are now {} total entries of movies and {} columns in it.'.format(rows-1, col))


# > So I have only one duplicate row and I already move it.

# >**3. Removing 0's from budget and the revenue columns**

# In[40]:


temp_list=['budget', 'revenue']

#this will replace all the value from '0' to NAN in the list
tmdb_data[temp_list] = tmdb_data[temp_list].replace(0, np.NAN)

#Removing all the row which has NaN value in temp_list 
tmdb_data.dropna(subset = temp_list, inplace = True)

rows, col = tmdb_data.shape
print('So after removing such entries, we now have only {} no.of movies.'.format(rows-1))


# > **4. Changing the release date column into standard date format**

# In[41]:


tmdb_data.release_date = pd.to_datetime(tmdb_data['release_date'])


# In[42]:


# printing the changed dataset
tmdb_data.head(5)


# >**5. Replacing zero with NAN in runtime column.**
# 

# In[43]:


# Replacing 0's with NaN of runtime column 
tmdb_data['runtime'] =tmdb_data['runtime'].replace(0, np.NAN)


# >**6. Changing format of budget and revenue column.**

# In[44]:


# Printing the data type of the dataset
tmdb_data.dtypes


# In[45]:


change_type=['budget', 'revenue']

#changing data type
tmdb_data[change_type]=tmdb_data[change_type].applymap(np.int64)

# Printing the data after changed
tmdb_data.dtypes


# > Checking the current format of columns in the dataset

# In[46]:


#printing the data type of the data set
tmdb_data.dtypes


# In[47]:


change_type=['budget', 'revenue']
#changing data type
tmdb_data[change_type]=tmdb_data[change_type].applymap(np.int64)
#printing the changed information
tmdb_data.dtypes


# <a id='eda'></a>
# ## Exploratory Data Analysis

# ### Research Question 1  : Movies with largest and lowest budgets

# In[48]:


import pprint
#defining the function
def calculate(column):
    #for highest budget
    high= tmdb_data[column].idxmax()
    high_details=pd.DataFrame(tmdb_data.loc[high])
    
    #for lowest budget
    low= tmdb_data[column].idxmin()
    low_details=pd.DataFrame(tmdb_data.loc[low])
    
    #collectin data in one place
    info=pd.concat([high_details, low_details], axis=1)
    
    return info


# In[49]:


#calling the function
calculate("budget")


# > as showen above the highset budget is (The Warrior's Way) movie and the lowest is (Lost & Found) movie.

# ### Research Question 2 : Movies with most and least earned revenue

# In[50]:


# Calling the function
calculate('revenue')


# > as showen above the largest revenue earned is (Avatar) movie and the lowest is (Shattered Glass) movie.

# ### Research Question 3 : Movies with longest and shortest runtime

# In[51]:


# we will call the same function **calculate(column)** again for this analysis
calculate('runtime')


# > Column with id 2107 shows the longest runtime. While column with id 5162 shows the shortest runtime.

# ### Research Question 4 : Average runtime of the movies

# In[52]:


# defining a function to find average of a column
def avg_fun(column):
    return tmdb_data[column].mean()


# In[53]:


#calling above function
avg_fun('runtime')


# > The average runtime of a movie is 109 minutes.

# > Now, I will show graphic that appear the result above that the average movie runtime is 109 min.

# In[54]:


#printing a histogram of runtime of movies

#giving the figure size(width, height)
plt.figure(figsize=(7,4), dpi = 90)

#Name of the histogram
plt.title('Movies Runtime', fontsize=14)
#x-axis 
plt.xlabel('Runtime of the Movies', fontsize = 11)
#y-axis 
plt.ylabel('Numbers of Movies in the Dataset', fontsize=11)

#giving a histogram plot
plt.hist(tmdb_data['runtime'], rwidth = 0.9, bins =35)
#displays the plot
plt.show()


# > As shown in above histogram most of the movies are timed between 80 to 130 minutes.

# In[55]:


import seaborn as sns
#The First plot is box plot of the runtime of the movies 
plt.figure(figsize=(7,4), dpi = 90)

#using seaborn
sns.boxplot(tmdb_data['runtime'], linewidth = 3)
#Name of the histogram
plt.title('Movies runtime distribution', fontsize=14)

#diplaying the plot
plt.show()


# > Above box plot gives us an overall idea of how is the distribution in movies runtime.

# ### Research Question 5 : Year of release vs Revenue

# In[56]:


#We will be using Line plot for this analysis

year_revenue = tmdb_data.groupby('release_year')['revenue'].sum()

#figure size(width, height)
plt.figure(figsize=(9,5), dpi = 100)

#on x-axis
plt.xlabel('Release Year of Movies', fontsize = 11)
#on y-axis
plt.ylabel('Revenue by all Movies', fontsize = 11)
#title of the line plot
plt.title('Representing Total Revenue by all movies Vs Year of their release.')

#plotting the graph
plt.plot(year_revenue)

#displaying the line plot
plt.show()


# In[57]:


#To find that which year made the highest profit?
year_revenue.idxmax()


# > So I can conclude my graphics analysis, this graphic and calculation shows that year 2015 was the year where movies made the highest profit.

# <a id='conclusions'></a>
# ## Conclusions
# 
# 
# **The data was very interesting to me, and after I finished with this analysis I found some facts about movies:
# 
# > 1. The runtime of Carlos movie is 338 while the runtime of Kid's Story is 15.
# > 2. Average duration of the movie is 109 minutes. 
# > 3. Year 2015 was the year where movies made the highest profit.
# > 4. As shown that the (Avatar) movie was the largest revenue(237000000).
# > 5. As appear (The Warrior's Way) movie was the highest budget(425000000).
# 
# 
# **The dataset have a limitation in some areas:
# 
# > 1. The dataset doesn't contain the producing countries, so we cannot know what is the favorite movies. Also,     
#      where they were made in order to identify which countries have the best and worst rated movies.
# > 2. The currency in budget and revenue doesn't specify.
# 
# **Finally, after did all of these analysis Thank you and I hope you enjoy reading this report.
# 
