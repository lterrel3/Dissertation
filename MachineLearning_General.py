import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import LeaveOneOut
from sklearn.neighbors import KNeighborsClassifier

#load csv with audio feature data
PL_1 = pd.read_csv('Location/FileName.csv')
PL_2 = pd.read_csv('Location/FileName.csv')
PL_3 = pd.read_csv('Location/FileName.csv')

#insert identifiers into dataframe
PL_1['type'] = 1
PL_2['type'] = 2
PL_3['type'] = 3

#one to one comparison
comparison1x2 = pd.concat(PL_1, PL_2)
comparison1x3 = pd.concat(PL_1, PL_3)
comparison2x3 = pd.concat(PL_2, PL_3)

#all playlists
pre_dataset = pd.concat(PL_1, PL_2)
allplaylists_data = pd.concat([pre_dataset, PL_3])

def GNB(dataframe, title):
      #clean data
      dataframe = dataframe.dropna()
      dataset = np.array(dataframe)

      #assign feature data to x and target labels to y
      x = dataset[:, 11:22] #audio feature data only
      x = x.astype(float) #ensure all floats
      y = dataset[:, 23] #targets
      y = y.astype(float) #ensure all floats

      #assign attribute labels
      attributes = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 
                  'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

      #create GNB classifier
      clf = GaussianNB()
      #create LOO cross validation
      loo = LeaveOneOut()

      successes = []
      for train_index, test_index in loo.split(x):
            clf.fit(x[train_index], y[train_index])
            successes.append(clf.score(x[test_index], y[test_index]))

      print('GaussianNB', np.mean(successes))

      return title, 'GaussianNB', np.mean(successes)

def KNN(dataset, title):
      #clean data
      dataframe = dataframe.dropna()
      dataset = np.array(dataframe)

      #assign feature data to x and target labels to y
      x = dataset[:, 11:22] #audio feature data only
      x = x.astype(float) #ensure all floats
      y = dataset[:, 23] #targets
      y = y.astype(float) #ensure all floats

      #assign attribute labels
      attributes = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 
                  'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']
      
      #create KNN classifier
      knn = KNeighborsClassifier()
      #create LOO cross validation
      loo = LeaveOneOut()

      successes = []
      for train_index, test_index in loo.split(x):
            knn.fit(x[train_index], y[train_index])
            successes.append(knn.score(x[test_index], y[test_index]))

      return title, 'KNN', np.mean(successes)
      
def Kbest(dataset, title, kbest):
      
      # get only the best features
      from sklearn.feature_selection import SelectKBest

      #clean data
      dataframe = dataframe.dropna()
      dataset = np.array(dataframe)

      #assign feature data to x and target labels to y
      x = dataset[:, 11:22] #audio feature data only
      x = x.astype(float) #ensure all floats
      y = dataset[:, 23] #targets
      y = y.astype(float) #ensure all floats

      #assign attribute labels
      attributes = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 
                  'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']
       
      #create KNN classifier
      knn = KNeighborsClassifier()
      #create LOO cross validation
      loo = LeaveOneOut()

      #create selectKBest, assign kbest number
      select = SelectKBest(k=kbest)
      #create scores for attributes
      select.fit(x,y)
      #sort and view scores
      indices = np.argsort(select.scores_)
      for index in indices:
            print(index, attributes[index], select.scores_[index])
      #fit with new feature data, using only kbest number of features
      x_new = select.fit_transform(x, y)

      successes = []

      for train_index, test_index in loo.split(x_new):
            knn.fit(x_new[train_index], y[train_index])
            successes.append(knn.score(x_new[test_index], y[test_index]))

      #print('New KNN', np.mean(successes4))
      return title, 'New KNN', np.mean(successes)

#assign sets of playlists and their titles to ordered lists     
sets = [comparison1x2, comparison1x3, comparison2x3, allplaylists_data]
titles = ['Comparison1x2', 'Comparison1x3', 'Comparison2x3', 'allplaylists_data']

#for each dataset (set), using its comparison title (title)
for set, title in sets, titles:
      #run GNB
      GNB(set, title)
      #run KNN
      KNN(set, title)
      #run Kbest where k is 1 through 12
      for i in range(0, 12, 1):
            Kbest(set, title, i)