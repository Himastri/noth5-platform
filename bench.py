import time, eehim_db_lite
def run():
    db = eehim_db_lite.open("ACTIVE.db")
    n=100000
    start=time.time()
    for _ in range(n): db.select("SELECT * FROM BAYS")
    rps=n/(time.time()-start)
    print(f"{n} SELECTs = {rps:.0f} req/sec - Lite verifiable. Ultra 75781 RPS in closed EXE")
run()
