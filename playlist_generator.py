import config
import spotipy
import re
import spotipy.util as util

class PlaylistGenerator(object):
    def __init__(self, token):
        self.sp = spotipy.Spotify(auth=token)
        self.username = self.sp.current_user()['id']

    def convert_string_to_list_of_tracks(self, songs):
        spotify_tracks = {"tracks":[], "status":[]}
        for track in songs.split("\n"):
            track = re.sub(r"\(.*\)", "", track)
            track = re.sub(r"\[.*\]", "", track)
            results = self.sp.search(q=track, limit=1)
            if len(results['tracks']['items'])>0:
                sp_track = results['tracks']['items'][0]
                spotify_tracks['tracks'].append(sp_track)
                print "{}  =>  {} - {}".format(track.encode('utf8'), sp_track['name'].encode('utf8'), sp_track['artists'][0]['name'].encode('utf8'))
                spotify_tracks['status'].append("{}  =>  {} - {}".format(track.encode('utf8'), sp_track['name'].encode('utf8'), sp_track['artists'][0]['name'].encode('utf8')))
            else:
                print "NOTICE: unable to find match for %s" % track.encode('utf8')
                spotify_tracks['status'].append("NOTICE: unable to find match for %s" % track.encode('utf8'))
        return spotify_tracks

    def get_all_playlists(self):
        offset = 0
        total = 1
        limit = 50
        playlist_all = []
        while offset < total:
            playlists = self.sp.user_playlists(self.username, limit=limit, offset=offset)
            playlist_all.extend(playlists['items'])
            offset += limit
            total = playlists['total']
        return playlist_all

    def find_playlist_by_name(self, playlistname):
        playlists = self.get_all_playlists()
        for playlist in playlists:
            if playlist['name'].lower() == playlistname:
                return playlist

    def create_playlist(self, playlistname, track_ids, public=True, overwrite=True):
        playlist = self.find_playlist_by_name(playlistname)
        if playlist is None:
            playlist = self.sp.user_playlist_create(self.username, playlistname, public=public)
        elif overwrite:
            self.clear_playlist(playlist['id'])
        self.sp.user_playlist_add_tracks(self.username, playlist['id'], track_ids)
        return playlist

    def get_all_tracks(self, playlist_id):
        offset = 0
        total = 1
        limit = 50
        tracks_all = []
        while offset < total:
            tracks = self.sp.user_playlist_tracks(self.username, playlist_id, limit=limit, offset=offset)
            track_ids = [track['track']['id'] for track in tracks['items']]
            tracks = self.sp.user_playlists(self.username, limit=limit, offset=offset)
            tracks_all.extend(track_ids)
            offset += limit
            total = tracks['total']
        return tracks_all

    def clear_playlist(self, playlist_id):
        track_ids = self.get_all_tracks(playlist_id)
        self.sp.user_playlist_remove_all_occurrences_of_tracks(self.username, playlist_id, track_ids)

def format_status(status_list):
    status = ""
    index = 1
    for s in status_list:
        if "NOTICE:" in s:
            status+="<br>{}".format(s.replace("NOTICE:","<b>NOTICE:</b>"))
        else:
            status+="<br><b>{}</b>: {}".format(index, s)
            index+=1
    return status

def get_auth_url(client_id, redirect_uri, scope, show_dialog=False):
    base_url = "https://accounts.spotify.com/authorize/"
    if show_dialog:
        params = "?client_id={}&response_type=code&redirect_uri={}&scope={}&show_dialog=true".format(client_id, redirect_uri, scope)
    else:
        params = "?client_id={}&response_type=code&redirect_uri={}&scope={}".format(client_id, redirect_uri, scope)
    auth_url = base_url+params
    return auth_url