#!/usr/bin/env python
# coding: utf-8

# Data *Online Retail*
# 
# **Oleh:** 
# 
# Dea Restika Augustina Pratiwi (06211740000023)
# 
# ##### Download Data : [online_retail.csv](https://drive.google.com/file/d/1sqrmytAewju0K6fnUoiQhp_GK2Dy__nz/view)

# In[1]:


import pandas as pd
import numpy as np
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import association_rules


# In[3]:


data = pd.read_csv('D:/online_retail.csv')
data


# In[4]:


data.StockCode.nunique()


# In[5]:


data.Description.nunique()


# In[6]:


data.groupby("StockCode").Description.nunique().sort_values(ascending=False).iloc[0:10]


# In[7]:


data.loc[data.StockCode == "23244"].Description.value_counts()


# In[8]:


missing_percentage = data.isnull().sum() / data.shape[0] * 100
missing_percentage


# In[9]:


data[data.Description.isnull()].head()


# In[10]:


data[data.Description.isnull()].CustomerID.isnull().value_counts()


# In[11]:


data[data.Description.isnull()].UnitPrice.value_counts()


# In[12]:


data[data.CustomerID.isnull()].head()


# In[13]:


data.loc[data.CustomerID.isnull(), ["UnitPrice", "Quantity"]].describe()


# In[14]:


data.loc[data.Description.isnull()==False, "lowercase_descriptions"] = data.loc[
    data.Description.isnull()==False,"Description"
].apply(lambda l: l.lower())

data.lowercase_descriptions.dropna().apply(
    lambda l: np.where("nan" in l, True, False)
).value_counts()


# In[15]:


data.loc[data.lowercase_descriptions.isnull()==False, "lowercase_descriptions"] = data.loc[
    data.lowercase_descriptions.isnull()==False, "lowercase_descriptions"
].apply(lambda l: np.where("nan" in l, None, l))


# In[16]:


data = data.loc[(data.CustomerID.isnull()==False) & (data.lowercase_descriptions.isnull()==False)].copy()
data.isnull().sum().sum()


# In[17]:


data["IsCancelled"]=np.where(data.InvoiceNo.apply(lambda l: l[0]=="C"), True, False)
data.IsCancelled.value_counts() / data.shape[0] * 100


# In[18]:


data.loc[data.IsCancelled==True].describe()


# In[19]:


data = data.loc[data.IsCancelled==False].copy()
data = data.drop("IsCancelled", axis=1)


# In[20]:


data['Description'] = data['Description'].str.strip()


# In[21]:


basket1 = data.groupby(['InvoiceNo','Description'])['Quantity'].sum().unstack()
basket1.shape


# In[22]:


basket1 = basket1.applymap(lambda x: 1 if x>0 else 0)
basket1


# In[23]:


basket1.iloc[0].value_counts()


# In[31]:


itemsets1 = apriori(basket1, min_support=0.03, use_colnames=True)


# In[32]:


itemsets1.sort_values('support',ascending=False)


# In[33]:


rules1 = association_rules(itemsets1, metric="lift", min_threshold=1)
rules1.shape


# In[34]:


basket2 = (data[data['Country'] =="France"].groupby(['InvoiceNo', 'Description'])
           ['Quantity'].sum().unstack().reset_index().set_index('InvoiceNo'))


# In[35]:


basket2 = basket2.applymap(lambda x: 1 if x>0 else 0)
basket2


# In[36]:


itemsets2 = apriori(basket2, min_support = 0.1, use_colnames=True)
itemsets2.shape


# In[37]:


itemsets2.sort_values('support',ascending=False)


# In[38]:


rules2 = association_rules(itemsets2, metric="lift", min_threshold=1)
rules2.shape


# In[39]:


rules2


# In[40]:


rulesc2 = association_rules(itemsets2, metric = "confidence", min_threshold = 0.5)
rulesc2


# In[41]:


ruless = rules2[(rules2['confidence'] >= 0.8 )&(rules2['lift'] >= 1.1 )]


# In[42]:


ruless


# In[43]:


ruless.shape


# In[45]:


ruless.to_excel (r'D:/output.xlsx', index = False, header=True)


# ## ANALISIS 15 NEGARA

# Ingin difilter 15 negara dari data yang sudah di preprocessig. Maka, filter dilakukan denan menggunakan bantuan excel. Sebelumnya dilakukan export data ke excel.

# In[ ]:


data.to_excel(r'D:/filter.xlsx', index = False, header = True)


# In[46]:


data15 = pd.read_excel('D:/15negara.xlsx')
data15


# In[47]:


np.sum(data15.isnull())


# In[48]:


data15.Country.nunique()


# In[49]:


basket3 = data15.groupby(['InvoiceNo','Description'])['Quantity'].sum().unstack()
basket3.shape


# In[50]:


basket3 = basket3.applymap(lambda x: 1 if x>0 else 0)
basket3


# In[51]:


itemsets3 = apriori(basket3, min_support=0.1, use_colnames=True)


# In[52]:


itemsets3.sort_values('support',ascending=False)


# In[53]:


rules3 = association_rules(itemsets3, metric="lift", min_threshold=1)
rules3.shape


# In[54]:


rules3


# In[55]:


rulesc3 = association_rules(itemsets3, metric = "confidence", min_threshold = 0.5)
rulesc3


# In[57]:


rulest3 = rules3[(rules3['confidence'] >= 0.5 )&(rules3['lift'] >= 1.1 )]


# In[58]:


rulest3


# In[59]:


rulest3.to_excel (r'D:/output2.xlsx', index = False, header=True)

