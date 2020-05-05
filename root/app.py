import flask
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


app = flask.Flask(__name__)
@app.route('/')
def index():
    return('It works')
@app.route("/read_and_broadcast", methods=['POST', "GET"])
def read_and_broadcast():
    if flask.request.method == 'GET':
        val_array = read_array("1RPn2loVmuXCAtr161HjdX3ZfRTIHzMuTK-SXqXD0UxE", "List1!d:d")
        return val_array

def read_array(spreadsheet_id, range_):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    # The file 4.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('4.pickle'):
        with open('4.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            print(flow)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('4.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_)
    response = request.execute()
    values = response.get('values')

    if not values:
        return 'No data found.'
    else:
        otvet3 = {"content": values}
        return otvet3