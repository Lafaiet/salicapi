import sys
sys.path.append('../../../')

from app import app

def build_link(document):

    doc_id = document['idDocumentosAgentes']

    if document['Anexado'] == '2':
        idPronac =  document['idPronac']
        link_file = app.config['SALIC_BASE_URL']+'verprojetos/abrir-documentos-anexados?id=%d&tipo=2&idPronac=%d'%(doc_id, idPronac)

    elif document['Anexado'] == '5':
        link_file = app.config['SALIC_BASE_URL']+'verprojetos/abrir?id=%d'%(doc_id)

    else:
        link_file = ''

    return link_file
