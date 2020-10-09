#!/usr/bin/env python
# coding: utf-8

# # Exploratory Data Analysis SuperStore

# ## Author: Rahul Kulkarni

# ### Problem Statement:
# Perform Exploratory Data Analysis on the given data to find weak areas which hamper the profits for the organisation.

# #### Importing Libraries

# In[1]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# #### Loading the data from the link and convert it into a pandas data frame.

# In[2]:


store = pd.read_csv('https://drive.google.com/u/0/uc?id=1lV7is1B566UQPYzzY8R2ZmOritTW299S&export=download')
store.head()


# #### The quantity of data that we have.

# In[3]:


store.shape


# #### Attributes that we need to consider while analysing the data.

# In[4]:


store.columns


# #### Checking if the datatypes of the attributes are correct.

# In[5]:


store.dtypes


# #### Check if there is any missing data.

# In[6]:


store.isnull().sum()


# #### Check for which countries is the data provided for.

# In[7]:


store['Country'].value_counts()


# Since the data is provided only for United States, we can safely drop the 'Country' and 'Postal Code' column from the data frame.

# In[8]:


store.drop(['Country','Postal Code'],axis=1,inplace=True)
store.head()


# #### Total profit and sales for the store.

# In[10]:


np,ns = store['Profit'].sum(),store['Sales'].sum()
print('Net Profit =',np)
print('Net Sales =',ns)
print('Operating Profit Ratio =',round(np/ns,2),'or',round((np/ns)*100,2),'%')


# Overall the performance of the store is not quite upto the mark, which can be clearly seen from the Operating Profit Ratio. Let's analyse the data to a deeper level to check which areas need improvement.

# Since the further analysis conatains numerous plots, predominantely Bar charts and Pie Charts. To ease the visualizaion process, I have created functions to quickly generate the required plots.

# In[35]:


def plotbar(w,h,x,y1,y2,y1label,y2label,title,xlabel,ylabel):
    plt.figure(figsize=(w,h))
    plot = sns.barplot(x=x,y=y1,color='b',label=y1label)
    sns.barplot(x=x,y=y2,color='r',label=y2label)
    plot.set_xticklabels(x, rotation=90)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid()
    plt.show()
def pieplot(x,l,r,title):
    print(title)
    plt.pie(x=x,labels=l,autopct='%1.1f%%',radius=r)
    plt.show()


# #### Areas to analyse
# I have divided my analysis into 5 parts, which take a look at different attributes and their relations with profit and sales.
# 1. Geographical Attributes (Region, State and City)
# 2. Category of Products
# 3. Customer Segement
# 4. Shipping Mode
# 5. Discounts

# #### Geographical Attributes
# Let's take a look the distribution of profit and sales across different regions.

# In[12]:


store.groupby('Region')[['Sales','Profit']].sum()


# In[14]:


regions = sorted(store['Region'].unique())
sales = store.groupby('Region')['Sales'].sum()
profits = store.groupby('Region')['Profit'].sum()
plotbar(7,5,regions,sales,profits,'Sales','Profit','Sales and Profit Across Different Regions','Region','Sales/Profit')
pieplot(sales,regions,1.5,'Sales Distribution Across Regions')
pieplot(profits,regions,1.5,'Profit Distribution Across Regions')


# Important Inferences:
# 1. Majority of sales are obtained from the West and East regions, they make up 61.1% of the total sales. Similar sort of distribution is seen in the profits, they make up of almost 70% of the total profits.
# 2. Even though the Central region has a higher sales than South, it has lower profits.

# Let's take a look at the profit and sales distribution across various states.

# In[15]:


store.groupby('State')[['Sales','Profit']].sum()


# In[16]:


states = sorted(store['State'].unique())
sales = store.groupby('State')['Sales'].sum()
profits = store.groupby('State')['Profit'].sum()
plotbar(16,8,states,sales,profits,'Sales','Profit','Sales and Profit Across Different States','States','Sales/Profit')


# Important Inferences:
# 1. California has the highest sales and profits but operating profit ratio seems low.
# 2. Even though Texas has mid range sales, it has the lowest profits among all states.
# 3. The condition in Texas needs immediate improvement, since it can be seen from the plot that states which have less sales than Texas have also churned out profits.
# 
# Let's analyse the data for states which churn out losses.

# In[17]:


loss = []
for i in range(len(profits)):
    if profits[i]<0:
        loss.append(states[i])
print(', '.join(loss))


# In[36]:


for state in loss:
    cities = sorted(store['City'][store['State']==state].unique())
    sales,profits=[],[]
    for city in cities:
        sales.append(store['Sales'][store['City']==city].sum())
        profits.append(store['Profit'][store['City']==city].sum())
    plotbar(14,6,cities,sales,profits,'Sales','Profit','Sales and Profit Across '+state,state,'Sales/Profit')
    pieplot(sales,cities,1.5,'Sales Distribution Across '+state)


