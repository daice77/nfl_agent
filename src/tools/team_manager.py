import requests

class TeamManager:
    def __init__(self, api_key, username, password):
        self.api_key = api_key
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.base_url = 'https://api.cbssports.com/fantasy'

        self.authenticate()

    def authenticate(self):
        # Authenticate with CBS Sports API
        auth_url = f'{self.base_url}/login'
        payload = {
            'userid': self.username,
            'password': self.password,
            'api_token': self.api_key
        }
        response = self.session.post(auth_url, data=payload)
        if response.status_code != 200:
            raise Exception("Authentication failed with CBS Sports API.")

    def manage_team(self, action, **kwargs):
        if action == 'get_roster':
            return self.get_roster()
        elif action == 'update_roster':
            return self.update_roster(kwargs.get('player_id'), kwargs.get('action_type'))
        else:
            return "Invalid team management action."

    def get_roster(self):
        roster_url = f'{self.base_url}/roster'
        response = self.session.get(roster_url)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error fetching roster: {response.status_code}"

    def update_roster(self, player_id, action_type):
        update_url = f'{self.base_url}/roster/update'
        payload = {
            'player_id': player_id,
            'action_type': action_type
        }
        response = self.session.post(update_url, data=payload)
        if response.status_code == 200:
            return "Roster updated successfully."
        else:
            return f"Error updating roster: {response.status_code}"