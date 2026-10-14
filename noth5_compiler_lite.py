# noth5_compiler_lite.py V3 - Independent DSL with Lexer + Parser + AST + Codegen
import re, sys

class Token:
    def __init__(self, typ, val, line): self.type=typ; self.value=val; self.line=line

class Lexer:
    SPEC = [
        ('STRING', r'"[^"]*"'),
        ('NUMBER', r'\d+'),
        ('GTE', r'>='), ('LTE', r'<='), ('EQEQ', r'=='),
        ('LPAREN', r'\('), ('RPAREN', r'\)'), ('COMMA', r','),
        ('GT', r'>'), ('LT', r'<'), ('EQ', r'='),
        ('PLUS', r'\+'), ('MINUS', r'-'),
        ('KEYWORD', r'\b(OPEN|DB|LET|IF|THEN|ELSE|ENDIF|FOR|IN|ENDFOR|CREATE|TABLE|INSERT|INTO|VALUES|RENDER|INSIDE|BUBBLE|FROM|SELECT|SLIDER|RATING|CALENDAR|TABLE|CHART|QR|DROPDOWN|MAP|YOUTUBE|VALUE|COLOR|LABEL|WHERE)\b'),
        ('IDENT', r'[A-Za-z_][A-Za-z0-9_]*'),
        ('SKIP', r'[ \t\n\r]+'),
    ]
    def tokenize(self, code):
        tokens=[]; pos=0; line=1
        while pos < len(code):
            m=None
            for typ,pat in self.SPEC:
                mm=re.compile(pat).match(code,pos)
                if mm:
                    if typ!='SKIP': tokens.append(Token(typ,mm.group(),line))
                    line+=mm.group().count('\n'); pos=mm.end(); m=True; break
            if not m: raise SyntaxError(f"Lexer error line {line}: '{code[pos:pos+30]}'")
        return tokens

# --- AST Nodes ---
class ASTNode: pass
class Program(ASTNode):
    def __init__(self, stmts): self.statements=stmts
class OpenDb(ASTNode):
    def __init__(self, path): self.path=path
class Let(ASTNode):
    def __init__(self, name, value): self.name=name; self.value=value
class Render(ASTNode):
    def __init__(self, ctype, params): self.ctype=ctype; self.params=params
class If(ASTNode):
    def __init__(self, cond, then_stmts, else_stmts): self.cond=cond; self.then_stmts=then_stmts; self.else_stmts=else_stmts
class For(ASTNode):
    def __init__(self, var, coll, body): self.var=var; self.coll=coll; self.body=body

class Parser:
    def __init__(self, tokens): self.t=tokens; self.p=0
    def peek(self): return self.t[self.p] if self.p < len(self.t) else None
    def consume(self, val
