def open(path):
    print(f"[EEHIM DB Lite] open {path}")
    class DB:
        def select(self, q): return [{"id":1,"rps":75781}]
    return DB()
