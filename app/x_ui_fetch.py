import requests
import os
import pickle
import json
import uuid
class AccessUri:
    HOST = 'https://vpn.techbluff.duckdns.org/vpn'
    PORT = 80

class AuthUri(AccessUri):
    LOGIN = AccessUri.HOST + '/login'

class PanelUri(AccessUri):
    API = '/api'
    PANEL = '/panel'
    INBOUNDS_LIST = AccessUri.HOST + PANEL + API + '/inbounds/list'
    INBOUND = AccessUri.HOST + PANEL + API + '/inbounds/get/'
    ADD_CLIENT = AccessUri.HOST + PANEL + API + '/inbounds/addClient'


class Authentication:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookies = None #login at start
        self.cookies_filename = 'panel_cookies.pkl'

    def save_cookies(self):
        if self.cookies:
            with open(self.cookies_filename, 'wb') as file:
                pickle.dump(self.cookies, file)
        else:
            print('something went wrong')

    
    def load_cookies(self):
        if os.path.exists('panel_cookies.pkl'):
            with open('panel_cookies.pkl', 'rb') as file:
                self.cookies = pickle.load(file)

    def login(self):
        '''return cookies of login and save inside the class'''
        try:
            payload = {
                'username': self.username,
                'password': self.password
            }
            response = requests.post(url=AuthUri.LOGIN, data=payload)
            response.raise_for_status()
            if response.status_code == 200:
                data = response.json()
                if data.get('success', False):
                    self.cookies = response.cookies
                    self.save_cookies()
        except Exception as e:
            print(e)
    
    def process_response(self, response):
        response = response.json()
        if response.get('success', False):
            return response.get('obj', None)
        return None

    def get_inbounds_all(self):
        try:
            response = requests.get(url=PanelUri.INBOUNDS_LIST, cookies=self.cookies)
            response = self.process_response(response=response)
            return response
        except Exception as e:
            self.login()
            print(f"error getting all inbound {e}")
    
    def get_inbound(self, inbound_id):
        try:
            response = requests.get(url=PanelUri.INBOUND + str(inbound_id), cookies=self.cookies)
            response = self.process_response(response=response)
            return response
        except Exception as e:
            print(f"errror getting inbound{e}")

    def get_client_from_inbound(self,client_id, inbound_data):
        try:
            print(inbound_data)
        except Exception as e:
            pass

    def get_client_vmess(self, client_id, inbound_id):
        inbound = self.get_inbound(inbound_id=inbound_id)
        client = self.get_client_from_inbound(client_id=client_id, inbound_data=inbound)

    def add_client(self, inbound_id, username):
        client_id = str(uuid.uuid4())
        totalGB = 214748364800
        expiryTime = -2592000000
        enable = True
        email = username
        payload = {
            'id': inbound_id,
            'settings': json.dumps({
                'clients': [{
                    'id': client_id,
                    'alterId': 0,
                    'email': email,
                    'limitIp': 0,
                    'totalGB': totalGB,
                    'expiryTime': expiryTime,
                    'enable': enable,
                    'tgId': '',
                    'subId': '',
                    'comment': "",
                    'reset': 0,
                }]
            }) #dump as json
            
        }
        print(payload)
        try:
            response = requests.post(url=PanelUri.ADD_CLIENT, data=payload, cookies=self.cookies)
            
            #response.raise_for_status()
            return response.json()
        except Exception as e:
            return None

    def get_online_clients():
        pass
if __name__ == '__main__':
    auth = Authentication(username='bdcloud', password='bdcloud')
    auth.load_cookies()
    #auth.login()
    #auth.save_cookies()
    auth.add_client(48, 'technoshop')
