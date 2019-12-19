# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   mongodb
# @Time:    2019-11-26 14:13:23
# @Desc:    mongodb

import time
import json
import base64
import hashlib
import datetime
from voluptuous import Schema
from bson.json_util import dumps
from bson.objectid import ObjectId
import pymongo
import pymongo.results
import pymongo.command_cursor
from pymongo import UpdateOne, InsertOne, DeleteOne

from config import settings, decorator
from db.base import BaseModel, QueryMode
from db.base import DBConfigExistError, QueryModeError, FindOneIdError, ProjectError
from microserver.db.mongodb import MongoDB


class MongoDBModel(BaseModel):

    _name = None
    _alias_name = None
    PRIMARY_KEY = 'id'

    def __init__(self):
        self.coll = self.get_coll()
        self.client = self.get_client()

    def get_client(self):
        mongodb_config = settings.DATABASES.get(self._alias_name)
        if not mongodb_config:
            raise DBConfigExistError("{klass}:{alias_name}".format(
                klass=self.__class__.__name__,
                alias_name=self._alias_name or self._alias_name,
            ))

        host = mongodb_config["host"]
        port = mongodb_config["port"]
        if mongodb_config.get("replicaset"):
            client = pymongo.MongoClient("{host}:{port}".format(
                host=host,
                port=port,
            ), replicaset="gtSet", connect=False)
        else:
            if mongodb_config.get("user"):
                from urllib.parse import quote_plus
                db = mongodb_config["db"]
                host = "%s:%s/%s" % (host, str(port), db)
                uri = "mongodb://%s:%s@%s" % (
                    quote_plus(mongodb_config["user"]), quote_plus(mongodb_config["password"]), host)
                client = pymongo.MongoClient(uri, connect=False)
            else:
                client = pymongo.MongoClient(host, port, connect=False)
        return client

    def get_coll(self):
        db_name = self._name.split(".")[0]
        coll_name = self._name.split(".")[1]
        client = self.get_client()
        db = client[db_name]
        coll = db[coll_name]
        return coll

    def mongodb_aggregate(self, body):
        cr = self.coll.aggregate(body, allowDiskUse=True)
        return cr

    def adapte_query(self, query, **kwargs):
        mode = kwargs.get("query_mode") or QueryMode.MONGODB.value[0]
        if mode == QueryMode.MONGODB.value[0]:
            return query
        else:
            raise QueryModeError(mode)

    def mongodb_count(self, query):
        count = self.coll.find(query).count()
        return count

    def count(self, query=None, **kwargs):
        if query == None:
            query = {}
        else:
            query = self.adapte_query(query, **kwargs)
        count = self.mongodb_count(query)
        return count

    def project_handle(self, project):

        if project:
            projection = {}
            if not isinstance(project, dict):
                raise ProjectError(project)

            project_items = project.items()
            for item in project_items:
                field = item[0]
                include = item[1]
                if include == 1 or include == True:
                    projection.update({field:True})
                elif include == -1 or include == False:
                    projection.update({field:False})
                else:
                    raise ProjectError(project)
        else:
            projection = {"_id": False}

        return projection

    def search(self, query=None, sort=None, project=None, page=None, page_size=None, **kwargs):
        if query == None:
            query = {}
        else:
            query = self.adapte_query(query, **kwargs)

        aggregate_obj = [
            {"$match": query},
        ]

        if sort != None:
            aggregate_obj.append({"$sort": sort})

        if project != None:
            aggregate_obj.extend([
                {"$project": project},
            ])

        if page != None:
            skip = self.page2skip(page, page_size)
        else:
            skip = 0
        aggregate_obj.extend([
            {"$skip": skip},
        ])

        if page_size != None:
            limit = int(page_size)
        else:
            limit = settings.PAGE_SIZE
        aggregate_obj.extend([
            {"$limit": limit}
        ])

        start_time = time.time()
        cr = self.mongodb_aggregate(aggregate_obj)
        time_consum = int((time.time() - start_time) * 1000)

        objs = []

        for obj in cr:
            obj = self.dump(obj)
            objs.append(obj)
        length = self.count(query)
        page = self.skip2page(skip, limit)
        pager = self.count_page(length, page, page_size=limit, time_consum=time_consum)

        return objs, pager

    def insert(self, vals, **kwargs):
        if hasattr(self, "scheme") and isinstance(self.scheme, Schema):
            vals = self.scheme(vals)
        key = vals.get(self.PRIMARY_KEY) or self.gen_objectid()
        vals["id"] = key
        vals["_id"] = ObjectId(key)
        insert_one_result = self.dump(self.coll.insert_one(vals))
        inserted_id = insert_one_result.get("inserted_id")
        return inserted_id

    def update_by_query(self, query, vals, **kwargs):
        upsert = bool(kwargs.get("upsert"))
        update_result = self.coll.update_one(query, {"$set": vals}, upsert=upsert)
        return self.dump(update_result)

    def remove(self, id, **kwargs):
        query = {"$or": [{"id":id}, {"_id":ObjectId(id)}]}
        delete_result = self.coll.delete_one(query)
        return self.dump(delete_result)

    def find_one(self, id, project=None, **kwargs):
        if id:
            id = self.gen_objectid(id)
        else:
            raise FindOneIdError(id)

        projection = self.project_handle(project)

        options = dict()

        options.update(dict(
            projection = projection
        ))

        obj = self.coll.find_one({"$or":[{"id":id}, {"_id":ObjectId(id)}]}, **options)
        return self.dump(obj)

    def bulk(self, requests, **kwargs):
        for request in requests:
            if not isinstance(request, UpdateOne)\
                    and not isinstance(request, InsertOne)\
                    and not isinstance(request, DeleteOne):
                raise Exception("批量操作元素格式错误， 必须为UpdateOne 或 InsertOne 或 DeleteOne")
        self.coll.bulk_write(requests)

    def bulks(self, param):
        pass

    def dump(self, obj):
        result = None
        if isinstance(obj, pymongo.cursor.Cursor) or \
                isinstance(obj, list) or \
                isinstance(obj, pymongo.command_cursor.CommandCursor):
            result = []
            for _s in obj:
                if type(_s) == type({}):
                    s = {}
                    for (k, v) in _s.items():
                        if type(v) == type(ObjectId()):
                            s[k] = json.loads(dumps(v))['$oid']
                        elif type(v) == type(datetime.datetime.utcnow()):
                            s[k] = v.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                        else:
                            s[k] = v
                else:
                    s = _s
                result.append(s)
        elif isinstance(obj, dict):
            for (k, v) in obj.items():
                if type(v) == type(ObjectId()):
                    obj[k] = json.loads(dumps(v))['$oid']
                elif type(v) == type(datetime.datetime.utcnow()):
                    obj[k] = v.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            result = obj
        elif isinstance(obj, pymongo.results.InsertOneResult):
            result = {"inserted_id": str(obj.inserted_id)}
        elif isinstance(obj, pymongo.results.DeleteResult):
            result = {"deleted_count":obj.deleted_count}
        elif isinstance(obj, pymongo.results.UpdateResult):
            result = {"deleted_count":obj.matched_count}
        elif obj is None:
            result = None
        elif len(obj) == 0:
            result = obj
        return result


class TestModel(MongoDBModel):

    _name = 'test.articles'
    _alias_name = 'mongodb'


if __name__ == '__main__':
    model = TestModel()
    # result = model.search(query={'author': '烟墨'})
    # result = model.update_by_query(query={'author': '烟墨'}, vals={"update_time": '2019-12-10 15:12:28'})
    # result = model.bulk([
    #     UpdateOne({'title': '测试文章'}, {'title': '测试文章*1'}, upsert=True),
    #     UpdateOne({'title': '测试文章*2'}, {'content': "测试文章内容>>>Hello World"}, upsert=True),
    #     UpdateOne({'title': '测试文章*3'}, {'update_time': "2019-12-12 15:12:28"}, upsert=True),
    # ])
    # result = model.insert({
    #     'id': '31a66a2bcc244db91818ebea',
    #     'name': 'Mike',
    #     'age': 21,
    #     'gender': 'male'
    # })
    result = model.find_one('31a66a2bcc244db91818ebec')
    print(result)
    # print(dir(result))
