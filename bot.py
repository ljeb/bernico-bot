import json
import config
from twython import Twython
from twython import TwythonStreamer

C_KEY = config.C_KEY
C_SECRET = config.C_SECRET
A_TOKEN_KEY = config.A_TOKEN_KEY
A_TOKEN_SECRET = config.A_TOKEN_SECRET


class Streamer(TwythonStreamer):
    # starts when @nicolette_sara sends tweet
    def on_success(self, tweet):
        print("found tweet")
        if 'text' in tweet.keys() \
            and "retweeted_status" not in tweet.keys() \
                and not tweet["in_reply_to_status_id"] \
                and tweet["user"]["screen_name"] == "nicolette_sara":
            print("text:", tweet["text"])
            reply(tweet)

    def on_error(self, status_code):
        print(status_code)


def reply(tweet):
    print("starting tweet reply")
    twitter = Twython(C_KEY, C_SECRET, A_TOKEN_KEY, A_TOKEN_SECRET)
    video = open('women.mp4', 'rb')
    response = twitter.upload_video(media=video, media_type='video/mp4')
    twitter.update_status(status='@nicolette_sara',
                          in_reply_to_status_id=tweet["id"],
                          media_ids=[response['media_id']])
    print("finished tweet reply")


def stream():
    stream = Streamer(C_KEY, C_SECRET, A_TOKEN_KEY, A_TOKEN_SECRET)
    stream.statuses.filter(follow=["780603996964651009"])


stream()
