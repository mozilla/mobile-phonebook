import os
import sys
import json
import urllib2
import Queue
from threading import Thread

MY_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_FILES_DIR = os.path.join(MY_DIR, 'static-files')
JSON_FEED_FILENAME = os.path.join(MY_DIR, 'people.json')
THUMBNAIL_DIR = os.path.join(STATIC_FILES_DIR, 'images', 'people')

BASE_URL = 'https://ldap.mozilla.org/phonebook'
NO_PHOTO_THUMBNAIL_SIZE = 3302
JSON_URL = '%s/directory.php' % BASE_URL
THUMBNAIL_URL = '%s/pic.php?type=thumb&mail=' % BASE_URL

def fetch_thumbnails(emails):
    def worker():
        while True:
            try:
                email = queue.get(True, 0.1)
            except Queue.Empty:
                return
            maybe_fetch_thumbnail(email)
            queue.task_done()

    NUM_WORKER_THREADS = 5

    queue = Queue.Queue()
    for email in emails:
        queue.put(email)
    for i in range(NUM_WORKER_THREADS):
        Thread(target=worker).start()
    queue.join()

def install_auth_handler(username, password):
    pw_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    pw_manager.add_password(realm=None,
                            uri=BASE_URL,
                            user=username,
                            passwd=password)
    auth_handler = urllib2.HTTPBasicAuthHandler(pw_manager)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)

def maybe_fetch_json_feed():
    if not os.path.exists(JSON_FEED_FILENAME):
        print "Fetching JSON feed."
        response = urllib2.urlopen(JSON_URL).read()
        # Bleh, have to strip out some PHP warnings.
        response = response[response.index('{'):]
        f = open(JSON_FEED_FILENAME, 'w')
        f.write(response)
        f.close()

def maybe_fetch_thumbnail(email):
    thumbnail = os.path.join(THUMBNAIL_DIR, '%s.jpg' % email)
    if not os.path.exists(thumbnail):
        return
    if os.stat(thumbnail).st_size != NO_PHOTO_THUMBNAIL_SIZE:
        return
    print "Fetching thumbnail for %s..." % email
    try:
        url = THUMBNAIL_URL + email
        response = urllib2.urlopen(url).read()
        f = open(thumbnail, 'wb')
        f.write(response)
        f.close()
    except urllib2.HTTPError, e:
        if e.code != 404:
            raise

if __name__ == '__main__':
    config = json.load(open('config.json', 'r'))
    install_auth_handler(config['username'], config['password'])
    
    maybe_fetch_json_feed()    
    people = json.load(open(JSON_FEED_FILENAME))

    if not os.path.exists(THUMBNAIL_DIR):
        os.mkdir(THUMBNAIL_DIR)

    fetch_thumbnails([email for email in people])
