import csv, json, subprocess, sys, tempfile, unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]

def read(rel):
    with (R/rel).open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))

class PortfolioIntegrity(unittest.TestCase):
    def test_synthetic_labels(self):
        rows=read('data/synthetic/channel/Simulated_Channel_Data_Original_1440_Rows.csv')
        self.assertEqual(len(rows),1440)
        self.assertTrue(all('SIMULATED' in x['Data_Status'].upper() for x in rows))
    def test_apc_undisclosed(self):
        rows=read('data/official_financials/APC_Quarterly_Official_2024_2026.csv')
        for x in rows:
            self.assertEqual(x['APC_Price_Contribution_pp'],'')
            self.assertEqual(x['APC_Volume_Contribution_pp'],'')
    def test_phase4_bridge(self):
        rows=read('data/synthetic/phase4/P4_Diagnostics.csv')
        self.assertEqual(len(rows),8)
        self.assertTrue(all(abs(float(x['Bridge_Reconciliation_EUR_CALC']))<0.01 for x in rows))
    def test_phase5_seeded(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable,'-m','src.run_phase5_engine','--output-dir',tmp],cwd=R,check=True,capture_output=True,text=True)
            out=json.loads((Path(tmp)/'P5_Validation.json').read_text(encoding='utf-8'))
            self.assertEqual(out['panel_rows'],720)
            self.assertEqual(out['distinct_synthetic_accounts'],120)
            self.assertEqual(len(out['effects']),5)
    def test_repository_validation(self):
        subprocess.run([sys.executable,'scripts/validate_repository.py'],cwd=R,check=True,capture_output=True,text=True)
if __name__=='__main__': unittest.main()
