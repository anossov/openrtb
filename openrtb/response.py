from decimal import Decimal

from . import constants
from .base import Object, Array, Field


class Bid(Object):
    id = Field(str, required=True)
    impid = Field(str, required=True)
    price = Field(Decimal, required=True)
    adid = Field(str)
    nurl = Field(str)
    adm = Field(str)
    adomain = Field(Array(str))
    iurl = Field(str)
    cid = Field(str)
    crid = Field(str)
    attr = Field(Array(constants.CreativeAttribute))
    ext = Field(Object)


class SeatBid(Object):
    bid = Field(Array(Bid), required=True)
    seat = Field(str)
    group = Field(int)


class BidResponse(Object):
    id = Field(str, required=True)
    seatbid = Field(Array(SeatBid), required=True)
    bidid = Field(str)
    cur = Field(str)
    customdata = Field(str)
    ext = Field(Object)

    @staticmethod
    def minimal(id, bid_id, bid_impid, bid_price):
        return BidResponse(id=id, seatbid=[
            SeatBid(bid=[
                Bid(id=bid_id, impid=bid_impid, price=bid_price)
            ])
        ])

    def first_bid(self):
        return self.seatbid[0].bid[0]

    def get_bid_id(self):
        return self.first_bid().id

    def get_imp_id(self):
        return self.first_bid().impid

    def get_ad_id(self):
        return self.first_bid().adid

    def get_first_price(self):
        return self.first_bid().price
