# noth5_compiler_lite.py - Real Parser for NOTH5 Lite
import re
import sys

TOKEN_SPEC = [
    ('STRING', r'"[^"]*"'),
    ('NUMBER', r'\d+'),
    ('KEYWORD', r'\b(OPEN|DB|RENDER|INSIDE|BUBBLE|CREATE|TABLE|INSERT|INTO|VALUES|SELECT|FROM|SLIDER|RATING|VALUE|COLOR|LABEL)\b'),
    ('IDENT', r'[A-Za-z_][A-Za-z0-9_]*'),
    ('SYMBOL', r'[(),]'),
    ('SKIP', r'[ \t\n]+'),
]

def tokenize(code):
    tokens = []
    pos = 0
    while pos < len(code):
        match = None
        for typ, pattern in TOKEN_SPEC:
            regex = re.compile(pattern)
            m = regex.match(code, pos)
            if m:
                if typ!= 'SKIP':
                    tokens.append((typ, m.group()))
                pos = m.end()
                match = True
                break
        if not match:
            raise SyntaxError(f"Unexpected char at {pos}: {code[pos:pos+20]}")
    return tokens

def parse_and_emit(tokens):
    out = ["import eehim_db_lite", "import render", ""]
    i = 0
    while i < len(tokens):
        if tokens[i][1] == 'OPEN':
            db_path = tokens[i+2][1]
            out.append(f'db = eehim_db_lite.open({db_path})')
            i += 3
        elif tokens[i][1] == 'RENDER':
            ctype = tokens[i+1][1]
            # collect params VALUE, COLOR, LABEL
            params = {}
            j = i+2
            while j < len(tokens) and tokens[j][1]!= 'RENDER' and tokens[j][1]!= 'OPEN':
                if tokens[j][1] in ('VALUE','COLOR','LABEL'):
                    params[tokens[j][1].lower()] = tokens[j+1][1]
                    j+=2
                else:
                    j+=1
            if ctype == 'SLIDER':
                out.append(f"render.render_slider_inside_bubble(value={params.get('value','75')}, color={params.get('color','\"#00ff88\"')}, label={params.get('label','\"Progress\"')})")
            elif ctype == 'RATING':
                out.append(f"render.render_rating_inside_bubble({params})")
            i = j
        else:
            i+=1
    return "\n".join(out)

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        code = f.read()
    tokens = tokenize(code)
    py = parse_and_emit(tokens)
    with open(sys.argv[1].replace('.noth5','.py'),'w') as out:
        out.write(py)
    print(f"Compiled {sys.argv[1]} -> {sys.argv[1].replace('.noth5','.py')} via tokenizer+parser")
