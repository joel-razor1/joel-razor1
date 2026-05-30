import os
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt


TOKEN = os.environ.get('GH_TOKEN')
HEADERS = {'Authorization': f'token {TOKEN}'}
USERNAME = 'joel-razor1'

def get_recent_commits():

    url = f'https://api.github.com/users/{USERNAME}/events'
    response = requests.get(url, headers=HEADERS)
    events = response.json()
    
    data = []
    for event in events:
        if event['type'] == 'PushEvent':
            date = event['created_at'][:10]
            for commit in event['payload']['commits']:
                # Fetch detailed commit info to get filenames
                c_url = f"https://api.github.com/repos/{event['repo']['name']}/commits/{commit['sha']}"
                files = requests.get(c_url, headers=HEADERS).json().get('files', [])
                for f in files:
                    ext = f['filename'].split('.')[-1]
                    data.append({'date': date, 'lang': ext})
    return pd.DataFrame(data)

df = get_recent_commits()
summary = df.groupby(['date', 'lang']).size().unstack(fill_value=0)
summary.to_json('stats.json')

summary.plot(kind='bar', stacked=True)
plt.savefig('chart.svg')