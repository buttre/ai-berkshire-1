#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os, datetime as dt

D = os.path.dirname(os.path.abspath(__file__))
def load(n): return json.load(open(os.path.join(D, n + ".json"), encoding="utf-8"))

lico = load("lico"); income = load("income"); bal = load("balance")
cf = load("cashflow"); val = load("valuation"); div = load("dividend")

def date(r, k="REPORT_DATE"):
    return (r.get(k) or r.get("REPORTDATE") or r.get("TRADE_DATE"))[:10]

def yi(x):
    return None if x is None else x / 1e8

def pct(x):
    return None if x is None else round(x * 100, 2)

# ---------- build dicts by date ----------
inc = {date(r): r for r in income}
bl = {date(r): r for r in bal}
cfl = {date(r): r for r in cf}
ke = {date(r, "REPORTDATE"): r for r in lico}

def years_back(n, up_to=2025):
    return list(range(up_to - n + 1, up_to + 1))

print("="*110)
print("【A】年度核心损益与盈利能力  2011-2025")
print("="*110)
hdr = f"{'年':<6}{'营收(亿)':>11}{'YoY%':>9}{'归母净利(亿)':>13}{'YoY%':>10}{'扣非(亿)':>11}{'毛利率%':>9}{'净利率%':>9}{'ROE加权%':>10}{'BPS':>8}{'EPS':>8}"
print(hdr)
rows = []
for y in range(2011, 2026):
    d = f"{y}-12-31"
    r = inc.get(d); b = bl.get(d); k = ke.get(d)
    if not r: continue
    rev = r.get("TOTAL_OPERATE_INCOME")
    np_ = r.get("PARENT_NETPROFIT")
    dnp = r.get("DEDUCT_PARENT_NETPROFIT")
    opc = r.get("OPERATE_COST")
    ctl = r.get("TOTAL_OPERATE_COST")
    gm = (1 - opc / rev) * 100 if rev and opc else None
    nm = np_ / rev * 100 if rev and np_ is not None else None
    roe = k.get("WEIGHTAVG_ROE") if k else None
    bps = k.get("BPS") if k else (b.get("PARENT_EQUITY_BALANCE", 0) / b.get("SHARE_CAPITAL") if b and b.get("SHARE_CAPITAL") else None)
    eps = r.get("BASIC_EPS")
    ry = r.get("TOTAL_OPERATE_INCOME_YOY")
    ny = r.get("PARENT_NETPROFIT_YOY")
    rows.append(dict(y=y, rev=rev, np=np_, dnp=dnp, gm=gm, nm=nm, roe=roe, bps=bps,
                     eps=eps, ry=ry, ny=ny))
    print(f"{y:<6}{yi(rev):>11.2f}{(ry or 0):>9.1f}{yi(np_):>13.2f}{(ny or 0):>10.1f}{yi(dnp):>11.2f}"
          f"{(gm or 0):>9.2f}{(nm or 0):>9.2f}{(roe or 0):>10.2f}{(bps or 0):>8.3f}{(eps or 0):>8.3f}")

print()
print("="*110)
print("【B】现金流 / 资产负债率  2011-2025 (亿元)")
print("="*110)
print(f"{'年':<6}{'经营现金流':>12}{'资本开支':>11}{'FCF':>11}{'资产负债率%':>12}{'归母净资产':>12}{'总资产':>11}{'货币资金':>10}")
for y in range(2011, 2026):
    d = f"{y}-12-31"
    c = cfl.get(d); b = bl.get(d)
    if not c or not b: continue
    ocf = c.get("NETCASH_OPERATE")
    capex = c.get("CONSTRUCT_LONG_ASSET")
    fcf = (ocf - capex) if (ocf is not None and capex is not None) else None
    dar = b.get("TOTAL_LIABILITIES") / b.get("TOTAL_ASSETS") * 100 if b.get("TOTAL_ASSETS") else None
    print(f"{y:<6}{yi(ocf):>12.2f}{yi(capex):>11.2f}{yi(fcf):>11.2f}{(dar or 0):>12.2f}"
          f"{yi(b.get('TOTAL_PARENT_EQUITY')):>12.2f}{yi(b.get('TOTAL_ASSETS')):>11.2f}{yi(b.get('MONETARYFUNDS')):>10.2f}")

print()
print("="*110)
print("【C】2026 中报 / 2026Q2 单季")
print("="*110)
def getq(d):
    r = inc.get(d);
    return r
h1 = inc["2026-06-30"]; q1 = inc["2026-03-31"]
h1b = bl["2026-06-30"]; h1c = cfl["2026-06-30"]; h1k = ke["2026-06-30"]
for lab, r, k, b, c in [("2026H1", h1, h1k, h1b, h1c), ("2026Q1", q1, ke.get("2026-03-31"), bl.get("2026-03-31"), cfl.get("2026-03-31"))]:
    rev = r["TOTAL_OPERATE_INCOME"]; np_ = r["PARENT_NETPROFIT"]; dnp = r["DEDUCT_PARENT_NETPROFIT"]
    gm = (1 - r["OPERATE_COST"] / rev) * 100
    print(f"{lab}: 营收 {rev/1e8:.2f}亿 (YoY {r['TOTAL_OPERATE_INCOME_YOY']:.2f}%) | 归母净利 {np_/1e8:.4f}亿 (YoY {r['PARENT_NETPROFIT_YOY']:.2f}%) | "
          f"扣非 {dnp/1e8:.4f}亿 (YoY {r['DEDUCT_PARENT_NETPROFIT_YOY']:.2f}%) | 毛利率 {gm:.2f}% | 净利率 {np_/rev*100:.2f}% | ROE加权 {k.get('WEIGHTAVG_ROE')}%")
    if c:
        print(f"    经营现金流 {c['NETCASH_OPERATE']/1e8:.2f}亿 | 资本开支 {c['CONSTRUCT_LONG_ASSET']/1e8:.2f}亿 | "
              f"FCF {(c['NETCASH_OPERATE']-c['CONSTRUCT_LONG_ASSET'])/1e8:.2f}亿 | 资产负债率 {b['TOTAL_LIABILITIES']/b['TOTAL_ASSETS']*100:.2f}% | BPS {h1k.get('BPS') if lab=='2026H1' else k.get('BPS')}")

