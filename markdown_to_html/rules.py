#!/usr/env/python3
# -*- coding: utf-8 -*-

class Rule:
    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True

class HeadingRule(Rule):
    '''
    标题占一行，字数小于70，且不以冒号结尾
    '''

    type = 'heading'

    def condition(self, block):
        return not '\n' in block and len(block) < 70 and not block[-1] == ':'

class TitleRule(HeadingRule):
    '''
    题目首先是标题，其次必须是在文档第一个块
    '''
    type = 'title'
    first = True

    def condition(self, block):
        if not self.first: return False
        self.first = False
        return HeadingRule.condition(self, block)

class ListItemRule(Rule):
    '''
    列表内的具体项，以连字符或者星号开始。此处先处理连字符。
    '''
    type = 'listitem'
    def condition(self, block):
        return block[0] == '-'

    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block[1:].strip())
        handler.end(self.type)
        return True

class UnorderedListRule(Rule):
    '''
    列表项从不是列表的块和随后的列表项之间开始，在最后一个连续列表项之后结束
    '''
    type = 'ulist'
    inside = False
    def condition(self, block):
        return True
    def action(self, block, handler):
        if not self.inside and ListItemRule.condition(self, block):
            inside = True
            handler.start(self.type)
        elif self.inside and not ListItemRule.condition(self, block):
            handler.end(self.type)
            inside = False
        # 无论是否适用规则，都要继续去尝试别的规则
        return False

class ParagraphRule(Rule):
    '''
    段落是其他规则没有覆盖到的块
    '''
    type = 'paragraph'
    def condition(self, block):
        return True

