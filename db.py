# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-23 10:29:56
# @Last Modified by:   edward
# @Last Modified time: 2016-07-23 17:16:17
from tinydb import TinyDB, Query

def connect():
    DB_NAME = 'RATHAED_COUNTDOWN.json'
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
    with connect() as db:
        return db.all()

