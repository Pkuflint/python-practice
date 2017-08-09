#!/usr/env/python3
# -*- coding: utf-8 -*-

import sys, re
from handlers import *
from rules import *
from util import *
from re_filter import *

import logging
logging.basicConfig(level=logging.INFO, filename='log')

logging.info('start programming')
class Parser:
    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.filters = []

    def addRule(self, rule):
        self.rules.append(rule)

    def addFilter(self, pattern, name):
        def filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)
        self.filters.append(filter)

    def parse(self, file):
        self.handler.start('document')
        for block in blocks(file):
            for filter in self.filters:
                block = filter(block, self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    last = rule.action(block, self.handler)
                    if last: break
        self.handler.end('document')

class BasicTextParser(Parser):
    logging.info('initialing parser')
    def __init__(self, handler):
        Parser.__init__(self, handler)
        self.addRule(UnorderedListRule())
        self.addRule(ListItemRule())
        self.addRule(TitleRule())
        self.addRule(HeadingRule())
        self.addRule(ParagraphRule())

handler = HTMLRenderer()
parser = BasicTextParser(handler)
filter_list = Filter()
for item in filter_list:
    parser.addFilter(item[1], item[0])

parser.parse(sys.stdin)