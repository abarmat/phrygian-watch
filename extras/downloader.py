import os.path
import grequests

from pymongo import MongoClient


DOWNLOADERS_NUM = 20


def handle_response(doc_id, url, filename):
    def do(r, **kwargs):
        with open(filename, 'wb') as fd:
            fd.write(r.raw.read())
        print '[W] : {} - {}'.format(doc_id, url)
    return do


def filename_from_id(doc_id):
    return 'data/' + doc_id + '.' + 'pdf'


def main():
    # Init
    client = MongoClient()
    db = client.ean2015
 
    rs = []

    # Prepare files to download 
    for doc in db.docs.find():
        doc_id = doc['docid']
        filename = filename_from_id(doc_id) 

        if not os.path.isfile(filename):
            url = doc['url'].replace('.htm', '.pdf')
            r = grequests.get(url, hooks=dict(response=handle_response(doc_id, url, filename)))
            rs.append(r)
            print '[D] : {} - {}'.format(doc_id, url)
        else:
            print '[I] : {}'.format(doc_id)
        
        if len(rs) == DOWNLOADERS_NUM:
            grequests.map(rs, size=DOWNLOADERS_NUM)
            rs = []
 

if __name__ == '__main__':
    main()

