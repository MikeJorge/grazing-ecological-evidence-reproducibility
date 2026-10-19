"""One-command deterministic numerical, test, and figure build (offline)."""
import os, subprocess, sys
from pathlib import Path
root=Path(__file__).resolve().parent
env=dict(os.environ, PYTHONHASHSEED='0', TZ='UTC', LC_ALL='C.UTF-8', MPLBACKEND='Agg')
for args in [['src/reproduce.py','--out','outputs'],['-m','unittest','discover','-s','tests','-v'],['figures/figure1.py','--out','outputs','--accessibility']]:
    subprocess.run([sys.executable,*args],cwd=root,env=env,check=True)
