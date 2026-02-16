import pytest
from lexer.lexer import Lexer, TokenType

def load_source(filename: str) -> str:
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

# TEST-2: Valid tests
@pytest.mark.parametrize('test_file,first_token', [
    ('tests/lexer/valid/test_keywords.src', TokenType.KW_IF),
])
def test_valid_lexer(test_file, first_token):
    source = load_source(test_file)
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    assert len(tokens) > 5
    assert tokens[0].type == first_token
    assert tokens[-1].type == TokenType.EOF


# Создаём все тестовые файлы
def create_test_files():
    valid = {
        'test_keywords.src': 'if else while for int float bool true false void struct fn return',}
    
    for name, content in valid.items():
        with open(f'tests/lexer/valid/{name}', 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == '__main__':
    create_test_files()