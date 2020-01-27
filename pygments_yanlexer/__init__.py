from pygments.lexer import RegexLexer, include, bygroups, words, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Whitespace


class YanLexer(RegexLexer):
    name = 'Yan'
    aliases = ['yan']
    filenames = ['*.yan']
