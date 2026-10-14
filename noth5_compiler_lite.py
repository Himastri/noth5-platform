# NOTH5 Compiler Lite V4 FINAL - Real AST + Nested Blocks + Indent Fix
import re
import sys

class Token:
    def __init__(self, typ, val, line):
        self.typ, self.val, self.line = typ, val, line

class Lexer:
    SPEC = [
        ('STRING', r'"[^"]*"'),
        ('NUMBER', r'\d+'),
        ('GTE', r'>='), ('LTE', r'<='), ('EQEQ', r'=='),
        ('GT', r'>'), ('LT', r'<'), ('EQ', r'='),
        ('PLUS', r'\+'), ('MINUS', r'-'), ('LPAREN', r'\('), ('RPAREN', r'\)'), ('COMMA', r','),
        ('KEYWORD', r'\b(OPEN|DB|LET|IF|THEN|ELSE|ENDIF|FOR|IN|ENDFOR|CREATE|TABLE|INSERT|INTO|RENDER|INSIDE|BUBBLE|FROM|SELECT|SLIDER|RATING|CALENDAR|CHART|QR|DROPDOWN|MAP|YOUTUBE|VIDEO|AUDIO|IMAGE|BUTTON|INPUT|CHECKBOX|RADIO|SWITCH|PROGRESS|AVATAR|BADGE|CARD|LIST|GRID|MODAL|TOOLTIP|ALERT|VALUE|COLOR|LABEL)\b'),
        ('IDENT', r'[A-Za-z_][A-Za-z0-9_]*'),
        ('SKIP', r'[ \t\n\r]+'),
        ('STAR', r'\*'),
    ]
    def tokenize(self, code):
        toks = []
        pos, line = 0, 1
        while pos < len(code):
            ok = False
            for typ, pat in self.SPEC:
                m = re.compile(pat).match(code, pos)
                if m:
                    if typ!= 'SKIP':
                        toks.append(Token(typ, m.group(), line))
                    line += m.group().count('\n')
                    pos = m.end()
                    ok = True
                    break
            if not ok:
                raise SyntaxError(f"Lexer line {line}: '{code[pos:pos+20]}'")
        return toks

class Node:
    def __init__(self, typ, line, **kw):
        self.typ = typ
        self.line = line
        self.__dict__.update(kw)

