import elasticsearch
import datetime
import sys
from club import models
from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch.client.utils import _make_path

GEO_INDEX = 'geo'
DOC_TYPE = 'clubs'
MAPPING = {DOC_TYPE: {
    "properties": {
        "added": {"type": "date"},
        "location": {"type": "geo_point"},
        "tags": {"type": "string"},
        "tag_suggest": {
            "type": "completion",
            "index_analyzer": "simple",
            "search_analyzer": "simple",
            "payloads": "false",
        }}}}
ES = Elasticsearch(settings.ES_HOSTS)


def sync_db():
    ES.transport.perform_request('POST',
                                 _make_path(GEO_INDEX,
                                            '_refresh', ''))


def reset_db():
    try:
        ES.delete(GEO_INDEX, '', '')
    except elasticsearch.exceptions.NotFoundError:
        print "index missing, but that's ok!"
    ES.transport.perform_request('PUT',
                                 _make_path(GEO_INDEX, '', ''))
    ES.transport.perform_request('PUT',
                                 _make_path(GEO_INDEX, DOC_TYPE,
                                            '_mapping'),
                                 body=MAPPING)


def reindex_db():
    reset_db()
    for club in models.Club.objects.first():
        print "Club: ", club
        sys.stdout.flush()
        add_club(club['club_id'], club)
    sync_db()


def get_mapping():
    _, data = ES.transport.perform_request('GET',
                                           _make_path(GEO_INDEX, DOC_TYPE,
                                                      '_mapping'))
    return data


def add_club(club_id, params):
    tags = params.get('tags')
    if tags:
        tags = tags.upper()
    else:
        tags = ''
    obj = {
        "club_id": params.get('club_id', ''),
        "type": params.get('type', 1),
        "added": params.get('added', ''),
        "location": {
            "lat": params.get('lat', ''),
            "lon": params.get('lon', ''),
        },
        "owner": {
            "id": params.get('owner_id', ''),
            "username": params.get('username', ''),
            "gender": params.get('gender', ''),
        },
        "name": params.get('name', ''),
        "description": params.get('description', ''),
        "tags": tags,
        "tag_suggest": tags,
    }
    ES.index(index=GEO_INDEX, doc_type=DOC_TYPE, id=club_id, body=obj)


def remove_club(club_id):
    ES.delete(GEO_INDEX, DOC_TYPE, club_id)


def prefix_search(prefix, lat, lon, radius_km, page_size=5):
    query = {"query": {"prefix": {"tags": prefix}}}
    conditions = []
    if radius_km > 0:
        conditions.append({"geo_distance": {"distance": "%skm" % radius_km,
                                            ("%s.location" % DOC_TYPE):
                                            {"lat": lat, "lon": lon}}})
        query['filter'] = {"bool": {"must": conditions}}
    params = {}
    params['size'] = page_size
    params['from'] = 0
    _, data = ES.transport.perform_request('GET',
                                           _make_path(GEO_INDEX,
                                                      DOC_TYPE, '_search'),
                                           body=query, params=params)
    rval = []
    for obj in data['hits']['hits']:
        es_club = obj['_source']
        club = {
            "added": datetime.datetime.fromtimestamp(
                es_club['added']).strftime('%Y-%m-%dT%H:%M:%S'),
            "club_type": es_club['type'],
            "description": es_club['description'],
            "id": es_club['club_id'],
            "lat": es_club['location']['lat'],
            "lon": es_club['location']['lon'],
            "coords": {"lat": es_club['location']['lat'],
                       "lon": es_club['location']['lon']},
            "name": es_club['name'],
            "owner_id": es_club['owner']['id'],
            "tags": es_club['tags']
        }
        rval.append(club)
    return rval
