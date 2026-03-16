import os
import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import LeaveOneOut
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import silhouette_score
from sklearn.feature_selection import SelectKBest

def load_playlists(subpath):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  pl_dict = {}
  counter = 0

  print('Loading Playlists In %s'%(os.path.join(dir_path, 'playlists', subpath)))

  for (root, dirs, file) in os.walk(os.path.join(dir_path, 'playlists', subpath)):
    for f in file:
      if '.csv' in f:

        pl_name = os.path.splitext(f)[0]
        try:
          
          pl_dict[pl_name] = pd.read_csv(os.path.join(dir_path, 'playlists', subpath, f))

        except:
          print('Failed to parse %s...  Skipping'%(pl_name))

        finally:
          print('\t%s'%(pl_name))
    
  return pl_dict

def load_rtplaylists(subpath, cluster):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  pl_dict = {}
  counter = 0

  print('Loading Playlists In %s'%(os.path.join(dir_path, 'playlists', '%s_groups'%(cluster), subpath)))

  for (root, dirs, file) in os.walk(os.path.join(dir_path, 'playlists', '%s_groups'%(cluster), subpath)):
    for f in file:
      if '.csv' in f:

        pl_name = os.path.splitext(f)[0]
        try:
          
          pl_dict[pl_name] = pd.read_csv(os.path.join(dir_path, 'playlists', '%s_groups'%(cluster), subpath, f))

        except:
          print('Failed to parse %s...  Skipping'%(pl_name))

        finally:
          print('\t%s'%(pl_name))
    
  return pl_dict

def merge_playlists(pl_dict, num):
    df = pd.DataFrame()
    for pl in pl_dict:
        df = pd.concat(list(pl_dict.values()), ignore_index=True)
        df['type'] = num
    return df

def GNB(df, title):
      #clean data
      dataframe = df.loc[:, ['Danceability', 'Energy', 'Key', 'Loudness', 'Mode', 'Speechiness', 'Acousticness', 'Instrumentalness', 
                             'Liveness', 'Valence', 'Tempo', 'Time Signature', 'type']]
      dataframe1 = dataframe.dropna()
      dataset = np.array(dataframe1)

      #assign feature data to x and target labels to y
      X = dataset[:, 0:11] #audio feature data only
      X = X.astype(float) #ensure all floats
      y = dataset[:, 12] #targets
      y = y.astype(float) #ensure all floats

      #assign attribute labels
      attributes = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 
                  'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']

      #create GNB classifier
      clf = GaussianNB()
      #create LOO cross validation
      loo = LeaveOneOut()

      successes = []
      for train_index, test_index in loo.split(X):
            clf.fit(X[train_index], y[train_index])
            successes.append(clf.score(X[test_index], y[test_index]))

      #print('GaussianNB', np.mean(successes))

      return title, 'GaussianNB', np.mean(successes)

def KNN(df, title, k):
      #clean data
      dataframe = df.loc[:, ['Danceability', 'Energy', 'Key', 'Loudness', 'Mode', 'Speechiness', 'Acousticness', 'Instrumentalness', 'Liveness', 'Valence', 'Tempo', 'Time Signature', 'type']]
      dataframe1 = dataframe.dropna()
      dataset = np.array(dataframe1)

      #assign feature data to x and target labels to y
      X = dataset[:, 0:11] #audio feature data only
      X = X.astype(float) #ensure all floats
      y = dataset[:, 12] #targets
      y = y.astype(float) #ensure all floats

      #assign attribute labels
      attributes = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 
                  'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']
      
      #create KNN classifier
      knn = KNeighborsClassifier()
      #create LOO cross validation
      loo = LeaveOneOut()

      successes = []
      for train_index, test_index in loo.split(X):
            knn.fit(X[train_index], y[train_index])
            successes.append(knn.score(X[test_index], y[test_index]))
      sil = silhouette_score(X, knn.predict(X))

      select = SelectKBest(k=k)
      select.fit(X, y)
      indices = np.argsort(select.scores_)
      for index in indices:
            print(index, ', ', attributes[index], ', ', select.scores_[index], ', ', select.pvalues_[index])

      return title, 'KNN', np.mean(successes), 'Silhouette Width', sil
      
