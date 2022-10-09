import os
import time
from dash import Dash
from flask import Flask
from flask_caching import Cache
import dash_bootstrap_components as dbc

server = Flask(__name__)

c_time = time.time()

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    # preload accessibility stylesheets
    {"id": "site-theme-default", "href": f"/assets/site_theme_default.css?m={c_time}", "rel": "preload", "as": "style"},
    {"id": "site-theme-dark", "href": f"/assets/site_theme_dark.css?m={c_time}", "rel": "preload", "as": "style"},
    {"id": "site-theme-colourblind", "href": f"/assets/site_theme_colourblind.css?m={c_time}", "rel": "preload",
     "as": "style"},
    {"id": "site-theme", "href": f"/assets/site_theme_default.css?m={c_time}", "rel": "stylesheet"},
    "https://fonts.googleapis.com/icon?family=Material+Icons"
]
external_scripts = [
    'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js'
]

app = Dash(__name__, server=server, suppress_callback_exceptions=True, assets_ignore=".*site\_theme.*\.css",
           external_stylesheets=external_stylesheets, external_scripts=external_scripts, title='OLPC Dashboard',
           update_title='Loading...')

app.cache = Cache(app.server, config={
    'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24,  # seconds
    'CACHE_TYPE': 'redis' if os.environ.get('REDIS_URL') else "null",
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL', '')
})
