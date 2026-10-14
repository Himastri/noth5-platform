import eehim_db_lite
import render
db = None

db = eehim_db_lite.open("D:/NOTH5_EXCLUSIVE/DATA/ACTIVE.db")
total = 0
score = 78
if score > 70:
    render.render_slider_inside_bubble(value=85, color="#00ff88", label="Trust Score")
    total = total + 10
else:
    render.render_rating_inside_bubble(value=2, label="Low Trust")
for user in users:
    if user == "admin":
        render.render_table_inside_bubble(query="SELECT * FROM BAYS")
    else:
        render.render_card_inside_bubble(label="User Card")

render.render_qr_inside_bubble(value="verify-email")
