#!/usr/bin/env python3
"""Regenerate synthetic analytical output from repository root (standard library only)."""
import subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
commands=[
 [sys.executable,'-m','src.channel_kpis','--input','data/synthetic/channel/Simulated_Channel_Data_Original_1440_Rows.csv','--output-dir','outputs/channel'],
 [sys.executable,'-m','src.run_phase4_engine','--output-dir','outputs/phase4'],
 [sys.executable,'-m','src.run_phase5_engine','--output-dir','outputs/phase5'],
 [sys.executable,'scripts/validate_repository.py'],
]
for cmd in commands:
    print('RUN:', ' '.join(cmd), flush=True)
    subprocess.run(cmd,cwd=root,check=True)
print('All reproducibility steps completed.')
