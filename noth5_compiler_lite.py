# NOTH5 Compiler Lite V3 - FINAL - Real AST + Code Generator with Indentation
# Independent DSL:.noth5 -> Lexer -> Parser -> AST -> Python
import re
import sys

class Token:
    def __init__(self, typ, val, line):
        self.typ = typ
        self.val = val
        self.line = line

class Lexer:
    SPEC = [
        ('STRING', r'"[^"]*"'),
        ('NUMBER', r'\d+'),
        ('GTE', r'>='),
        ('LTE', r'<='),
        ('EQEQ', r'=='),
        ('GT', r'>'),
        ('LT', r'<'),
        ('EQ', r'='),
        ('KEYWORD', r'\b(OPEN|DB|LET|IF|THEN|ELSE|ENDIF|FOR|IN|ENDFOR|CREATE|TABLE|INSERT|INTO|RENDER|INSIDE|BUBBLE|FROM|SELECT|SLIDER|RATING|CALENDAR|CHART|QR|DROPDOWN|VALUE|COLOR|LABEL)\b'),
        ('IDENT', r'[A-Za-z_][A-Za-z0-9_]*'),
        ('SKIP', r'[ \t\n\r]+'),
    ]
    def tokenize(self, code):
        tokens = []
        pos = 0
        line = 1
        while pos < len(code):
            ok = False
            for typ, pat in self.SPEC:
                m = re.compile(pat).match(code, pos)
                if m:
                    if typ!= 'SKIP':
                        tokens.append(Token(typ, m.group(), line))
                    line += m.group().count('\n')
                    pos = m.end()
                    ok = True
                    break
            if not ok:
                raise SyntaxError(f"Lexer line {line}: {code[pos:pos+20]}")
        return tokens

class ASTNode:
    def __init__(self, typ, line, data):
        self.typ = typ
        self.line = line
        self.data = data

class Parser:
    def __init__(self, tokens):
        self.toks = tokens
        self.pos = 0
        self.ast = []

    def peek(self):
        return self.toks[self.pos] if self.pos < len(self.toks) else None
    def consume(self, expect=None):
        t = self.peek()
        if not t:
            raise SyntaxError("Unexpected EOF")
        if expect and t.val!= expect:
            raise SyntaxError(f"Line {t.line}: expected {expect}, got {t.val}")
        self.pos += 1
        return t

    def parse(self):
        while self.peek():
            v = self.peek().val
            if v == 'OPEN': self.ast.append(self.parse_db())
            elif v == 'LET': self.ast.append(self.parse_let())
            elif v == 'IF': self.ast.append(self.parse_if())
            elif v == 'FOR': self.ast.append(self.parse_for())
            elif v == 'RENDER': self.ast.append(self.parse_render())
            elif v in ('CREATE','INSERT'): self.ast.append(self.parse_sql())
            else: self.pos += 1
        return self.ast

    def parse_db(self):
        t = self.consume('OPEN'); self.consume('DB')
        path = self.consume()
        return ASTNode('DB_OPEN', t.line, {'path': path.val})

    def parse_let(self):
        t = self.consume('LET')
        name = self.consume()
        self.consume('=')
        expr = self.consume()
        return ASTNode('LET', t.line, {'name': name.val, 'expr': expr.val})

    def parse_if(self):
        t = self.consume('IF')
        cond = []
        while self.peek() and self.peek().val!= 'THEN':
            cond.append(self.consume().val)
        self.consume('THEN')
        return ASTNode('IF', t.line, {'cond': ' '.join(cond)})

    def parse_for(self):
        t = self.consume('FOR')
        var = self.consume()
        self.consume('IN')
        col = self.consume()
        self.consume('THEN')
        return ASTNode('FOR', t.line, {'var': var.val, 'col': col.val})

    def parse_render(self):
        t = self.consume('RENDER')
        ctype = self.consume()
        self.consume('INSIDE'); self.consume('BUBBLE')
        params = {}
        while self.peek() and self.peek().val not in ('RENDER','OPEN','LET','IF','FOR','ENDIF','ENDFOR','ELSE','CREATE','INSERT'):
            if self.peek().val in ('VALUE','COLOR','LABEL'):
                k = self.consume().val.lower()
                v = self.consume().val
                params[k] = v
            else:
                break
        return ASTNode('RENDER', t.line, {'ctype': ctype.val, 'params': params})

    def parse_sql(self):
        t = self.consume()
        return ASTNode('SQL', t.line, {'kw': t.val})

class CodeGen:
    def __init__(self, ast):
        self.ast = ast
        self.lines = ["import eehim_db_lite", "import render", "db = None", ""]
        self.indent = 0

    def emit(self, s):
        self.lines.append(" "*self.indent + s)

    def generate(self):
        for n in self.ast:
            if n.typ == 'DB_OPEN':
                self.emit(f"db = eehim_db_lite.open({n.data['path']})")
            elif n.typ == 'LET':
                self.emit(f"{n.data['name'].lower()} = {n.data['expr']}")
            elif n.typ == 'IF':
                self.emit(f"if {n.data['cond'].lower()}:")
                self.indent += 1
            elif n.typ == 'FOR':
                self.emit(f"for {n.data['var'].lower()} in {n.data['col'].lower()}:")
                self.indent += 1
            elif n.typ == 'RENDER':
                c = n.data['ctype'].lower()
                p = n.data['params']
                if c == 'slider':
                    self.emit(f"render.render_slider_inside_bubble(value={p.get('value','75')}, color={p.get('color','\"#00ff88\"')}, label={p.get('label','\"Progress\"')})")
                else:
                    self.emit(f"render.render_{c}_inside_bubble({p})")
        return "\n".join(self.lines)

if __name__ == "__main__":
    src = sys.argv[1]
    with open(src) as f:
        code = f.read()
    tokens = Lexer().tokenize(code)
    ast = Parser(tokens).parse()
    py = CodeGen(ast).generate()
    out = src.replace('.noth5', '.py')
    with open(out, 'w') as o:
        o.write(py)
    print(f"[NOTH5 Lexer] {len(tokens)} tokens")
    print(f"[NOTH5 Parser] {len(ast)} AST nodes")
    print(f"[NOTH5 CodeGen] {out} - Real AST + indent, not regex")
