from main import gate
from bevyframe import *
import json


@gate
def get(r: Request) -> Page:
    with open('../db/users.json', 'rb') as f:
        users = json.load(f)
        users = dict(sorted(users.items(), key=lambda item: item[0].lower().replace('ç', 'c'), reverse=False))
    widgets_all = [
        Label(
            '<i>Don\'t see to have your information here? Log in to your account to hide, contact your network administrator for help.</i>',
            style={'color': '#80808080'}
        )
    ]
    for user in users:
        widgets = []
        widgets.append(Title('&nbsp;'.join([
            Widget(
                'img',
                src=users[user][i]['profile_photo'],
                style={'width': '0.9em', 'height': '0.9em', 'border-radius': '50%'},
                onerror='this.style.visibility = "hidden"'
            ).render()
            for i in users[user]
        ] + [user])))
        widgets.append(f'<b>Handlers:</b> {", ".join(users[user].keys())}<br>')
        admin_of = []
        for alt in users[user]:
            if alt.split('@')[0] == 'Administrator':
                admin_of.append(alt.split('@')[1])
        if len(admin_of) > 0:
            widgets.append(f'<b>Admin of:</b> {", ".join(admin_of)}<br>')
        subs = {
            0: 'Free',
            1: 'Plus',
            2: 'Pro',
            3: 'Ultra'
        }
        if len(users[user]) == 1:
            widgets.append(f'<b>Subscription:</b> {subs[users[user][list(users[user].keys())[0]]['plus']]}<br>')
        else:
            sub_text = []
            for alt in users[user]:
                sub_text += [f'{subs[users[user][alt]["plus"]]} ({alt.split("@")[1]})']
            widgets.append(f'<b>Subscriptions:</b> {", ".join(sub_text)}<br>')
        for i in [
            ['Birthday', 'birthday'],
            ['ChamyChain Address', 'chamychain_public_key'],
            ['RSA Key', 'rsa_public_key'],
            ['Country', 'country'],
            ['Gender', 'gender'],
            ['Phone Number', 'phone_number'],
            ['Zip Code', 'postcode'],
            ['Timezone', 'timezone'],
        ]:
            values = []
            for alt in users[user]:
                if users[user][alt][i[1]] not in values:
                    values.append(users[user][alt][i[1]])
            for value in values:
                if str(value).replace('*', '') == '':
                    values.remove(value)
            if len(values) == 0:
                continue
            elif len(values) == 1:
                widgets.append(f'<b>{i[0]}:</b> {values[0]}<br>')
            else:
                widgets.append(Widget(
                    'a',
                    style={'color': 'red'},
                    innertext=f'<b>{i[0]}:</b> {", ".join(values)}<br>'
                ))
        widgets_all.append(Widget(
            'div',
            style={'overflow-y': 'auto', 'width': 'calc(100vw - 210px)'},
            childs=[Widget(
                'div',
                style={'width': 'max-content'},
                childs=widgets
            )]
        ))
    return Page(
        childs=[
            Widget(
                'div',
                childs=widgets_all
            )
        ]
    )
