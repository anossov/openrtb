import re


MACRO_PATTERN = re.compile('|'.join(
    re.escape('${AUCTION_%s}' % macro)
    for macro in ['ID', 'BID_ID', 'IMP_ID', 'SEAT_ID', 'AD_ID', 'PRICE', 'CURRENCY']
))


class MacroReplacer(object):
    def __init__(self, data):
        self.data = data

    def __call__(self, match):
        k = match.group(0)
        return str(self.data[k] or '')


def substitution(request, response, price, template):
    macro_map = {
        '${AUCTION_ID}': request.id,
        '${AUCTION_BID_ID}': response.bidid,
        '${AUCTION_IMP_ID}': response.get_imp_id(),
        '${AUCTION_SEAT_ID}': response.seatbid[0].seat,
        '${AUCTION_AD_ID}': response.get_ad_id(),
        '${AUCTION_PRICE}': price,
        '${AUCTION_CURRENCY}': 'USD'
    }

    return MACRO_PATTERN.sub(MacroReplacer(macro_map), template)