class Parser:
    def __init__(self, toks):
        self.t = toks
        self.p = 0

    def peek(self):
        return self.t[self.p] if self.p < len(self.t) else None

    def consume(self, exp=None):
        cur = self.peek()
        if not cur:
            raise SyntaxError("Unexpected EOF")
        if exp and cur.val!= exp:
            raise SyntaxError(f"Line {cur.line}: expected {exp}, got {cur.val}")
        self.p += 1
        return cur

    def parse_block(self, stop=()):
        nodes = []
        while self.peek() and self.peek().val not in stop:
            v = self.peek().val
            if v == 'OPEN':
                nodes.append(self.parse_db())
            elif v == 'LET':
                nodes.append(self.parse_let())
            elif v == 'IF':
                nodes.append(self.parse_if())
            elif v == 'FOR':
                nodes.append(self.parse_for())
            elif v == 'RENDER':
                nodes.append(self.parse_render())
            elif v in ('CREATE','INSERT'):
                nodes.append(self.parse_sql())
            else:
                raise SyntaxError(f"Line {self.peek().line}: unknown '{self.peek().val}' - typo not skipped")
        return nodes

    def parse_db(self):
        t = self.consume('OPEN'); self.consume('DB')
        path = self.consume()
        return Node('DB', t.line, path=path.val)

    def parse_let(self):
        t = self.consume('LET')
        name = self.consume()
        self.consume('=')
        expr_parts = []
        while self.peek() and self.peek().val not in ('OPEN','LET','IF','FOR','RENDER','CREATE','INSERT','ELSE','ENDIF','ENDFOR','FROM'):
            expr_parts.append(self.consume().val)
            if len(expr_parts) >= 10:
                break
        return Node('LET', t.line, name=name.val, expr=' '.join(expr_parts))

    def parse_if(self):
        t = self.consume('IF')
        cond = []
        while self.peek() and self.peek().val!= 'THEN':
            cond.append(self.consume().val)
        self.consume('THEN')
        then_body = self.parse_block(stop=('ELSE','ENDIF'))
        else_body = []
        if self.peek() and self.peek().val == 'ELSE':
            self.consume('ELSE')
            else_body = self.parse_block(stop=('ENDIF',))
        self.consume('ENDIF')
        return Node('IF', t.line, cond=' '.join(cond), then_body=then_body, else_body=else_body)

    def parse_for(self):
        t = self.consume('FOR')
        var = self.consume()
        self.consume('IN')
        col = self.consume()
        self.consume('THEN')
        body = self.parse_block(stop=('ENDFOR',))
        self.consume('ENDFOR')
        return Node('FOR', t.line, var=var.val, col=col.val, body=body)

    def parse_render(self):
        t = self.consume('RENDER')
        ctype = self.consume()
        self.consume('INSIDE'); self.consume('BUBBLE')
        params = {}
        while self.peek() and self.peek().val not in ('OPEN','LET','IF','FOR','RENDER','ELSE','ENDIF','ENDFOR','CREATE','INSERT','FROM'):
            if self.peek().val in ('VALUE','COLOR','LABEL'):
                k = self.consume().val.lower()
                v = self.consume().val
                params[k] = v
            else:
                break
        if self.peek() and self.peek().val == 'FROM':
            self.consume('FROM')
            q = []
            while self.peek() and self.peek().val not in ('OPEN','LET','IF','FOR','RENDER','ELSE','ENDIF','ENDFOR','CREATE','INSERT'):
                q.append(self.consume().val)
            params['query'] = ' '.join(q)
        return Node('RENDER', t.line, ctype=ctype.val, params=params)

    def parse_sql(self):
        t = self.consume()
        rest = []
        while self.peek() and self.peek().val not in ('OPEN','LET','IF','FOR','RENDER','ELSE','ENDIF','ENDFOR','CREATE','INSERT'):
            rest.append(self.consume().val)
        return Node('SQL', t.line, kw=t.val, rest=' '.join(rest))

class CodeGen:
    def __init__(self, nodes):
        self.nodes = nodes
        self.lines = ["import eehim_db_lite", "import render", "db = None", ""]
        self.indent = 0

    def emit(self, s):
        self.lines.append(" " * self.indent + s)

    def gen_nodes(self, nodes):
        for n in nodes:
            if n.typ == 'DB':
                self.emit(f"db = eehim_db_lite.open({n.path})")
            elif n.typ == 'LET':
                self.emit(f"{n.name.lower()} = {n.expr}")
            elif n.typ == 'IF':
                self.emit(f"if {n.cond.lower()}:")
                self.indent += 1
                self.gen_nodes(n.then_body)
                self.indent -= 1
                if n.else_body:
                    self.emit("else:")
                    self.indent += 1
                    self.gen_nodes(n.else_body)
                    self.indent -= 1
            elif n.typ == 'FOR':
                self.emit(f"for {n.var.lower()} in {n.col.lower()}:")
                self.indent += 1
                self.gen_nodes(n.body)
                self.indent -= 1
            elif n.typ == 'RENDER':
                c = n.ctype.lower()
                p = n.params
                args = []
                if 'value' in p: args.append(f"value={p['value']}")
                if 'color' in p: args.append(f"color={p['color']}")
                if 'label' in p: args.append(f"label={p['label']}")
                if 'query' in p: args.append(f"query=\"{p['query']}\"")
                self.emit(f"render.render_{c}_inside_bubble({', '.join(args)})")
            elif n.typ == 'SQL':
                self.emit(f"# {n.kw} {n.rest}")

    def generate(self):
        self.gen_nodes(self.nodes)
        return "\n".join(self.lines)

if __name__ == "__main__":
    src = sys.argv[1]
    with open(src) as f:
        code = f.read()
    toks = Lexer().tokenize(code)
    ast = Parser(toks).parse_block()
    py = CodeGen(ast).generate()
    out = src.replace('.noth5','.py')
    with open(out, 'w') as o:
        o.write(py)
    print(f" Lexer {len(toks)} tokens, {len(ast)} AST nodes with then_body/else_body nesting")
    print(f" CodeGen indent fixed, kwargs fixed - {out}")
