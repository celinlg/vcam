# ===== UTILIDADES =====
import subprocess
from typing import List

ADB = "adb"

def run_command(cmd_list: List[str]) -> str:
    """Executa um comando ADB e retorna o output"""
    try:
        r = subprocess.run(cmd_list, capture_output=True, text=True, timeout=15)
        return r.stdout + r.stderr
    except Exception as e:
        return str(e)
