#!/usr/env/python3
# -*- coding:utf-8 -*-
import logging
import re

logging.basicConfig(level=logging.INFO, filename='log')

class Handler:
    '''
    Handler会对文本进行html处理
    '''
    def callback(self, prefix, name, *args):
        method = getattr(self, prefix+name, None)
        try:
            return method(*args)
        except Exception:
            pass

    def start(self, name):
        self.callback('start_', name)
    def end(self, name):
        self.callback('end_', name)
    def sub(self, name):
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result is None: 
                result = match.group(0)
            return result
        return substitution

class HTMLRenderer(Handler):

    def start_document(self):
        print('<html><head><title>...</title></head><body>')
    def end_document(self):
        print('</body></html>')
    def start_paragraph(self):
        print('<p>')
    def end_paragraph(self):
        print('</p>')
    def start_heading(self):
        print('<h2>')
    def end_heading(self):
        print('</h2>')
    def start_title(self):
        print('<h1>')
    def end_title(self):
        print('</h1>')
    def start_ulist(self):
        print('<ul>')
    def end_ulist(self):
        print('</ul>')
    def start_listitem(self):
        print('<li>')
    def end_listitem(self):
        print('</li>')

    def sub_emphasis(self, match):
        return '<em>%s</em>' % match.group(1)
    def sub_italic(self, match):
        return '<i>%s</i>' % match.group(1)
    def sub_image(self, match):
        #links = re.split('["]', match.group(2))
        links = match.group(2).split('"') 

        if len(links) > 1:
            return '<img src="%s" alt="%s" title="%s">' % (links[0].strip(), match.group(1), links[1])
        else:
            return '<img src="%s" alt="%s">' % (match.group(2), match.group(1))

    def sub_url(self, match):
        logging.info('enter sub_url method')
        links = re.split('["]', match.group(2))
        # 非常不解的是，为什么下面的代码无法正常工作
        #links = match.group(2).split('"') 
        logging.info('here is the link: %s' % links)
        logging.info('this is shit!')
        if len(links) > 1:
            return '<a href="%s" title="%s">%s</a>' % (links[0].strip(), links[1], match.group(1))
        else:
            return '<a href="%s">%s</a>' % (match.group(2).strip(), match.group(1))
    
    def sub_mail(self, match):
        return '<a href="mailto:%s">%s</a>' % (match.group(1), match.group(1))

    def feed(self, data):
        print(data)
