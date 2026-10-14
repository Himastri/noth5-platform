# NOTH5 Grammar V5 - Matches Canonical Compiler

## Syntax Actually Accepted by noth5_compiler_lite.py V5

This grammar describes the syntax the canonical compiler implements (regex-based source-to-source translation).

### Variables
```
VAR name = "value"
VAR bays = ["BAY-A", "BAY-B", "BAY-C"]
VAR count = 1
```

### Database (Lite executes via eehim_db_lite.py)
```
CREATE TABLE BAYS (id INT, name TEXT)
INSERT INTO BAYS VALUES (1, "BAY-A")
SELECT * FROM BAYS    -- STAR token supported
```

### Control Flow
```
IF name == "ZENA"
  RENDER chat_bubble "Hi, I am ZENA"
ELSE
  RENDER chat_bubble "Hello Guest"
END

FOR bay IN bays DO
  RENDER slider bay
  RENDER gauge bay
END
```

### Rendering (controls INSIDE chat bubble)
```
RENDER chat_bubble "text"
RENDER slider <label>
RENDER gauge <label>
RENDER rating <label>
RENDER table <data>
RENDER chart <data>
```

### Compiler Implementation
- Lexical tokenization (VAR, IF, ELSE, END, FOR, IN, DO, RENDER)
- Source-to-source translation to Python via regex-based statement handling (Lite)
- Full Factory EXE uses nested AST parser (not exposed in Lite)
- Lite generates: db.execute("""..."""), render.render_*_inside_bubble(...), if/for Python

### Canonical Command (single source of truth)
```
python noth5_compiler_lite.py workflow.noth5 -o workflow.py
```
Requires -o argument (arg parser requirement).

### Example workflow.noth5
```
VAR name = "ZENA"
VAR bays = ["BAY-A", "BAY-B", "BAY-C"]
CREATE TABLE BAYS (id INT, name TEXT)
INSERT INTO BAYS VALUES (1, "BAY-A")
SELECT * FROM BAYS
IF name == "ZENA"
  RENDER chat_bubble "Hi, I am ZENA - Workflow Demo"
ELSE
  RENDER chat_bubble "Hello Guest"
END
FOR bay IN bays DO
  RENDER slider bay
  RENDER gauge bay
END
RENDER chat_bubble "Workflow complete"
```
Compiles to workflow.py with db.execute, render.render_*_inside_bubble, STAR token.
