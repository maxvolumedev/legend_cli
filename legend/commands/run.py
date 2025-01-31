import subprocess

def run(args):
    print("Starting Azure Functions locally...")
    subprocess.run(["func", "start"], check=True)
