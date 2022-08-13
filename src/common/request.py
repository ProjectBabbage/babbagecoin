"""
This is a wrapper of the requests package.
The idea is to send the data to redis instead of doing a http request,
depending on the configuration (config.py).
"""
import requests
import redis
from config import Config

conf = Config()


class RedisRequest:
    def __init__(self):
        self.redis = redis.Redis(host="localhost", port=6379, db=0)
        self.pubsub = self.redis.pubsub()
        self.pubsub.psubscribe(f"{conf.myIp}*")

    def get(self, url, *args, **kwargs):

        print("IN get")
        print(args[0])
        pass

    def post(self, url: str, payload: str, *args, **kwargs):
        self.redis.publish(url, payload)


node_request = RedisRequest() if conf.redis_pub_sub else requests


if __name__ == "__main__":
    print("REDIS" if isinstance(node_request, RedisRequest) else "requests")
    node_request.get("https://google.fr")
