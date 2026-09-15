#!/usr/bin/env python3
"""ETF / 指数 数据工具 — 零外部依赖（仅 stdlib）。

为 /etf-checklist 提供指数估值、ETF 规模与费率等数据。

数据源与覆盖：
    指数行情     腾讯行情 qt.gtimg.cn        全市场
    指数估值     蛋卷(雪球) danjuanfunds.com  PE/PB/历史分位/ROE/股息率/股债利差
    ETF 列表     东方财富 push2             全市场 1300+ 只（规模/价格/涨跌）
    ETF 明细     集思录                     ⚠️ 仅覆盖部分 ETF，命中时给费率/折溢价/IOPV

用法：
    python3 tools/etf_data.py index 000300        # 指数行情 + 估值分位
    python3 tools/etf_data.py etf 510300          # ETF 规模 +（命中时）费率/折溢价
    python3 tools/etf_data.py list --top 30       # 按规模列出最大 ETF
    python3 tools/etf_data.py search 沪深300       # 按名称/指数搜索 ETF

已知限制（诚实声明）：
    - 集思录免费接口只返回少量 ETF（实测约 20 条子集），因此**费率与折溢价不保证取到**；
      取不到时请人工到基金公司官网 / 集思录 / 天天基金查询，不要猜测。
    - 蛋卷估值分位的口径由蛋卷定义，与其他平台（如理杏仁、中证指数官网）可能不同；
      跨平台引用必须注明口径，不得混用。
    - 东财对指数不返回 PE/PB（字段恒为 0），指数估值请走蛋卷。
"""

import argparse
import json
import ssl
import sys
import urllib.request

_TIMEOUT = 20
_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"


# ---------------------------------------------------------------------------
# 通用
# ---------------------------------------------------------------------------

def _fetch(url, referer=None, encoding="utf-8"):
    headers = {"User-Agent": _UA}
    if referer:
        headers["Referer"] = referer
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=_TIMEOUT) as r:
        raw = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            import gzip, io
            raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
    return raw.decode(encoding, errors="replace")


def _qq_prefix(code, is_index=False):
    """拼腾讯行情前缀。指数与个股/ETF 的规则不同（这是常见坑）。"""
    c = code.strip().lower()
    if c.startswith(("sh", "sz", "bj")):
        return c
    if is_index:
        # 指数：000xxx/999xxx 在上交所发布；399xxx 在深交所
        return ("sh" if c.startswith(("000", "999")) else "sz") + c
    # 个股/ETF：5/6/9 开头为沪市，0/1/2/3 为深市
    return ("sh" if c[0] in "569" else "sz") + c


def _qq_quote(code, is_index=False):
    txt = _fetch(f"https://qt.gtimg.cn/q={_qq_prefix(code, is_index)}", encoding="gbk")
    if '="' not in txt:
        return None
    body = txt.split('="', 1)[1].rstrip('";\n')
    fields = body.split("~")
    return fields if len(fields) > 5 else None


def _dj_code(code):
    """指数 -> 蛋卷代码：000300 -> SH000300，399006 -> SZ399006。"""
    c = code.strip().lower().replace("sh", "").replace("sz", "")
    return ("SH" if c.startswith(("000", "999")) else "SZ") + c


def _em_code(code):
    """ETF -> 东财 secid：510300 -> 1.510300（1=沪,0=深）。"""
    c = code.strip().lower().replace("sh", "").replace("sz", "")
    return ("1." if c[0] in "569" else "0.") + c


# ---------------------------------------------------------------------------
# 指数
# ---------------------------------------------------------------------------

def cmd_index(code):
    print("=" * 64)
    print(f"指数 {code}")
    print("=" * 64)

    q = _qq_quote(code, is_index=True)
    if q:
        print(f"  名称        : {q[1]}")
        print(f"  最新点位    : {q[3]}")
        try:
            print(f"  涨跌幅      : {q[32]}%")
        except IndexError:
            pass
    else:
        print("  ⚠️ 腾讯行情未取到（检查指数代码）")

    dj = _dj_code(code)
    try:
        d = json.loads(_fetch(f"https://danjuanfunds.com/djapi/index_eva/detail/{dj}")).get("data") or {}
    except Exception as e:
        print(f"\n  ⚠️ 估值取数失败：{e}")
        return
    if not d:
        print(f"\n  ⚠️ 蛋卷未收录该指数（{dj}）的估值")
        return

    def p2(v):
        try:
            return f"{float(v) * 100:.2f}%"
        except (TypeError, ValueError):
            return "—"

    print("\n  ── 估值（蛋卷口径，跨平台引用须注明）──")
    print(f"  PE(TTM)       : {d.get('pe')}")
    print(f"  PB            : {d.get('pb')}")
    print(f"  PE 历史分位   : {p2(d.get('pe_percentile'))}")
    print(f"  PB 历史分位   : {p2(d.get('pb_percentile'))}")
    print(f"  指数 ROE      : {p2(d.get('roe'))}")
    print(f"  股息率        : {p2(d.get('yeild'))}")
    print(f"  蛋卷评价      : {d.get('eva_type')}   (low=低估 / mid=适中 / high=高估)")
    # 注意：蛋卷返回的 bond_yeild 恒为 5.00%（占位值，非真实国债收益率），
    # 因此本工具**不计算股债利差**——请人工取当日 10 年期国债收益率后自行比对。
    print("\n  ⚠️ 股债利差未计算：蛋卷的 bond_yeild 字段恒为固定占位值，不可用。")
    print("     请自行查当日 10 年期国债收益率（中债登 / 中国货币网 / 东财债券频道）后比对。")


