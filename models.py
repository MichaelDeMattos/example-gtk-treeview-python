# -*- coding: utf-8 -*-

from datetime import datetime 
from peewee import *

db = SqliteDatabase("quotation.db")
db.connect()

""" This model structure """
class Quotation(Model):
    id = IntegerField(primary_key=True)
    coin = CharField(max_length=256, null=False)
    bid = FloatField(null=False)
    ask = FloatField(null=False)
    varBid = FloatField(null=False)
    date_consult = DateField(null=False)
    date_create = DateField(default=datetime.now())

    class Meta:
        database = db

db.create_tables([Quotation])
