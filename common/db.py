# -*- coding:utf-8 -*-

# Created on 2023/5/13.

from peewee import *
from playhouse.shortcuts import model_to_dict
from common.config import db_config
from common.config import task_init_configs


class DbConn:
    _db = None

    def __enter__(self):
        db = MySQLDatabase(
            db_config["database"],
            user=db_config["user"],
            password=db_config["password"],
            host=db_config["host"],
            port=db_config["port"],
            charset='utf8'
        )
        db.connect()
        self._db = db
        return db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db.close()


def make_user(db):
    class User(Model):
        id = AutoField()
        user_id = CharField(index=True)

        class Meta:
            database = db
            table_name = 'user'

    return User


def make_config(db):
    class Config(Model):
        id = AutoField()
        configKey = CharField(index=True)
        configValue = TextField()
        configDesc = CharField()

        class Meta:
            database = db
            table_name = 'config'

    return Config


def bulk_create_user(users):
    with DbConn() as db:
        model = make_user(db)
        model.insert_many(users).execute()


def clear_user():
    with DbConn() as db:
        model = make_user(db)
        query = model.delete()
        query.execute()


def query_user(filters=None, offset=None, limit=None):
    """
    filters = {
        "user_ids": [1, 2, 5],
    }
    :param filters:
    :param offset:
    :param limit:
    :return:
    """
    if filters is None:
        filters = {}
    with DbConn() as db:
        model = make_user(db)
        conditions = []
        if filters.get("user_ids"):
            conditions.append(model.user_id << filters["user_id"])
        q = model.select()
        if conditions:
            q = q.where(*conditions)
        total_count = q.count()
        if offset:
            q = q.offset(offset)
        if limit:
            q = q.limit(limit)
        return dict(
            TotalCount=total_count,
            users=list(map(model_to_dict, q))
        )


def get_config(keys):
    with DbConn() as db:
        config = make_config(db)
        lines = config.select().dicts()
        if isinstance(keys, str):
            for line in lines:
                if line['configKey'] == keys:
                    return line['configValue']
        elif isinstance(keys, tuple):
            result = list()
            for k in keys:
                for line in lines:
                    if line['configKey'] == k:
                        result.append(line['configValue'])
                        break
            return tuple(result)


def clear_config():
    with DbConn() as db:
        model = make_config(db)
        query = model.delete()
        query.execute()


def get_all_config():
    with DbConn() as db:
        model = make_config(db)
        lines = model.select().dicts()
        return lines


def bulk_create_config(configs):
    with DbConn() as db:
        model = make_config(db)
        model.insert_many(configs).execute()


def get_config_by_id(config_id):
    with DbConn() as db:
        model = make_config(db)
        q = model.select().where(model.id == config_id)
        return list(map(model_to_dict, q))[0]


def update_config_by_id(config_id, config_key, config_value):
    _config = {
        "configKey": config_key,
        "configValue": config_value,
    }
    with DbConn() as db:
        model = make_config(db)
        model.update(**_config).where(model.id == config_id).execute()


def init_config():
    clear_config()
    bulk_create_config(task_init_configs)


def create_databases():
    sql = "create database huya default character set utf8 COLLATE utf8_bin;"
    with DbConn() as db:
        db.execute_sql(sql)


def create_all_tables():
    with DbConn() as db:
        user = make_user(db)
        config = make_config(db)
        db.create_tables([user, config], safe=True)


def init_data():
    init_config()


def init_db():
    # create_databases()
    create_all_tables()
    init_data()






