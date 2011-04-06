import os
import sys
import json
import urllib2

MY_DIR = os.path.abspath(os.path.dirname(__file__))
JSON_FEED_FILENAME = os.path.join(MY_DIR, 'people.json')
THUMBNAIL_DIR = os.path.join(MY_DIR, 'static-files', 'images', 'people')

BASE_URL = 'https://ldap.mozilla.org/phonebook'
JSON_URL = '%s/directory.php' % BASE_URL
THUMBNAIL_URL = '%s/pic.php?type=thumb&mail=' % BASE_URL

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
        sys.stdout.write("Fetching thumbnail for %s... " % email)
        sys.stdout.flush()
        try:
            url = THUMBNAIL_URL + email
            response = urllib2.urlopen(url).read()
            f = open(thumbnail, 'wb')
            f.write(response)
            f.close()
            print "OK."
        except urllib2.HTTPError, e:
            if e.code != 404:
                raise
            print "Not Found."

if __name__ == '__main__':
    config = json.load(open('config.json', 'r'))
    install_auth_handler(config['username'], config['password'])
    
    maybe_fetch_json_feed()    
    people = json.load(open(JSON_FEED_FILENAME))

    if not os.path.exists(THUMBNAIL_DIR):
        os.mkdir(THUMBNAIL_DIR)

    for email, info in people.items():
        maybe_fetch_thumbnail(email)
