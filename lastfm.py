import requests
import collections.abc
import dataset
from lastfm_info import *

user = AS_USER
api_key = AS_KEY
secret = AS_SECRET
api_url = AS_API
per_page = 200


def flatten(d, parent_key=''):
    ''' (dict, key) -> dict

    Flattens a nested dictionary.
    '''
    items = []
    for key, val in d.items():
        new_key = parent_key + '_' + key if parent_key else key
        if isinstance(val, collections.MutableMapping):
            items.extend(flatten(val, new_key).items())
        else:
            items.append((new_key, val))
    return dict(items)
    
    # old:
    # items = []
    # for key, val in d.items():
    #     if parent_key:
    #         new_key = parent_key + '_' + key
    #     else:
    #         key
    #     if isinstance(val, collections.MutableMapping):
    #         items.extend(flatten(val, new_key).items())
    #     else:
    #         new_key = new_key.replace('#', '')
    #         items.append((new_key, val))
    # return dict(items)

def process_track(track):
    ''' (Track) -> Track

    Processes Track data. Removes 'image' keys, and
    replaces empty strings with NoneType
    '''
    if "image" in track:
        del track["image"]
    flattened_track = flatten(track)
    for key, val in flattened_track.items():
        if val == "":
            flattened_track[key] = None
    return flattened_track

def recent_tracks(user, api_key, page, limit):
    '''
    Retrieves most recent tracks from 'user' with associated 'api_key'.
    Beginning at page 'page' and ending at 'limit'. Below we use the values
    '1' for page, and '10' for limit.
    '''
    return requests.get(api_url % (user, api_key, page, limit)).json()


def createdb():
    '''
    The main program. Creates an SQLite db with filename 'lastfm.sqlite',
    creates an empty table, then iterates over all pages, processing each
    track and inserting the processed track into the table.
    '''
    resp = recent_tracks(user, api_key, 1, 200)
    total_pages = int(resp['recenttracks']['@attr']['totalPages'])
    all_pages = []
    for page_num in range(1, total_pages + 1):
        print('P1: Page {0} of {1}'.format(page_num,total_pages))
        page = recent_tracks(user, api_key, page_num, 200)
        all_pages.append(page)

    db = dataset.connect('sqlite:///lastfm.sqlite')
    tracks = db['tracks']

    num_pages = len(all_pages)
    for page_num, page in enumerate(all_pages):
        print('P2: Page {0} of {1}'.format(page_num + 1,num_pages))
        for track in page['recenttracks']['track']:
            tracks.insert(process_track(track))

    print('Done. {0} rows in table ""tracks"'.format(len(tracks)))

if __name__ == '__main__':
    createdb()