# ---------------------------------------------------------------------------
# ETF
# ---------------------------------------------------------------------------

_ETF_LIST = ("https://push2.eastmoney.com/api/qt/clist/get"
             "?pn=1&pz={pz}&po=1&np=1&fltt=2&invt=2&fid=f21"
             "&fs=b:MK0021,b:MK0022,b:MK0023,b:MK0024"
             "&fields=f12,f13,f14,f2,f3,f21")


def _em_etfs(pz=5000):
    """东财 ETF 全列表，按规模降序。"""
    txt = _fetch(_ETF_LIST.format(pz=pz), referer="https://quote.eastmoney.com/")
    diff = (json.loads(txt).get("data") or {}).get("diff") or {}
    rows = diff.values() if isinstance(diff, dict) else diff
    out = []
    for r in rows:
        try:
            out.append({
                "code": str(r.get("f12")),
                "name": r.get("f14") or "",
                "price": r.get("f2"),
                "chg": r.get("f3"),
                "scale": float(r.get("f21") or 0) / 1e8,  # 元 -> 亿元
            })
        except (TypeError, ValueError):
            continue
    return sorted(out, key=lambda x: -x["scale"])


_JISILU = "https://www.jisilu.cn/data/etf/etf_list/?___jsl=LST___t=1"


def _jisilu_lookup(code):
    """集思录 ETF 明细（仅覆盖其子集，取不到返回 None）。"""
    try:
        txt = _fetch(_JISILU, referer="https://www.jisilu.cn/data/etf/")
        rows = json.loads(txt).get("rows", [])
    except Exception:
        return None
    return next((r["cell"] for r in rows if str(r.get("cell", {}).get("fund_id")) == code), None)


def cmd_etf(code):
    code = code.strip().lower().replace("sh", "").replace("sz", "")
    print("=" * 64)
    print(f"ETF {code}")
    print("=" * 64)

    hit = next((e for e in _em_etfs() if e["code"] == code), None)
    if hit:
        print(f"  名称        : {hit['name']}")
        print(f"  最新价      : {hit['price']}   ({hit['chg']}%)")
        print(f"  最新规模    : {hit['scale']:.2f} 亿元")
        if hit["scale"] < 2:
            print("  ⚠️ 规模 <2 亿，存在清盘风险，需核查")
    else:
        print("  ⚠️ 东财未找到该 ETF（检查代码）")

    js = _jisilu_lookup(code)
    if js:
        f = lambda k: (js.get(k) if js.get(k) not in (None, "-", "") else "—")
        print("\n  ── 成本 ──")
        print(f"  总费率      : {f('fee')}%   (管理 {f('m_fee')}% + 托管 {f('t_fee')}%)")
        print(f"  基金公司    : {f('issuer_nm')}")
        print(f"  跟踪指数    : {f('index_nm')}")
        print("\n  ── 折溢价（ETF 特有）──")
        print(f"  净值(NAV)   : {f('fund_nav')}   ({f('nav_dt')})")
        print(f"  折溢价率    : {f('discount_rt')}%")
        print(f"  IOPV折溢价  : {f('iopv_discount_rt')}%")
        print(f"  成交量      : {f('volume')} 万手")
        print(f"  T+0         : {'是' if js.get('t0') == 'Y' else '否'}")
    else:
        print("\n  ⚠️ 费率/折溢价未取到（集思录免费接口仅覆盖部分 ETF）")
        print("     → 请人工核对：基金公司官网 / 集思录 / 天天基金；**不要猜测费率**")


def cmd_list(top=30):
    rows = _em_etfs()
    print(f"东财 ETF 列表：共 {len(rows)} 只（按规模降序，显示前 {top}）\n")
    print(f"{'代码':<9}{'名称':<28}{'规模(亿)':>10}{'价格':>9}")
    print("-" * 60)
    for r in rows[:top]:
        print(f"{r['code']:<9}{r['name'][:26]:<28}{r['scale']:>10.2f}{str(r['price']):>9}")


def cmd_search(kw):
    rows = _em_etfs()
    k = kw.lower()
    hits = [r for r in rows if k in r["name"].lower() or k in r["code"]]
    print(f"匹配 “{kw}” 的 ETF：{len(hits)} 只（按规模降序）\n")
    if not hits:
        print("  （未命中）")
        return
    print(f"{'代码':<9}{'名称':<28}{'规模(亿)':>10}{'价格':>9}")
    print("-" * 60)
    for r in hits[:40]:
        print(f"{r['code']:<9}{r['name'][:26]:<28}{r['scale']:>10.2f}{str(r['price']):>9}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description="ETF/指数数据工具")
    sub = p.add_subparsers(dest="cmd")

    a = sub.add_parser("index", help="指数行情 + 估值分位")
    a.add_argument("code", help="指数代码，如 000300 / 000688 / 399006")

    b = sub.add_parser("etf", help="ETF 规模 +（命中时）费率/折溢价")
    b.add_argument("code", help="ETF 代码，如 510300")

    l = sub.add_parser("list", help="按规模列出 ETF")
    l.add_argument("--top", type=int, default=30)

    c = sub.add_parser("search", help="按名称搜索 ETF")
    c.add_argument("keyword")

    args = p.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    if args.cmd == "index":
        cmd_index(args.code)
    elif args.cmd == "etf":
        cmd_etf(args.code)
    elif args.cmd == "list":
        cmd_list(args.top)
    elif args.cmd == "search":
        cmd_search(args.keyword)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
