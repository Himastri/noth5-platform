import db
import render

def main():
    name = "ZENA"
    bays = ["BAY-A", "BAY-B", "BAY-C"]
    db.execute("""CREATE TABLE BAYS (id INT, name TEXT)""")
    db.execute("""INSERT INTO BAYS VALUES (1, "BAY-A")""")
    db.execute("""INSERT INTO BAYS VALUES (2, "BAY-B")""")
    db.execute("""INSERT INTO BAYS VALUES (3, "BAY-C")""")
    # STAR token detected in: SELECT * FROM BAYS
    result = db.execute("""SELECT * FROM BAYS""")
    if name == "ZENA":
        render.render_chat_bubble_inside_bubble("Hi, I am ZENA - Workflow Demo")
    else:
        render.render_chat_bubble_inside_bubble("Hello Guest")
    for bay in bays:
        render.render_slider_inside_bubble(bay)
        render.render_gauge_inside_bubble(bay)
    render.render_chat_bubble_inside_bubble("Workflow complete")

if __name__ == "__main__":
    main()
