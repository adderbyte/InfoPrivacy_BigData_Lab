
# coding: utf-8

# In[2]:


import numpy as np


# In[30]:


ls


# In[ ]:


output/output1.txt


# In[536]:



# This loops reads my input file from the shadow models
results = [];
labels = [];
finals = [];
print(len(finals))
count = 0
with open('output_file/output19.txt') as inputfile:
    for line in inputfile:
       # if count < 100:
        #    count = count + 1 ;
        #if count == 100:
        #    break
        if 'tr' in line :
            labels.append(line)
        elif line.startswith("["):
            #line = line.strip('[')
            #line = line.strip('\n')
            #data.append(ast.literal_eval(i.strip()))
            #results.append(ast.literal_eval(line))
            words = line.replace('[', '').replace('\n', '').split()
            #words = line.split(',')
            results.extend([float(i) for i in words])
            
        elif "]" in line :
            #words = line.replace('\n', '').split()
            words = line.replace("]", '').replace("'", '').replace('\n', '').split()
            results.extend([float(i) for i in words])
            tmp = np.array([results])
            finals.append(tmp)
            results = []
        else: 
            words = line.replace('\n', '').split()
            results.extend([float(i) for i in words])
print(len(finals))        
        
            
            


# In[544]:


# load pickle file I used
with open('parrot.pkl', 'rb') as f:
       final = pickle.load(f)


# In[714]:


# Generate dataset set threshold for probabilities to be used
trainers = []
trainers2 = []
for i in range(0,len(final)): 
        #print(finals[i].max())
        if final[i].max() >  0.20:
            #if final[i].shape == (1,100):
            trainers.append(final[i])
        #elif# final[i].shape == (1,100):
        else:
            trainers2.append(final[i])
            


# In[717]:


# import keras modules
from keras.layers import Dense, Flatten, MaxPooling2D, Dropout, Conv2D
from keras.models import Sequential
import numpy as np
import pickle


# In[718]:


# attack modules provided
NUM_CLASSES = 100

def build_attack_model():
    model = Sequential()

    # Input - Layer
    model.add(Dense(128, activation="relu", input_shape=(NUM_CLASSES,)))

    # Hidden - Layers
    model.add(Dropout(0.3, noise_shape=None, seed=None))
    model.add(Dense(64, activation="relu"))
    model.add(Dropout(0.2, noise_shape=None, seed=None))
    model.add(Dense(64, activation="relu"))

    # Output- Layer
    model.add(Dense(1, activation="sigmoid"))

    model.summary()

    return model


# In[719]:


model = build_attack_model()


# In[720]:


# compile model
from keras import optimizers
#adam = optimizers.Adam(lr=0.95, beta_1=0.9, beta_2=0.3, epsilon=None, decay=0.1, amsgrad=True)
#sgd = optimizers.SGD(lr=0.5, decay=1e-3, momentum=0.9, nesterov=True)
model.compile(loss='binary_crossentropy', optimizer='sgd', metrics = ['accuracy'])


# postiveImgNumbers = 7144
# negativeImgNumbers = 7144

# labelsPostive=np.ones((postiveImgNumbers,),dtype=int)
# labelsNegative=np.zeros((negativeImgNumbers,),dtype=int)
# labels=np.concatenate((labelsPostive,labelsNegative))

# for a, b in zip(trainers, labelsPostive):
#     print a, b

# in_ = zip(trainers, labelsPostive)

# out_ = zip(trainer2_, labelsNegative)

# In[721]:


# add good samples to dataset
dic = {};
for i,v in enumerate(trainers):
    dic[i] = (v,1)
    


# In[722]:


len(dic)


# In[723]:


# make a dictionary from datatset
sample_bad = len(trainers) # sample to collect from abs dataset
for i,v in enumerate(trainers2):
    dic[i+sample_bad] = (v,0)
   


# In[724]:


