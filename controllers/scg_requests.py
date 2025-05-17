import re
import time
import random
import requests
from time import sleep
from models.api_request import ApiRequest

api_request = ApiRequest()


class StacityGamesAPI():

    def __init__(self, base_url, cardlist, max_attemps):
        self.base_url = base_url
        self.cardlist = cardlist
        self.max_attemps = max_attemps

    def get_scg_headers_request(self):
        scg_agent = api_request.get_user_agent()
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': 'https://starcitygames.com/',
            'Content-Type': 'application/json',
            'Origin': 'https://starcitygames.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'DNT': '1',
            'Sec-GPC': '1',
            'Priority': 'u=4',
        }
        headers.update(scg_agent)
        return headers

    def get_body_request(self, cardlist):
        """
        Create a dict to search all cards 
        and all of its variants available
        ex.
        {
            'qty': 1,
            'term': '',#cardname
            'setCode': '',
            'setNames': [],
            'tags': {
                'sku': '', #sgl-mtg-ema-49-enn
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

        json_data = {
            'metadata': {
                'department': 'mtg',
            },
            'options': {
                'mode': 'manual',
            },
            'filters': {
                'availability': [
                    'Available',
                ],
                'condition': [
                    'NM',
                    'PL',
                ],
                'filter_set': [],
                'finish': [
                    'Non-foil',
                    'Foil'
                ],
                'variant_instockonly': [
                    'Yes',
                ],
                'variant_language': [
                    'EN',
                ],
                'tournament_legality': [
                    'Legal',
                ],
            },
            'data': formatted_cardlist,
        }

        return json_data

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
                # set a delay
                time.sleep(random.uniform(1, 3))
                # get all scg available options for specified cards
                response = scg_session.post(
                    self.base_url,
                    headers=self.get_scg_headers_request(),
                    json=self.get_body_request(cardlist=self.cardlist)
                )
                json_response = response.json()
                return json_response

            except requests.RequestException as e:
                if attemp == max_attemps:
                    return {
                        "error": f"{str(e)}"
                    }
                # Exponential backoff to retry multiple  time
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
            cardlist_data = source_dict.get("data", [])
        except Exception as e:
            return {
                "error": f"{str(e)}"
            }
