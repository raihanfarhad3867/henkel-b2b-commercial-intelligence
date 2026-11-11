"""Henkel APC Phase 5 | independent portfolio simulation.

Reproducible synthetic commercial experiment panel and analysis, NOT Henkel's
real customer/distributor data or an actual experiment.
Python 3.10+, standard library only.  Outputs CSV/JSON to this script's folder.
"""
from __future__ import annotations
from collections import defaultdict
from csv import DictWriter
from pathlib import Path
from math import isfinite
import argparse, json, random, statistics

_parser=argparse.ArgumentParser(description="Generate synthetic Phase 5 experiment data")
_parser.add_argument('--output-dir',default='outputs/phase5')
_args=_parser.parse_args()
ROOT = Path(_args.output_dir).resolve()
ROOT.mkdir(parents=True, exist_ok=True)
SEED = 20261111
RNG = random.Random(SEED)
STATUS = "SIMULATED — NOT HENKEL CUSTOMER OR DISTRIBUTOR DATA"

EXPERIMENTS = [
    dict(id="EX-01", market="Vietnam footwear", program="Technical qualification recovery", p4="ACT-01", design="Matched nonrandom comparison", assign="Eligible manufacturing accounts", primary="Contribution per eligible account-month", guardrail="Line qualification + product safety / returns", months=6, fixed_cost=2400, volume_effect=0.19, price_effect=0, baseline_kg=165, price=4.35, cost_kg=2.75, fee_kg=0.10, bar=0, owner="Application engineering + regional sales", gate="Technical sign-off and verified trial protocol", risk="Selection into technical trials"),
    dict(id="EX-02", market="Vietnam footwear", program="Distributor skills & joint selling", p4="ACT-03", design="Cluster assignment if feasible", assign="Distributor-led account cluster", primary="Contribution per account-month", guardrail="Customer complaint rate / channel conflicts", months=6, fixed_cost=1500, volume_effect=0.095, price_effect=0, baseline_kg=180, price=4.25, cost_kg=2.76, fee_kg=0.11, bar=0, owner="Channel excellence + sales enablement", gate="Partner participation and no contamination", risk="Cluster spillover / too few distributors"),
    dict(id="EX-03", market="EU paper packaging", program="OTIF service-recovery intervention", p4="ACT-10", design="Staggered rollout / matched comparison", assign="Service-affected converting accounts", primary="Recovered contribution per account-month", guardrail="Working capital / stockouts / service fairness", months=6, fixed_cost=1900, volume_effect=0.155, price_effect=0, baseline_kg=195, price=3.43, cost_kg=2.30, fee_kg=0.08, bar=0, owner="Customer service + supply chain + sales", gate="Operations confirms stock and working-capital feasibility", risk="Nonparallel demand trends; do not withhold needed service"),
    dict(id="EX-04", market="EU paper packaging", program="Value-selling coaching", p4="ACT-13", design="Account-level randomized offer if feasible", assign="Sales account", primary="Contribution per account-month", guardrail="Volume retention and customer satisfaction", months=6, fixed_cost=1950, volume_effect=-0.005, price_effect=0.055, baseline_kg=145, price=3.25, cost_kg=2.25, fee_kg=0.08, bar=0, owner="Pricing + technical sales", gate="Legal / pricing approval; no unjustified discounts", risk="Commercial spillover; realized net price mix"),
    dict(id="EX-05", market="EU paper packaging", program="Paper-seal application expansion", p4="ACT-16", design="Qualified application pilot with matched comparison", assign="Eligible converter / application", primary="Incremental contribution per account-month", guardrail="Product qualification, compliance and repeat orders", months=6, fixed_cost=3800, volume_effect=0.080, price_effect=0, baseline_kg=140, price=3.96, cost_kg=2.48, fee_kg=0.09, bar=0, owner="Packaging product management + technical sales", gate="Compliance + product trial approval before scale", risk="Qualification bias and uncertain repeat volumes"),
]


def round2(x): return round(float(x),2)

def write_csv(path, rows, columns):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w=DictWriter(f, fieldnames=columns);w.writeheader();w.writerows([{k:r.get(k,"") for k in columns} for r in rows])

