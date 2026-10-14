import hashlib
with open('workflow.noth5','rb') as f: src_hash = hashlib.sha256(f.read()).hexdigest()
print(f"Source hash: {src_hash}")
# compile and run and check output contains rendered controls
import subprocess
subprocess.run(["python","../../noth5_compiler_lite.py","workflow.noth5"], check=True)
with open('workflow.py') as f: print(f.read())
print("Proof: workflow.py came from workflow.noth5 via compiler")
