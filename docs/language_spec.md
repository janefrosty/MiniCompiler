# MiniCompiler Language Specification (Lexical)

## Character Set
UTF-8. Whitespace: space, tab, \n, \r.

## Tokens (EBNF)

### Keywords
keyword = 'if' | 'else' | 'while' | 'for' | 'int' | 'float' | 'bool' |
'true' | 'false' | 'void' | 'struct' | 'fn' | 'return';
text### Identifiers
identifier = letter { letter | digit | '_' };
text### Literals
- int_literal = ['-'] digit { digit };
- float_literal = ['-'] digit { digit } '.' digit { digit };
- string_literal = '"' { any } '"';
- bool_literal = 'true' | 'false';

### Operators & Delimiters
+ - * / % == != < <= > >= && || ! = ( ) { } [ ] ; , . ->

### Comments
// single-line
/* multi-line */

**Соответствует LANG-1..LANG-6.**
