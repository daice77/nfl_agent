import re

import requests


class CbsFantasySportsApiTokenFetcher:
    TOKEN_REGEX = r'(?<=var token = ").+(?=")'
    URL = "https://www.cbssports.com/login"
    # VERSION = "0.1.0"

    def __init__(self, league_name, password, user_id):
        self.league_name = league_name
        self.password = password
        self.user_id = user_id

    def fetch(self):
        page_content = self.page()
        print(f"Page content received: {page_content}")

        token_match = re.search(self.TOKEN_REGEX, page_content)
        if token_match:
            token = token_match.group(0)
            print(f"Token found: {token}")
            return token
        else:
            print("No token found in the page content.")
            return None

    def page(self):
        response = requests.post(
            self.URL,
            data={
                "userid": self.user_id,
                "password": self.password,
                "xurl": self.xurl(),
            },
        )
        return response.text

    def xurl(self):
        return f"https://{self.league_name}.cbssports.com/"


# Example usage:
fetcher = CbsFantasySportsApiTokenFetcher(
    league_name="internationalfantasyfootballleag.football",
    password="Mi7cbssport!",
    user_id="olaf.kupschina@gmail.com",
)
token = fetcher.fetch()
