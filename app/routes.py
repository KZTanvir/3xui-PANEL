from flask import current_app, render_template, flash, Blueprint, jsonify, request
from app.x_ui_fetch import Authentication
import json
import logging

main = Blueprint('/', __name__, template_folder='../frontend/main', static_folder='../frontend/main/assets')

# Setup a logger (optional, recommended)
logger = logging.getLogger(__name__)

def get_auth():  # without app context
    try:
        auth = Authentication(
            username=current_app.config['PANEL_USERNAME'],
            password=current_app.config['PANEL_PASSWORD']
        )
        auth.load_cookies()
        return auth
    except KeyError as e:
        logger.error(f"Missing config key: {e}")
        raise RuntimeError("Authentication configuration missing.") from e
    except Exception as e:
        logger.exception("Failed to initialize authentication.")
        raise RuntimeError("Authentication initialization failed.") from e

@main.route('/', methods=['GET', 'POST'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.exception("Error rendering index page.")
        flash('An error occurred while loading the page.', 'danger')
        return "Internal Server Error", 500

@main.route('/interface_list', methods=['GET'])
def interface_list():
    try:
        auth = get_auth()
        interfaces = auth.get_inbounds_all()

        for interface in interfaces:
            try:
                if isinstance(interface.get('settings'), str):
                    interface['settings'] = None
            except Exception as e:
                logger.warning(f"Error processing interface: {interface} - {e}")
        
        return jsonify(interfaces), 200

    except RuntimeError as e:
        logger.error(f"Runtime error: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logger.exception("Unexpected error in /interface_list")
        return jsonify({"error": "Internal server error."}), 500
