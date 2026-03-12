# MiniCompiler Syntax Specification (Sprint 2)

## Context-Free Grammar (EBNF)

program         ::= function_decl*

function_decl   ::= 'fn' IDENTIFIER '(' param_list? ')' '{' statement* '}'

param_list      ::= param (',' param)*
param           ::= 'int' IDENTIFIER

statement       ::= var_decl
                  | return_stmt
                  | expr_stmt

var_decl        ::= 'int' IDENTIFIER '=' expression ';'

return_stmt     ::= 'return' expression ';'

expr_stmt       ::= expression ';'

expression      ::= equality

equality        ::= comparison (('==' | '!=') comparison)*
comparison      ::= term (('<' | '<=' | '>' | '>=') term)*
term            ::= factor (('+' | '-') factor)*
factor          ::= unary (('*' | '/') unary)*
unary           ::= ('!' | '-') unary | primary

primary         ::= INT_LITERAL | IDENTIFIER | '(' expression ')'

# Поддержка комментариев и whitespace уже из Lexer
