# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-23 10:29:56
# @Last Modified by:   edward
# @Last Modified time: 2016-07-27 13:14:27
from tinydb import TinyDB, Query
import os

DB_NAME = 'RATHAED_COUNTDOWN.json'
def connect(tableName=None):
    if tableName is not None:
        db = TinyDB(DB_NAME)
        return db.table(tableName)
    return TinyDB(DB_NAME)
def insert(dictObj):
    with connect() as db:
        eid = db.insert(dictObj)
    return eid
def update(updates, eids):
    with connect() as db:
        db.update(updates, eids)
def delete(eids):
    with connect() as db:
        db.remove(eids=eids)
def all():
    if not os.path.exists(DB_NAME):
        return []
    with connect() as db:
        return db.all()

