#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""中远海特 600428.SH 数据采集 — 东方财富 datacenter / datacenter-web"""
import json, subprocess, sys, os, time
from urllib.parse import quote

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
OUT = os.path.dirname(os.path.abspath(__file__))

def curl(url, referer="https://data.eastmoney.com/"):
    for attempt in range(3):
        r = subprocess.run(["curl", "-s", "--max-time", "40", "--noproxy", "*",
                            "-H", f"User-Agent: {UA}", "-H", f"Referer: {referer}", url],
                           capture_output=True)
        if r.returncode == 0 and r.stdout.strip():
            try:
                return json.loads(r.stdout.decode("utf-8"))
            except Exception:
                pass
        time.sleep(1.5)
    raise RuntimeError("fail: " + url[:180])

def dc_web(report, filt, page_size=500, sort_cols="", sort_types="-1", page=1):
    url = ("https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=" + report +
           "&columns=ALL&filter=" + quote(filt, safe="") +
           f"&pageSize={page_size}&pageNumber={page}&sortColumns={sort_cols}&sortTypes={sort_types}"
           "&source=WEB&client=WEB")
    return curl(url)

def dc_sec(report, filt, page_size=500, sort_cols="", sort_types="-1", page=1):
    url = ("https://datacenter.eastmoney.com/securities/api/data/v1/get?reportName=" + report +
           "&columns=ALL&filter=" + quote(filt, safe="") +
           f"&pageSize={page_size}&pageNumber={page}&sortColumns={sort_cols}&sortTypes={sort_types}"
           "&source=HSF10&client=PC")
    return curl(url, referer="https://emweb.securities.eastmoney.com/")

def fetch_all(fn, report, filt, sort_cols, page_size=500, tag=""):
    """fetch all pages"""
    allrows = []
    p = 1
    while True:
        j = fn(report, filt, page_size=page_size, sort_cols=sort_cols, page=p)
        res = j.get("result")
        if not res:
            break
        allrows += res.get("data") or []
        pages = res.get("pages", 1)
        if p >= pages:
            break
        p += 1
        if p > 20:
            break
    print(f"[{tag}] {report}: {len(allrows)} rows")
    return allrows

def save(name, rows):
    path = os.path.join(OUT, name + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)
    print("  -> saved", path)

F = '(SECURITY_CODE="600428")'
FS = '(SECUCODE="600428.SH")'

# 1. 业绩报表（关键指标，全历史）
save("lico", fetch_all(dc_web, "RPT_LICO_FN_CPD", F, "REPORTDATE", tag="key"))
# 2. 利润表
save("income", fetch_all(dc_sec, "RPT_F10_FINANCE_GINCOME", FS, "REPORT_DATE", tag="inc"))
# 3. 资产负债表
save("balance", fetch_all(dc_sec, "RPT_F10_FINANCE_GBALANCE", FS, "REPORT_DATE", tag="bal"))
# 4. 现金流量表
save("cashflow", fetch_all(dc_sec, "RPT_F10_FINANCE_GCASHFLOW", FS, "REPORT_DATE", tag="cf"))
# 5. 估值历史
save("valuation", fetch_all(dc_web, "RPT_VALUEANALYSIS_DET", F, "TRADE_DATE", tag="val"))
# 6. 分红
save("dividend", fetch_all(dc_web, "RPT_SHAREBONUS_DET", F, "EX_DIVIDEND_DATE", tag="div"))
print("ALL DONE")
