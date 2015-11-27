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
            row_recurrido = root.xpath('.//th[text()="Votos recurridos"]')[0]
            row_impugnado = root.xpath('.//th[text()="Votos impugnados"]')[0]
            row_estado = root.xpath('.//th[text()="Estado"]')[0]

            db.docs.update_one(
                {"docid": doc_id},
                {"$set": {
                    "votos_macri": int(row_macri.getnext().text),
                    "votos_scioli": int(row_scioli.getnext().text),
                    "votos_nulos": int(row_nulo.getnext().text),
                    "votos_blancos": int(row_blanco.getnext().text),
                    "votos_recurridos": int(row_recurrido.getnext().text),
                    "votos_impugnados": int(row_impugnado.getnext().text),
                    "estado": row_estado.getnext().text
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

