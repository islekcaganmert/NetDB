import sys
from bevyframe import *
from TheProtocols import Network, User
# from bevy2flask import Frame
from threading import Thread
import requests
import dotenv
import json
import time
import os

dotenv.load_dotenv('../.env')
app = Frame(
    package='me.islekcaganmert.netdb',
    developer='islekcaganmert@hereus.net',
    administrator=None,
    secret=os.environ.get('SECRET'),
    style='',
    icon='/favicon.ico'
)


def gate(func) -> any:
    def wrapper(r: Request) -> (str, Response):
        if 'Guest' != r.email.split('@')[0] or (
            r.path not in []
        ):
            data: (Page, Response, str) = func(r)
            if isinstance(data, Page):
                data.data['icon'] = {
                    'href': '/static/favicon.png',
                    'type': 'image/x-icon'
                }
                data.data['title'] = 'NetDB'
                data.content = [
                    Widget(
                        'link',
                        rel='stylesheet',
                        href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css'
                    ),
                    Widget(
                        'script',
                        src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.min.js',
                        innertext=''
                    ),
                    Widget(
                        'link',
                        rel='stylesheet',
                        href='https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/dist/css/bootstrap-icons.min.css'
                    ),
                    Widget(
                        'div',
                        selector='d-flex flex-column flex-shrink-0 p-3 bg-light',
                        style={
                            'width': '200px',
                            'height': '100vh',
                            'position': 'fixed',
                            'left': '0px',
                            'top': '0px'
                        },
                        childs=[
                            Widget(
                                'ul',
                                selector='nav nav-pills flex-column mb-auto',
                                childs=[
                                   Widget(
                                       'li',
                                       selector='nav-item',
                                       childs=[
                                           Label('NetDB', selector='nav-link py-3 text-dark text-center')
                                       ]
                                   )
                                ] + [
                                    Widget(
                                        'li',
                                        selector='nav-item',
                                        style={'cursor': 'pointer'},
                                        childs=[
                                            Widget(
                                                'a',
                                                href=i[1],
                                                selector='nav-link' + (
                                                    ' active' if r.path == i[1]
                                                    else ' link-dark'
                                                ),
                                                innertext=i[0]
                                            )
                                        ]
                                    )
                                    for i in [
                                        ['Home', '/'],
                                        ['Networks', '/Networks.py'],
                                        ['Server Softwares', '/Softwares.py'],
                                        ['Users', '/Users.py'],
                                        ['Docs', 'https://github.com/islekcaganmert/TheProtocols']
                                    ]
                                ]
                            )
                        ]
                    ),
                    Widget(
                        'div',
                        id='root',
                        style={
                            'margin-left': '210px',
                            'width': 'max-content',
                            'margin-top': '15px'
                        },
                        childs=data.content
                    )
                ]
                return data.render()
            else:
                return data
        else:
            return redirect('/login')
    return wrapper


def bs_card(title: str, childs: list[(Widget, str)], style: dict = None) -> Widget:
    r = Widget(
        'div',
        selector='card',
        style={
            'margin': '5px'
        },
        childs=[
            Widget(
                'div',
                selector='card-header',
                innertext=title
            ),
            Widget(
                'div',
                selector='card-body',
                style={
                    'width': '300px'
                },
                childs=childs
            )
        ]
    )
    if style is not None:
        for i in style:
            r.style.update({i: style[i]})
    return r


def refresh() -> str:
    networks = {}
    users = {}
    print()
    for line in requests.get('https://raw.githubusercontent.com/islekcaganmert/TheProtocols/main/Directory/Networks.md').text.split('\n'):
        try:
            if line.startswith('| ') and '**' not in line:
                network = line.split('|')[1].strip()
                print(f'      Fetching {network}...')
                net = Network(network)
                networks.update({network: json.loads(net.json())})
                for user in net.users:
                    if user not in ['Guest']:
                        print(f'      Fetching {user}@{network}...')
                        u = User(f'{user}@{network}')
                        key = str(u) if str(u).replace('*', '') == str(u) else (
                            network if str(u).split('@')[0] == 'Administrator' else user
                        )
                        if key in users:
                            users[key].update({f'{user}@{network}': json.loads(u.json())})
                        else:
                            users.update({key: {f'{user}@{network}': json.loads(u.json())}})
        except Exception as e:
            return str(e)
    with open('../db/users.json', 'wb') as f:
        data = json.dumps(users).encode('UTF-8')
        f.write(data)
    with open('../db/networks.json', 'wb') as f:
        data = json.dumps(networks).encode('UTF-8')
        f.write(data)
    return ''


working = True


def auto_refresh():
    while working:
        for i in range(6):
            print(f'      Refreshing in {6 - i} hours.')
            time.sleep(60 * 60)
        print('      Refreshing...')
        refresh()


if __name__ == '__main__':
    refresh()
    refresh_task = Thread(target=auto_refresh)
    refresh_task.start()
    app.run(host='0.0.0.0', port=8000, debug=True)
    sys.exit(0)
