import unittest
from unittest.mock import Mock, patch

import requests


class TeamManager:
    def __init__(self, api_key, username, password):
        self.api_key = api_key
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.base_url = "https://api.cbssports.com/fantasy"

        self.authenticate()

    def authenticate(self):
        # Authenticate with CBS Sports API
        auth_url = f"{self.base_url}/login"
        payload = {
            "userid": self.username,
            "password": self.password,
            "api_token": self.api_key,
        }
        response = self.session.post(auth_url, data=payload)
        if response.status_code != 200:
            raise Exception("Authentication failed with CBS Sports API.")

    def manage_team(self, action, **kwargs):
        if action == "get_roster":
            return self.get_roster()
        elif action == "update_roster":
            return self.update_roster(
                kwargs.get("player_id"), kwargs.get("action_type")
            )
        else:
            return "Invalid team management action."

    def get_roster(self):
        roster_url = f"{self.base_url}/roster"
        response = self.session.get(roster_url)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error fetching roster: {response.status_code}"

    def update_roster(self, player_id, action_type):
        update_url = f"{self.base_url}/roster/update"
        payload = {"player_id": player_id, "action_type": action_type}
        response = self.session.post(update_url, data=payload)
        if response.status_code == 200:
            return "Roster updated successfully."
        else:
            return f"Error updating roster: {response.status_code}"


class TestTeamManager(unittest.TestCase):

    @patch("requests.Session.post")
    def test_authenticate_success(self, mock_post):
        # Mock a successful authentication response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        manager = TeamManager(
            api_key="fake_api_key", username="fake_user", password="fake_pass"
        )
        self.assertIsNotNone(manager.session)

    @patch("requests.Session.post")
    def test_authenticate_failure(self, mock_post):
        # Mock a failed authentication response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response

        with self.assertRaises(Exception) as context:
            TeamManager(
                api_key="fake_api_key", username="fake_user", password="fake_pass"
            )
        self.assertTrue(
            "Authentication failed with CBS Sports API." in str(context.exception)
        )

    @patch("requests.Session.get")
    @patch("requests.Session.post")
    def test_get_roster_success(self, mock_post, mock_get):
        # Mock a successful authentication response
        mock_auth_response = Mock()
        mock_auth_response.status_code = 200
        mock_post.return_value = mock_auth_response

        # Mock a successful get roster response
        mock_roster_response = Mock()
        mock_roster_response.status_code = 200
        mock_roster_response.json.return_value = {"roster": "data"}
        mock_get.return_value = mock_roster_response

        manager = TeamManager(
            api_key="fake_api_key", username="fake_user", password="fake_pass"
        )
        roster = manager.get_roster()
        self.assertEqual(roster, {"roster": "data"})

    @patch("requests.Session.get")
    @patch("requests.Session.post")
    def test_get_roster_failure(self, mock_post, mock_get):
        # Mock a successful authentication response
        mock_auth_response = Mock()
        mock_auth_response.status_code = 200
        mock_post.return_value = mock_auth_response

        # Mock a failed get roster response
        mock_roster_response = Mock()
        mock_roster_response.status_code = 404
        mock_get.return_value = mock_roster_response

        manager = TeamManager(
            api_key="fake_api_key", username="fake_user", password="fake_pass"
        )
        roster = manager.get_roster()
        self.assertEqual(roster, "Error fetching roster: 404")

    @patch("requests.Session.post")
    def test_update_roster_success(self, mock_post):
        # Mock a successful authentication response
        mock_auth_response = Mock()
        mock_auth_response.status_code = 200
        mock_post.return_value = mock_auth_response

        # Mock a successful update roster response
        mock_update_response = Mock()
        mock_update_response.status_code = 200
        mock_post.return_value = mock_update_response

        manager = TeamManager(
            api_key="fake_api_key", username="fake_user", password="fake_pass"
        )
        result = manager.update_roster(player_id="123", action_type="add")
        self.assertEqual(result, "Roster updated successfully.")

    @patch("requests.Session.post")
    def test_update_roster_failure(self, mock_post):
        # Mock a successful authentication response
        mock_auth_response = Mock()
        mock_auth_response.status_code = 200
        mock_post.return_value = mock_auth_response

        # Mock a failed update roster response
        mock_update_response = Mock()
        mock_update_response.status_code = 400
        mock_post.return_value = mock_update_response

        manager = TeamManager(
            api_key="fake_api_key", username="fake_user", password="fake_pass"
        )
        result = manager.update_roster(player_id="123", action_type="add")
        self.assertEqual(result, "Error updating roster: 400")


if __name__ == "__main__":
    unittest.main()
