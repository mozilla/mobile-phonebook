import os
import fetch
import json

DEV_MODE = False
LOAD_PEOPLE = os.path.join(fetch.MY_DIR, 'static-files', 'load-people.js')

if __name__ == '__main__':
    print 'Writing %s.' % LOAD_PEOPLE

    people = json.load(open(fetch.JSON_FEED_FILENAME, 'r'))
    thumbnails = os.listdir(fetch.THUMBNAIL_DIR)
    people_list = []
    for email, info in people.items():
        info['name'] = info['name'].strip()
        info['email'] = email
        if '%s.jpg' % email in thumbnails:
            info['thumbnail'] = True
        people_list.append(info)
    
    def compare(a, b):
        return cmp(a['name'], b['name'])
    
    people_list.sort(compare)

    if DEV_MODE:
        people_list = people_list[:10]

    f = open(LOAD_PEOPLE, 'w')
    f.write('onLoadPeople(%s);' % json.dumps(people_list))
    f.close()
