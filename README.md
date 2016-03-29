This app is (probably) running live here: http://playlistgenerator.herokuapp.com/

To run this locally, you need to 

- create an application at spotify's dev center (https://developer.spotify.com/my-applications). 

- Once you've created the above application add `http://127.0.0.1:8080/authenticate` to Redirect URIs list:

- Clone this repo

- add a `config.py` file to the directory you just cloned with the following two lines:
  ```python
  SPOTIPY_CLIENT_ID='your-spotiy-client-id'
  SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
  ```
  you'll find both 'your-spotiy-client-id' and 'your-spotify-client-secret' on the Spotify application page you just created.

- run the app.py script passing a port and host as optional params
```bash
> python app.py
```
