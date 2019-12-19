# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   test
# @Time:    2019-12-11 11:57:34
# @Desc:    test

from elasticsearch import Elasticsearch
from config.encrypt import md5_encrypt


es_servers = [{
    "host": 'localhost',
    "port": '9200'
}]

# 构造Es客户端
es = Elasticsearch(es_servers)


def create_index(index):
    """
    ES7.5(去除doc_type) 创建索引
    :param index: 索引名
    :return:
    """
    _index_mappings = {
        "mappings": {
            "properties": {
                "id": {
                    "index": False,  # 不建索引
                    "type": "text"
                },
                "name": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "ignore_above": 256,
                            "type": "keyword"
                        }
                    }
                },
                "sex": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "ignore_above": 256,
                            "type": "keyword"
                        }
                    }
                },
                "age": {
                    "type": "long"
                },
                "address": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "ignore_above": 256,
                            "type": "keyword"
                        }
                    }
                },
                "happy": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "ignore_above": 256,
                            "type": "keyword"
                        }
                    }
                },
                "countries": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "ignore_above": 256,
                            "type": "keyword"
                        }
                    }
                },
            }
        }
    }
    es.indices.create(index=index, body=_index_mappings)


def insert_record(index):
    """
    插入一条记录
    :param index: 索引名
    :return:
    """
    val = {
        "id": md5_encrypt('YanMo'),
        'name': 'YanMo',
        "sex": "男",
        "age": 23,
        "address": "河南-郑州",
        "happy": [
            "吃",
            "喝"
        ],
        "countries": "中国河南"
    }
    res = es.index(index=index, id=val["id"], body=val)
    print(res)


def get_record(index, id):
    """
    查询单条记录(_source的json数据)
    :param index: 索引名
    :param id: 记录ID
    :return:
    """
    res = es.get(index=index, id=id)
    print(res)


def get_source(index, id):
    """
    查询单条记录
    :param index:
    :param id:
    :return:
    """
    res = es.get_source(index=index, id=id)
    print(res)


def search(index):
    """
    批量查询
    :param index:
    :return:
    """
    res = es.search(index=index, body={"query": {"match_all": {}}})
    print("Count %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print(hit["_source"])


def update_record(index, doc_id):
    """
    更新单条记录(ID更新)
    :param index:
    :param doc_id: 记录ID
    :return:
    """
    body = {
        "script": {
            "inline": "ctx._source.name = params.name",
            "params": {
                "name": "YanMo",
            }
        }
    }
    es.update(index=index, id=doc_id, body=body)


def update_record_query(index):
    """
    更新单条记录(条件更新)
    :param index:
    :return:
    """
    query = {
        # 定位条件
        "query": {
            "match": {
                "name": "YanMo"
            }
        },
        # 待更新字段
        "script": {
            "inline": "ctx._source.name = params.name; ctx._source.age = params.age",
            "params": {
                "name": "YanYu",
                "age": 20
            }
        }
    }
    res = es.update_by_query(index=index, body=query)
    print(res)


def delete_record(index, doc_id):
    """
    删除单条记录(ID删除)
    :param index:
    :param doc_id:
    :return:
    """
    res = es.delete(index=index, id=doc_id)
    print(res)


def delete_record_query(index):
    """
    删除单条记录(条件删除)
    :param index:
    :param doc_type:
    :return:
    """
    body = {
        'query': {
            'match': {
                'name': 'ZhangSan'
            }
        }
    }
    es.delete_by_query(index=index, body=body)


def count_record(index):
    """
    统计当前索引记录条数
    :param index:
    :return:
    """
    body = {
        "query": {
            "match_all": {}
        }
    }
    res = es.count(index=index, body=body)
    print(res["count"])


if __name__ == '__main__':
    index_name = 'test'
    doc_id = '5eeeb102bc6c9173a9ff3d2ef333fc8d'
    create_index(index_name)    # 创建索引
    insert_record(index_name)   # 插入数据
    get_record(index_name, doc_id)  # 查询单条
    # search(index_name)    # 批量查询
    # update_record(index_name, doc_id)   # id更新
    # update_record_query(index_name)     # 条件更新
    # delete_record(index_name, doc_id)     # id删除
    # delete_record_query(index_name)     # 条件删除
    # count_record(index_name)    # 获取总数
