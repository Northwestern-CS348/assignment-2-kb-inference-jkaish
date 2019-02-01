import unittest
import read, copy
from logical_classes import *
from student_code import KnowledgeBase


class KBTest(unittest.TestCase):

    def setUp(self):
        # Assert starter facts
        file = 'statements_kb3.txt'
        self.data = read.read_tokenize(file)
        data = read.read_tokenize(file)
        self.KB = KnowledgeBase([], [])
        for item in data:
            if isinstance(item, Fact) or isinstance(item, Rule):
                self.KB.kb_assert(item)

    def test1(self):
        ask1 = read.parse_input("fact: (goodman a)")
        answer = self.KB.kb_ask(ask1)
        self.assertEqual(answer[0].bindings, [])

        self.KB.kb_retract(ask1)

        answer = self.KB.kb_ask(ask1)
        self.assertEqual(answer[0].bindings, [])

    def test2(self):
        ask1 = read.parse_input("fact: (hero a)")
        ask2 = read.parse_input("fact: (goodman a)")
        self.KB.kb_retract(ask2)

        answer = self.KB.kb_ask(ask2)
        self.assertEqual(answer[0].bindings, [])

        self.KB.kb_retract(ask1)
        answer = self.KB.kb_retract(ask2)
        self.assertFalse(answer)



