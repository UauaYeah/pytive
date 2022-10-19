from logging import getLogger, basicConfig, INFO
from typing import Optional
from enum import Enum

import requests
import secrets
import uuid

from attrdict import AttrDict

logger = getLogger('Pytive')
basicConfig(
    level=INFO,
    format='[%(levelname)s] %(message)s'
)

class CommentType(Enum):
    NORMAL: int = 1
    JOIN_LOG: int = 3

class Pytive:
    def __init__(self):
        self.session = requests.session()
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

        self.lang   = 'ja' # Language
        self.id     = ''   # Mirrativ Id
        self.unique = ''   # Account UUID

    def login(self, id: str, unique: str):
        self.id = id
        self.unique = unique

    def my_profile(self) -> Optional[AttrDict]:
        resp = self.session.get(
            'https://www.mirrativ.com/api/user/me',
            headers=dict(**self.common_headers, **{
                'User-Agent': self.user_agent,
                'Accept': '*/*',
                'Accept-Language': 'ja-jp',
                'Connection': 'keep-alive',
                'x-referer': 'my_page',
                'Cookie': 'lang={}; mr_id={}; f={};'.format(self.lang, self.id, self.unique)
            })
        )
        if resp.status_code != 200:
            return None
        return AttrDict(resp.json())

    def profile(self, user_id: str) -> Optional[AttrDict]:
        resp = self.session.get(
            'https://www.mirrativ.com/api/user/profile',
            params={
                'user_id': user_id
            },
            headers=dict(**self.common_headers, **{
                'User-Agent': self.user_agent,
                'Accept': '*/*',
                'Accept-Language': 'ja-jp',
                'Connection': 'keep-alive',
                'x-referer': 'profile',
                'Cookie': 'lang={}; mr_id={}; f={};'.format(self.lang, self.id, self.unique)
            })
        )
        if resp.status_code != 200:
            return None
        return AttrDict(resp.json())

    def onlive_apps(self) -> Optional[AttrDict]:
        resp = self.session.get(
            'https://www.mirrativ.com/api/app/onlive_apps',
            headers=dict(**self.common_headers, **{
                'User-Agent': self.user_agent,
                'Accept': '*/*',
                'Accept-Language': 'ja-jp',
                'Connection': 'keep-alive',
                'x-referer': 'home.select',
                'Cookie': 'lang={}; mr_id={}; f={};'.format(self.lang, self.id, self.unique)
            })
        )
        if resp.status_code != 200:
            return None
        return AttrDict(resp.json())

    def live_info(self, live_id: str) -> Optional[AttrDict]:
        if live_id is None:
            return None

        resp = self.session.get(
            'https://www.mirrativ.com/api/live/live',
            params={
                'live_id': live_id
            },
            headers=dict(**self.common_headers, **{
                'User-Agent': self.user_agent,
                'Accept': '*/*',
                'Accept-Language': 'ja-jp',
                'Connection': 'keep-alive',
                'x-referer': 'live_view',
                'Cookie': 'lang={}; mr_id={}; f={};'.format(self.lang, self.id, self.unique)
            })
        )
        if resp.status_code != 200:
            return None
        return AttrDict(resp.json())

    def live_status(self, live_id: str) -> Optional[AttrDict]:
        if live_id is None:
            return None

        resp = self.session.get(
            'https://www.mirrativ.com/api/live/get_streaming_url',
            params={
                'live_id': live_id
            },
            headers=dict(**self.common_headers, **{
                'User-Agent': self.user_agent,
                'Accept': '*/*',
                'Accept-Language': 'ja-jp',
                'Connection': 'keep-alive',
                'x-referer': 'live_view',
                'Cookie': 'lang={}; mr_id={}; f={};'.format(self.lang, self.id, self.unique)
            })
        )
        if resp.status_code != 200:
            return None
        return AttrDict(resp.json())

    def live_comments(self, live_id: str) -> Optional[AttrDict]:
        if live_id is None:
            return None

        resp = self.session.get(
            'https://www.mirrativ.com/api/live/live_comments',
            params={
                'live_id': live_id
            },
            headers=dict(**self.common_headers, **{
                'User-Agent': self.user_agent,
                'Accept': '*/*',
                'Accept-Language': 'ja-jp',
                'Connection': 'keep-alive',
                'x-referer': 'live_view',
                'Cookie': 'lang={}; mr_id={}; f={};'.format(self.lang, self.id, self.unique)
            })
        )
        if resp.status_code != 200:
            return None
        return AttrDict(resp.json())

    def live_polling(self, live_id: str) -> Optional[AttrDict]:
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
                'Accept': '*/*',
                'Accept-Language': 'ja-jp',
                'Connection': 'keep-alive',
                'x-referer': 'live_view',
                'Cookie': 'lang={}; mr_id={}; f={};'.format(self.lang, self.id, self.unique)
            })
        )
        if resp.status_code != 200:
            return None
        return AttrDict(resp.json())

    def join_live(self, live_id: str):
        live_info = self.live_info(live_id)
        if live_info is None:
            logger.error('配信情報の取得に失敗しました')
            return

        if self.session.get(
            'https://www.mirrativ.com/api/event/notice',
            params={
                'type': '2',
                'live_id': live_id
            },
            headers=dict(**self.common_headers, **{
                'User-Agent': self.user_agent,
                'Accept': '*/*',
                'Accept-Language': 'ja-jp',
                'Connection': 'keep-alive',
                'Cookie': 'lang={}; mr_id={}; f={};'.format(self.lang, self.id, self.unique)
            })
        ).status_code != 200:
            return

        live_comments = self.live_comments(live_id)
        if live_comments is None:
            logger.error('コメントの取得に失敗しました')
            return

        live_status = self.live_status(live_id)
        if live_info is None:
            logger.error('配信情報の取得に失敗しました')
            return

        if live_status.status.ok != 1 | live_status.is_live == 0:
            logger.error('配信は終了しています')
            return

        if live_status.is_private == 1:
            logger.error('この配信はプライベートです')
            return

        # Send JoinLog
        self.comment(live_id, 3, '')

    def request_live(self, user_id: str, count: int = 1) -> Optional[AttrDict]:
        resp = self.session.post(
            'https://www.mirrativ.com/api/user/post_live_request',
            data={
                'count': str(count),
                'user_id': user_id,
                'where': 'profile'
            },
            headers=dict(**self.common_headers, **{
                'User-Agent': self.user_agent,
                'Accept': '*/*',
                'Accept-Language': 'ja-jp',
                'Connection': 'keep-alive',
                'x-referer': 'profile',
                'Cookie': 'lang={}; mr_id={}; f={};'.format(self.lang, self.id, self.unique)
            })
        )
        if resp.status_code != 200:
            logger.error('ライブリクエストに失敗しました (Code: {})'.format(resp.status_code))
            return None
        return AttrDict(resp.json())

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
                'Accept': '*/*',
                'Accept-Language': 'ja-jp',
                'Connection': 'keep-alive',
                'x-referer': 'live_view',
                'Cookie': 'lang={}; mr_id={}; f={};'.format(self.lang, self.id, self.unique)
            })
        )
        if resp.status_code != 200:
            logger.error('コメントの送信に失敗しました (Code: {})'.format(resp.status_code))
