__author__ = 'adam hajari'

import cherrypy
import requests
import json
import sys

from playlist_generator import PlaylistGenerator
from playlist_generator import get_auth_url
from playlist_generator import format_status
import config
import html

scope = 'playlist-modify-public'
client_id = config.SPOTIPY_CLIENT_ID
client_secret = config.SPOTIPY_CLIENT_SECRET

class PlaylistGeneratorApp(object):
    def __init__(self,port,url):
        self.redirect_uri="{}:{}/authenticate".format(url, port)

    @cherrypy.expose
    def index(self):
        auth_url = get_auth_url(client_id, self.redirect_uri, scope)
        reauth_url = get_auth_url(client_id, self.redirect_uri, scope, show_dialog=True)
        if 'pg' not in cherrypy.session:
            raise cherrypy.HTTPRedirect(auth_url)
        return html.get_index( reauth_url )

    @cherrypy.expose
    def authenticate(self, **args):
        code = args['code']
        url = "https://accounts.spotify.com/api/token"
        data = {"grant_type":"authorization_code",
                "code":code,
                "redirect_uri":self.redirect_uri,
                "client_id":client_id,
                "client_secret":client_secret}
        r = requests.post(url, data)
        response = json.loads(r.text)
        print response
        token = response['access_token']
        cherrypy.session['pg'] = PlaylistGenerator(token)
        raise cherrypy.HTTPRedirect("/")

    @cherrypy.expose
    def generate_playlist(self, **args):
        playlistname = args['name']
        songs = args['songs']
        pg = cherrypy.session['pg']
        tracks = pg.convert_string_to_list_of_tracks(songs)
        track_ids = [track['id'] for track in tracks['tracks']]
        playlist = pg.create_playlist(playlistname, track_ids, public=True, overwrite=True)
        url = playlist['external_urls']['spotify']
        html_str = html.get_playlist_generated(url, playlistname, format_status(tracks['status']))
        return html_str


if __name__ == '__main__':
    args = sys.argv[1:]
    conf = {'/': {'tools.sessions.on': True}}
    port = 8080
    url = "http://127.0.0.1"
    if len(args)>=1:
        port = int(args[0])
        cherrypy.server.socket_port = port
    if len(args)==2:
        url = "http://dc1dsci001.tnbsound.com"
        cherrypy.server.socket_host = args[1]
    cherrypy.quickstart(PlaylistGeneratorApp(port, url), '/', conf)
