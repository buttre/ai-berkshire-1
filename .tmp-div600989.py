import json, time, random, requests, sys

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
URL = "https://datacenter-web.eastmoney.com/api/data/v1/get"
S = requests.Session()
S.headers.update({"User-Agent": UA})

def em_get(url, params, timeout=15):
    time.sleep(1.0 + random.uniform(0.1, 0.4))
    return S.get(url, params=params, timeout=timeout)

# RPT_SHAREBONUS_DET full columns
params = {
    "reportName": "RPT_SHAREBONUS_DET",
    "columns": "ALL",
    "filter": '(SECURITY_CODE="600989")',
    "pageNumber": "1",
    "pageSize": "60",
    "sortColumns": "EX_DIVIDEND_DATE,NOTICE_DATE",
    "sortTypes": "-1,-1",
    "source": "WEB",
    "client": "WEB",
}
r = em_get(URL, params)
d = r.json()
res = d.get("result") or {}
data = res.get("data") or []
print("TOTAL ROWS:", len(data))
if data:
    print("KEYS:", list(data[0].keys()))
    for row in data:
        print("=" * 100)
        for k, v in row.items():
            if v is not None and v != "" and v != 0:
                print(f"  {k}: {v}")