def Kbest(df, title, k):
      dataframe = df.loc[:, ['Danceability', 'Energy', 'Key', 'Loudness', 'Mode', 'Speechiness', 'Acousticness', 'Instrumentalness', 'Liveness', 'Valence', 'Tempo', 'Time Signature', 'type']]
      dataframe1 = dataframe.dropna()
      dataset = np.array(dataframe1)

      #assign feature data to x and target labels to y
      X = dataset[:, 0:11] #audio feature data only
      X = X.astype(float) #ensure all floats
      y = dataset[:, 12] #targets
      y = y.astype(float) #ensure all floats

      attributes = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 
                  'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']

      knn = KNeighborsClassifier()
      loo = LeaveOneOut()

      select = SelectKBest(k=k)
      select.fit(X, y)
      indices = np.argsort(select.scores_)
     
      x_new = X[:, indices[0+(abs(k-10)):10]]

      successes4 = []

      for train_index, test_index in loo.split(x_new):
            knn.fit(x_new[train_index], y[train_index])
            successes4.append(knn.score(x_new[test_index], y[test_index]))
      sil = silhouette_score(x_new, knn.predict(x_new))

      return title, 'New KNN', np.mean(successes4), k, sil

if __name__ == '__main__':
  
  #case study #1: Barbenheimer
  barbenheimer = merge_playlists(load_playlists('barbenheimer'), 1)
  barbie = merge_playlists(load_playlists('barbie'), 2)
  oppenheimer = merge_playlists(load_playlists('oppenheimer'), 3)

  barbenheimerxbarbie = pd.concat([barbenheimer, barbie])
  barbenheimerxoppenheimer = pd.concat([barbenheimer, oppenheimer])
  barbiexoppenheimer = pd.concat([barbie, oppenheimer])
  allbarbplaylists = pd.concat([barbenheimer, barbie, oppenheimer])

  #case study #2: D&D
  dms = merge_playlists(load_playlists('dms'), 1)
  reddit = merge_playlists(load_playlists('reddit'), 2)
  whiterun = merge_playlists(load_playlists('whiterun'), 3)

  dmsxwhiterun = pd.concat([dms, whiterun])
  redditxwhiterun = pd.concat([reddit, whiterun])

  #case study #3: roadtrips
  rtg = merge_playlists(load_rtplaylists('rtg', 'f'), 1)
  singalong = merge_playlists(load_rtplaylists('singalong', 'f'), 2)

  country_rock = merge_playlists(load_rtplaylists('country_rock', 'g'), 1)
  pop_indie = merge_playlists(load_rtplaylists('pop-indie', 'g'), 2)
  pop_punk = merge_playlists(load_rtplaylists('pop_punk', 'g'), 3)
  pop_rap = merge_playlists(load_rtplaylists('pop_rap', 'g'), 4)
  pop_rock = merge_playlists(load_rtplaylists('pop_rock', 'g'), 5)
  rap_rnb = merge_playlists(load_rtplaylists('rap_rnb', 'g'), 6)

  sevnine = merge_playlists(load_rtplaylists('70s-90s', 'y'), 1)
  postcovid = merge_playlists(load_rtplaylists('2023-2025', 'y'), 2)
  precovid = merge_playlists(load_rtplaylists('2017-2019', 'y'), 3)
  thousands = merge_playlists(load_rtplaylists('2000s', 'y'), 4)
  twelve = merge_playlists(load_rtplaylists('2012', 'y'), 5)

  functions = pd.concat([rtg, singalong])
  genres = pd.concat([country_rock, pop_indie, pop_punk, pop_rap, pop_rock, rap_rnb])
  years = pd.concat([sevnine, postcovid, precovid, thousands, twelve])

  #assign sets of playlists and their titles to ordered lists     
  barb_sets = [barbenheimerxbarbie, barbenheimerxoppenheimer, barbiexoppenheimer, allbarbplaylists]
  barb_titles = ['Barbenheimer and Barbie', 'Barbenheimer and Oppenheimer', 'Barbie and Oppenheimer', 'All Barbenheimer Playlists']

  dnd_sets = [dmsxwhiterun, redditxwhiterun]
  dnd_titles = ['DMs and Whiterun', 'Reddit and Whiterun']

  rt_sets = [functions, genres, years]
  rt_titles = ['F Groups', 'G Groups', 'Y Groups']

  all_sets = [barbenheimerxbarbie, barbenheimerxoppenheimer, barbiexoppenheimer, allbarbplaylists, 
              dmsxwhiterun, redditxwhiterun, functions, genres, years]
  all_titles = ['Barbenheimer and Barbie', 'Barbenheimer and Oppenheimer', 'Barbie and Oppenheimer', 'All Barbenheimer Playlists',
                'DMs and Whiterun', 'Reddit and Whiterun', 'F Groups', 'G Groups', 'Y Groups']

  #for each dataset (set), using its comparison title (title)
  for set, title in zip(all_sets, all_titles):
        #run GNB
        print(GNB(set, title))
        #run KNN
        print(KNN(set, title, 12))
        #run Kbest where k is 1 through 12
        for i in range(1, 12):
            print(Kbest(set, title, i))