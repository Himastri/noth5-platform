# NOTH5 Grammar V80 — Minimal Public Grammar
program := { statement }
statement := db_open | render_control
db_open := "OPEN" "DB" string_literal
render_control := "RENDER" control_type "INSIDE" "BUBBLE" [params]
control_type := "SLIDER" | "RATING" | "CALENDAR" | "TABLE"
Example:
OPEN DB "D:/NOTH5_EXCLUSIVE/DATA/ACTIVE.db"
RENDER SLIDER INSIDE BUBBLE VALUE 75 COLOR "#00ff88" LABEL "Progress"
