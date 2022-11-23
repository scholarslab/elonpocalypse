import json
import sys
import glob
import os


DIRECTORY = "slab"
if len(sys.argv)>1:
    DIRECTORY = sys.argv[1]

files = []
files = glob.glob(DIRECTORY+"/*.jsonl")

i = 0
while i<len(files):
    if files[i].endswith("_conversations.jsonl") or files[i].endswith("_replycontexts.jsonl") or files[i].endswith("followers.jsonl") or files[i].endswith("following.jsonl"):
        files.pop(i)
    else:
        i+=1

def is_top_level(t):
    if "referenced_tweets" in t:
        for ref in t["referenced_tweets"]:
            if ref["type"] == "replied_to":
                return False
    return True

def is_top_level_not_rt(t):
    if "referenced_tweets" in t:
        for ref in t["referenced_tweets"]:
            if ref["type"] == "replied_to" or ref["type"] == "retweet":
                return False
    return True

if not os.path.exists(DIRECTORY+"/replycontexts/"):
    os.makedirs(DIRECTORY+"/replycontexts/")

for file in files:
    thread_id_path = DIRECTORY+"/replycontexts/"+file.split("/")[-1][:-6]+"_thread_ids.txt"
    if os.path.exists(thread_id_path):
        continue
    tweets = []
    with open(file,"r") as infile:
        for line in infile:
            tweets.extend(json.loads(line)["data"])

    threads = set()
    self_threads = set()
    for tweet in tweets:
        if is_top_level(tweet):
            self_threads.add(tweet["id"])
    for tweet in tweets:
        if not is_top_level(tweet) and tweet["conversation_id"] not in self_threads:
            threads.add(tweet["conversation_id"])
    

    print(thread_id_path,len(threads))
    outfile = open(thread_id_path,"w")
    for i in threads:
        outfile.write(i+"\n")
    outfile.close()
