#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自算历史 PE(TTM) / PB 序列并计算近5年、近10年分位"""
import json, os, datetime as dt

D = os.path.dirname(os.path.abspath(__file__))
L = lambda n: json.load(open(os.path.join(D, n + ".json"), encoding="utf-8"))

income = L("income"); bal = L("balance"); val = L("valuation")
kraw = json.load(open(os.path.join(D, "kline_raw.json"), encoding="utf-8"))["data"]["klines"]

def dd(s): return dt.date.fromisoformat(s[:10])

# ---------- 1. 单季归母净利 & 归母净资产，按公告日 ----------
inc = {}
for r in income:
    rd = dd(r["REPORT_DATE"])
    nd = dd(r["NOTICE_DATE"]) if r.get("NOTICE_DATE") else rd
    inc[rd] = dict(r, NOTICE=nd)
bl = {}
for r in bal:
    rd = dd(r["REPORT_DATE"])
    nd = dd(r["NOTICE_DATE"]) if r.get("NOTICE_DATE") else rd
    bl[rd] = dict(r, NOTICE=nd)

def key(y, m, d):
    try: return dt.date(y, m, d)
    except Exception: return None

ann = sorted(inc)
q_np = {}          # (year, quarter) -> single-quarter 归母净利
for rd, r in inc.items():
    y, m = rd.year, rd.month
    if m == 3:
        q_np[(y, 1)] = r["PARENT_NETPROFIT"]
    elif m == 6:
        q1 = inc.get(key(y, 3, 31))
        if q1: q_np[(y, 2)] = r["PARENT_NETPROFIT"] - q1["PARENT_NETPROFIT"]
    elif m == 9:
        h1 = inc.get(key(y, 6, 30))
        if h1: q_np[(y, 3)] = r["PARENT_NETPROFIT"] - h1["PARENT_NETPROFIT"]
    elif m == 12:
        q3 = inc.get(key(y, 9, 30))
        if q3: q_np[(y, 4)] = r["PARENT_NETPROFIT"] - q3["PARENT_NETPROFIT"]

# 公告日 -> TTM 与 净资产
events = []   # (notice_date, ttm_np, parent_equity)
sorted_q = sorted(q_np.keys())
for rd, r in inc.items():
    y, m = rd.year, rd.month
    qn = {3: 1, 6: 2, 9: 3, 12: 4}[m]
    # TTM = 本季 + 前3季
    seq = []
    cy, cq = y, qn
    for _ in range(4):
        seq.append((cy, cq))
        cq -= 1
        if cq == 0: cy -= 1; cq = 4
    if all(s in q_np for s in seq):
        ttm = sum(q_np[s] for s in seq)
        ev = r["NOTICE"]
        eq = bl.get(rd, {}).get("TOTAL_PARENT_EQUITY")
        events.append((ev, ttm, eq, rd))
events.sort()
print("事件数:", len(events))

def state_on(d):
    ttm = eq = None
    for ev, t, e, rd in events:
        if ev <= d:
            ttm, eq = t, e
        else:
            break
    return ttm, eq

# ---------- 2. 股本序列 ----------
sc = []
prev = None
for r in sorted(bal, key=lambda x: x["REPORT_DATE"]):
    v = r.get("SHARE_CAPITAL")
    if v != prev:
        sc.append((dd(r["REPORT_DATE"]), v)); prev = v

def shares_on(d):
    v = sc[0][1]
    for rd, s in sc:
        if rd <= d: v = s
        else: break
    return v

# ---------- 3. 逐日市值 / PE / PB ----------
rows = []
for k in kraw:
    p = k.split(",")
    d = dd(p[0]); close = float(p[2])
    ttm, eq = state_on(d)
    sh = shares_on(d)
    mc = close * sh
    pe = mc / ttm if ttm and ttm > 0 else None
    pb = mc / eq if eq else None
    rows.append((d, close, mc, pe, pb, sh, ttm, eq))
print("交易日:", len(rows), rows[0][0], "->", rows[-1][0])

def pctl(vals, x):
    v = sorted([i for i in vals if i is not None])
    if not v: return None
    return sum(1 for i in v if i <= x) / len(v) * 100

def window(years, end=dt.date(2026, 9, 15)):
    start = end - dt.timedelta(days=int(365.25 * years))
    return [r for r in rows if start <= r[0] <= end], start

