scg_headers = {
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

scg_body = {
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
        'condition': [],
        'filter_set': [],
        'finish': 'ANY',
        'variant_instockonly': [
            'Yes',
        ],
        'variant_language': 'EN',
        'tournament_legality': [
            'Legal',
        ],
    },
    # 'data': formatted_cardlist,
}
