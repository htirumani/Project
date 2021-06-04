"""
Fetches data off of Fitbit account, adapted from:
https://towardsdatascience.com/using-the-fitbit-web-api-with-python-f29f119621ea

Using an unofficial api from:
https://github.com/orcasgit/python-fitbit
"""

from datetime import datetime
import gather_keys_oauth2 as Oauth2
import fitbit
import json
import os

# define client id and secret
CLIENT_ID = ''
CLIENT_SECRET = ''

# write file method
def write_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

# authorize API calls
server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID,CLIENT_SECRET,oauth2=True,access_token=ACCESS_TOKEN,refresh_token=REFRESH_TOKEN)

day = datetime.today().strftime('%Y-%m-%d')

# get data from API calls
data_body = auth2_client.body(day)
data_act = auth2_client.activities(day)
data_sleep = auth2_client.sleep(day)
data_heart = auth2_client.intraday_time_series('activities/heart', day)

# save data to external JSON files
new_dir = os.getcwd() + '/output/' + day
os.mkdir(new_dir)
write_json(data_body, new_dir+'/body.json')
write_json(data_act, new_dir+'/activities.json')
write_json(data_sleep, new_dir+'/sleep.json')
write_json(data_heart, new_dir+'/heart.json')