panel=[]
accounts=defaultdict(lambda: defaultdict(list))
for ex in EXPERIMENTS:
    for arm in ("Treatment", "Control"):
        for ai in range(1,13):
            account=f"SYN-{ex['id']}-{arm[0]}{ai:02d}"
            # Account-specific heterogeneity is fixed through baseline and follow-up.
            account_scale=RNG.uniform(.70,1.30)
            account_price_scale=RNG.uniform(.975,1.025)
            account_vol_shock=RNG.uniform(-.04,.04)
            for month in range(1,7):
                period="Pre" if month<=3 else "Post"
                noise=RNG.uniform(-.035,.035)
                volume_index=1+account_vol_shock+noise
                if period=="Post":
                    volume_index*=0.985 # common demand headwind
                    if arm=="Treatment":
                        volume_index*=1+ex["volume_effect"]
                vol=round2(ex["baseline_kg"]*account_scale*volume_index)
                price=ex["price"]*account_price_scale*(1.012 if period=="Post" else 1)
                if period=="Post" and arm=="Treatment": price*=1+ex["price_effect"]
                price=round2(price)
                revenue=round2(vol*price)
                total_variable=round2(vol*(ex["cost_kg"]+ex["fee_kg"]))
                contribution=round2(revenue-total_variable)
                otif=round2(max(75,min(100,89+RNG.uniform(-3,3)+(7 if (ex['id']=="EX-03" and period=="Post" and arm=="Treatment") else 0))))
                trial=1 if (ex['id'] in ('EX-01','EX-05') and period=="Post" and arm=="Treatment" and ai<=5 and month==6) else 0
                row={"Experiment_ID":ex['id'],"Synthetic_Account_ID":account,"Market":ex['market'],"Arm":arm,"Period":period,"Simulation_Month":f"SIM-M{month}","Volume_Kg_SIM":vol,"Net_Price_EUR_Kg_SIM":price,"Net_Sales_EUR_SIM":revenue,"Variable_And_Channel_Cost_EUR_SIM":total_variable,"Contribution_EUR_SIM":contribution,"OTIF_pct_SIM":otif,"Qualified_Trial_Illustration_SIM":trial,"Data_Status":STATUS}
                panel.append(row);accounts[ex['id']][account].append(row)

# Account-level pre-post comparisons; arithmetic mean of monthly contribution per account.
account_metrics={}
for e,accts in accounts.items():
    account_metrics[e]={}
    for aid,rows in accts.items():
        pre=statistics.mean(r['Contribution_EUR_SIM'] for r in rows if r['Period']=='Pre')
        post=statistics.mean(r['Contribution_EUR_SIM'] for r in rows if r['Period']=='Post')
        account_metrics[e][aid]={'arm':rows[0]['Arm'],'pre':pre,'post':post,'delta':post-pre}

def did(vals_t, vals_c): return statistics.mean(vals_t)-statistics.mean(vals_c)

def bootstrap_ci(t,c,seed=1945,rounds=2400):
    rg=random.Random(seed); sample=[]
    for i in range(rounds):
        st=[t[rg.randrange(len(t))] for _ in t]
        sc=[c[rg.randrange(len(c))] for _ in c]
        sample.append(did(st,sc))
    sample.sort(); return sample[int(rounds*.05)],sample[int(rounds*.95)-1]

results=[]
for idx,ex in enumerate(EXPERIMENTS):
    ac=account_metrics[ex['id']]
    treat=[a for a,v in ac.items() if v['arm']=='Treatment']
    control=[a for a,v in ac.items() if v['arm']=='Control']
    tp=statistics.mean(ac[a]['pre'] for a in treat);tq=statistics.mean(ac[a]['post'] for a in treat)
    cp=statistics.mean(ac[a]['pre'] for a in control);cq=statistics.mean(ac[a]['post'] for a in control)
    monthly_did=did([ac[a]['delta'] for a in treat],[ac[a]['delta'] for a in control])
    lo,hi=bootstrap_ci([ac[a]['delta'] for a in treat],[ac[a]['delta'] for a in control],seed=1945+idx)
    # 12-month upside extrapolates a 3-month simulation; do not treat as forecast.
    annual=monthly_did*len(treat)*12
    net=annual-ex['fixed_cost']
    ci_net_low=lo*len(treat)*12-ex['fixed_cost']
    ci_net_high=hi*len(treat)*12-ex['fixed_cost']
    if net<=0: decision="HOLD — economics unfavorable"
    elif ci_net_low<=0: decision="LEARN MORE — uncertain range"
    else: decision="CONDITIONAL PILOT — gates required"
    results.append({"Experiment_ID":ex['id'],"Program":ex['program'],"Treated_Accounts_SIM":len(treat),"Control_Accounts_SIM":len(control),"Treatment_Pre_Contribution_EUR_per_Account_Month_SIM":round2(tp),"Treatment_Post_Contribution_EUR_per_Account_Month_SIM":round2(tq),"Control_Pre_Contribution_EUR_per_Account_Month_SIM":round2(cp),"Control_Post_Contribution_EUR_per_Account_Month_SIM":round2(cq),"DiD_EUR_per_Account_Month_CALC":round2(monthly_did),"Annualized_Contribution_Before_Program_EUR_SCENARIO":round2(annual),"Program_Fixed_Cost_EUR_ASSUMED":ex['fixed_cost'],"Annualized_Net_EUR_SCENARIO":round2(net),"Bootstrap_90pct_Low_Net_EUR_SIM":round2(ci_net_low),"Bootstrap_90pct_High_Net_EUR_SIM":round2(ci_net_high),"Decision_Screen":decision,"Causal_Interpretation":"NOT causal proof; simulated counterfactual with stated design limitations","Data_Status":STATUS})

