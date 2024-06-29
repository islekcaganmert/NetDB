from main import gate
from bevyframe import *
import json


@gate
def get(r: Request) -> Page:
    with open('../db/networks.json', 'rb') as f:
        networks = json.load(f)
    with open('../db/users.json', 'rb') as f:
        users = json.load(f)
    users_byhandler = {}
    for u in users:
        for i in users[u]:
            users_byhandler.update({i: users[u][i]})
            users_byhandler[i].update({'@': f"{users_byhandler[i]['@']} ({', '.join(users[u].keys())})"})
    return Page(
        childs=[
            Widget(
                'div',
                childs=[Title(network)] + [
                    f'<b>{i[0]}:</b> {i[1]}<br>'
                    for i in [
                        ['Owner', users_byhandler[f"Administrator@{network}"]["@"]],
                        ['Location', f'{users_byhandler[f"Administrator@{network}"]["postcode"]}, {users_byhandler[f"Administrator@{network}"]["country"]}'],
                        ['TheProtocols Version', networks[network]['version']],
                        [
                            'Server Software',
                            ' '.join([
                                json.loads(networks[network]['software'])['name'],
                                json.loads(networks[network]['software'])['version'].removesuffix('.0').removesuffix('.0'),
                                json.loads(networks[network]['software'])['channel'].replace('Stable', ''),
                                f"(Build: {json.loads(networks[network]['software'])['build']})"
                            ])
                        ],
                        ['Server Software Developer', json.loads(networks[network]['software'])['developer']],
                        [
                            'Server OS',
                            ' '.join([
                                json.loads(networks[network]['os'])['name'],
                                json.loads(networks[network]['os'])['version'].removesuffix('.0').removesuffix('.0'),
                                json.loads(networks[network]['os'])['arch']
                            ])
                        ],
                    ]
                ]
            ) if False not in [
                f"Administrator@{network}" in users_byhandler
            ] else ''
            for network in networks
        ]
    )
