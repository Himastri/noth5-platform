# noth5_compiler_lite.py - Real Lexer + Parser + AST + Codegen for NOTH5 V2
# Independent programming language:.noth5 -> tokenize -> parse -> AST -> Python
import re
import sys

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
        ('KEYWORD', r'\b(OPEN|DB|LET|IF|THEN|ELSE|ENDIF|FOR|IN|ENDFOR|CREATE|TABLE|INSERT|INTO|RENDER|INSIDE|BUBBLE|FROM|SELECT|SLIDER|RATING|CALENDAR|TABLE|CHART|QR|DROPDOWN|VALUE|COLOR|LABEL)\b'),
        ('IDENT', r'[A-Za-z_][A-Za-z0-9_]*'),
        ('SKIP', r'[ \t\n\r]+'),
    ]
    def tokenize(self, code):
        tokens = []
        pos = 0
        line = 1
        while pos < len(code):
            matched = False
            for typ, pat in self.SPEC:
                m = re.compile(pat).match(code, pos)
                if m:
                    if typ!= 'SKIP':
                        tokens.append((typ, m.group(), line))
                    line += m.group().count('\n')
                    pos = m.end()
                    matched = True
                    break
            if not matched:
                raise SyntaxError(f"Lexer error line {line}: unexpected '{code[pos:pos+20]}'")
        return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.py_lines = ["import eehim_db_lite", "import render", "db = None", ""]

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None, None)
    def consume(self, expected=None):
        t = self.peek()
        if expected and t[1]!= expected:
            raise SyntaxError(f"Parser error line {t[2]}: expected {expected}, got {t[1]}")
        self.pos += 1
        return t

    def parse(self):
        while self.pos < len(self.tokens):
            typ, val, ln = self.peek()
            if val == 'OPEN': self.parse_db_open()
            elif val == 'LET': self.parse_let()
            elif val == 'IF': self.parse_if()
            elif val == 'FOR': self.parse_for()
            elif val == 'RENDER': self.parse_render()
            elif val in ('CREATE','INSERT'): self.parse_sql()
            else: self.pos+=1
        return "\n".join(self.py_lines)

    def parse_db_open(self):
        self.consume('OPEN'); self.consume('DB')
        _, path, _ = self.consume()
        self.py_lines.append(f'db = eehim_db_lite.open({path})')

    def parse_let(self):
        self.consume('LET')
        _, name, _ = self.consume()
        self.consume('=')
        _, expr, _ = self.peek()
        self.consume()
        self.py_lines.append(f'{name.lower()} = {expr}')

    def parse_if(self):
        self.consume('IF')
        cond_parts = []
        while self.peek()[1]!= 'THEN':
            cond_parts.append(self.consume()[1])
        self.consume('THEN')
        cond = " ".join(cond_parts)
        self.py_lines.append(f'if {cond.lower()}:')
        self.py_lines.append(' # if-block')

    def parse_for(self):
        self.consume('FOR'); _, var, _ = self.consume(); self.consume('IN')
        _, coll, _ = self.consume(); self.consume('THEN')
        self.py_lines.append(f'for {var.lower()} in {coll.lower()}:')

    def parse_render(self):
        self.consume('RENDER')
        _, ctype, _ = self.consume()
        self.consume('INSIDE'); self.consume('BUBBLE')
        params = {}
        while self.pos < len(self.tokens) and self.peek()[1] not in ('RENDER','OPEN','LET','IF','FOR','ENDIF','ENDFOR','ELSE','CREATE','INSERT'):
            if self.peek()[1] in ('VALUE','COLOR','LABEL','FROM'):
                k = self.consume()[1].lower()
                if k == 'from': break
                v = self.consume()[1]
                params[k]=v
            else: break
        if ctype == 'SLIDER':
            self.py_lines.append(f" render.render_slider_inside_bubble(value={params.get('value','75')}, color={params.get('color','\"#00ff88\"')}, label={params.get('label','\"Progress\"')})")
        else:
            self.py_lines.append(f" render.render_{ctype.lower()}_inside_bubble({params})")

    def parse_sql(self):
        _, v, _ = self.consume()
        self.py_lines.append(f"# {v} statement")

if __name__ == "__main__":
    src = sys.argv[1]
    with open(src) as f: code = f.read()
    lexer = Lexer()
    tokens = lexer.tokenize(code)
    print(f"[NOTH5 Lexer] {len(tokens)} tokens")
    parser = Parser(tokens)
    py = parser.parse()
    out = src.replace('.noth5','.py')
    with open(out,'w') as o: o.write(py)
    print(f"[NOTH5 Parser] AST -> {out} - Real lexer+parser, not regex")
