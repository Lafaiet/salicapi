import sys
sys.path.append('../../../')
from app import app


def build_link(document):

    doc_id = document['id_arquivo']

    link_file = app.config['SALIC_BASE_URL']+'verprojetos/abrir?id=%d'%(doc_id)

    return link_file
