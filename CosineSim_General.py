import pandas as pd
import math
import os

def load_playlists(subpath):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  pl_list = []

  print('Loading Playlists In %s'%(os.path.join(dir_path, 'playlists', subpath)))

  for (root, dirs, file) in os.walk(os.path.join(dir_path, 'playlists', subpath)):
    for f in file:
      if '.csv' in f:
        pl_name = os.path.splitext(f)[0]
        try:
          pl_list.append(pd.read_csv(os.path.join(dir_path, 'playlists', subpath, f)))
        except:
          
          print('Failed to parse %s...  Skipping'%(pl_name))
          
        finally:
          
          print('\t%s'%(pl_name))

  return pl_list

def cosine_sim(a, b):
    dot = (a * b).sum()
    mag_a = math.sqrt((a * a).sum())
    mag_b = math.sqrt((b * b).sum())
    return dot / (mag_a * mag_b)

def cosine_sim_report(pl_list, title):
    report_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'reports', 'cosine reports', '%s.csv'%(title))
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('Playlist A, Playlist B, Feature, Cosine Similarity\n')

        columns = ['Duration (ms)', 'Popularity', 'Danceability', 'Energy', 'Key', 'Loudness', 'Mode', 'Speechiness', 'Acousticness', 
            'Instrumentalness', 'Liveness', 'Valence', 'Tempo', 'Time Signature']
        
        for column in columns:
            for i in range(0, len(pl_list) - 1):
                for j in range(i + 1, len(pl_list)):
                    sim = cosine_sim(pl_list[i][column], pl_list[j][column])
                    f.write('%s,%s,%s,%.2f\n'%(i, j, column, sim))

if __name__ == '__main__':

  barbenheimer = load_playlists('barbenheimer')
  barbie = load_playlists('barbie')
  oppenheimer = load_playlists('oppenheimer')

  dms = load_playlists('dms')
  reddit = load_playlists('reddit')
  whiterun = load_playlists('whiterun')

  rtg = load_playlists('roadtripgenre')
  singalong = load_playlists('singalong')

  pl_lists = [barbenheimer, barbie, oppenheimer, dms, reddit, whiterun, rtg, singalong]
  names = ['Barbenheimer', 'Barbie', 'Oppenheimer', 'DMs', 'Reddit', 'Whiterun', 'Road Trip Genre', 'Sing Along']

  for pl_list, name in zip(pl_lists, names): 
    cosine_sim_report(pl_list, '%s Cosine Similarity Report'%(name))
    print('%s Cosine Similarity Report'%(name))