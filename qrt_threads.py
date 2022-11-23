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

if not os.path.exists(DIRECTORY+"/qrt/"):
    os.makedirs(DIRECTORY+"/qrt/")

for file in files:
    qrt_thread_id_path = DIRECTORY+"/qrt/"+file.split("/")[-1][:-6]+"_qrt_thread_ids.txt"
    qrt_reply_id_path = DIRECTORY+"/qrt/"+file.split("/")[-1][:-6]+"_reply_thread_ids.txt"
    tweets = []
    with open(file,"r") as infile:
        for line in infile:
            tweets.extend(json.loads(line)["data"])

    threads = []
    replies = []
    for tweet in tweets:
        if is_top_level_not_rt(tweet):
            threads.append(tweet["id"])
        elif not is_top_level(tweet):
            replies.append(tweet["id"])

    print(qrt_thread_id_path,len(threads))
    outfile = open(qrt_thread_id_path,"w")
    for i in threads:
        outfile.write("quotes_of_tweet_id:"+i+"\n")
    outfile.close()
    print(qrt_reply_id_path,len(replies))
    outfile = open(qrt_reply_id_path,"w")
    for i in replies:
        outfile.write("quotes_of_tweet_id:"+i+"\n")
    outfile.close()