# Important Inferences:
# 1. Phoenix has the highest sales in Arizona but has the lowest profit.
# 2. No city in Colorado produces profits.
# 2. Aurora and Louisville have very high sales but still don't churn out profits.
# 3. Jacksonville has the highest sales in Florida but has the lowest profit.
# 4. Chicago has the highest sales in Illinois but has the lowest profit.
# 5. Burlington has mid level sales in North Carolina but has the lowest profit.
# 6. Lancaster has almost equal amount of sales and losses.
# 7. Philadelphia has the highest sales in Pennsylvania but has the lowest profit.
# 8. There are various cities in Tennessee which have small losses.
# 9. Houston has the highest sales in Texas but has the lowest profit and a couple of cities where sales are mid level but chrun out losses.
# 
# Major trend which can be observed after analysing all the data is that even though there are cities with high amount of sales, they don't produce profits.

# #### Category of products
# Let's take a look at the profit and sales distribution across various categories of products.

# In[37]:


profits = store.groupby(['Category','Sub-Category'])['Profit'].sum()
sales = store.groupby(['Category','Sub-Category'])['Sales'].sum()
store.groupby(['Category','Sub-Category'])[['Sales','Profit']].sum()


# In[38]:


furn = sorted(store['Sub-Category'][store['Category']=='Furniture'].unique())
os = sorted(store['Sub-Category'][store['Category']=='Office Supplies'].unique())
tech = sorted(store['Sub-Category'][store['Category']=='Technology'].unique())
plotbar(6,4,furn,sales[0:4],profits[0:4],'Sales','Profit','Sales and Profit Across Furniture Category','Furniture','Sales/Profit')
pieplot(sales[:4],furn,1.5,'Sales Distribution Across Furniture')
plotbar(6,4,os,sales[4:13],profits[4:13],'Sales','Profit','Sales and Profit Across Office Supplies Category','Office Supplies','Sales/Profit')
pieplot(sales[4:13],os,1.5,'Sales Distribution Across Office Supplies')
plotbar(6,4,tech,sales[13:],profits[13:],'Sales','Profit','Sales and Profit Across Technology Category','Technology','Sales/Profit')
pieplot(sales[13:],tech,1.5,'Sales Distribution Across Technology')


# Important Inferences:
# 1. Tables are the major loss point and Chairs are the strong point for the Furniture category.
# 2. Profits in the Supplies sub-category can be improved in Office Supplies.
# 3. Machines produce second highest sales in Technology category but don't generate significant profits.

# #### Customer Segment
# Let's analyse the sales and profit distribution across various segments.

# In[39]:


store.groupby('Segment')[['Sales','Profit']].sum()


# In[40]:


segments = sorted(store['Segment'].unique())
profits = store.groupby('Segment')['Profit'].sum()
sales = store.groupby('Segment')['Sales'].sum()
plotbar(6,6,segments,sales,profits,'Sales','Profit','Sales and Profit Across Segments','Segments','Sales/Profit')
pieplot(sales,segments,1.5,'Sales')
pieplot(profits,segments,1.5,'Profits')


# Important Inferences:
# 1. There are no losses reported across segments.
# 2. Consumer segment has a highest chunk of the overall sales,makes up just over 50% of overall sales.
# 3. But similar distribution isn't observed with profits, where Consumer segment makes up less than 50% of the overall profits. 
# 
# Let's dig deeper into the Sub-Categories preffered by the segments.

# In[41]:


profit = store.groupby(['Segment','Sub-Category'])['Profit'].sum()
sales = store.groupby(['Segment','Sub-Category'])['Sales'].sum()
store.groupby(['Segment','Sub-Category'])[['Sales','Profit']].sum()


# In[42]:


sub = sorted(store['Sub-Category'].unique())


# In[43]:


for i,seg in zip(range(3),segments):
    plotbar(12,8,sub,sales[i*17:(i+1)*17],profit[i*17:(i+1)*17],'Sales','Profit',seg,'Sub-Categories','Sales/Profit')
    pieplot(sales[i*17:(i+1)*17],sub,2,'Sales Distribution Across '+seg+' Segment')


# Important Inferences:
# 1. Chairs, Phones, Storage and Tables make the major chunk of sales across segments.
# 2. Accessories,Appliances,Binders, Copiers and Paper contribute significantly to the profits but have less share in the sales individually.
# 3. Sub-Categories which have low sales, tend to produce profits.
# 4. Tables have significant sales but don't generate profits.

# #### Shipping Mode
# Let's analyse profits and sales across various shipping modes.

# In[44]:


store.groupby('Ship Mode')[['Sales','Profit']].sum()


# In[45]:


mode = sorted(store['Ship Mode'].unique())
sales = store.groupby('Ship Mode')['Sales'].sum()
profit = store.groupby('Ship Mode')['Profit'].sum()
plotbar(5,5,mode,sales,profit,'Sales','Profit','Sales And Profit Across Shipping Modes','Mode','Sales/Profit')
pieplot(sales,mode,1.5,'Sales Across Various Shipping Modes')
pieplot(profit,mode,1.5,'Profit Across Various Shipping Modes')


