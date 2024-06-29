from main import gate, bs_card
from bevyframe import *
import json


@gate
def get(r: Request) -> Page:
    with open('../db/networks.json', 'rb') as f:
        networks = json.load(f)
    softwares = {}
    for network in networks:
        if json.loads(networks[network]['software'])['name'] in softwares:
            softwares[networks[network]]['used'] += 1
            if json.loads(networks[network]['software'])['version'] in softwares[networks[network]]['versions']:
                softwares[networks[network]]['versions'][json.loads(networks[network]['software'])['version']] += 1
            else:
                softwares[networks[network]]['versions'].update({json.loads(networks[network]['software'])['version']: 1})
        else:
            softwares.update({json.loads(networks[network]['software'])['name']: {
                'used': 1,
                'developer': json.loads(networks[network]['software'])['developer'],
                'source': json.loads(networks[network]['software'])['source'],
                'versions': {json.loads(networks[network]['software'])['version']: 1}
            }})
    softwares = dict(sorted(softwares.items(), key=lambda item: item[1]['used'], reverse=True))
    return Page(
        childs=[
            Widget(
                'div',
                childs=[Title(software)] + [
                    f'<b>{i[0]}:</b> {i[1]}<br>'
                    for i in [
                        [
                            'Latest Version',
                            ''.join([
                                ' ('.join([
                                    str(i) for i in
                                    sorted(softwares[software]['versions'].items(), key=lambda item: item[0], reverse=True)[0]
                                ]),
                                ')'
                            ])
                        ],
                        [
                            'Most Popular Version',
                            ''.join([
                                ' ('.join([
                                    str(i) for i in
                                    sorted(softwares[software]['versions'].items(), key=lambda item: item[1],
                                           reverse=True)[0]
                                ]),
                                ')'
                            ])
                        ],
                        ['Developer', softwares[software]['developer']],
                        ['Source', softwares[software]['source']],
                        ['Network Count', softwares[software]['used']]
                    ]
                ]
            )
            for software in softwares
        ]
    )
