"""
boolean_retrieval.py
---------------------
Implements Boolean query processing on top of the inverted index.

Supported query syntax:
    term1 AND term2
    term1 OR term2
    NOT term1
    ( ... )         parentheses for grouping
    Any combination, e.g.  (cat OR dog) AND NOT bird

Design choice: operator precedence is NOT > AND > OR (the standard IR
convention), and this is implemented with a small recursive-descent
parser rather than Python's eval() -- eval() on raw user input would be
an unsafe/unpredictable way to build a Boolean query engine.
"""

from index_builder import tokenize

PRECEDENCE_NOTE = "Operator precedence: NOT > AND > OR"


class BooleanRetrieval:
    def __init__(self, inverted_index, all_doc_ids):
        self.index = inverted_index
        self.all_docs = set(all_doc_ids)  # universe, needed to evaluate NOT

    def _postings(self, term):
        return set(self.index.get(term.lower(), []))

    def search(self, query):
        """
        Evaluate a Boolean query string and return a sorted list of
        matching document IDs.
        """
        tokens = self._lex(query)
        self._tokens = tokens
        self._pos = 0
        result = self._parse_or()
        if self._pos != len(self._tokens):
            raise ValueError(f"Unexpected token near: {self._tokens[self._pos:]}")
        return sorted(result)

    # ---- Lexer -----------------------------------------------------
    def _lex(self, query):
        query = query.replace("(", " ( ").replace(")", " ) ")
        raw_tokens = query.split()
        tokens = []
        for tok in raw_tokens:
            upper = tok.upper()
            if upper in ("AND", "OR", "NOT", "(", ")"):
                tokens.append(upper if upper != "(" and upper != ")" else tok)
            else:
                tokens.append(tok)
        return tokens

    # ---- Recursive-descent parser (precedence: OR < AND < NOT) -----
    def _parse_or(self):
        left = self._parse_and()
        while self._peek() == "OR":
            self._advance()
            right = self._parse_and()
            left = left | right
        return left

    def _parse_and(self):
        left = self._parse_not()
        while self._peek() == "AND":
            self._advance()
            right = self._parse_not()
            left = left & right
        return left

    def _parse_not(self):
        if self._peek() == "NOT":
            self._advance()
            operand = self._parse_not()
            return self.all_docs - operand
        return self._parse_atom()

    def _parse_atom(self):
        tok = self._peek()
        if tok == "(":
            self._advance()
            result = self._parse_or()
            if self._peek() != ")":
                raise ValueError("Missing closing parenthesis")
            self._advance()
            return result
        elif tok is None:
            raise ValueError("Unexpected end of query")
        else:
            self._advance()
            return self._postings(tok)

    def _peek(self):
        if self._pos < len(self._tokens):
            return self._tokens[self._pos]
        return None

    def _advance(self):
        self._pos += 1
