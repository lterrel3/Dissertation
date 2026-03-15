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

#merges a list of playlist dictionaries
#returns a dict with all playlists
def merge_dicts(dicts):

  dict_all = {}

  for dict_pl in dicts:
    for key in dict_pl.keys():
      dict_all[key] = dict_pl[key]

  return dict_all

#merges all playlists in a dict into a single dataframe
def merge_playlists(dict_pl):
  return pd.concat(list(dict_pl.values()), ignore_index=True)

#input dictionary of all playlists
#make a csv file containing the frequency of each artist in playlist type
#frequency = # of times artist occurs/total # of unique artists
def artist_freq_report(playlist, title='report', pl_num=1):
  report_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'reports', 'artist reports', '%s.csv'%(title))

  try:
    with open(report_path, 'w', encoding='utf-8') as f:
      f.write('artists,occurrence,freqency\n')

      for artist in playlist['Artist Name(s)'].unique():
        artist_oc = len(playlist[playlist['Artist Name(s)'] == artist])
        f.write('\"%s\",%d,%f\n'%(artist, artist_oc, artist_oc / pl_num))

  except ValueError as e:
    print(e)
    print('Failed to write report to %s'%(report_path))

  finally:
    print('Frequency report for %s written to: %s'%(title, report_path))

#compares two playlists and counts the common and unique artists between them
#returns a tuple of (unique artists, common artists)
def artist_comp_playlists(pl_a, pl_b):
  common = 0

  total_tracks = len(pl_a['Artist Name(s)'].unique()) + len(pl_b['Artist Name(s)'].unique())
  for artist in pl_a['Artist Name(s)'].unique():
    if artist in pl_b['Artist Name(s)'].unique():
      common += 1

  return (total_tracks - (2 * common), common)

#input dictionary of playlists
#loop over each combination of playlists and runs artist_comp_playlists
#return csv with similarity report between all playlists
def artist_similarity_report(dict_pl, title='report'):
  pl_names = list(dict_pl.keys())
  report_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'reports', 'artist reports', '%s.csv'%(title))

  try:
    #encoding utf-8 necessary for pls with emojis in the title
    with open(report_path, 'w', encoding='utf-8') as f:
      f.write('playlist a,playlist b,common artists, unique artists\n')

      for i in range(0, len(pl_names) - 1):
        for j in range(i + 1, len(pl_names)):
          (unique, common) = artist_comp_playlists(dict_pl[pl_names[i]], dict_pl[pl_names[j]])
          f.write('\"%s\",\"%s\",%d,%d\n'%(pl_names[i], pl_names[j], common, unique))

  except ValueError as e:
    print(e)
    print('Failed to write report to %s'%(report_path))

  finally:
    print('Similarity report for %s written to: %s'%(title, report_path))

#input dictionary of all playlists
#make a csv file containing the frequency of each track in playlist type
#frequency = # of times track occurs/total # of tracks
def track_freq_report(playlist, title='report', pl_num=1):
  report_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'reports', 'track reports', '%s.csv'%(title))

  try:
    with open(report_path, 'w', encoding='utf-8') as f:
      f.write('tracks,occurrence,freqency\n')

      for track in playlist['Track Name'].unique():
        track_oc = len(playlist[playlist['Track Name'] == track])
        f.write('\"%s\",%d,%f\n'%(track, track_oc, track_oc / pl_num))

  except ValueError as e:
    print(e)
    print('Failed to write report to %s'%(report_path))

  finally:
    print('Frequency report for %s written to: %s'%(title, report_path))

#compares two playlists and counts the common and unique tracks between them
#returns a tuple of (unique tracks, common tracks)
def track_comp_playlists(pl_a, pl_b):
  common = 0

  total_tracks = len(pl_a['Track Name'].unique()) + len(pl_b['Track Name'].unique())
  for track in pl_a['Track Name'].unique():
    if track in pl_b['Track Name'].unique():
      common += 1

  return (total_tracks - (2 * common), common)

#input dictionary of playlists
#loop over each combination of playlists and runs track_comp_playlists
#return csv with similarity report between all playlists
def track_similarity_report(dict_pl, title='report'):
  pl_names = list(dict_pl.keys())
  report_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'reports', 'track reports', '%s.csv'%(title))

  try:
    #encoding utf-8 necessary for pls with emojis in the title
    with open(report_path, 'w', encoding='utf-8') as f:
      f.write('playlist a,playlist b,common tracks, unique tracks\n')

      for i in range(0, len(pl_names) - 1):
        for j in range(i + 1, len(pl_names)):
          (unique, common) = track_comp_playlists(dict_pl[pl_names[i]], dict_pl[pl_names[j]])
          f.write('\"%s\",\"%s\",%d,%d\n'%(pl_names[i], pl_names[j], common, unique))

  except ValueError as e:
    print(e)
    print('Failed to write report to %s'%(report_path))

  finally:
    print('Similarity report for %s written to: %s'%(title, report_path))

