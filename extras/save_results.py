import grequests
import lxml.html

from pymongo import MongoClient

DOWNLOADERS_NUM = 20

def parse_doc(doc_id):
    def do(r, **kwargs):
        try:
            root = lxml.html.document_fromstring(r.content)
            row_scioli = root.xpath('.//th[text()="FRENTE PARA LA VICTORIA "]')[0]
            row_macri = root.xpath('.//th[text()="CAMBIEMOS "]')[0]
            row_nulo = root.xpath('.//th[text()="Votos nulos"]')[0]
            row_blanco = root.xpath('.//th[text()="Votos en blanco"]')[0]

            db.docs.update_one(
                {"docid": doc_id},
                {"$set": {
                    "macri": int(row_macri.getnext().text),
                    "scioli": int(row_scioli.getnext().text),
                    "blanco": int(row_nulo.getnext().text) + int(row_blanco.getnext().text)
                }}
            )
            print 'OK', doc_id
        except:
            print 'ERROR', doc_id
    return do


def main():
    global client, db
    client = MongoClient()
    db = client.ean2015
 
    rs = []

    for doc in db.docs.find():
        doc_id = doc['docid']
        
        r = grequests.get(doc['url'], hooks=dict(response=parse_doc(doc_id)))
        rs.append(r)

        if len(rs) == DOWNLOADERS_NUM:
            grequests.map(rs, size=DOWNLOADERS_NUM)
            rs = []


if __name__ == '__main__':
    main()

