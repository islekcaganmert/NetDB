from main import gate, bs_card
from bevyframe import *
import json


@gate
def get(r: Request) -> Page:
    with open('../db/users.json', 'rb') as f:
        users = json.load(f)
    with open('../db/networks.json', 'rb') as f:
        networks = json.load(f)
    softwares = {}
    for network in networks:
        if json.loads(networks[network]['software'])['name'] in softwares:
            softwares[json.loads(networks[network]['software'])['name']] += 1
        else:
            softwares.update({json.loads(networks[network]['software'])['name']: 1})
    softwares = dict(sorted(softwares.items(), key=lambda item: item[1], reverse=True))
    return Page(
        childs=[
            Widget(
                'div',
                childs=[
                    bs_card('User Count', childs=[
                        Label(len(users), style={'font-size': '2em'})
                    ], style={'float': 'left'}),
                    bs_card('Network Count', childs=[
                        Label(len(networks), style={'font-size': '2em'})
                    ], style={'float': 'left'}),
                    bs_card('Software Count', childs=[
                        Label(len(softwares), style={'font-size': '2em'})
                    ], style={'float': 'left'})
                ]
            ),
            Widget(
                'div',
                childs=[
                    bs_card('Software-Network Distribution', childs=[
                        Widget(
                            'ul',
                            selector='list-group list-group-flush',
                            style={
                                'margin-left': '-15px',
                                'width': 'calc(100% + 30px)'
                            },
                            childs=[
                                Widget(
                                    'li',
                                    selector='list-group-item',
                                    childs=[
                                        i,
                                        Widget(
                                            'span',
                                            selector='badge bg-primary rounded-pill',
                                            innertext=softwares[i],
                                            style={
                                                'float': 'right'
                                            }
                                        )
                                    ]
                                )
                                for i in softwares
                            ]
                        )
                    ], style={'float': 'left'})
                ]
            )
        ]
    )