if __name__ == '__main__':
    
    #load playlists into dicts
    barbenheimer = load_playlists('barbenheimer')
    barbie = load_playlists('barbie')
    oppenheimer = load_playlists('oppenheimer')
    dms = load_playlists('dms')
    reddit = load_playlists('reddit')
    whiterun = load_playlists('whiterun')
    rtg = load_playlists('roadtripgenre')
    singalong = load_playlists('singalonggenre')
    
    #create a dictionary of playlists separated into different entries from a subpath
    dict_barb = merge_dicts([barbie, barbenheimer, oppenheimer])
    dict_dnd = merge_dicts([dms, reddit, whiterun])
    dict_rts = merge_dicts([singalong, rtg])
    dict_all = merge_dicts([barbenheimer, barbie, oppenheimer, dms, reddit, whiterun, rtg, singalong])

    #generate artist similarity report
    artist_similarity_report(barbenheimer, title='Barbenheimer Artist Sim')
    artist_similarity_report(barbie, title='Barbie Artist Sim')
    artist_similarity_report(oppenheimer, title='Oppenheimer Artist Sim')
    artist_similarity_report(dms, title='DMs Artist Sim')
    artist_similarity_report(reddit, title='Reddit Artist Sim')
    artist_similarity_report(whiterun, title='Whiterun Artist Sim')
    artist_similarity_report(rtg, title='Roadtrip Genre Artist Sim')
    artist_similarity_report(singalong, title='Singalong Artist Sim')

    artist_similarity_report(dict_barb, title='Case Study #1 Artist Sim')
    artist_similarity_report(dict_dnd, title='Case Study #2 Artist Sim')
    artist_similarity_report(dict_rts, title='Case Study #3 Artist Sim')

    artist_similarity_report(dict_all, title='All Playlists Artist Sim')

    #generate track similarity report
    track_similarity_report(barbenheimer, title='Barbenheimer Track Sim')
    track_similarity_report(barbie, title='Barbie Track Sim')
    track_similarity_report(oppenheimer, title='Oppenheimer Track Sim')
    track_similarity_report(dms, title='DMs Track Sim')
    track_similarity_report(reddit, title='Reddit Track Sim')
    track_similarity_report(whiterun, title='Whiterun Track Sim')
    track_similarity_report(rtg, title='Roadtrip Genre Track Sim')
    track_similarity_report(singalong, title='Singalong Track Sim')

    track_similarity_report(dict_barb, title='Case Study #1 Track Sim')
    track_similarity_report(dict_dnd, title='Case Study #2 Track Sim')
    track_similarity_report(dict_rts, title='Case Study #3 Track Sim')

    track_similarity_report(dict_all, title='All Playlists Track Sim')
    
    #create one dictionary of all playlists from a subpath
    barb_pls = merge_playlists(barbenheimer)
    barbie_pls = merge_playlists(barbie)
    op_pls = merge_playlists(oppenheimer)
    dm_pls = merge_playlists(dms)
    reddit_pls = merge_playlists(reddit)
    whiterun_pls = merge_playlists(whiterun)
    rtg_pls = merge_playlists(rtg)
    singalong_pls = merge_playlists(singalong)

    all_barb = merge_playlists(dict_barb)
    all_dnd = merge_playlists(dict_dnd)
    all_rts = merge_playlists(dict_rts)

    all_pls = merge_playlists(dict_all)

    #generate artist frequence report
    artist_freq_report(barb_pls, title='Barbenheimer Artist Freq', pl_num=len(barbenheimer.keys()))
    artist_freq_report(barbie_pls, title='Barbie Artist Freq', pl_num=len(barbie.keys()))
    artist_freq_report(op_pls, title='Oppenheimer Artist Freq', pl_num=len(oppenheimer.keys()))
    artist_freq_report(dm_pls, title='DMs Artist Freq', pl_num=len(dms.keys()))
    artist_freq_report(reddit_pls, title='Reddit Artist Freq', pl_num=len(reddit.keys()))
    artist_freq_report(whiterun_pls, title='Whiterun Artist Freq', pl_num=len(whiterun.keys()))
    artist_freq_report(rtg_pls, title='Roadtrip Genre Artist Freq', pl_num=len(rtg.keys()))
    artist_freq_report(singalong_pls, title='Singalong Artist Freq', pl_num=len(singalong.keys()))

    artist_freq_report(all_barb, title='Case Study #1 Artist Freq', pl_num=len(dict_barb.keys()))
    artist_freq_report(all_dnd, title='Case Study #2 Artist Freq', pl_num=len(dict_dnd.keys()))
    artist_freq_report(all_rts, title='Case Study #3 Artist Freq', pl_num=len(dict_rts.keys()))

    artist_freq_report(all_pls, title='All Pls Artist Freq', pl_num=len(dict_all.keys()))

    #generate track frequency report
    track_freq_report(barb_pls, title='Barbenheimer Track Freq', pl_num=len(barbenheimer.keys()))
    track_freq_report(barbie_pls, title='Barbie Track Freq', pl_num=len(barbie.keys()))
    track_freq_report(op_pls, title='Oppenheimer Track Freq', pl_num=len(oppenheimer.keys()))
    track_freq_report(dm_pls, title='DMs Track Freq', pl_num=len(dms.keys()))
    track_freq_report(reddit_pls, title='Reddit Track Freq', pl_num=len(reddit.keys()))
    track_freq_report(whiterun_pls, title='Whiterun Track Freq', pl_num=len(whiterun.keys()))
    track_freq_report(rtg_pls, title='Roadtrip Genre Track Freq', pl_num=len(rtg.keys()))
    track_freq_report(singalong_pls, title='Singalong Track Freq', pl_num=len(singalong.keys()))

    track_freq_report(all_barb, title='Case Study #1 Track Freq', pl_num=len(dict_barb.keys()))
    track_freq_report(all_dnd, title='Case Study #2 Track Freq', pl_num=len(dict_dnd.keys()))
    track_freq_report(all_rts, title='Case Study #3 Track Freq', pl_num=len(dict_rts.keys()))

    track_freq_report(all_pls, title='All Pls Track Freq', pl_num=len(dict_all.keys()))