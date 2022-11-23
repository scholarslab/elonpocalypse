import json
from collections import OrderedDict
from operator import itemgetter


def isTopLevel(tweet):
   if "referenced_tweets" in tweet:
      for ref in tweet["referenced_tweets"]:
         if ref["type"] == "replied_to":
            return False
   return True

def isTopLevelNotRT(tweet):
   if "referenced_tweets" in tweet:
      for ref in tweet["referenced_tweets"]:
         if ref["type"] == "replied_to" or ref["type"] == "retweet":
            return False
   return True

tweets = []
ratio = {}
liked = {}
with open("molly/tweets.jsonl","r") as infile:
   for line in infile:
      tweets.extend(json.loads(line)["data"])

for tweet in tweets:
   if tweet["public_metrics"]["like_count"]>10 and isTopLevelNotRT(tweet):
      ratio[tweet["id"]] = (tweet["public_metrics"]["reply_count"]+tweet["public_metrics"]["quote_count"])/(tweet["public_metrics"]["retweet_count"]+tweet["public_metrics"]["like_count"]+1)
      liked[tweet["id"]] = tweet["public_metrics"]["retweet_count"]+tweet["public_metrics"]["like_count"]
   # if tweet["id"] == tweet["conversation_id"] and "referenced_tweets" not in tweet.keys():

ratio = OrderedDict(sorted(ratio.items(), key = itemgetter(1), reverse = True))
liked = OrderedDict(sorted(liked.items(), key = itemgetter(1), reverse = True))


print("Top Likes:")
for l in list(liked.items())[:10]:
   print(l[1],"https://twitter.com/socialistdogmom/status/"+l[0])

print("\nTop Ratios:")
for r in list(ratio.items())[:10]:
   print(r[1],"https://twitter.com/socialistdogmom/status/"+r[0])