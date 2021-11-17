from pypresence import Presence
from configparser import ConfigParser
from time import sleep


import logging


log = logging.getLogger(__name__)
rpc = None


kwargs_keyword = {
    "State": "state",
    "Details": "details",
    "StartTime": "start",
    "EndTime": "end",
    "LargeImage": "large_image",
    "LargeImageTooltip": "large_text",
    "SmallImage": "small_image",
    "SmallImageTooltip": "small_text",
    "ProcessID": "pid",
    "Button": "buttons"
}


def format_button(btn_str: str):
    btn = list(map(lambda x: x.rstrip().lstrip(), btn_str.split(',')))
    btn_url = list(map(lambda y: y.split('*'), btn))
    btn_result = []
    for item in btn_url:
        btn_result.append({"label": str(item[0]).rstrip(), "url": str(item[1]).lstrip()})
    return btn_result


class Validate:

    def __init__(self, connected: bool):
        self.connected = connected
        self.result = {}
        self.result_kwargs()

    def result_kwargs(self):
        parser = ConfigParser()
        parser.read('config.ini')
        client_id = parser.get('Discord', 'client_id')
        for item in kwargs_keyword:
            if len((parser.get('Input', item))) > 1:
                self.result.update({f"{kwargs_keyword[item]}": f"{parser.get('Input', item)}"})
        if 'buttons' in list(self.result.keys()):
            self.result['buttons'] = format_button(self.result['buttons'])
        Run(client_id=client_id, connected=self.connected, **self.result)


class Run:

    def __init__(self, client_id, connected, **kwargs):
        self.kwargs = kwargs
        self.client = client_id
        self.connected = connected
        self.connect()

    def connect(self):
        if not self.connected:
            global rpc
            rpc = Presence(str(self.client))
            log.info('Connecting to discord API..')
            rpc.connect()
            log.info('Connected to discord API')
        self.update()

    def update(self):
        global rpc
        log.info('Rich Presence updated')
        rpc.update(**self.kwargs)
        loop()


def loop():
    default = None
    while True:
        parser = ConfigParser()
        parser.read('config.ini')
        if default != list(i[1] for i in parser['Input'].items()):
            if default is not None:
                log.info('New changes detected, RPC updated.')
                validate(connected=True)
            default = list(i[1] for i in parser['Input'].items())
        sleep(5)


validate = Validate