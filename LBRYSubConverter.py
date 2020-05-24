from bs4 import BeautifulSoup
import requests
import os
import json

if os.name == 'nt':
    fileToOpen = 'subscription_manager.xml'
else:
    fileToOpen = 'subscription_manager'
saveFileName = 'LBRY_Subscriptions.txt'
if os.path.exists(saveFileName):
    append_write = 'a'
else:
    append_write = 'w'
writeLbrySubs = open(saveFileName,append_write)
with open(fileToOpen) as f:
    data = f.read()

soup = BeautifulSoup(data, "lxml")

ids = []
for node in soup.find_all('outline'):
    url = node.get('xmlurl')
    if url:
        _, channel_id = url.split('=')
        ids.append(channel_id)

newids = ','.join(ids)
print(newids)
resp = requests.get("https://api.lbry.com/yt/resolve?channel_ids={"+newids+"}")
#url= f'https://api.lbry.com/yt/resolve?channel_ids={'+newids+'}'
#x = requests.get(url)
print(resp.text)
parsed_json = json.loads(resp.text)
datas = parsed_json["data"]
channels = datas["channels"]
print ("channels %s" % json.dumps(channels))
for tempchannels in channels:
    if not channels[tempchannels] is None :
        print ("lbry://%s" % channels[tempchannels])
        writeLbrySubs.write("lbry://"+channels[tempchannels] + '\n')
writeLbrySubs.close()
count = 0
with open(saveFileName, 'r') as f:
    for line in f:
        count += 1
print ("Total number of YouTube channels are availible on LBRY: %s" % count)