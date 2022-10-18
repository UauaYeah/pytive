from attrdict import AttrDict

import tls_client, secrets, uuid, json
import main

class Mirrativ:
    def __init__(self):
        self.logger = main.logger
        self.session = tls_client.Session(
            # You can also use the following as `client_identifier`:
            # Chrome --> chrome_103, chrome_104, chrome_105
            # Firefox --> firefox_102, firefox_104
            # Opera --> opera_89, opera_90
            # Safari --> safari_15_3, safari_15_6_1, safari_16_0
            # iOS --> safari_ios_15_5, safari_ios_15_6, safari_ios_16_0
            # iPadOS --> safari_ios_15_6
            client_identifier='chrome_105'
        )
        self.user_agent = 'MR_APP/9.84.0/StiffCock/F4-RT/1.33.7'
        self.common_headers = {
            'HTTP_X_TIMEZONE': 'Asia/Tokyo',
            'x-idfv': secrets.token_hex(int(17 / 2)),
            'x-ad': str(uuid.uuid4()),
            'x-hw': 'intel',
            'x-network-status': '2',
            'x-os-push': '1',
            'x-client-unixtime': '', # TODO
            'x-adjust-adid': secrets.token_hex(int(33 / 2))
        }

        self.lang = 'ja' # Language
        self.id = ''     # Mirrativ Id
        self.unique = '' # Account UUID

    def login(self, id: str, unique: str):
        self.id = id
        self.unique = unique

    def my_info(self):
        resp = self.session.get(
            'https://www.mirrativ.com/api/user/me',
            headers=dict(**self.common_headers, **{
                'User-Agent': self.user_agent,
                'Accept-Language': 'ja-jp',
                'Connection': 'keep-alive',
                'x-referer': 'my_page',
                'Cookie': 'lang={}; mr_id={}; f={};'.format(self.lang, self.id, self.unique)
            }),
            # cookies={
            #     'lang': self.lang,
            #     'mr_id': self.id,
            #     'f': self.unique
            # },
            insecure_skip_verify=True
        )
        if resp.status_code != 200:
            return None
        return AttrDict(json.loads(resp.text))

    def onlive_apps(self):
        resp = self.session.get(
            'https://www.mirrativ.com/api/app/onlive_apps',
            headers=dict(**self.common_headers, **{
                'User-Agent': self.user_agent,
                'Accept-Language': 'ja-jp',
                'Connection': 'keep-alive',
                'x-referer': 'home.select',
                'Cookie': 'lang={}; mr_id={}; f={};'.format(self.lang, self.id, self.unique)
            }),
            # cookies={
            #     'lang': self.lang,
            #     'mr_id': self.id,
            #     'f': self.unique
            # },
            insecure_skip_verify=True
        )
        if resp.status_code != 200:
            return None
        return AttrDict(json.loads(resp.text))

    def live_info(self, live_id: str):
        if live_id is None:
            return None

        resp = self.session.get(
            'https://www.mirrativ.com/api/live/live',
            params={
                'live_id': live_id
            },
            headers=dict(**self.common_headers, **{
                'User-Agent': self.user_agent,
                'Accept-Language': 'ja-jp',
                'Connection': 'keep-alive',
                'x-referer': 'live_view',
                'Cookie': 'lang={}; mr_id={}; f={};'.format(self.lang, self.id, self.unique)
            }),
            # cookies={
            #     'lang': self.lang,
            #     'mr_id': self.id,
            #     'f': self.unique
            # },
            insecure_skip_verify=True
        )
        if resp.status_code != 200:
            return None
        return AttrDict(json.loads(resp.text))

    def live_status(self, live_id: str):
        if live_id is None:
            return None

        resp = self.session.get(
            'https://www.mirrativ.com/api/live/get_streaming_url',
            params={
                'live_id': live_id
            },
            headers=dict(**self.common_headers, **{
                'User-Agent': self.user_agent,
                'Accept-Language': 'ja-jp',
                'Connection': 'keep-alive',
                'x-referer': 'live_view',
                'Cookie': 'lang={}; mr_id={}; f={};'.format(self.lang, self.id, self.unique)
            }),
            # cookies={
            #     'lang': self.lang,
            #     'mr_id': self.id,
            #     'f': self.unique
            # },
            insecure_skip_verify=True
        )
        if resp.status_code != 200:
            return None
        return AttrDict(json.loads(resp.text))

    def live_comments(self, live_id: str):
        if live_id is None:
            return None

        resp = self.session.get(
            'https://www.mirrativ.com/api/live/live_comments',
            params={
                'live_id': live_id
            },
            headers=dict(**self.common_headers, **{
                'User-Agent': self.user_agent,
                'Accept-Language': 'ja-jp',
                'Connection': 'keep-alive',
                'x-referer': 'live_view',
                'Cookie': 'lang={}; mr_id={}; f={};'.format(self.lang, self.id, self.unique)
            }),
            # cookies={
            #     'lang': self.lang,
            #     'mr_id': self.id,
            #     'f': self.unique
            # },
            insecure_skip_verify=True
        )
        if resp.status_code != 200:
            return None
        return AttrDict(json.loads(resp.text))

    def join_live(self, live_id: str):
        live_info = self.live_info(live_id)
        if live_info is None:
            self.logger.error('配信情報の取得に失敗しました')
            return

        notice_resp = self.session.get(
            'https://www.mirrativ.com/api/event/notice',
            params={
                'type': '2',
                'live_id': live_id
            },
            headers=dict(**self.common_headers, **{
                'User-Agent': self.user_agent,
                'Accept-Language': 'ja-jp',
                'Connection': 'keep-alive',
                'Cookie': 'lang={}; mr_id={}; f={};'.format(self.lang, self.id, self.unique)
            }),
            # cookies={
            #     'lang': self.lang,
            #     'mr_id': self.id,
            #     'f': self.unique
            # },
            insecure_skip_verify=True
        )

        live_comments = self.live_comments(live_id)
        if live_comments is None:
            self.logger.error('コメントの取得に失敗しました')
            return

        live_status = self.live_status(live_id)
        if live_info is None:
            self.logger.error('配信情報の取得に失敗しました')
            return

        if live_status.status.ok != 1 | live_status.is_live == 0:
            self.logger.error('配信は終了しています')
            return

        if live_status.is_private == 1:
            self.logger.error('配信はプライベートです')
            return

        # Send JoinLog
        self.comment(live_id, 3, '')

    # TODO
    def polling(self, live_id: str):
        if live_id is None:
            return None

        resp = self.session.post(
            'https://www.mirrativ.com/api/live/live_polling',
            data={
                'live_id': live_id,
                'live_user_key': '', # ???
                'is_ui_hidden': '0'
            },
            headers=dict(**self.common_headers, **{
                'User-Agent': self.user_agent,
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept-Language': 'ja-jp',
                'Connection': 'keep-alive',
                'x-referer': 'live_view',
                'Cookie': 'lang={}; mr_id={}; f={};'.format(self.lang, self.id, self.unique)
            }),
            # cookies={
            #     'lang': self.lang,
            #     'mr_id': self.id,
            #     'f': self.unique
            # },
            insecure_skip_verify=True
        )
        if resp.status_code != 200:
            return None
        return AttrDict(json.loads(resp.text))

    # Type
    # 1 = Normal Message,
    # 2 = ???,
    # 3 = Join Message
    def comment(self, live_id: str, type: int, message: str):
        if live_id is None:
            return

        resp = self.session.post(
            'https://www.mirrativ.com/api/live/live_comment',
            data={
                'live_id': live_id,
                'comment': message,
                'type': str(type)
            },
            headers=dict(**self.common_headers, **{
                'User-Agent': self.user_agent,
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept-Language': 'ja-jp',
                'Connection': 'keep-alive',
                'x-referer': 'live_view',
                'Cookie': 'lang={}; mr_id={}; f={};'.format(self.lang, self.id, self.unique)
            }),
            # cookies={
            #     'lang': self.lang,
            #     'mr_id': self.id,
            #     'f': self.unique
            # },
            proxy={
                'http': 'http://localhost:8788'
            },
            insecure_skip_verify=True
        )
        if resp.status_code != 200:
            self.logger.error('コメントの送信に失敗しました')
