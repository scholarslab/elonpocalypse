import json
import os
import requests
import time
import sys

TWEETFILE = "uva/scholars_lab.jsonl"
if len(sys.argv)>1:
    TWEETFILE = sys.argv[1]
MEDIA_PATH = "/".join(TWEETFILE.split("/")[:-1])+"/"+TWEETFILE.split("/")[-1][:-6]+"_media/"
# Create media dir if it doesn't exist
if not os.path.exists(MEDIA_PATH):
    os.makedirs(MEDIA_PATH)

media = {}
with open(TWEETFILE,"r") as infile:
   for line in infile:
      tweets = json.loads(line)
      if "includes" in tweets and "media" in tweets["includes"]:
         media_list = tweets["includes"]["media"]
         for m in media_list:
            if m["type"] == "photo":
               media[m["media_key"]] = m["url"]
with open(MEDIA_PATH+TWEETFILE.split("/")[-1][:-6]+"_media.json","w") as outfile:
   outfile.write(json.dumps(media))

count = 1
start = time.perf_counter()
for m in media:
   print(str(count)+"/"+str(len(media))+" ("+str(int(time.perf_counter()-start))+"s) "+media[m])
   if not os.path.exists(MEDIA_PATH+media[m].split('/')[-1]):
      url = media[m]
      filename = MEDIA_PATH+media[m].split('/')[-1]
      r = requests.get(url, allow_redirects=True)
      open(filename, 'wb').write(r.content)
      time.sleep(3)
   count+=1