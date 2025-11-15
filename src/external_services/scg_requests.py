import re
import time
import random
import requests
from time import sleep
from src.utils.api import ApiUtils
from data.json_dicts.scg_dicts import scg_headers, scg_body

utils = ApiUtils()


class StacityGamesAPI():

    def __init__(self, base_url, cardlist, max_attemps):
        self.base_url = base_url
        self.cardlist = cardlist
        self.max_attemps = max_attemps

    def get_scg_headers_request(self):
        """
        Must update the original headers dict to create
        a random user-agent to emulate the original behaviour
        of a browser request
        """
        scg_agent = utils.get_user_agent()
        scg_headers.update(scg_agent)
        return scg_headers

    def get_body_request(self, cardlist):
        """
        Given an array of dicts with information about
        each card, they are adapted to the 
        format required by the request.

        FROM THIS.

        TO THIS
        {
            'qty': 1,
            'term': '',#cardname
            'setCode': '',
            'setNames': [],
            'tags': {
                'sku': '', #sgl-mtg-<exp name(3 letters)>-<cardnumber>-<lang>
            },
        }
        """
        formatted_cardlist = []

        for card in cardlist:
            cardname = card.get('cardname', False)
            name, card_sku = self.parse_cardname(cardname)
            card_dict = {
                'term': name,
                'qty': card.get('qty', 0),
                'setCode': '',
                'setNames': [],
                'tags': {},
            }
            if card_sku:
                card_dict['tags'].update({
                    'sku': card_sku
                })

            formatted_cardlist.append(card_dict)

        scg_body.update({'data': formatted_cardlist})
        return scg_body

    def get_cardlist(self):
        """
        Creates a request session to store all cookies,
        and get all specified cards and their prices
        """
        max_attemps = self.max_attemps
        for attemp in range(max_attemps):
            try:
                # create a session
                scg_session = requests.Session()
                scg_session.headers.update(self.get_scg_headers_request())
                # set a delay
                time.sleep(random.uniform(1, 3))
                # get all scg available options for specified cards
                response = scg_session.post(
                    self.base_url,
                    json=self.get_body_request(cardlist=self.cardlist)
                )
                json_response = response.json()
                # pass the current request dict to create the returned_dict
                cards_dict = self.get_clean_dict(json_response)
                return cards_dict

            except requests.RequestException as e:
                if attemp == max_attemps:
                    return {
                        "error": f"{str(e)}"
                    }
                # Exponential backoff to retry multiple times the request
                time.sleep(2 ** attemp)

    def parse_cardname(self, name):
        """
        Parses a name to create a "code" to recreate the common
        format in scg webiste requests
        Ex.
        Morphic Pool (CLB) 357 -> sgl-mtg-clb-357-enn
        """
        pattern = r'(.+?)\s+\((\w{3})\)\s+(\d{1,3})$'
        coincidence = re.search(pattern, name)

        # If a coincidice with the pattern was not found,
        # the parsing proccess is skipped
        if not coincidence:
            return (name, False)

        original_cardname = coincidence.group(1)
        code = coincidence.group(2)
        number = coincidence.group(3).zfill(3)
        parsed_name = f"SGL-MTG-{code}-{number}-ENN"
        return (original_cardname, parsed_name)

    def get_clean_dict(self, source_dict):
        """
        Transforms the source dict to create a simplified version of it 
        with the available quantity, the card version and it's price
        """
        try:
            available_cards = []
            unavailable_cards = []
            cardlist_data = source_dict.get("data", [])

            # First, we search all cards in response
            for card in cardlist_data:
                context = card.get('context', {})
                term = context.get('term', False)
                required_qty = context.get('qty', False)
                error = card.get('error', {})
                matches = card.get('matches', [])
                card_details = {
                    'name': term,
                    'qty': required_qty
                }

                # Prevent to check get info from cards with errors
                if error or error == 'Out of stock':
                    card_details.update({
                        'error': error
                    })
                    unavailable_cards.append(card_details)
                    continue

                # Get all available matches for current card
                all_matches = []
                for match in matches:
                    card_doc = match.get('Document', {})
                    cardstate_details = card_doc.get(
                        'hawk_child_attributes', [])
                    image = card_doc.get('image', [0])[0]
                    match_detail = {
                        'image': image
                    }
                    # Get all conditions (near mint or played) from current card
                    available_conditions = []
                    for detail in cardstate_details:
                        price = detail.get('price', [0])[0]
                        price_sale = detail.get('price_sale', [0])[0]
                        available_qty = detail.get('qty', [0])[0]
                        condition = detail.get('condition', [''])[0]
                        state_detail = {
                            'current_price': price,
                            'discount_price': price_sale,
                            'available_qty': available_qty,
                            'condition': condition
                        }
                        available_conditions.append(state_detail)

                    if available_conditions:
                        match_detail.update({
                            'conditions': available_conditions
                        })

                    all_matches.append(match_detail)

                card_details.update({
                    'matches': all_matches
                })
                available_cards.append(card_details)

            # Return all cards
            return {
                'available': available_cards,
                'unavailable': unavailable_cards
            }
        except Exception as e:
            return {
                "error": f"{str(e)}"
            }
