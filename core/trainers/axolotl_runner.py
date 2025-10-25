import os, subprocess, sys

def run_axolotl(config_path: str):
    image = "winglian/axolotl:main-cuda12.1"  # public image commonly used
    workspace = os.getcwd()
    cmd = [
        "docker","run","--gpus","all","--rm",
        "-v", f"{workspace}:/workspace",
        "-e","HF_TOKEN",
        image,
        "axolotl","train",config_path
    ]
    print("Running:", " ".join(cmd), flush=True)
    return subprocess.call(cmd)
