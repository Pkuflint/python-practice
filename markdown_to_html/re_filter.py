#!/usr/env/python3
# -*- coding: utf-8 -*-

class Filter(list):
    def __init__(self):
        list.__init__(self)
        self.append(('emphasis', r'\*{2}(.+?)\*{2}'))
        self.append(('italic', r'\*(.+?)\*'))
        self.append(('image', r'\!\[(.*?)\]\((.*?)\)'))
        self.append(('url', r'\[(.*?)\]\((.*?)\)'))
        self.append(('mail', r'([\.\-\_a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+)'))