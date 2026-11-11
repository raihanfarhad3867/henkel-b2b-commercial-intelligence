#!/usr/bin/env python3
"""Lightweight schema, provenance and arithmetic checks; not a substitute for source verification."""
import csv, json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def csvrows(path):
    with (root/path).open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))

def check():
    channel=csvrows('data/synthetic/channel/Simulated_Channel_Data_Original_1440_Rows.csv')
    assert len(channel)==1440
    assert all('SIMULATED' in x['Data_Status'].upper() for x in channel)
    assert {str(x['Year']) for x in channel}=={'2024','2025'}
    at=csvrows('data/official_financials/AT_Quarterly_Official_2024_2026.csv')
    apc=csvrows('data/official_financials/APC_Quarterly_Official_2024_2026.csv')
    for y in (2024,2025,2026):
        row=next(x for x in at if x['Year']==str(y) and x['Quarter']=='Q3')
        assert row['Organic_Status']=='Official actual' and row['Price_Status']=='Official actual'
        assert abs(float(row['AT_Organic_Growth_pct'])-float(row['AT_Price_Contribution_pp'])-float(row['AT_Volume_Contribution_pp']))<0.11
        ar=next(x for x in apc if x['Year']==str(y) and x['Quarter']=='Q3')
        assert ar['APC_Price_Contribution_pp']=='' and ar['APC_Volume_Contribution_pp']==''
        assert 'Not disclosed' in ar['Price_Status'] and 'Not disclosed' in ar['Volume_Status']
    q3=next(x for x in at if x['Year']=='2026' and x['Quarter']=='Q3')
    assert float(q3['AT_Organic_Growth_pct'])==7.9
    assert float(q3['AT_Price_Contribution_pp'])==7.2
    assert float(q3['AT_Volume_Contribution_pp'])==0.7
    assert len(csvrows('data/synthetic/phase4/P4_Monthly_Orders.csv'))==144
    diagnostics=csvrows('data/synthetic/phase4/P4_Diagnostics.csv')
    assert max(abs(float(x['Bridge_Reconciliation_EUR_CALC'])) for x in diagnostics)<0.01
    p5=csvrows('data/synthetic/phase5/P5_Synthetic_Experiment_Panel.csv')
    assert len(p5)==720 and len({x['Synthetic_Account_ID'] for x in p5})==120
    assert all('SIMULATED' in x['Data_Status'].upper() for x in p5)
    for x in csvrows('data/synthetic/phase5/P5_Effect_Estimates.csv'):
        assert 'SIMULATED' in x['Data_Status'].upper()
    generated=root/'outputs/phase5/P5_Validation.json'
    if generated.exists():
        summary=json.loads(generated.read_text(encoding='utf-8'))
        assert summary['panel_rows']==720
    notebooks=list((root/'notebooks').glob('*.ipynb'))
    assert len(notebooks)==5
    for notebook in notebooks:
        doc=json.loads(notebook.read_text(encoding='utf-8'))
        assert doc.get('nbformat')==4 and doc['cells']
    print('PASS: provenance labels, 2024–26 reporting metrics, simulated ledgers, bridge, experimental records and notebooks.')
if __name__=='__main__': check()
