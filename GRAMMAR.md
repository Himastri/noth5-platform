# NOTH5 Grammar V2 - Independent DSL with Parser

program := { statement }
statement := db_open | let_stmt | if_stmt | for_stmt | create_table | insert | render_control
db_open := "OPEN" "DB" string_literal
let_stmt := "LET" identifier "=" expression
if_stmt := "IF" expression "THEN" { statement } [ "ELSE" { statement } ] "ENDIF"
for_stmt := "FOR" identifier "IN" expression "THEN" { statement } "ENDFOR"
render_control := "RENDER" control_type "INSIDE" "BUBBLE" [ params ]
control_type := SLIDER | RATING | CALENDAR | TABLE | CHART | QR | DROPDOWN | MAP | YOUTUBE |... (105 total)
expression := term { (">" | "<" | ">=" | "<=" | "==" | "=") term }
