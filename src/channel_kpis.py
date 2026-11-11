#!/usr/bin/env python3
"""Compute five channel intelligence outputs from explicitly simulated channel CSV.
This program makes no assertions about Henkel's real customer or distributor data.
"""
from __future__ import annotations
import argparse, csv
from collections import defaultdict
from pathlib import Path

parser=argparse.ArgumentParser(description='Synthetic B2B channel KPI engine')
parser.add_argument('--input', default='data/synthetic/channel/Simulated_Channel_Data_Original_1440_Rows.csv')
parser.add_argument('--output-dir', default='outputs/channel')
args=parser.parse_args()
SOURCE=Path(args.input)
OUT=Path(args.output_dir)
OUT.mkdir(parents=True,exist_ok=True)
with SOURCE.open(encoding='utf-8-sig',newline='') as f:
    records=list(csv.DictReader(f))
assert len(records)==1440, 'Expected 1,440 synthetic base records'
assert all('SIMULATED' in str(r['Data_Status']).upper() for r in records), 'Unlabelled channel data'
def num(v):
 try:return float(v or 0)
 except (ValueError,TypeError):return 0.0
def save(name,headers,values):
 with (OUT/name).open('w',newline='',encoding='utf-8-sig') as f:
  wr=csv.writer(f);wr.writerow(headers);wr.writerows(values)
 print(name,len(values))
# Historical comparison: full-year 2024 vs 2025, or latest available year if different.
years=sorted(set(int(r['Year']) for r in records)); prior,current=years[-2:]
# Grouping at distributor × region × product for a meaningful drilldown.
agg=defaultdict(lambda: {'sales':0.,'target':0.,'units':0.,'returns':0.,'inventory':0.})
for r in records:
 key=(int(r['Year']),str(r['Region']),str(r['Distributor_ID']),str(r['Distributor_Name']),str(r['Product_Category']))
 a=agg[key]
 for source,dest in [('Net_Sales_EUR','sales'),('Sales_Target_EUR','target'),('Units_Sold','units'),('Returns_EUR','returns'),('Inventory_Value_EUR','inventory')]:a[dest]+=num(r[source])
performance=[]; alerts=[]; distributor=defaultdict(lambda:{'sales':0.,'prior':0.,'target':0.,'category':defaultdict(float)})
for (yr,region,did,dname,category),a in sorted(agg.items()):
 if yr!=current:continue
 p=agg.get((prior,region,did,dname,category))
 prior_sales=p['sales'] if p else 0
 growth=(a['sales']/prior_sales-1) if prior_sales>0 else None
 attainment=a['sales']/a['target'] if a['target']>0 else None
 prior_units=p['units'] if p else 0
 price_now=a['sales']/a['units'] if a['units'] else None
 price_prior=prior_sales/prior_units if prior_units else None
 price_effect=(price_now-price_prior)*prior_units if price_now is not None and price_prior is not None else None
 volume_effect=(a['units']-prior_units)*price_now if price_now is not None and price_prior is not None else None
 status='DERIVED FROM SIMULATED CHANNEL DATA'
 performance.append([current,region,did,dname,category,round(a['sales'],2),round(prior_sales,2),round(a['target'],2),round(growth,5) if growth is not None else '',round(attainment,5) if attainment is not None else '',status])
 if growth is not None and growth<=-0.10:
  alerts.append([region,did,dname,category,round(growth,5),round(a['sales']-prior_sales,2),round(price_effect,2) if price_effect is not None else '',round(volume_effect,2) if volume_effect is not None else '','REVIEW: simulated drop; price/volume descriptive, not causal',status])
 d=distributor[(region,did,dname)];d['sales']+=a['sales'];d['prior']+=prior_sales;d['target']+=a['target'];d['category'][category]+=a['sales']
save('sales_performance.csv',['Year','Region','Distributor_ID','Distributor_Name','Product_Category','Sales_EUR','Prior_Sales_EUR','Target_EUR','YoY_Growth_Fraction','Target_Attainment_Fraction','Data_Status'],performance)
save('growth_drop_alerts.csv',['Region','Distributor_ID','Distributor_Name','Product_Category','YoY_Growth_Fraction','Sales_Change_EUR','Price_Effect_EUR','Volume_Effect_EUR','Suggested_Review','Data_Status'],alerts)
scorecard=[]; whitespace=[]; queue=[]
max_sales=max((d['sales'] for d in distributor.values()),default=1)
for (region,did,dname),d in sorted(distributor.items()):
 growth=d['sales']/d['prior']-1 if d['prior']>0 else None
 concentration=max(d['category'].values())/d['sales'] if d['sales']>0 else 0
 attainment=d['sales']/d['target'] if d['target'] else None
 risk='HIGH' if (growth is not None and growth < -0.10) or concentration > 0.65 else 'WATCH' if (growth is not None and growth<0) else 'NORMAL'
 scorecard.append([region,did,dname,round(d['sales'],2),round(d['prior'],2),round(growth,5) if growth is not None else '',round(attainment,5) if attainment is not None else '',round(concentration,5),risk,'DERIVED FROM SIMULATED CHANNEL DATA'])
 headroom=d['sales']*0.35; captured=headroom*0.25
 whitespace.append([region,did,dname,round(d['sales'],2),1.35,0.25,round(headroom,2),round(captured,2),'SCENARIO ONLY – SIMULATED, NOT MARKET SIZE'])
 drop=min(1,max(0,-growth)/0.3) if growth is not None else 0
 exposure=d['sales']/max_sales
 conc=min(1,concentration/0.8)
 space=min(1,captured/(max_sales*0.35*0.25))
 score=100*(.4*drop+.3*exposure+.2*conc+.1*space)
 action='Investigate volume/customer losses' if growth is not None and growth < -0.10 else 'Validate cross-sell / territory headroom' if captured>0 else 'Monitor'
 queue.append([region,did,dname,round(score,1),risk,action,round(captured,2),'ILLUSTRATIVE PRIORITY – SIMULATED'])
save('distributor_scorecard.csv',['Region','Distributor_ID','Distributor_Name','Sales_EUR','Prior_Sales_EUR','YoY_Growth_Fraction','Target_Attainment_Fraction','Largest_Category_Share','Risk_Flag','Data_Status'],scorecard)
save('whitespace_opportunities.csv',['Region','Distributor_ID','Distributor_Name','Current_Sales_EUR','Addressable_Multiplier_Assumption','Capture_Rate_Assumption','Modeled_Gap_EUR','Illustrative_Capture_EUR','Data_Status'],whitespace)
save('action_queue.csv',['Region','Distributor_ID','Distributor_Name','Priority_Score_0_100','Risk_Flag','Recommended_Next_Step','Illustrative_Capture_EUR','Data_Status'],sorted(queue,key=lambda r:-r[3]))
print('Comparison',prior,current,'records',len(records),'SIMULATED')
