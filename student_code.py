import read, copy
from util import *
from logical_classes import *

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB
        Args:
            fact_rule (Fact|Rule) - the fact or rule to be added
        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = True

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

    def kb_retract(self, fact_or_rule):
        """Retract a fact from the KB

        Args:
            fact (Fact) - Fact to be retracted

        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [fact_or_rule])
        ####################################################
        # Student code goes here
        if factq(fact_or_rule):
            f = self._get_fact(fact_or_rule)
            if f.asserted:
                f.asserted = False
                if not f.supported_by:
                    for supported_fact in f.supports_facts:
                        supported_fact = self._get_fact(supported_fact)
                        f_index = supported_fact.supported_by.index(f)
                        f_to_remove = supported_fact.supported_by[f_index]
                        r_to_remove = supported_fact.supported_by[f_index + 1]
                        supported_fact.supported_by.remove(f_to_remove)
                        supported_fact.supported_by.remove(r_to_remove)
                        if not supported_fact.supported_by and not supported_fact.asserted:
                            for ff in supported_fact.supports_facts:
                                self.kb_retract(ff)
                            # for rr in supported_fact.supports_rules:
                            #     self.remove_rule(rr)
                            self.facts.remove(supported_fact)

                    for supported_rule in f.supports_rules:
                        r_index = supported_rule.supported_by.index(f)
                        f_to_remove = supported_rule.supported_by[r_index]
                        r_to_remove = supported_rule.supported_by[r_index + 1]
                        supported_rule.supported_by.remove(f_to_remove)
                        supported_rule.supported_by.remove(r_to_remove)
                        if not supported_rule.supported_by and not supported_rule.asserted:
                            for ff in supported_rule.supports_facts:
                                self.kb_retract(ff)
                            # for rr in supported_rule.supports_rules:
                            #     self.remove_rule(rr)
                            # self.rules.remove(supported_rule)
                    for rule in self.rules:
                        self.remove_rule(rule)

                    self.facts.remove(f)
            elif not f.supported_by:
                self.facts.remove(f)

    def remove_rule(self, rule):
        r = self._get_rule(rule)
        if r and not r.asserted and not r.supported_by:
            for ff in r.supports_facts:
                ff = self._get_fact(ff)
                r_index = ff.supported_by.index(r)
                f_to_remove = ff.supported_by[r_index - 1]
                r_to_remove = ff.supported_by[r_index]
                ff.supported_by.remove(f_to_remove)
                ff.supported_by.remove(r_to_remove)
                self.kb_retract(ff)
            for rr in r.supports_rules:
                self.remove_rule(rr)
            self.rules.remove(r)
        

class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing            
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        # Student code goes here
        to_check = rule.lhs[0]
        res = match(to_check, fact.statement)
        if res:
            if len(rule.lhs) == 1:
                new_fact_statement = instantiate(rule.rhs, res)
                new_fact = Fact(new_fact_statement, supported_by=[fact, rule])
                fact.supports_facts.append(new_fact)
                rule.supports_facts.append(new_fact)
                kb.kb_add(new_fact)
            else:
                new_lhs = []
                for conds in rule.lhs[1:]:
                    new_lhs.append(instantiate(conds, res))
                new_rhs = instantiate(rule.rhs, res)
                new_rule = Rule([new_lhs, new_rhs], supported_by=[fact, rule])
                fact.supports_rules.append(new_rule)
                rule.supports_rules.append(new_rule)
                kb.kb_add(new_rule)
