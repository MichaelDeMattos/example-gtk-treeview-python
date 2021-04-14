# -*- coding: utf-8 -*-

from models import *
from datetime import datetime

class ControllerQuotation(object):
    def __init__(self, *args):
        ...
    
    """ Register history request counting """
    def insert_quotation(self, coin, bid, ask, varBid, date_consult):
        try:
            query = Quotation(coin=coin, bid=bid, ask=ask, varBid=varBid, date_consult=date_consult)
            query.save()

        except Exception as error:
            db.rollback()
            print("Error: ", error)
    
    """ The funciton select all history consult dollar """
    def select_quotation(self):
        try:
            Quotation = Table("quotation")
            query = (Quotation.select(Quotation.c.coin, Quotation.c.bid, Quotation.c.ask,
                                      Quotation.c.varBid, Quotation.c.date_consult))

            quotations = []
            for row in query.execute(db):
                quotations.append(row)
            return quotations

        except Exception as error:
            db.rollback()
            print("Error: ", error)

    def delete_from_history(self):
        try:
            query = Quotation.delete()
            query.execute(db)
            
        except Exception as error:
            db.rollback()
            print("Error: ", error)
