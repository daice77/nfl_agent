import requests
from bs4 import BeautifulSoup

# NEW API URL: https://api.cbssports.com/fantasy/league/teams?version=3.0&league_id=640ee45d14644ba3d28a
# but missing league ID

# Create a session object
session = requests.Session()

# Define the login page URL
login_page_url = "https://www.cbssports.com/login"

# Get the login page to establish cookies and scrape hidden fields
login_page_response = session.get(login_page_url)
soup = BeautifulSoup(login_page_response.text, "html.parser")

# Find the login form
login_form = soup.find("form")

if not login_form:
    print("Login form not found on the login page.")
    exit()

# Extract the action URL from the form
action_url = login_form.get("action")
if not action_url or action_url == "":
    # If the action attribute is empty, the form submits to the current URL
    action_url = login_page_url
elif action_url.startswith("/"):
    action_url = "https://www.cbssports.com" + action_url

print(f"Action URL: {action_url}")

# Prepare the payload with hidden fields
payload = {}
for input_tag in login_form.find_all("input"):
    name = input_tag.get("name")
    value = input_tag.get("value", "")
    if name:
        payload[name] = value

# Update the payload with your email and password
# Update the payload with your email and password
payload.update(
    {
        "email": "olaf.kupschina@gmail.com",  # Replace with your email
        "password": "Mi7cbssport!",  # Replace with your password
        # 'remember': 'on',  # Include if you want to be remembered
    }
)

print(f"Payload: {payload}")

# Set headers
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/128.0.0.0 Safari/537.36",
    "Referer": login_page_url,
    "Origin": "https://www.cbssports.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# Perform the login
response = session.post(action_url, data=payload, headers=headers)

# Check if login was successful
if response.status_code == 200:
    # Look for an indication that login was successful
    if "Logout" in response.text or "Sign Out" in response.text:
        print("Login successful!")

        # Now fetch the league information page
        league_url = "https://fantasy-api.cbssports.com/internationalfantasyfootballleag.football"
        league_response = session.get(league_url, headers=headers)
        soup = BeautifulSoup(league_response.text, "html.parser")

        # Extract league information (adjust selectors as needed)
        league_name_element = soup.select_one(
            ".league-name"
        )  # Adjust based on actual HTML
        if league_name_element:
            league_name = league_name_element.text.strip()
            print(f"League Name: {league_name}")
        else:
            print("League name element not found.")
    else:
        print("Login failed: Incorrect credentials or login error.")
        # Optionally, print response.text to debug
        # print(response.text)
else:
    print(f"Login failed. Status code: {response.status_code}")
    # Optionally, print response.text to debug
    # print(response.text)
