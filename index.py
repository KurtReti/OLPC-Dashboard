import os
from dash.dependencies import Input, Output
from flask import send_from_directory
from app import app
from apps.layouts import landing, app as web_app
from apps.layouts.index import layout as index_layout
# import all callbacks so they are registered by dash
import apps.callbacks

app.layout = index_layout
server = app.server


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if '/app' in pathname:
        view = web_app.layout
    elif pathname == "/":
        view = landing.layout

    return view


@server.route('/assets/<string:name>')
def static_file(name):
    """
    Override the ability to server files to add a max_age to the response.
    This is needed for switching of stylesheets to work better so the sheet is loaded from cache
    :param name: string
    :return: Flask Response
    """
    static_folder = os.path.join(os.getcwd(), 'assets')
    return send_from_directory(static_folder, name, max_age=1000)


if __name__ == '__main__':
    app.run_server(debug=os.environ.get("DEBUG", False))
