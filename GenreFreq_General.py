import pandas as pd
import os

#Loads all csv files in a folder in "playlists," must be housed in same folder as this file
#use "subpath" folders if there are predetermined pl subtypes
#Returns a dict of dataframes
def load_playlists(subpath):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  pl_dict = {}

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

#merges all playlists in a dict into a single dataframe
def merge_playlists(dict_pl):
  return pd.concat(list(dict_pl.values()), ignore_index=True)

#input csv file
#access genres in CSV files
#return dict of genres and frequencies
def get_genre_oc(df):
 
    genre_oc = {}
    dataframe = df.dropna()
    for genre in dataframe['Genres'].values:
      genre = genre.strip()
      for word in genre.split(','):
        #if new genre, create new genre tag that equals 1
        if word.strip() not in genre_oc:
            genre_oc[word.strip()] = 0
        #else, add one occurance to existing genre tag
        genre_oc[word.strip()] += 1
    return genre_oc

#input genre occurence
#write genre report to csv file in "genre reports" subfolder
def write_report(genre_oc, title):
    #assign path to text file
    report_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'reports', 'genre reports', '%s.csv'%(title))
    with open(report_path, 'w', encoding='utf-8') as f:
       #create columns in new file
       f.write('genre, occurence\n')
       #write genres and occurences to the new file
       for word in genre_oc:
          f.write('\"%s\",%d\n'%(word, genre_oc[word]))

if __name__ == '__main__':

  #loadplaylists
  barbie_pls = load_playlists('barbie')
  bh_pls = load_playlists('barbenheimer')
  op_pls = load_playlists('oppenheimer')

  dms_pls = load_playlists('dms')
  reddit_pls = load_playlists('reddit')
  whiterun_pls = load_playlists('whiterun')

  rtg_pls = load_playlists('roadtripgenre')
  singalong_pls = load_playlists('singalonggenre')

  pl_dicts = [barbie_pls, bh_pls, op_pls, dms_pls, reddit_pls, whiterun_pls, rtg_pls, singalong_pls]

  #generate genre occurence and write genre report for all individual playlists
  #for pl_dict in pl_dicts:
    #for pl, name in zip(pl_dict.values(), pl_dict.keys()):
        #write_report(get_genre_oc(pl), title='%s Genre Report'%(name))

  #create 1 df for each playlist type
  all_barbie = merge_playlists(barbie_pls)
  all_bh = merge_playlists(bh_pls)
  all_op = merge_playlists(op_pls)

  all_dms = merge_playlists(dms_pls)
  all_reddit = merge_playlists(reddit_pls)
  all_whiterun = merge_playlists(whiterun_pls)

  all_rtg = merge_playlists(rtg_pls)
  all_singalong = merge_playlists(singalong_pls)

  type_dicts = [all_barbie, all_bh, all_op, all_dms, all_reddit, all_whiterun, all_rtg, all_singalong]
  type_names = ['Barbie', 'Barbenheimer', 'Oppenheimer', 'DMs', 'Reddit', 'Whiterun', 'Road Trip Genre', 'Sing Along']

  #generate genre occurence and write genre report for playlist types
  for type_dict, name in zip(type_dicts, type_names):
    write_report(get_genre_oc(type_dict), title='%s Genre Report'%(name))