# Q2 single quarter
def q_single(cur, prev, key):
    a = cur.get(key); b_ = prev.get(key)
    if a is None or b_ is None: return None
    return a - b_
print()
r2 = {}
for key, nm_ in [("TOTAL_OPERATE_INCOME","营收"),("PARENT_NETPROFIT","归母净利"),("DEDUCT_PARENT_NETPROFIT","扣非"),
                 ("OPERATE_COST","营业成本"),("TOTAL_OPERATE_COST","营业总成本"),("OPERATE_PROFIT","营业利润"),
                 ("TOTAL_PROFIT","利润总额"),("NETPROFIT","净利润"),("MINORITY_INTEREST","少数股东损益")]:
    r2[key] = q_single(h1, q1, key)
rev2 = r2["TOTAL_OPERATE_INCOME"]
print(f"2026Q2单季: 营收 {rev2/1e8:.2f}亿 | 归母净利 {r2['PARENT_NETPROFIT']/1e8:.4f}亿 | 扣非 {r2['DEDUCT_PARENT_NETPROFIT']/1e8:.4f}亿 | "
      f"毛利率 {(1-r2['OPERATE_COST']/rev2)*100:.2f}% | 净利率 {r2['PARENT_NETPROFIT']/rev2*100:.2f}%")
# YoY for Q2 single
h1_25 = inc["2025-06-30"]; q1_25 = inc["2025-03-31"]
rev2_25 = h1_25["TOTAL_OPERATE_INCOME"] - q1_25["TOTAL_OPERATE_INCOME"]
np2_25 = h1_25["PARENT_NETPROFIT"] - q1_25["PARENT_NETPROFIT"]
dnp2_25 = h1_25["DEDUCT_PARENT_NETPROFIT"] - q1_25["DEDUCT_PARENT_NETPROFIT"]
print(f"2025Q2单季: 营收 {rev2_25/1e8:.2f}亿 | 归母净利 {np2_25/1e8:.4f}亿 | 扣非 {dnp2_25/1e8:.4f}亿")
print(f"2026Q2 YoY: 营收 {(rev2/rev2_25-1)*100:.2f}% | 归母净利 {(r2['PARENT_NETPROFIT']/np2_25-1)*100:.2f}% | 扣非 {(r2['DEDUCT_PARENT_NETPROFIT']/dnp2_25-1)*100:.2f}%")

print()
print("="*110)
print("【D】2026H1 资产负债表健康度")
print("="*110)
B = h1b
items = {
 "货币资金": "MONETARYFUNDS", "交易性金融资产": "TRADE_FINASSET", "应收账款": "ACCOUNTS_RECE",
 "存货": "INVENTORY", "固定资产": "FIXED_ASSET", "在建工程": "CIP", "使用权资产": "USERIGHT_ASSET",
 "无形资产": "INTANGIBLE_ASSET", "商誉": "GOODWILL", "长期股权投资": "LONG_EQUITY_INVEST",
 "总资产": "TOTAL_ASSETS", "流动资产": "TOTAL_CURRENT_ASSETS", "非流动资产": "TOTAL_NONCURRENT_ASSETS",
 "短期借款": "SHORT_LOAN", "应付账款": "ACCOUNTS_PAYABLE", "一年内到期非流动负债": "NONCURRENT_LIAB_1YEAR",
 "长期借款": "LONG_LOAN", "应付债券": "BOND_PAYABLE", "租赁负债": "LEASE_LIAB",
 "长期应付款": "LONG_PAYABLE", "总负债": "TOTAL_LIABILITIES", "流动负债": "TOTAL_CURRENT_LIAB",
 "非流动负债": "TOTAL_NONCURRENT_LIAB", "归母净资产": "TOTAL_PARENT_EQUITY",
 "少数股东权益": "MINORITY_EQUITY", "股东权益合计": "TOTAL_EQUITY", "股本(股)": "SHARE_CAPITAL",
 "永续债": "PERPETUAL_BOND",
}
for k, v in items.items():
    x = B.get(v)
    if x is None: print(f"  {k:<22} N/A"); continue
    if k == "股本(股)": print(f"  {k:<22} {x/1e8:.4f}亿股")
    else: print(f"  {k:<22} {x/1e8:>12.4f} 亿")

print()
print("="*110)
print("【E】分红历史")
print("="*110)
for r in div:
    print(f"{date(r,'REPORT_DATE'):<12} 方案: {r.get('IMPL_PLAN_PROFILE')!s:<40} 除权日: {date(r,'EX_DIVIDEND_DATE')} 股息率: {r.get('DIVIDENT_RATIO')} 每股分红(税前元): {r.get('PRETAX_BONUS_RMB')} EPS: {r.get('BASIC_EPS')} BPS: {r.get('BVPS')}")
