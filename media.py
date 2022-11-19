import json
import requests
import time
import sys
from os.path import exists

TARGET = "uva/scholars_lab"
if len(sys.argv)>1:
    TARGET = sys.argv[1]

media = {}
with open(TARGET+".jsonl","r") as infile:
   for line in infile:
      tweets = json.loads(line)
      if "includes" in tweets and "media" in tweets["includes"]:
         media_list = tweets["includes"]["media"]
         for m in media_list:
            if m["type"] == "photo":
               media[m["media_key"]] = m["url"]
with open(TARGET+"_media.json","w") as outfile:
   outfile.write(json.dumps(media))

count = 1
start = time.perf_counter()
for m in media:
   print(str(count)+"/"+str(len(media))+" ("+str(int(time.perf_counter()-start))+"s) "+media[m])
   if not exists(TARGET+"_media/"+media[m].split('/')[-1]):
      url = media[m]
      filename = TARGET+"_media/"+media[m].split('/')[-1]
      r = requests.get(url, allow_redirects=True)
      open(filename, 'wb').write(r.content)
      time.sleep(3)
   count+=1