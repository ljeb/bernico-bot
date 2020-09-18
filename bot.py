import json
import config
from twython import Twython
from twython import TwythonStreamer
from os import environ

C_KEY = environ['C_KEY']
C_SECRET = environ['C_SECRET']
A_TOKEN_KEY = environ['A_TOKEN_KEY']
A_TOKEN_SECRET = environ['A_TOKEN_SECRET']


class Streamer(TwythonStreamer):
    # starts when @nicolette_sara sends tweet
    def on_success(self, tweet):
        print("found tweet")
        # checks that tweet is not a RT or a reply, and is in fact by @nicolette_sara
        # if it passes the checks, the reply function is called
        if 'text' in tweet.keys() \
            and "retweeted_status" not in tweet.keys() \
                and not tweet["in_reply_to_status_id"] \
                and tweet["user"]["screen_name"] == "bernicobot":
            print("text:", tweet["text"])
            reply(tweet)

    def on_error(self, status_code):
        print(status_code)


def stream():
    stream = Streamer(C_KEY, C_SECRET, A_TOKEN_KEY, A_TOKEN_SECRET)
    # streams tweets filtered by @nicolette_sara's twitter id
    stream.statuses.filter(follow=["1306981968618422274"])


def reply(tweet):
    # replies to the checked tweet with a video
    print("starting tweet reply")
    twitter = Twython(C_KEY, C_SECRET, A_TOKEN_KEY, A_TOKEN_SECRET)
    video = open('women.mp4', 'rb')
    response = twitter.upload_video(media=video, media_type='video/mp4')
    twitter.update_status(status='@bernicobot',
                          in_reply_to_status_id=tweet["id"],
                          media_ids=[response['media_id']])
    print("finished tweet reply")


stream()
