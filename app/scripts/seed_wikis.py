import os
import requests
import json
from app.models import Wiki


def run():
    filename = os.path.dirname(os.path.realpath(__file__))+'/../../datafiles/wikis.json'
    if not os.path.exists(filename):
        response = requests.get('http://search-s10:8983/solr/xwiki/select',
                                params=dict(wt='json', rows=10000, sort='wam_i desc', fl='id', q='lang_s:en'))
        with open(filename, 'w') as datafile:
            datafile.write(json.dumps(response.json()['response']['docs']))
    with open(filename, 'r') as datafile:
        data = json.loads(datafile.read())
        for wiki_grouping in data:
            wiki_id = wiki_grouping.get('id')
            if wiki_id is not None:
                Wiki.seed_data(int(wiki_id))
