import os.path
import requests

from pymongo import MongoClient

chunk_size = 1024 ** 2


def main():
    # Init
    client = MongoClient()
    db = client.ean2015
 
    # Get files
    for doc in db.docs.find():
        filename = 'data/' + doc['docid'] + '.' + 'pdf'

        if not os.path.isfile(filename):
            url = doc['url'].replace('.htm', '.pdf')
            print '[D] : {} - {}'.format(doc['docid'], url)
            r = requests.get(url, stream=True)

            with open(filename, 'wb') as fd:
                for chunk in r.iter_content(chunk_size):
                    fd.write(chunk)
        else:
            print '[I] : {}'.format(doc['docid'])

if __name__ == '__main__':
    main()

