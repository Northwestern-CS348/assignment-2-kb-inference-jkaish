import unittest
import read, copy
from logical_classes import *
from student_code import KnowledgeBase


class KBTest(unittest.TestCase):

    def setUp(self):
        # Assert starter facts
        file = 'statements_kb2.txt'
        self.data = read.read_tokenize(file)
        data = read.read_tokenize(file)
        self.KB = KnowledgeBase([], [])
        for item in data:
            if isinstance(item, Fact) or isinstance(item, Rule):
                self.KB.kb_assert(item)

    def test1(self):
        ask_string = "fact: (defeatable {})"
        ask1 = read.parse_input(ask_string.format("Sarorah"))
        answer = self.KB.kb_ask(ask1)
        self.assertFalse(answer)

        ask2 = read.parse_input(ask_string.format("Nosliw"))
        answer = self.KB.kb_ask(ask2)
        self.assertFalse(answer)




