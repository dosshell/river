import json
from typing import List


class Settings:
    def __init__(self):
        self.auth_file: str = None
        self.blacklist: List = []
        self.cache_file: str = None
        self.clear_cache: bool = False
        self.daemon: bool = False
        self.email: bool = False
        self.fetch: bool = False
        self.email_to: str = None
        self.gmail_username: str = None
        self.gmail_password: str = None
        self.avanza_username: str = None
        self.avanza_password: str = None
        self.avanza_private_key: str = None

    def read_args(self, args):
        if args.config_file is not None:
            with open(args.config_file) as f:
                fc = json.load(f)
            for key in self.config_keys():
                if key in fc:
                    setattr(self, key, fc[key])
        for key in self.config_keys():
            v = getattr(args, key)
            if v is not None:
                setattr(self, key, v)
        if self.auth_file is not None:
            with open(self.auth_file) as f:
                fa = json.load(f)
            for key in self.auth_keys():
                if key in fa:
                    setattr(self, key, fa[key])

    def __str__(self):
        d = {}
        for key in vars(self).keys():
            d[key] = getattr(self, key)
        for key in self.pass_keys():
            if d[key] is not None:
                d[key] = '******'
        return str(d)

    def config_keys(self):
        return [x for x in vars(self).keys() if x not in self.auth_keys()]

    def auth_keys(self):
        return ["gmail_username", "gmail_password", "avanza_username", "avanza_password", "avanza_private_key"]

    def pass_keys(self):
        return ['gmail_password', 'avanza_password', 'avanza_private_key']
