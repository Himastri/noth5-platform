# NOTH5 GRAMMAR V81 - Independent DSL

program := { statement }

statement := db_open
           | create_table
           | insert
           | render_control

db_open := "OPEN" "DB" string_literal

create_table := "CREATE" "TABLE" ident "(" column_def { "," column_def } ")"
column_def := ident type [ "PRIMARY" "KEY" ]

insert := "INSERT" "INTO" ident "VALUES" "(" literal { "," literal } ")"

render_control := "RENDER" control_type ["INSIDE" "BUBBLE"] [params]

control_type := "SLIDER" | "RATING" | "TABLE" | "CHART" | "QR" | "DROPDOWN" | "CALENDAR" | "YOUTUBE" | "MAP" | "TEXT" | "BUTTON"

params := { param }
param := ident (string_literal | number | "[" list "]")
list := string_literal { "," string_literal }

type := "INT" | "TEXT" | "FLOAT"
ident := [A-Z_][A-Z0-9_]*
string_literal := '"' { char } '"'
literal := string_literal | number
