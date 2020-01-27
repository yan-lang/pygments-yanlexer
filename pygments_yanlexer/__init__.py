from pygments.lexer import RegexLexer, include, bygroups, words, default, using, this
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Whitespace, Error


class YanLexer(RegexLexer):
    name = 'Yan'
    aliases = ['yan']
    filenames = ['*.yan']

    tokens = {
        'whitespace': [
            (r'\n', Text),
            (r'\s+', Text),
            # (r'\\\n', Text),  # line continuation
            (r'//(\n|[\w\W]*?[^\\]\n)', Comment.Single),
            (r'/(\\\n)?[*][\w\W]*?[*](\\\n)?/', Comment.Multiline),
            # Open until EOF, so no ending delimiter
            (r'/(\\\n)?[*][\w\W]*', Comment.Multiline),
        ],
        'root': [
            include('whitespace'),
            # functions
            (r'(func)(\s+)'  # func
             r'([a-zA-Z_]\w*)',  # method name
             bygroups(Keyword, Text, Name.Function)),
            default('statement'),
        ],
        'statement': [
            include('whitespace'),
            include('statements'),
            # ('[{}]', Punctuation),
            (';', Punctuation, '#pop'),
        ],
        'function': [
            include('whitespace'),
            include('statements'),
            (';', Punctuation),
            (r'\{', Punctuation, '#push'),
            (r'\}', Punctuation, '#pop'),
        ],
        'string': [
            (r'"', String, '#pop'),
            (r'\\([\\abfnrtv"\']|x[a-fA-F0-9]{2,4}|'
             r'u[a-fA-F0-9]{4}|U[a-fA-F0-9]{8}|[0-7]{1,3})', String.Escape),
            (r'[^\\"\n]+', String),  # all other characters
            (r'\\\n', String),  # line continuation
            (r'\\', String),  # stray backslash
        ],
        'statements': [
            (r'(")', String, 'string'),
            (r"(')(\\.|\\[0-7]{1,3}|\\x[a-fA-F0-9]{1,2}|[^\\\'\n])(')",
             bygroups(String.Char, String.Char, String.Char)),
            (r'(\d+\.\d*|\.\d+|\d+)', Number.Float),  # optimized
            (r'\d+', Number.Integer),
            (r'\*/', Error),
            (r'[~!%^&*+=|?<>/-]', Operator),
            (r'[()\[\].:,\{\}]|->', Punctuation),
            (words(('func', 'break', 'continue', 'else', 'if', 'return', 'while', 'var'),
                   suffix=r'\b'), Keyword),
            (r'(bool|int|float|char|string)\b',
             Keyword.Type),
            (r'(true|false)\b', Keyword.Constant),
            (r'[a-zA-Z_]\w*', Name),
        ]
    }


if __name__ == '__main__':
    lexer = YanLexer()
    text = """
    func power(base: int, e: int) -> int {
    var i = 0;
    var result = 1;
    while(i < e) {
        result *= base;
        i += 1;
    }
    return result;
}
    """
    for index, token, value in lexer.get_tokens_unprocessed(text):
        print(index, token, value)