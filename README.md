# DUIs Are Expensive: An App Using the Uber API

This is a simple Python/Flask app that uses the Uber API to request the estimates of Uber services according to a user's starting and ending addresses. The app also calculates a user's blood alcohol content (BAC), and suggests the user call an Uber if their BAC is over the legal limit. If the user says an Uber is too epensive, the app compares the estimates to the average price of a DUI.

https://github.com/liz-acosta/uber-api-app/blob/master/duis-are-expensive.gif

# How To Use This App

1. Navigate over to https://developer.uber.com/, and sign up for an Uber developer account.
2. Register a new Uber application and make your Redirect URI `http://localhost:8000/submit` - ensure that both the `profile` and `history` OAuth scopes are checked.
3. You will have to create your own yaml file with your client id and secret as environmental variables. You will also have to add a secret key for the app session. See [the yaml example](https://github.com/liz-acosta/uber-api-app/blob/master/ENV.yaml.example).
4. Run `pip install -r requirements.txt` to install dependencies
5. Run `python app.py`
6. Navigate to http://localhost:8000 in your browser

# Challenges And Future Builds

Attempted deployment, still working out bugs. I think I probably have my environment variables set up incorrectly.

Eventually, the app will be able to request an Uber for the user.

