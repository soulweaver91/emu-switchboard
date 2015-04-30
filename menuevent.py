#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Soulweaver'


MenuEventType = {
    "none"           : 0,
    "up"             : 1,
    "down"           : 2,
    "left"           : 3,
    "right"          : 4,
    "accept"         : 5,
    "cancel"         : 6,
    "information"    : 7,
    "return_to_menu" : 8
}


class MenuEvent:
    def __init__(self, kind=MenuEventType["none"], repeat=False):
        self.kind = kind
        self.repeat = repeat
