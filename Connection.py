from firebase import firebase
import requests
import time

URL_DB = 'https://news-latest-24h.firebaseio.com'
DB = firebase.FirebaseApplication(URL_DB)


def save(path, category, data):
    DB.put(path, category, data)


if __name__ == '__main__':
    while (True):
        time.sleep(1)