def stat(name, idx, years):
    w, start = window(years)
    vals = [r[idx] for r in w if r[idx] is not None and r[idx] > 0]
    if not vals: print(f"{name} 无数据"); return
    cur = None
    for r in reversed(rows):
        if r[0] <= dt.date(2026, 9, 15) and r[idx] is not None:
            cur = r[idx]; break
    sv = sorted(vals)
    def q(p): return sv[min(len(sv) - 1, int(len(sv) * p))]
    print(f"\n【{name}】 窗口 {start} ~ 2026-09-15  样本 {len(vals)}个交易日")
    print(f"  当前值: {cur:.3f}")
    print(f"  分位数(当前值在历史中的位置): {pctl(vals, cur):.1f}%")
    print(f"  最低 {sv[0]:.2f} | 5% {q(0.05):.2f} | 25% {q(0.25):.2f} | 中位 {q(0.5):.2f} | 75% {q(0.75):.2f} | 95% {q(0.95):.2f} | 最高 {sv[-1]:.2f}")
    print(f"  均值 {sum(sv)/len(sv):.2f}")

print("\n" + "=" * 90)
print("自算估值分位（不复权收盘价 × 当期总股本，TTM按公告日生效）")
print("=" * 90)
stat("PE(TTM)", 3, 5); stat("PE(TTM)", 3, 10)
stat("PB(MRQ)", 4, 5); stat("PB(MRQ)", 4, 10)

# 年度PE/PB区间
print("\n" + "=" * 90)
print("年度 PE / PB 区间（自算，年末值 + 年内区间）")
print("=" * 90)
for y in range(2011, 2027):
    w = [r for r in rows if r[0].year == y]
    if not w: continue
    pes = [r[3] for r in w if r[3] and r[3] > 0]
    pbs = [r[4] for r in w if r[4] and r[4] > 0]
    last = w[-1]
    pe_s = f"{last[3]:>7.2f}" if last[3] else "   N/A "
    pb_s = f"{last[4]:>5.2f}" if last[4] else " N/A "
    pe_r = f"{min(pes):.1f}-{max(pes):.1f}" if pes else "全年亏损/无正PE"
    pb_r = f"{min(pbs):.2f}-{max(pbs):.2f}" if pbs else "N/A"
    print(f"{y}: 年末收盘 {last[1]:>6.2f} | 总市值 {last[2]/1e8:>7.1f}亿 | 股本 {last[5]/1e8:.2f}亿 | 年末PE {pe_s} (区间 {pe_r}) | 年末PB {pb_s} (区间 {pb_r})")

# ---------- 4. 与东财官方 PE_TTM/PB 对照（2018+）----------
print("\n" + "=" * 90)
print("交叉验证：自算 vs 东方财富 RPT_VALUEANALYSIS_DET（抽样）")
print("=" * 90)
vmap = {dd(r["TRADE_DATE"]): r for r in val}
mine = {r[0]: r for r in rows}
cnt = 0
for d in sorted(vmap, reverse=True):
    if d in mine and cnt < 12:
        a = mine[d]
        b = vmap[d]
        eps = abs(a[3] - b["PE_TTM"]) / b["PE_TTM"] * 100 if a[3] else None
        pbs = abs(a[4] - b["PB_MRQ"]) / b["PB_MRQ"] * 100 if a[4] else None
        print(f"{d} 自算PE {a[3]:.3f} / 东财 {b['PE_TTM']:.3f} (差{eps:.2f}%) | 自算PB {a[4]:.3f} / 东财 {b['PB_MRQ']:.3f} (差{pbs:.2f}%) | 收盘 {a[1]} / {b['CLOSE_PRICE']}")
        cnt += 1

# ---------- 5. 东财估值序列分位 ----------
print("\n" + "=" * 90)
print("东方财富 RPT_VALUEANALYSIS_DET 全量分位（2018-01-02 起）")
print("=" * 90)
vrows = sorted(val, key=lambda r: r["TRADE_DATE"])
cur = vrows[-1]
print("最新记录日:", cur["TRADE_DATE"][:10], "PE_TTM", round(cur["PE_TTM"], 3), "PB", round(cur["PB_MRQ"], 3),
      "PS_TTM", round(cur["PS_TTM"], 3), "PE_LAR", round(cur["PE_LAR"], 3), "总市值", round(cur["TOTAL_MARKET_CAP"]/1e8, 2), "亿")
for fld in ["PE_TTM", "PB_MRQ", "PS_TTM"]:
    vals = [r[fld] for r in vrows if r.get(fld) and r[fld] > 0]
    sv = sorted(vals)
    c = cur.get(fld)
    print(f"  {fld}: 当前 {c:.3f} | 分位 {sum(1 for x in sv if x<=c)/len(sv)*100:.1f}% | 最低 {sv[0]:.2f} 中位 {sv[len(sv)//2]:.2f} 最高 {sv[-1]:.2f} | 样本 {len(sv)}")
