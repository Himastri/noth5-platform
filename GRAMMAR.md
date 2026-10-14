# NOTH5 Grammar V2 - Independent DSL with Parser

program := { statement }

statement := db_open | create_table | insert | let_stmt | render_control | if_stmt

let_stmt := "LET" identifier "=" expression
expression := string_literal | number | identifier

db_open := "OPEN" "DB" string_literal
create_table := "CREATE" "TABLE" identifier
insert := "INSERT" "INTO" identifier

render_control := "RENDER" control_type "INSIDE" "BUBBLE" [params]
control_type := "SLIDER" | "RATING" | "CALENDAR" | "TABLE" | "CHART" | "QR" | "DROPDOWN" | "MAP" | "YOUTUBE" | "FILE_UPLOAD" | "CHART" | "KANBAN" | "TIMELINE" |... (105 total)

if_stmt := "IF" condition "THEN" statement

Example V2:
LET progress = 75
OPEN DB "D:/NOTH5_EXCLUSIVE/DATA/ACTIVE.db"
RENDER SLIDER INSIDE BUBBLE VALUE progress COLOR "#00ff88" LABEL "Progress"
IF progress > 50 THEN RENDER TABLE INSIDE BUBBLE SELECT * FROM BAYS