panel_fields=list(panel[0])
result_fields=list(results[0])
write_csv(ROOT/'P5_Synthetic_Experiment_Panel.csv',panel,panel_fields)
write_csv(ROOT/'P5_Effect_Estimates.csv',results,result_fields)
design=[]
for e in EXPERIMENTS:
    design.append({"Experiment_ID":e['id'],"Market":e['market'],"Program":e['program'],"Linked_P4_Action":e['p4'],"Study_Design":e['design'],"Assignment_Unit":e['assign'],"Primary_Metric":e['primary'],"Guardrail":e['guardrail'],"Simulated_Months":e['months'],"Program_Cost_EUR_ASSUMED":e['fixed_cost'],"Treatment_Volume_Effect_ASSUMED":e['volume_effect'],"Treatment_Price_Effect_ASSUMED":e['price_effect'],"Account_Count_Per_Arm_SIM":12,"Owner_Role":e['owner'],"Mandatory_Gate":e['gate'],"Design_Threat":e['risk'],"Data_Status":STATUS})
write_csv(ROOT/'P5_Experiment_Design.csv',design,list(design[0]))

decisions=[]
for r,e in zip(results,EXPERIMENTS):
    decisions.append({"Experiment_ID":e['id'],"Program":e['program'],"Screened_Net_EUR_Annualized":r['Annualized_Net_EUR_SCENARIO'],"Uncertainty_Low_EUR":r['Bootstrap_90pct_Low_Net_EUR_SIM'],"Screen_Result":r['Decision_Screen'],"Mandatory_Gate":e['gate'],"Evidence_Required":"Real CRM / customer or plant KPIs, baseline comparability, cost approval, legal and safety review","Can_Deploy_Now":"NO — synthetic exercise, no real approvals","Data_Status":STATUS})
write_csv(ROOT/'P5_Management_Decision_Gates.csv',decisions,list(decisions[0]))

summary={"seed":SEED,"panel_rows":len(panel),"experiments":len(EXPERIMENTS),"distinct_synthetic_accounts":len(set(r['Synthetic_Account_ID'] for r in panel)),"treatment_control_balance":{e['id']: {arm:len(set(r['Synthetic_Account_ID'] for r in panel if r['Experiment_ID']==e['id'] and r['Arm']==arm)) for arm in ('Treatment','Control')} for e in EXPERIMENTS},"data_status":STATUS,"effects":results,"limitations":["All observations generated from hypothetical assumptions; no Henkel operational data.","Treatment and comparison series are synthetic; results are NOT evidence of real causality.","Annualized value assumes 12 months of post period performance and excludes unmodeled overhead and implementation uncertainty.","Bootstrap interval describes synthetic sampling variation only, not uncertainty about the real world.","Rollout requires actual customers, approvals, baseline checks and ethics/safety review."]}
(ROOT/'P5_Validation.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')

assert len(panel)==5*2*12*6
assert all(isfinite(r['Annualized_Net_EUR_SCENARIO']) for r in results)
assert len({r['Synthetic_Account_ID'] for r in panel})==120
for e in EXPERIMENTS:
    vals=account_metrics[e['id']]
    assert len(vals)==24
print(json.dumps({"panel_rows":len(panel),"synthetic_accounts":120,"results":[(r['Experiment_ID'],r['Annualized_Net_EUR_SCENARIO'],r['Decision_Screen']) for r in results]},indent=2))