# Important Inferences:
# 1. No losses generated across various shipping modes.
# 2. Similar distribution across sales and profits for every shipping mode.
# 
# Let's look at the Sub-Categories shipped across various modes.

# In[46]:


store.groupby(['Ship Mode','Sub-Category'])[['Sales','Profit']].sum()


# In[48]:


profit = store.groupby(['Ship Mode','Sub-Category'])['Profit'].sum()
sales = store.groupby(['Ship Mode','Sub-Category'])['Sales'].sum()
for i,md in zip(range(4),mode):
    plotbar(12,8,sub,sales[i*17:(i+1)*17],profit[i*17:(i+1)*17],'Sales','Profit',md,'Sub-Categories','Sales/Profit')
    pieplot(sales[i*17:(i+1)*17],sub,2,'Sales Distribution Across '+md)


# Important Inferences:
# 1. Chairs and Phones contibute significantly towards sales across different modes.
# 2. Accessories, Binders, Copiers and Paper contribute heavily to the profit but make a smaller share of sales individually.
# 3. Tables generate losses with significant amount of sales.
# 
# In addition to above inferences:
# 1. First Class: Copiers and Art make up the majority of sales. Appliances and Storage make up significant share of the profits but are on the mid level of sales.
# 2. Same Day: Machines and Accesories make up majority of sales. Storage contribute heavily to the profit but make a smaller share of sales individually.
# 3. Second Class: Storage makes up majority of sales. Applicances contribute heavily to the profit but make a smaller share of sales individually.
# 4. Standard: Storage makes up majority of sales.

# #### Discounts
# Let's analyse the data for various percentages of discounts given to customers.

# In[49]:


store.groupby('Discount')[['Sales','Profit']].sum()


# In[51]:


disc = sorted(store['Discount'].unique())
profit = store.groupby('Discount')['Profit'].sum()
sales = store.groupby('Discount')['Sales'].sum()
plotbar(8,8,disc,sales,profit,'Sales','Profit','Sales And Profit For Various Discounts','Discounts','Sales/Profit')
pieplot(sales,disc,2,'Sales Distribution Across Discounts')


# Important Inferences:
# 1. As expected higher discounts result in higher losses.
# 2. Even though discounts are being provided, the respective sales are very low.
# 
# Let's look at the discounts provided for various Categories.

# In[52]:


store.groupby(['Category','Discount'])[['Profit','Sales']].sum()


# In[53]:


sales = store.groupby(['Category','Discount'])['Sales'].sum()
profit = store.groupby(['Category','Discount'])['Profit'].sum()
furn = sorted(store['Discount'][store['Category']=='Furniture'].unique())
os = sorted(store['Discount'][store['Category']=='Office Supplies'].unique())
tech = sorted(store['Discount'][store['Category']=='Technology'].unique())
plotbar(8,8,furn,sales[:11],profit[:11],'Sales','Profit','Sales And Profit For Furniture','Discounts','Sales/Profit')
plotbar(8,8,os,sales[11:16],profit[11:16],'Sales','Profit','Sales And Profit For Office Supplies','Discounts','Sales/Profit')
plotbar(8,8,tech,sales[16:],profit[16:],'Sales','Profit','Sales And Profit For Technology','Discounts','Sales/Profit')


# Important Inferences:
# 1. Higher discounts didn't produce higher sales.
# 2. Discounts of more than 30% don't generate any profits.
# 3. Discount of 20% generate the most sales among all the discounts given.

# #### Conclusion:

# Areas which need improvement:
# 1. Attempts should be made to improve sales in the Central and South region.
# 2. One trend which was observed across loss bearing states is that even though the cities in those states generated good amount of sales, they don't churn out profits. This could be avoided by providing much more polished services.
# 3. The condition in Texas needs immediate improvement since it contributes strongly towards sales(3rd highest) but still churn out losses. 
# 3. Furniture category isn't making any significant contributions to the profits. Particularly Tbales aren't beneficial across any states. Improvement or scrapping of this sub-category should be considered.
# 4. Supplies sub-category need help as they have good amount of sales but still run into losses.
# 5. Overall Technology category is performing pretty good, but Machines need to improve as they have the second highest sales in the category but barely generate any profit.
# 6. Consumer segement has a strong hold on sales but similar trend isn't observed with respect profits.
# 7. Improving sales for Home Office and Corporate segments should be prioritised.
# 8. No significant changes can be made to shipping modes, as no particular trend could be observed.
# 9. Discounts are very important for attracting more customers therefore even though higher discounts generate losses, we can't scrap them. 
# 10. Interesting trend which was observed among discounts was that 20% discount attracted alot of customers, maybe this has a psychological effect on customers where they prefer it over the rest of the discounts. Since higher discounts generally mean the products have become outdated or might have some minor defects. 
# 11. Rather than providing more discounts, which doesn't seem to be elevating the sales, organisation should concentrate more on marketing various products to appropriate customer segments. They should make use of recommender systems to provide customers an amazing shopping experience.

# In[ ]:




