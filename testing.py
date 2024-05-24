import requests

base_url = "http://127.0.0.1:11434/api"


def getUrl(path):
    return "{}/{}".format(base_url, path)