# collect all dictionary in a key
keys =  list(dic.keys())      # Python 3; use keys = d.keys() in Python 2



# In[725]:


# shuffle the data set in the dictionary by shuffling the dictionary
for i in range(100):
    random.shuffle(keys)
train_dic = [(key, dic[key]) for key in keys]        


# In[726]:


len(train_dic)


# In[727]:


# collect training and test set
trainset_ = []
trainlabels_ = []
for i,v in train_dic:
    trainset_.append(v[0])
    trainlabels_.append(v[1])
    


# In[728]:


len(trainset_)


# In[729]:


# Generate train and test set
trainsize = len(trainset_);
trainset= np.array(trainset_).reshape(trainsize, 100);
trainlabels= np.array(trainlabels_).reshape(trainsize,);


# In[730]:


for i in range(2):    
    model.fit( x=trainset, y=trainlabels, batch_size=10, epochs=100,shuffle= True)


# In[732]:


# get results
results = [];
labels = [];
finals = [];
print(len(finals))
count = 0
with open('my_test.txt') as inputfile:
    for line in inputfile:
       # if count < 100:
        #    count = count + 1 ;
        #if count == 100:
        #    break
        if 'images' in line :
            labels.append(line)
        elif line.startswith("["):
            #line = line.strip('[')
            #line = line.strip('\n')
            #data.append(ast.literal_eval(i.strip()))
            #results.append(ast.literal_eval(line))
            words = line.replace('[', '').replace('\n', '').split()
            #words = line.split(',')
            results.extend([float(i) for i in words])
            
        elif "]" in line :
            #words = line.replace('\n', '').split()
            words = line.replace("]", '').replace("'", '').replace('\n', '').split()
            results.extend([float(i) for i in words])
            tmp = np.array([results])
            finals.append(tmp)
            results = []
        else: 
            words = line.replace('\n', '').split()
            results.extend([float(i) for i in words])
print(len(finals))        
        
            
            


# In[733]:


testsize = 100
testset= np.array(finals).reshape(testsize, 100);


# In[734]:


prediction = model.predict( testset, batch_size=10) # make predictions


# In[735]:


prediction


# In[736]:


ans = []
for i in prediction :
    if i ==1.:
        ans.append(1)
    else:
        ans.append(0)


# In[737]:


print(ans,)


# In[738]:


import requests
#d = [0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0]
#d = [1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0]
data = {"email":"lukman.olagoke@epfl.ch", "predictions": str(ans)}
response = requests.post('http://com402.epfl.ch/hw5/ex4_predictions', json=data)
response.content


# In[82]:


labels


# In[54]:


results[2]


# In[55]:


a = np.loadtxt('pic.txt')


# In[32]:


file = pd.read_csv('pic.txt',delim_whitespace=True)


# In[6]:


import pickle
pickle.seek(0)
with open(r"text.pkl", "rb") as input_file:
     e = pickle.load(input_file)


# In[28]:


mainlist = []
infile = open('pic.txt', 'r')
for line in infile:
    print(line)
    line = line.replace('\n', '').replace('[', '').replace(']', '').replace("'", "").replace(' ', '')
    mainlist.append(line.split(','))
infile.close()



# In[29]:


mainlist


# In[12]:


f = open("text.pkl", "r+b")
frame_list = []

while 1:
    f.seek(0)
    try:
        f.seek(0)
        frame_list.append (pickle.load(f))
        f.seek(0)
        frame_list = sum(frame_list, [])
    except EOFError:
        break
f.close()


# In[20]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[21]:


PIK = 'pic.dat'
with open(data.pkl, "wb") as f:
    pickle.dump(len(data), f)
    for value in data:
        pickle.dump(value, f)


# In[15]:


data2 = []
PIK = 'text.pkl'
with open(PIK, "rb") as f:
    f.seek(0)
    for _ in range(pickle.load(f)):
        data2.append(pickle.load(f))
print (data2)

