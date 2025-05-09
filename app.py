from flask import Flask, request, jsonify, render_template_string
import requests
import os
import pickle

class AccessUri:
    HOST = 'https://vpn.techbluff.duckdns.org/vpn'
    PORT = 80

class AuthUri(AccessUri):
    LOGIN = AccessUri.HOST + '/login'

class PanelUri(AccessUri):
    API = '/api'
    PANEL = '/panel'
    INBOUNDS_LIST = AccessUri.HOST + PANEL + API + '/inbounds/list'
    INBOUND_DETAIL = AccessUri.HOST + PANEL + API + '/inbounds/get/'
    ADD_CLIENT = AccessUri.HOST + PANEL + API + '/inbound/addClient'

class Authentication:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookies = None

    def login(self):
        payload = {'username': self.username, 'password': self.password}
        response = requests.post(url=AuthUri.LOGIN, data=payload)
        response.raise_for_status()
        if response.status_code == 200:
            data = response.json()
            if data.get('success', False):
                self.cookies = response.cookies
            else:
                raise Exception("Login failed")

    def get_inbounds(self):
        if not self.cookies:
            self.login()
        response = requests.get(url=PanelUri.INBOUNDS_LIST, cookies=self.cookies)
        response.raise_for_status()
        data = response.json()
        return data.get('obj', []) if data.get('success') else []

    def get_inbound_detail(self, inbound_id):
        if not self.cookies:
            self.login()
        response = requests.get(url=f"{PanelUri.INBOUND_DETAIL}{inbound_id}", cookies=self.cookies)
        response.raise_for_status()
        data = response.json()
        return data.get('obj', {}) if data.get('success') else {}

    def add_client(self, inbound_id, username):
        if not self.cookies:
            self.login()
        payload = {
            "id": inbound_id,
            "settings": {
                "clients": [{"id": "", "alterId": 0, "email": username}]
            },
            "expire": 30 * 24 * 3600
        }
        response = requests.post(url=PanelUri.ADD_CLIENT, cookies=self.cookies, json=payload)
        response.raise_for_status()
        return response.json()

app = Flask(__name__)
auth = Authentication(username='bdcloud', password='bdcloud')

@app.route('/')
def index():
    inbounds = auth.get_inbounds()
    return render_template_string('''
        <h1>Inbound List</h1>
        <ul>
        {% for inbound in inbounds %}
            <li>{{ inbound['remark'] }} (ID: {{ inbound['id'] }}) - <a href="/inbound/{{ inbound['id'] }}">View Clients</a></li>
        {% endfor %}
        </ul>
        <h2>Add Client</h2>
        <form method="post" action="/add-client">
            Inbound ID: <input name="inbound_id"><br>
            Username: <input name="username"><br>
            <input type="submit" value="Add Client">
        </form>
    ''', inbounds=inbounds)

@app.route('/inbound/<int:inbound_id>')
def view_clients(inbound_id):
    try:
        inbound = auth.get_inbound_detail(inbound_id)
        clients = inbound.get('settings', {}).get('clients', [])
        return render_template_string('''
            <h1>Clients for Inbound {{ inbound_id }}</h1>
            {% if clients %}
                <ul>
                {% for client in clients %}
                    <li>Username: {{ client['email'] }} | ID: {{ client['id'] }}</li>
                {% endfor %}
                </ul>
            {% else %}
                <p>No clients found.</p>
            {% endif %}
            <a href="/">Back to Inbounds</a>
        ''', inbound_id=inbound_id, clients=clients)
    except Exception as e:
        return f"⚠ Error: {str(e)} <a href='/'>Back</a>"

@app.route('/add-client', methods=['POST'])
def add_client():
    inbound_id = request.form['inbound_id']
    username = request.form['username']
    try:
        result = auth.add_client(int(inbound_id), username)
        if result.get('success'):
            return f"✅ Client {username} added successfully! <a href='/inbound/{inbound_id}'>View Clients</a>"
        else:
            return f"❌ Failed to add client: {result.get('msg')} <a href='/'>Back</a>"
    except Exception as e:
        return f"⚠ Error: {str(e)} <a href='/'>Back</a>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
