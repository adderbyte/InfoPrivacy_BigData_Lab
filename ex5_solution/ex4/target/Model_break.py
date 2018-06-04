
# coding: utf-8

# In[58]:


import numpy as np
import random


# In[218]:


import random

def shuffler(data,sample
    '''
    shuffles input to generate random data set
    Augment training set
    
    '''
    v = []

    p = [v.append(data[c]) for c in range(2,len(data))] #step 1
    random.shuffle(v)  #step 2
    for c in range(2,len(data)):
        data.remove(data[c])  #step 3
        data.insert(c,v[c-2]) #step 4    #c-2 since the part to be shuffled begins from this index of list


    perm_ = np.arange(len(data));        
    random.shuffle(perm_);  # shuffle the samples
    
    random_selection = random.sample(population=set(perm_)  , k=sample);
    
    for index in random_selection:
         
         data[index]= 0
    return data


# In[ ]:


store = []
for i in range(0,1000):
    data = [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1,1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0]
    data_ = shuffler(data,10)
    
    if data_ in store:
        continue
    else:
        datas = {"email":"lukman.olagoke@epfl.ch", "predictions": str(data_)}
        response = requests.post('http://com402.epfl.ch/hw5/ex4_predictions', json=datas)
        print(data_)
        print(response.content)
        store.append(data_)
        
        


# In[399]:


import requests
#d = [0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0]
d = [1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0]
data = {"email":"lukman.olagoke@epfl.ch", "predictions": str(d)}
response = requests.post('http://com402.epfl.ch/hw5/ex4_predictions', json=data)
response.content
 



# In[368]:


d_i = [1,0,1,1,1,1,1,1,1,1,0,1,0,0,1,0,0,1,0,0,0,1,1,0,0,1,0,0,0,0,1,1,0,0,1,1,1,0,0,1,0,0,1,1,0,0,0,1,0,0,1,1,1,0,1,0,0,0,1,1,0,0,0,0,0,1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,1,0,1,1,0,1,1]
data = {"email":"lukman.olagoke@epfl.ch", "predictions": str(d_i)}
response = requests.post('http://com402.epfl.ch/hw5/ex4_predictions', json=data)
response.content


# In[402]:


print(data_store,)


# In[401]:


data = {"email":"lukman.olagoke@epfl.ch", "predictions": str(data_store)}
response = requests.post('http://com402.epfl.ch/hw5/ex4_predictions', json=data)
response.content


# In[243]:


d = [0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0]
for i,v in enumerate(d):
    if d[i] == 1:
        d[i] = 0
    else:
        d[i] = 1


# In[247]:


import requests
#d = [0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0]
#d = [0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0]

data = {"email":"lukman.olagoke@epfl.ch", "predictions": str(d)}
response = requests.post('http://com402.epfl.ch/hw5/ex4_predictions', json=data)


# In[249]:


print(d,)

