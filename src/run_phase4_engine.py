#!/usr/bin/env python3
"""Phase 4 commercial diagnostic / win-loss demonstration.
ONLY synthetic case studies. No company-specific Henkel customer/distributor data.
Reproducible with Python standard library. Run: python run_phase4_engine.py --output-dir ./data
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

STATUS = 'SIMULATED — NOT HENKEL CUSTOMER OR DISTRIBUTOR DATA'
CASES = [
('SIM-VN-FW-01','Vietnam','Footwear','SIM-DIST-VN-01','Footwear site A',14000,9800,4.20,4.35,2.50,2.75,'Competitive displacement / specification change','Medium','Technical lead and brand-approved qualification; actual supplier unknown'),
('SIM-VN-FW-02','Vietnam','Footwear','SIM-DIST-VN-01','Footwear site B',11500,8600,4.10,4.24,2.58,2.88,'Customer production slowdown','Medium','Check factory production index and end-customer orders'),
('SIM-VN-FW-03','Vietnam','Footwear','SIM-DIST-VN-02','Footwear site C',8900,10100,4.45,4.58,2.71,3.00,'Positive demand / account expansion','Low','Confirm customer production and new model launch'),
('SIM-VN-FW-04','Vietnam','Footwear','SIM-DIST-VN-02','Footwear site D',7600,5300,4.60,4.80,2.79,3.05,'Delayed technical qualification','Medium','Review technical trial stages and specification approval'),
('SIM-EU-PK-01','Europe','Paper packaging','SIM-DIST-EU-01','Corrugated converter A',15000,11200,3.30,3.43,2.07,2.30,'Supply reliability / fulfillment gap','Medium','Inspect fill rate and lead-time deviations'),
('SIM-EU-PK-02','Europe','Paper packaging','SIM-DIST-EU-01','Paper mailer converter B',6000,9000,3.80,3.96,2.25,2.48,'New paper-seal application adoption','Low','Confirm customer line qualification and expected repeat volume'),
('SIM-EU-PK-03','Europe','Paper packaging','SIM-DIST-EU-02','Packaging converter C',12500,10500,3.15,3.25,2.08,2.25,'Competitive price pressure','Low','Request won/lost quotations and total cost-in-use comparison'),
('SIM-EU-PK-04','Europe','Paper packaging','SIM-DIST-EU-02','Packaging converter D',8500,8700,3.60,3.70,2.22,2.47,'Stable / minor expansion','Low','Identify adjacent applications; current share unknown'),
]
MONTH_WEIGHTS_2025 = [8,9,10,11,11,12,14,13,12]
MONTH_WEIGHTS_2026_DECLINING = [12,12,12,11,11,10,9,11,12]
MONTH_WEIGHTS_2026_NORMAL = [8,9,10,11,11,12,14,13,12]
MONTH_WEIGHTS_2026_GROWING = [7,8,9,10,11,12,14,14,15]

# Evidence items describe facts within a fictional scenario, not observed Henkel data.
SIGNALS = [
('SIM-VN-FW-01','CRM quotation note','2026-05-07','Customer requested alternative bonding specification','Supports technical/supplier-switch hypothesis','Medium','Check approved materials list and win/loss conversation'),
('SIM-VN-FW-01','Order records','2026-08-12','Falling order quantities after April','Supports customer volume decline','High','Compare customer output and all suppliers'),
('SIM-VN-FW-01','Pricing log','2026-08-30','Realized price increased while volume fell','Ambiguous: correlation, not causality','High','Validate competing quotes and usage rates'),
('SIM-VN-FW-02','Distributor conversation','2026-06-18','Customer communicated reduction in footwear output','Supports external demand hypothesis','Medium','Request production-unit or industry evidence'),
('SIM-VN-FW-02','Service log','2026-09-10','No recorded stockouts for illustrative customer','Weakens supply issue hypothesis','Medium','Validate delivery service levels independently'),
('SIM-VN-FW-03','CRM activity','2026-07-09','New shoe-model production line reportedly approved','Supports expansion hypothesis','Medium','Confirm repeat purchase and technical approvals'),
('SIM-VN-FW-04','Technical service log','2026-05-20','Application trial awaiting bond strength approval','Supports qualification delay hypothesis','High','Obtain trial protocol and objective criteria'),
('SIM-VN-FW-04','Sales opportunity','2026-09-02','Forecasted customer order deferred, not cancelled','Supports timing issue; loss not confirmed','Medium','Verify go/no-go date'),
('SIM-EU-PK-01','Order fulfillment','2026-07-21','Illustrative 87% on-time-in-full vs 96% target','Supports delivery issue hypothesis','High','Validate OTIF calculation and customer impact'),
('SIM-EU-PK-01','Customer complaint','2026-08-05','Urgent orders split across deliveries','Supports reliability hypothesis','Medium','Assess service recovery economics'),
('SIM-EU-PK-02','Technical trial','2026-03-17','Pilot of paper sealing method passed scenario acceptance test','Supports new-application opportunity','Medium','Validate compliance and production-scale run'),
('SIM-EU-PK-02','Order records','2026-09-17','Repeat quarterly order quantities increased','Supports repeat adoption','High','Check ordering seasonality'),
('SIM-EU-PK-03','Lost quote note','2026-04-22','Customer cited competitor unit price in rejected bid','Supports price objection','Medium','Request total-cost-in-use and exact specification'),
('SIM-EU-PK-03','Service log','2026-08-15','No material complaint recorded','Weakens technical failure hypothesis','Low','Check unrecorded quality issues'),
('SIM-EU-PK-04','Order records','2026-09-05','Order levels similar to last year','Supports stable-base hypothesis','High','Review price and volume trends'),
]

# (id,case_id,action,hypothesis,incremental_kg,probability_pct,net_price,cost_per_kg,channel_fee_per_kg,trial_cost,enablement_cost,discount_leakage,gate)
ACTIONS = [
('ACT-01','SIM-VN-FW-01','Technical qualification pilot','Competitive technical displacement',5000,65,4.35,2.75,.10,1800,500,0,'Needs technical approval'),
('ACT-02','SIM-VN-FW-01','Broad price discount','Price competitiveness unproven',6500,70,4.02,2.75,.10,350,250,2700,'Defer: price causality unverified'),
('ACT-03','SIM-VN-FW-01','Distributor application training','Sales knowledge gap',2500,60,4.35,2.75,.10,250,800,0,'Pilot after skills assessment'),
('ACT-04','SIM-VN-FW-02','New-customer prospecting','End-market demand contraction',2600,35,4.24,2.88,.10,600,1600,0,'Qualify addressable accounts first'),
('ACT-05','SIM-VN-FW-02','Selective cross-selling','Existing application adjacency',1800,50,4.38,2.96,.12,850,400,0,'Validate application and share of wallet'),
('ACT-06','SIM-VN-FW-02','Price reduction to recover volumes','Demand contraction not price-driven',2200,30,3.98,2.88,.10,100,100,1500,'Do not approve without price elasticity'),
('ACT-07','SIM-VN-FW-04','Complete delayed qualification','Technical trial not yet approved',4200,70,4.80,3.05,.12,1900,600,0,'Confirm trial success and qualification'),
('ACT-08','SIM-VN-FW-04','Cross-sell additional formulations','Adjacent applications unknown',1600,40,4.85,3.15,.12,1100,500,0,'Needs customer process mapping'),
('ACT-09','SIM-VN-FW-04','Immediate channel price discount','Qualification is primary gap',3000,25,4.40,3.05,.12,250,250,1600,'Defer: does not remove qualification gate'),
('ACT-10','SIM-EU-PK-01','OTIF recovery and safety stock','Delivery reliability',5000,78,3.43,2.30,.08,300,1800,0,'Validate stock cost and service root cause'),
('ACT-11','SIM-EU-PK-01','Technical efficiency demo','Technical proof may unlock share',3200,48,3.52,2.35,.08,1750,500,0,'Seek production-trial commitment'),
('ACT-12','SIM-EU-PK-01','Customer-wide price discount','Volume loss due to logistics',5000,30,3.10,2.30,.08,150,300,2200,'Defer: fix service before price'),
('ACT-13','SIM-EU-PK-03','Total-cost-in-use value selling','Observed price objection',3500,60,3.25,2.25,.08,750,950,0,'Needs comparable technical and cost evidence'),
('ACT-14','SIM-EU-PK-03','Competitor price match','Pure price explanation unproven',4500,72,2.98,2.25,.08,150,400,1700,'Assess account-level retained margin'),
('ACT-15','SIM-EU-PK-03','New converting application trial','Upsell through differentiation',2800,48,3.65,2.45,.10,1900,700,0,'Obtain application and compliance requirements'),
('ACT-16','SIM-EU-PK-02','Scale qualified paper-mailer application','Confirmed volume upside in scenario',3500,68,3.96,2.48,.09,1600,700,0,'Validate repeatability and compliance'),
('ACT-17','SIM-EU-PK-04','Adjacent product discovery','Share of wallet unmeasured',2200,45,3.70,2.47,.09,1000,700,0,'Map adhesive spend by application'),
]

OPPS = [
('OP-001','SIM-VN-FW-01','Lost','Technical specification',5700,'2026-01-09','2026-03-03'),
('OP-002','SIM-VN-FW-01','Open','Unknown',5000,'2026-07-04',''),
('OP-003','SIM-VN-FW-02','Lost','Customer project postponed',2500,'2026-02-10','2026-05-16'),
('OP-004','SIM-VN-FW-02','Open','Unknown',1800,'2026-08-08',''),
('OP-005','SIM-VN-FW-03','Won','Not applicable',2700,'2026-01-13','2026-04-19'),
('OP-006','SIM-VN-FW-03','Won','Not applicable',1000,'2026-05-14','2026-07-22'),
('OP-007','SIM-VN-FW-04','Open','Qualification pending',4100,'2026-05-11',''),
('OP-008','SIM-VN-FW-04','Lost','Approval / timing',1900,'2026-02-05','2026-06-19'),
('OP-009','SIM-EU-PK-01','Lost','Delivery reliability',3900,'2026-01-20','2026-05-20'),
('OP-010','SIM-EU-PK-01','Open','Unknown',2400,'2026-08-17',''),
('OP-011','SIM-EU-PK-02','Won','Not applicable',3600,'2026-01-11','2026-04-02'),
('OP-012','SIM-EU-PK-02','Won','Not applicable',1900,'2026-06-12','2026-09-15'),
('OP-013','SIM-EU-PK-03','Lost','Price objection',3400,'2026-03-21','2026-06-13'),
('OP-014','SIM-EU-PK-03','Open','Unknown',2900,'2026-08-03',''),
('OP-015','SIM-EU-PK-04','Won','Not applicable',1200,'2026-05-11','2026-07-26'),
('OP-016','SIM-EU-PK-04','Open','Unknown',1500,'2026-09-15',''),
]

def write_csv(path, headers, rows):
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w=csv.writer(f); w.writerow(headers); w.writerows(rows)

def allocate(total, weights):
    arr=[round(total*w/sum(weights)) for w in weights[:-1]]
    return arr+[total-sum(arr)]

def build(out):
    out.mkdir(parents=True,exist_ok=True)
    profile=[]; ledger=[]; diagnostic=[]
    for (cid,region,market,distributor,label,q0,q1,p0,p1,c0,c1,reason,confidence,verify) in CASES:
        profile.append([cid,label,market,region,distributor,reason,confidence,verify,'Unknown; not a real account',STATUS])
        for year, total_qty, price, cost in [(2025,q0,p0,c0),(2026,q1,p1,c1)]:
            if year==2025: weights=MONTH_WEIGHTS_2025
            elif q1<q0: weights=MONTH_WEIGHTS_2026_DECLINING
            else: weights=MONTH_WEIGHTS_2026_GROWING
            for month, qty in enumerate(allocate(total_qty, weights), start=1):
                revenue=round(qty*price,2); variable=round(qty*cost,2)
                ledger.append([f'{year}-{month:02d}-01',year,month,cid,market,region,distributor,qty,price,cost,revenue,variable,round(revenue-variable,2),STATUS])
        rev0=q0*p0;rev1=q1*p1; v=(q1-q0)*p0; pr=q1*(p1-p0)
        diagnostic.append([cid,market,region,round(q0),round(q1),round(rev0,2),round(rev1,2),p0,p1,round(v,2),round(pr,2),round(rev1-rev0,2),round(v+pr-(rev1-rev0),9),round((q1/q0-1)*100,3),round((rev1/rev0-1)*100,3),round(q1*(p1-c1),2),reason,confidence,verify,STATUS])
    write_csv(out/'P4_Case_Profile.csv',['Case_ID','Scenario_Account_Label','Market','Region','Distributor_Sim_ID','Working_Root_Cause_Hypothesis','Evidence_Confidence','Next_Verification','Real_Henkel_Relationship','Data_Status'],profile)
    write_csv(out/'P4_Monthly_Orders.csv',['Month_Start','Year','Month_Number','Case_ID','Market','Region','Distributor_Sim_ID','Volume_kg_SIM','Price_EUR_per_kg_SIM','Variable_Cost_EUR_per_kg_SIM','Net_Sales_EUR_SIM_CALC','Variable_Cost_EUR_SIM_CALC','Contribution_EUR_SIM_CALC','Data_Status'],ledger)
    write_csv(out/'P4_Diagnostics.csv',['Case_ID','Market','Region','Volume_2025_9M_kg_SIM','Volume_2026_9M_kg_SIM','Sales_2025_9M_EUR_SIM','Sales_2026_9M_EUR_SIM','Price_2025_EUR_kg_SIM','Price_2026_EUR_kg_SIM','Volume_Effect_EUR_CALC','Price_Effect_EUR_CALC','Sales_Change_EUR_CALC','Bridge_Reconciliation_EUR_CALC','Volume_Change_pct_CALC','Sales_Change_pct_CALC','2026_Contribution_EUR_SIM','Root_Cause_Hypothesis','Evidence_Confidence','Next_Verification','Data_Status'],diagnostic)
    evidence=[[f'SIG-{i:03}',cid,etype,date,observation,meaning,conf,verification,'Observed within synthetic case only',STATUS] for i,(cid,etype,date,observation,meaning,conf,verification) in enumerate(SIGNALS,1)]
    write_csv(out/'P4_Evidence_Log.csv',['Signal_ID','Case_ID','Evidence_Type_SIM','Signal_Date','Scenario_Observation','Interpretation','Confidence','Required_Verification','Evidence_Status','Data_Status'],evidence)
    opportunities=[]
    for oid,cid,stage,reason,kg,opened,closed in OPPS:
        market=next(c[2] for c in CASES if c[0]==cid)
        opportunities.append([oid,cid,market,stage,reason,kg,opened,closed,'CRM classification is synthetic, reason not independently verified',STATUS])
    write_csv(out/'P4_Win_Loss.csv',['Opportunity_ID','Case_ID','Market','Opportunity_Stage','CRM_Reason_Hypothesis','Potential_Annual_Volume_kg_ASSUMED','Created_On','Closed_On','Reason_Validation_Status','Data_Status'],opportunities)
    intervention=[]
    for aid,cid,action,hyp,kg,prob,price,cost,fee,trial,enable,discount,gate in ACTIONS:
        expected_gross=kg*(price-cost-fee)*prob/100
        exp_net=expected_gross-trial-enable-discount
        denom=kg*(price-cost-fee)
        breakeven=100*(trial+enable+discount)/denom if denom>0 else None
        intervention.append([aid,cid,action,hyp,kg,prob,price,cost,fee,trial,enable,discount,round(expected_gross,2),round(exp_net,2),round(breakeven,2) if breakeven is not None else '',gate,STATUS])
    write_csv(out/'P4_Interventions.csv',['Action_ID','Case_ID','Action','Causal_Hypothesis','Conditional_Incremental_Volume_kg_ASSUMED','Success_Probability_pct_ASSUMED','Incremental_Net_Price_EUR_kg_ASSUMED','Variable_Cost_EUR_kg_ASSUMED','Channel_Fee_EUR_kg_ASSUMED','Trial_Cost_EUR_ASSUMED','Enablement_Cost_EUR_ASSUMED','Retained_Base_Discount_Leakage_EUR_ASSUMED','Expected_Contribution_Before_Fixed_EUR_CALC','Expected_Net_Contribution_EUR_CALC','BreakEven_Probability_pct_CALC','Approval_Gate','Data_Status'],intervention)
    winners=[]
    for cid,*_ in CASES:
        candidates=[r for r in intervention if r[1]==cid]
        if not candidates:
            winners.append([cid,'HOLD','No modeled intervention',0,'Investigate before prioritizing','Hold / no monetized option',STATUS])
            continue
        winner=max(candidates,key=lambda r:r[13])
        if winner[13]<=0:
            winners.append([cid,'HOLD','No positive modeled intervention',0,'Reassess evidence and assumptions','Hold; no economically positive option',STATUS])
        else:
            winners.append([cid,winner[0],winner[2],winner[13],winner[15],'Screened option only; approval pending',STATUS])
    write_csv(out/'P4_Action_Shortlist.csv',['Case_ID','Highest_Model_Score_Action_ID','Action','Expected_Net_Contribution_EUR_SIM','Mandatory_Approval_Gate','Decision_Status','Data_Status'],winners)
    total_2025=sum(r[5] for r in diagnostic); total_2026=sum(r[6] for r in diagnostic)
    wins=sum(x[2]=='Won' for x in OPPS); losses=sum(x[2]=='Lost' for x in OPPS)
    kpis={'case_count':len(CASES),'simulated_monthly_records':len(ledger),'simulated_sales_2025_9m_eur':round(total_2025,2),'simulated_sales_2026_9m_eur':round(total_2026,2),'sales_yoy_pct':round((total_2026/total_2025-1)*100,3),'volume_effect_eur':round(sum(r[9] for r in diagnostic),2),'price_effect_eur':round(sum(r[10] for r in diagnostic),2),'bridge_reconciliation_eur':round(sum(r[12] for r in diagnostic),6),'closed_wins':wins,'closed_losses':losses,'closed_win_rate_pct':round(100*wins/(wins+losses),2),'open_opportunities':sum(x[2]=='Open' for x in OPPS),'highest_option_expected_net_total_eur':round(sum(r[3] for r in winners),2),'all_data':'SIMULATED; no actual Henkel CRM sales, distributor or customer data'}
    (out/'P4_Run_Results.json').write_text(json.dumps(kpis,indent=2),encoding='utf-8')
    assert abs(kpis['bridge_reconciliation_eur'])<0.001
    assert len(ledger)==144
    assert all(r[-1]==STATUS for r in ledger)
    return kpis

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--output-dir',default=str(Path(__file__).parent))
    args=parser.parse_args()
    print(json.dumps(build(Path(args.output_dir)),indent=2))
