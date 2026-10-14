class DB:
    def select(self, q): 
        print(f"[DB SELECT] {q}")
        return [{"id":1}]
    def execute(self, q):
        print(f"[DB EXECUTE] {q} - Lite demo, full factory executes")
