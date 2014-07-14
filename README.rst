This package contains classes mirroring the `OpenRTB 2.2  <http://www.iab.net/media/file/OpenRTBAPISpecificationVersion2_2.pdf>`_ and `OpenRTB Mobile 1.0 <https://code.google.com/p/openrtb/downloads/detail?name=OpenRTB%20Mobile%20RTB%20API%20-%201.0.pdf&can=2&q=>`_ protocol schemas.

***************
Modules
***************

* All classes have a ``deserialize`` method that creates the appropiate objects from a Python dict (e.g. decoded from JSON).
* All objects have a ``serialize`` method that serializes the object back to a Python dict.

request
------------------

Contains the ``BidRequest`` class and the bid request subobject classes:

 * ``Impression``
 * ``Banner``
 * ``Video``
 * ``Site``
 * ``App``
 * ``Publisher``
 * ``Device``
 * ``User``
 * ``Geo``
 * ``Content``
 * ``Data``
 * ``Segment``
 * ``Producer``

response
--------------

Contains the ``BidResponse`` class and the bid response subobject classes, ``SeatBid`` and ``Bid``.

mobile
---------

Contains the OpenRTB Mobile ``BidRequest`` classes and its subobjects:

 * ``Impression``
 * ``Device``
 * ``User``
 * ``Site``
 * ``App``
 * ``Restrictions``
 * ``Regulations``
 * ``PMP``
 * ``Deal``

Also contains the ``OpenRTB20Adapter`` class that can be used to ``deserialize`` an OpenRTB Mobile bid request into OpenRTB 2.0 objects.

macros
---------

Contains the `substitution` function that performs substitution macro replacement in a string.

 * `substitution(BidRequest, BidResponse, auction_price, string_with_macros) -> string with expanded macros`

constants
----------

Contains enum-like wrappers around the integer constants used in bid requests (see chapter 6 of the OpenRTB 2.0 spec):

 * ``AuctionType``
 * ``BannerType``
 * ``CreativeAttribute``
 * ``CompanionType``
 * ``AdPosition``
 * ``ConnectionType``
 * ``ExpandableDirection``
 * ``ContentContext``
 * ``ContentDeliveryMethod``
 * ``LocationType``
 * ``DeviceType``
 * ``APIFramework``
 * ``VideoLinearity``
 * ``VideoProtocol``
 * ``VideoPlaybackMethod``
 * ``VideoQuality``
 * ``QAGMediaRating``
 * ``NoBidReason``

iab
-----

Contains the IAB’s contextual category taxonomy:

 * ``CATEGORIES`` — a list of ``(category_name, list_of_subcategories)`` tuples