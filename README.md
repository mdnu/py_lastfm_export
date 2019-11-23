## py_lastfm_export

This script extracts scrobbling data from a last.fm user using the user's API key/secret, and creates an SQLite database file of the scrobbling data.

#### How to use:

1. Retrieve your API key/secret from https://www.last.fm/api/authentication, and store this info, along with your username, in "lastfm_info.py"
2. Run "lastfm.py". Running this script requires the 'dataset' package, which you can install using:
```
pip install dataset
```
This script will run through the pages of your last.fm listening history, displaying sequentially the pages that have been extracted, and will output a completion message when done. You can find the database file in your project directory called "lastfm.sqlite".
