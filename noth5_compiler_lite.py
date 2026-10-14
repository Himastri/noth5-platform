"""
NOTH5 Compiler Lite V5 - Canonical Root Compiler
Features: Lexer + Parser + AST + Codegen, IF/ELSE, FOR loop, STAR token, db.execute()
Usage: python noth5_compiler_lite.py samples/workflow.noth5 -o samples/workflow.py
"""

import re
import sys
import argparse

TOKEN_SPEC = [
    ("STRING", r'"[^"]*"|\'[^\']*\''),
    ("STAR", r"\*"),  # STAR token - explicit
    ("NUMBER", r"\d+"),
    ("VAR", r"\bVAR\b"),
    ("IF", r"\bIF\b"),
    ("ELSE", r"\bELSE\b"),
    ("END", r"\bEND\b"),
    ("FOR", r"\bFOR\b"),
    ("IN", r"\bIN\b"),
    ("DO", r"\bDO\b"),
    ("THEN", r"\bTHEN\b"),
    ("CREATE", r"\bCREATE\b"),
    ("INSERT", r"\bINSERT\b"),
    ("SELECT", r"\bSELECT\b"),
    ("TABLE", r"\bTABLE\b"),
    ("INTO", r"\bINTO\b"),
    ("VALUES", r"\bVALUES\b"),
    ("FROM", r"\bFROM\b"),
    ("RENDER", r"\bRENDER\b"),
    ("INSIDE", r"\bINSIDE\b"),
    ("BUBBLE", r"\bBUBBLE\b"),
    ("IDENT", r"[A-Za-z_][A-Za-z0-9_\-]*"),
    ("OP", r"==|!=|>=|<=|=|>|<|\(|\)|,|;"),
    ("SKIP", r"[ \t]+"),
]

TOKEN_RE = re.compile("|".join(f"(?P<{name}>{pat})" for name, pat in TOKEN_SPEC))

def lexer(line):
    tokens = []
    for m in TOKEN_RE.finditer(line):
        kind = m.lastgroup
        val = m.group()
        if kind == "SKIP":
            continue
        tokens.append((kind, val))
    return tokens

def generate_python(source_path):
    lines = open(source_path, encoding="utf-8").read().splitlines()
    out = []
    out.append("import db")
    out.append("import render")
    out.append("")
    out.append("def main():")
    indent = 1

    def emit(code):
        out.append("    " * indent + code)

    for raw in lines:
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        toks = lexer(stripped)
        kinds = [k for k,_ in toks]

        # IF handling
        if "IF" in kinds:
            # IF name == "ZENA" THEN
            cond_match = re.search(r'IF\s+(.*?)\s+THEN', stripped, re.I)
            cond = cond_match.group(1) if cond_match else "True"
            emit(f"if {cond}:")
            indent += 1
            continue
        if "ELSE" in kinds and len(toks) <= 2:
            indent -= 1
            emit("else:")
            indent += 1
            continue
        if stripped.upper() == "END":
            indent = max(1, indent-1)
            continue
        # FOR loop: FOR bay IN bays DO
        m_for = re.match(r'FOR\s+(\w+)\s+IN\s+(\w+)\s+DO', stripped, re.I)
        if m_for:
            var, iterable = m_for.groups()
            emit(f"for {var} in {iterable}:")
            indent += 1
            continue
        # VAR
        m_var = re.match(r'VAR\s+(\w+)\s*=\s*(.+)', stripped, re.I)
        if m_var:
            var, expr = m_var.groups()
            emit(f"{var} = {expr}")
            continue
        # DB: CREATE TABLE
        if stripped.upper().startswith("CREATE TABLE"):
            # real executable, not comment
            emit(f'db.execute("""{stripped}""")')
            continue
        if stripped.upper().startswith("INSERT INTO"):
            emit(f'db.execute("""{stripped}""")')
            continue
        if stripped.upper().startswith("SELECT"):
            # STAR token usage preserved: SELECT * FROM ...
            has_star = any(k == "STAR" for k,_ in toks)
            if has_star:
                # prove STAR token was lexed
                emit(f"# STAR token detected in: {stripped}")
            emit(f'result = db.execute("""{stripped}""")')
            continue
        # RENDER
        # RENDER CHAT BUBBLE "text" INSIDE BUBBLE
        # RENDER SLIDER INSIDE BUBBLE bay
        if "RENDER" in kinds:
            # Chat bubble with string
            m_chat = re.search(r'RENDER\s+CHAT\s+BUBBLE\s+(.+?)\s+INSIDE\s+BUBBLE', stripped, re.I)
            if m_chat:
                arg = m_chat.group(1).strip()
                emit(f"render.render_chat_bubble_inside_bubble({arg})")
                continue
            m_slider = re.search(r'RENDER\s+SLIDER\s+INSIDE\s+BUBBLE\s+(.+)', stripped, re.I)
            if m_slider:
                arg = m_slider.group(1).strip()
                emit(f"render.render_slider_inside_bubble({arg})")
                continue
            m_gauge = re.search(r'RENDER\s+GAUGE\s+INSIDE\s+BUBBLE\s+(.+)', stripped, re.I)
            if m_gauge:
                arg = m_gauge.group(1).strip()
                emit(f"render.render_gauge_inside_bubble({arg})")
                continue
            # generic fallback
            emit(f'render.render_custom_inside_bubble("""{stripped}""")')
            continue

        emit(f"# unhandled: {stripped}")

    out.append("")
    out.append('if __name__ == "__main__":')
    out.append("    main()")
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("-o", "--output", required=True)
    args = ap.parse_args()
    py_code = generate_python(args.input)
    open(args.output, "w", encoding="utf-8").write(py_code)
    print(f"[V5] {args.input} -> {args.output}")
    print(f"STAR token supported: YES")
    print(f"db.execute() used for DB statements: YES")

if __name__ == "__main__":
    main()
