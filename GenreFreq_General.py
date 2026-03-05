import pandas as pd
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud

#load csv with genre data
PL_1 = pd.read_csv('Location/FileName.csv')
PL_2 = pd.read_csv('Location/FileName.csv')
PL_3 = pd.read_csv('Location/FileName.csv')

#input csv file
#access genres in CSV files
#return dict of genres and frequencies, write dict to text file
def get_genres(dataframe, title='report'):
    #assign path to text file
    report_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'reports', '%s.csv'%(title))
    genre_oc = {}
    for genre in dataframe['Genres'].values:
      genre = genre.strip()
      for word in genre.split(','):
        #if new genre, create new genre tag that equals 1
        if word.strip() not in genre_oc:
            genre_oc[word.strip()] = 0
        #else, add one occurance to existing genre tag
        genre_oc[word.strip()] += 1
    with open(report_path, 'w', encoding='utf-8') as f:
       #create columns in new file
       f.write('genre, occurence\n')
       #write genres and occurences to the new file
       for word in genre_oc:
          f.write('\"%s\",%d\n'%(word, genre_oc[word]))
    return genre_oc

#create word cloud
mywc = WordCloud(background_color='white', width=1000, height=1000, max_words=25, relative_scaling=0.5, normalize_plurals=False).generate_from_frequencies(get_genres(PL_1, title='PL_1 Genres'))

plt.imshow(mywc)

plt.axis('off')
plt.show()


