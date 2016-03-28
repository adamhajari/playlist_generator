__author__ = 'ahajari'

def get_index( auth_url):
    index_html = """
    <html>
        <head><title>automatic playlist generator</title></head>
        <body>
            <form action="generate_playlist" method="post">
              <fieldset>
                playlist name:<br>
                <input type="text" name="name" value="auto:" ><br>
                songs:<br>
                <textarea cols="80" rows="15" name="songs"></textarea><br>
                <input type="submit" value="Generate Playlist">
              </fieldset>
            </form>
            <a href='{}'><button>Switch Users</button></a>
        </body>
    </html>
    """.format(auth_url)
    return index_html

def get_playlist_generated(url, playlistname,formated_status):
    js = """<script  type="text/javascript">
                     window.open('{}','_blank');
                </script>""".format(url)
    html_str = """<html>
                    <head><title>playlist</title></head>
                    <body>
                        <h3><a href='{}' target='_blank'>{}</a></h3>{}
                        <br><a href='/'>make another</a>
                    </body>
                    {}
                </html>
                """.format(url, playlistname, formated_status, js)
    return html_str
