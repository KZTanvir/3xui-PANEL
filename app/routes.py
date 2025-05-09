from flask import current_app, render_template, flash, Blueprint, jsonify, request
from app.x_ui_fetch import Authentication
import json
main = Blueprint('/', __name__, template_folder='../frontend/main', static_folder='../frontend/main/assets')

def get_auth(): #without app context
    auth = Authentication(
        username=current_app.config['PANEL_USERNAME'],
        password=current_app.config['PANEL_PASSWORD']
    )

    auth.load_cookies()

    return auth

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/interface_list', methods=['GET'])
def interface_list():
    auth = get_auth()
    interfaces = auth.get_inbounds_all()
    for interface in interfaces:
        if isinstance(interface.get('settings'), str):
            interface['settings'] = None

    return jsonify(interfaces), 200
    #return jsonify(interfaces), 200