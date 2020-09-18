import tweepy
import json
import config

from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
from twython import Twython

C_KEY = config.C_KEY
C_SECRET = config.C_SECRET
A_TOKEN_KEY = config.A_TOKEN_KEY
A_TOKEN_SECRET = config.A_TOKEN_SECRET

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN_KEY, A_TOKEN_SECRET)
twitter = Twython(C_KEY, C_SECRET, A_TOKEN_KEY, A_TOKEN_SECRET)


class MyListener(StreamListener):

    def __init__(self):
        super(MyListener, self).__init__()

    def on_data(self, data):
        tweet = json.loads(data)
        print("found tweet")
        if 'text' in tweet.keys() \
            and "retweeted_status" not in tweet.keys() \
                and not tweet["in_reply_to_status_id"] \
                and tweet["user"]["screen_name"] == "bernicobot":
            print("text:", tweet["text"])
            reply(tweet)

    def on_error(self, status):
        print(status)


def reply(tweet):
    print("replying to tweet")
    video = open('women.mp4', 'rb')
    response = twitter.upload_video(media=video, media_type='video/mp4')
    twitter.update_status(status='@bernicobot',
                          in_reply_to_status_id=tweet["id"],
                          media_ids=[response['media_id']])
    print("done replying to tweet")


def stream():
    myStream = Stream(auth, MyListener())
    myStream.filter(follow=["1306981968618422274"])
    # myStream.filter(follow=["780603996964651009"])


stream()
