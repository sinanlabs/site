# -*- coding: utf-8 -*-
"""sinanlab.com 母站 v5：司南实验室总入口。数据驱动首页（读 Compute 的 data_v2.json / media.json 与 Robo 的 seed），
与 Compute 同一套视觉（亮色卡片 + 近地轨道地球）。无框架，python3 build.py 生成到 public/。"""
import io, os, json, shutil, html as H, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "public"); os.makedirs(OUT, exist_ok=True)
COMPASS = os.path.join(os.path.dirname(HERE), "compass", "site")
ROBO = os.path.join(os.path.dirname(HERE), "sinan-robo", "data", "seed_v0.json")
BASE = "https://sinanlab.com"; C = "https://compute.sinanlab.com"; R = "https://robo.sinanlab.com"

D = json.load(io.open(os.path.join(COMPASS, "data_v2.json"), encoding="utf-8"))
MEDIA = json.load(io.open(os.path.join(COMPASS, "media.json"), encoding="utf-8")) if os.path.exists(os.path.join(COMPASS, "media.json")) else {"video": [], "image": []}
ROBOD = json.load(io.open(ROBO, encoding="utf-8")) if os.path.exists(ROBO) else {"models": [], "embodiments": []}
GEN = D["generated_at"][:10]
esc = lambda s: H.escape("" if s is None else str(s), quote=True)
def fmt(x): return "—" if x is None else (("%.3f" % x) if x < 1 else ("%.2f" % x))
def pct(r): return "—" if r is None else (("%.1f%%" % (r * 100)) if r < .1 else ("%.0f%%" % (r * 100)))

# 资源：字体、地球脚本与贴图与 Compute 同源复制
shutil.copytree(os.path.join(HERE, "fonts"), os.path.join(OUT, "fonts"), dirs_exist_ok=True)
for d_ in ("img",):
    src = os.path.join(COMPASS, d_)
    if os.path.exists(src): shutil.copytree(src, os.path.join(OUT, d_), dirs_exist_ok=True)
os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
if os.path.exists(os.path.join(HERE, "static")):   # 站长平台验证文件等原样放根目录
    for f in os.listdir(os.path.join(HERE, "static")): shutil.copy(os.path.join(HERE, "static", f), os.path.join(OUT, f))
if os.path.exists(os.path.join(COMPASS, "dist", "assets", "earth.js")): shutil.copy(os.path.join(COMPASS, "dist", "assets", "earth.js"), os.path.join(OUT, "assets", "earth.js"))

CSS = r"""
@font-face{font-family:"Sora";font-style:normal;font-weight:400 700;font-display:swap;src:url(/fonts/Sora-latin.woff2) format("woff2")}
@font-face{font-family:"JetBrains Mono";font-style:normal;font-weight:400 600;font-display:swap;src:url(/fonts/JetBrainsMono-latin.woff2) format("woff2")}
:root{--ground:#F2F3F9;--ground-2:#E9EAF3;--card:#fff;--hair:#E6E7F0;--hair-2:#D5D7E6;--ink:#0F1222;--ink-2:#5A6079;--ink-3:#9AA0B8;--p:#6E56F5;--p-deep:#4B36D6;--p-soft:#EEEBFF;--p-ink:#3A2AA8;--robo:#F79009;--robo-soft:#FFF3E0;--good:#17B26A;--good-soft:#E6F7EF;--warn:#F79009;--warn-soft:#FFF3E0;--crit:#F04438;--crit-soft:#FDECEC;
--shadow-1:0 1px 2px rgba(20,22,50,.04),0 8px 24px -12px rgba(20,22,50,.12);--shadow-2:0 2px 6px rgba(20,22,50,.06),0 24px 48px -20px rgba(55,40,160,.22);--ease:cubic-bezier(.22,1,.36,1);--spring:cubic-bezier(.34,1.4,.64,1);
--sans:"Sora","Noto Sans SC","PingFang SC","Microsoft YaHei",system-ui,sans-serif;--mono:"JetBrains Mono",ui-monospace,Menlo,monospace}
*{box-sizing:border-box}html,body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--sans);font-size:15px;line-height:1.65;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}button{font:inherit;color:inherit}.mono{font-family:var(--mono);font-variant-numeric:tabular-nums}
.wrap{max-width:1180px;margin:0 auto;padding:0 28px}
header.top{position:sticky;top:0;z-index:20;background:rgba(242,243,249,.82);backdrop-filter:blur(12px);border-bottom:1px solid var(--hair)}
.bar{display:flex;align-items:center;gap:22px;height:64px}
.brand{display:flex;align-items:center;gap:11px}.brand .mark{width:34px;height:34px;border-radius:11px;background:linear-gradient(145deg,#8B77FF,#4B36D6);box-shadow:0 8px 18px -8px rgba(75,54,214,.7),inset 0 1px 0 rgba(255,255,255,.35);position:relative;flex:none}
.brand .mark:after{content:"";position:absolute;inset:9px 12px;border-radius:2px 2px 8px 8px;background:linear-gradient(#fff,#E9E6FF);transform:rotate(-28deg);box-shadow:0 2px 4px rgba(0,0,0,.25)}
.brand b{font-size:17px;font-weight:700;letter-spacing:-.01em;display:block;line-height:1.1}.brand small{display:block;font-size:10.5px;color:var(--ink-3);letter-spacing:.06em;margin-top:2px;white-space:nowrap}
nav.main{display:flex;gap:4px;margin-left:12px}nav.main a{padding:8px 12px;border-radius:10px;color:var(--ink-2);font-weight:500;font-size:14px;white-space:nowrap}nav.main a:hover{background:var(--card);color:var(--ink)}nav.main a.on{color:var(--ink);background:var(--card);box-shadow:var(--shadow-1)}
.right{margin-left:auto;display:flex;gap:8px;align-items:center}
.pl{display:inline-flex;align-items:center;gap:8px;padding:6px 12px;border-radius:999px;border:1px solid var(--hair-2);background:var(--card);font-size:13px;font-weight:600;white-space:nowrap}.right .lang,.right .auth{white-space:nowrap}.brand{flex:none}.pl .d{width:8px;height:8px;border-radius:50%}
.pl.c .d{background:var(--p)}.pl.r .d{background:var(--robo)}
.auth img{width:28px;height:28px;border-radius:50%;border:1px solid var(--hair)}
main{padding:22px 0 80px}
.card{background:var(--card);border:1px solid var(--hair);border-radius:18px;box-shadow:var(--shadow-1)}.pad{padding:22px 24px}
h1,h2,h3{margin:0;letter-spacing:-.01em}h2.sec{font-size:22px;font-weight:700}.lead{color:var(--ink-2);font-size:14px;margin:6px 0 0;max-width:760px}
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--p)}
/* hero */
.hero{min-height:560px;border-radius:26px;overflow:hidden;position:relative;background:radial-gradient(600px 300px at 12% 0%,rgba(110,86,245,.28),transparent 60%),#040611;color:#fff;box-shadow:0 2px 6px rgba(20,22,50,.1),0 30px 60px -24px rgba(10,10,40,.7);isolation:isolate}
.hero canvas{position:absolute;inset:0;width:100%;height:100%;display:block}.hero .stars{pointer-events:none}.hero #gl{cursor:grab;z-index:1}
.hero .scrim{position:absolute;inset:0;background:linear-gradient(100deg,rgba(4,6,17,.78) 0%,rgba(4,6,17,.4) 45%,rgba(4,6,17,0) 70%);pointer-events:none}
.hero .txt{position:relative;z-index:2;max-width:680px;padding:56px 52px 52px}
.hero h1{margin:14px 0 0;font-size:52px;line-height:1.08;letter-spacing:-.025em;font-weight:700;text-wrap:balance}
.hero p{margin:16px 0 0;font-size:16px;line-height:1.75;max-width:520px;color:rgba(255,255,255,.84)}
.search{margin-top:26px;display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.96);border-radius:16px;padding:0 8px 0 16px;height:56px;max-width:560px;box-shadow:0 20px 40px -20px rgba(0,0,0,.6)}
.search input{flex:1;border:0;outline:0;background:transparent;font:inherit;font-size:15px;color:var(--ink);min-width:0}
.search button{height:42px;padding:0 16px;border:0;border-radius:11px;background:var(--p);color:#fff;font-weight:600;cursor:pointer}
.search .ex{display:none}
.hero .hint{margin-top:10px;font-size:12.5px;color:rgba(255,255,255,.6)}.hero .hint a{color:#fff;text-decoration:underline;text-decoration-color:rgba(255,255,255,.35)}
.hero .stat{position:absolute;right:26px;top:22px;z-index:2;display:flex;gap:10px}
.hero .stat div{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.18);backdrop-filter:blur(10px);border-radius:14px;padding:10px 14px;text-align:right}
.hero .stat b{display:block;font-family:var(--mono);font-size:20px;font-weight:600;line-height:1}.hero .stat small{font-size:11px;opacity:.8}
.hero .tag{position:absolute;right:26px;bottom:16px;z-index:2;font-family:var(--mono);font-size:10px;letter-spacing:.1em;opacity:.5;text-align:right;line-height:1.6}
/* board */
.board{margin-top:18px;overflow:hidden}
.bh{display:flex;align-items:flex-end;gap:14px;padding:22px 24px 8px;flex-wrap:wrap}.bh .r{margin-left:auto;font-family:var(--mono);font-size:11.5px;color:var(--ink-3)}
.tablewrap{overflow-x:auto}table{width:100%;border-collapse:collapse}
th{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);text-align:left;font-weight:500;padding:12px 16px;border-bottom:1px solid var(--hair);white-space:nowrap}
th:first-child,td:first-child{padding-left:24px}td{padding:13px 16px;border-bottom:1px solid var(--hair);vertical-align:middle}tr:last-child td{border-bottom:0}tbody tr:hover{background:#FAFAFE}
td.num,th.num{text-align:right;font-family:var(--mono);font-variant-numeric:tabular-nums;white-space:nowrap}
.name{font-weight:600}.sub{font-size:11.5px;color:var(--ink-3);margin-top:2px}.big{font-size:16px;font-weight:600}
.dom{font-family:var(--mono);font-size:13px;font-weight:500}
.pill{display:inline-flex;align-items:center;gap:6px;font-size:11.5px;font-weight:500;padding:4px 10px;border-radius:999px;white-space:nowrap}.pill:before{content:"";width:6px;height:6px;border-radius:50%;background:currentColor}
.pill.explainable,.pill.normal{background:var(--good-soft);color:#067647}.pill.below_bulk{background:var(--warn-soft);color:#B54708}.pill.premium{background:var(--p-soft);color:var(--p-ink)}.pill.new{background:var(--p-soft);color:var(--p-ink)}
.r{font-family:var(--mono);font-size:13px;font-weight:600}.r.explainable,.r.normal{color:#067647}
.tfoot{display:flex;flex-wrap:wrap;gap:8px 22px;padding:14px 24px;border-top:1px solid var(--hair);font-size:12px;color:var(--ink-3)}
/* kpis */
.kpis{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-top:18px}
.kpi{padding:18px 20px 16px;display:block;transition:transform .45s var(--spring),box-shadow .45s var(--ease)}.kpi:hover{transform:translateY(-3px);box-shadow:var(--shadow-2)}
.kpi .k{font-size:12px;color:var(--ink-2);font-weight:500}.kpi .v{font-family:var(--mono);font-size:30px;font-weight:600;letter-spacing:-.02em;margin-top:10px;line-height:1}.kpi .v small{font-size:12px;color:var(--ink-3);font-weight:500;margin-left:4px}.kpi .n{font-size:12px;color:var(--ink-3);margin-top:8px}
/* products */
.prods{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:18px}
.prod{padding:26px 28px;position:relative;overflow:hidden;display:block;transition:transform .5s var(--spring),box-shadow .5s var(--ease)}.prod:hover{transform:translateY(-3px);box-shadow:var(--shadow-2)}
.prod .orb{position:absolute;right:-40px;top:-40px;width:170px;height:170px;border-radius:50%}
.prod.c .orb{background:radial-gradient(circle at 32% 30%,#C9BEFF,#6E56F5 55%,#2E1E9C);box-shadow:inset -18px -22px 36px rgba(30,10,110,.4)}
.prod.r .orb{background:radial-gradient(circle at 32% 30%,#FFD9A0,#F79009 55%,#A45A00);box-shadow:inset -18px -22px 36px rgba(110,50,0,.35)}
.prod .k{font-family:var(--mono);font-size:11px;letter-spacing:.18em;text-transform:uppercase}.prod.c .k{color:var(--p)}.prod.r .k{color:#B54708}
.prod h3{font-size:26px;margin-top:8px;max-width:78%}.prod p{color:var(--ink-2);font-size:14px;margin:10px 0 0;max-width:80%}
.prod ul{margin:14px 0 0;padding:0;list-style:none;display:grid;gap:6px;font-size:13.5px}.prod li b{font-family:var(--mono);font-weight:600}
.prod .go{margin-top:18px;display:inline-flex;align-items:center;gap:8px;font-weight:600;color:var(--p-ink)}.prod.r .go{color:#B54708}
/* grid */
.grid2{display:grid;grid-template-columns:1.3fr 1fr;gap:16px;margin-top:18px}
.feed .row{display:grid;grid-template-columns:52px 1fr;gap:12px;padding:12px 0;border-bottom:1px solid var(--hair);font-size:13px}.feed .row:last-child{border-bottom:0}.feed .t{font-family:var(--mono);font-size:11px;color:var(--ink-3);padding-top:2px}
.old{color:var(--ink-3);text-decoration:line-through;font-family:var(--mono)}.new{color:var(--good);font-family:var(--mono);font-weight:600}
.why{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:14px}.why .it{padding:16px 18px;border:1px solid var(--hair);border-radius:14px;background:#FBFBFE}.why .it b{display:block;font-size:14px}.why .it span{font-size:13px;color:var(--ink-2)}
.btn{display:inline-flex;align-items:center;gap:8px;height:42px;padding:0 18px;border-radius:12px;border:0;cursor:pointer;font-weight:600;font-size:13.5px;transition:transform .35s var(--spring)}.btn:hover{transform:translateY(-2px)}
.btn.p{background:var(--p);color:#fff;box-shadow:0 10px 22px -12px rgba(75,54,214,.9)}.btn.o{background:var(--card);color:var(--ink);border:1px solid var(--hair-2)}.btn.w{background:#fff;color:var(--p-deep)}.btn.g{background:rgba(255,255,255,.08);color:#fff;border:1px solid rgba(255,255,255,.3)}
.law{counter-reset:c;list-style:none;padding:0;margin:14px 0 0;display:grid;grid-template-columns:repeat(2,1fr);gap:12px}.law li{display:grid;grid-template-columns:40px 1fr;gap:12px;padding:16px 18px;border:1px solid var(--hair);border-radius:14px;background:#FBFBFE}.law li:before{counter-increment:c;content:counter(c,decimal-leading-zero);font-family:var(--mono);color:var(--p);font-size:12px;padding-top:3px}.law b{display:block;font-size:14.5px;margin-bottom:3px}.law span{color:var(--ink-2);font-size:13px;grid-column:2}
.prose{max-width:780px;font-size:15px;line-height:1.85}.prose h1{font-size:30px;margin:0 0 8px}.prose h2{font-size:20px;margin:28px 0 8px}.prose h3{font-size:16px;margin:20px 0 6px}.prose p{margin:8px 0;color:var(--ink-2)}.prose ul{padding-left:20px;color:var(--ink-2)}.prose a{color:var(--p-ink);text-decoration:underline;text-decoration-color:var(--hair-2)}
.notice{border:1px solid #F5C87A;background:var(--warn-soft);border-radius:12px;padding:12px 16px;color:#7A4B00;font-size:13.5px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:14px}.box{padding:18px 20px;border:1px solid var(--hair);border-radius:14px;background:#FBFBFE}.box h3{font-size:15px;margin-bottom:8px}.box ul{margin:0;padding-left:18px;color:var(--ink-2);font-size:13.5px}.box.ok{border-color:#9ADBB9}.box.no{border-color:#F5A9A3}
footer.ft{border-top:1px solid var(--hair);margin-top:60px}footer.ft .in{display:flex;flex-wrap:wrap;gap:16px 20px;padding:22px 0;font-size:12.5px;color:var(--ink-3)}footer.ft a{color:var(--ink-3)}footer.ft a:hover{color:var(--ink)}
.rise{animation:rise .8s var(--ease) both;animation-delay:calc(var(--i,0)*70ms)}@keyframes rise{from{opacity:0;transform:translateY(18px) scale(.985)}}
@media (prefers-reduced-motion:reduce){*,*:before,*:after{animation-duration:.01ms!important;transition-duration:.01ms!important}}
@media (max-width:1360px){.brand small{display:none}.bar{gap:14px}}
@media (max-width:1180px){.pl span{display:none}nav.main a{padding:8px 9px}}
@media (max-width:1100px){.kpis{grid-template-columns:repeat(3,1fr)}.why{grid-template-columns:1fr}.law{grid-template-columns:1fr}}
@media (max-width:860px){nav.main{display:none}.hero{min-height:620px}.hero .txt{padding:28px 24px 30px;max-width:none}.hero h1{font-size:34px}.hero .scrim{background:linear-gradient(180deg,rgba(4,6,17,.8) 0%,rgba(4,6,17,.35) 55%,transparent 80%)}.hero .stat,.hero .tag{display:none}.prods,.grid2,.two{grid-template-columns:1fr}.kpis{grid-template-columns:1fr 1fr}.prod h3,.prod p{max-width:none}.pl span{display:none}}
"""

NAV = [("/", "首页", "index.html"), ("/constitution", "为什么可信", "constitution.html"), ("/about", "关于", "about.html"), ("/subscribe", "订阅", "subscribe.html")]
def page(fn, title, desc, body, active="", og="/img/og.png", jsonld=None, scripts=""):
    nav = "".join('<a href="%s"%s>%s</a>' % (h, ' class="on"' if f == active else "", t) for h, t, f in NAV)
    path = "" if fn == "index.html" else fn.replace(".html", "")
    ld = "".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False).replace("</", "<\\/") for x in (jsonld or []))
    html = u"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>%s</title><meta name="description" content="%s"><link rel="canonical" href="%s/%s"><meta property="og:site_name" content="Sinan Lab"><meta property="og:type" content="website"><meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:url" content="%s/%s"><meta property="og:image" content="%s%s"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="%s%s"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><meta name="theme-color" content="#040611"><link rel="alternate" type="application/rss+xml" title="Sinan Compute 价格变动" href="%s/feed.xml">%s<style>%s</style></head><body>
<header class="top"><div class="wrap bar"><a class="brand" href="/"><span class="mark"></span><div><b>Sinan Lab</b><small>司南实验室 · AI 基础设施的中立测量者</small></div></a><nav class="main">%s</nav><div class="right"><a class="pl c" href="%s"><span class="d"></span><span>Sinan Compute</span></a><a class="pl r" href="%s"><span class="d"></span><span>Sinan Robo</span></a><span class="auth" id="auth"></span></div></div></header>
<main><div class="wrap">%s</div></main>
<footer class="ft"><div class="wrap in"><span>© 2026 Sinan Lab · 司南实验室</span><a href="/constitution">为什么可信</a><a href="/disclosure">收入透明</a><a href="/privacy">隐私政策</a><a href="/disclaimer">免责声明</a><a href="%s/method">方法论与数据</a><a href="%s/feed.xml">RSS</a><a href="mailto:hello@sinanlab.com">hello@sinanlab.com</a><span style="margin-left:auto">每个数字可追溯来源 · 不收任何被测渠道的钱</span></div></footer>
<script>(function(){var b=document.getElementById("auth");if(!b)return;fetch("%s/api/me",{credentials:"include"}).then(function(r){return r.json();}).then(function(m){if(m&&m.user){b.innerHTML='<a href="%s/me" title="我的关注">'+(m.user.avatar_url?'<img src="'+m.user.avatar_url+'" alt="">':'我的')+'</a>';}else if(m&&m.login){b.innerHTML='<a class="pl" href="%s/api/auth/github/start?return_to='+encodeURIComponent(location.href)+'">GitHub 登录</a>';}}).catch(function(){});})();</script>%s</body></html>""" % (
        esc(title), esc(desc), BASE, path, esc(title), esc(desc), BASE, path, C if og.startswith("/img") else BASE, og, C if og.startswith("/img") else BASE, og, C, ld, CSS, nav, C, R, body, C, C, C, C, C, scripts)
    io.open(os.path.join(OUT, fn), "w", encoding="utf-8").write(html)

# ---------------- 首页 ----------------
st = D["stats"]; CL = st["clusters"]
# 行情板：最新两代里有报价最多的 8 个模型
board_models = sorted([m for m in D["models"] if m["is_latest"]], key=lambda m: -m["n_relay"])[:8]
def best_row(m):
    ok = [r for r in m["rows"] if not r["held"] and r["band"] in ("explainable", "normal")]
    return min(ok, key=lambda r: r["out"]) if ok else None
board = ""
for m in board_models:
    b = best_row(m); f = m["floor"]
    un = sum(1 for r in m["rows"] if not r["held"] and r["band"] == "unsustainable")
    board += '<tr><td><a class="name" href="%s/m/%s">%s</a><div class="sub">%s · %d 家在卖</div></td><td class="num"><span class="big">$%s</span><span class="sub">%s</span></td>%s<td class="num">%d</td><td class="num"><a class="btn o" style="height:32px;padding:0 12px;font-size:12px" href="%s/m/%s">全部 %d 家 →</a></td></tr>' % (
        C, esc(m["id"]), esc(m["name"]), esc(D["vendor_name"].get(m["vendor"], m["vendor"])), m["n_relay"], fmt(f["out"]), esc(f["vendor"]),
        ('<td class="num"><span class="big">$%s</span><span class="sub"><a class="dom" href="%s/s/%s">%s</a></span></td><td><span class="r %s">%s</span> <span class="pill %s">%s</span></td>' % (fmt(b["out"]), C, esc(b["vendor"]), esc(b["vendor"]), b["band"], pct(b["ratio"]), b["band"], "价格说得通" if b["band"] == "explainable" else "与公开价接近")) if b else '<td class="num">—</td><td><span class="sub">没有落在说得通区间的报价</span></td>',
        un, C, esc(m["id"]), m["n_relay"])
changes = D.get("changes", [])[:6]
feed = "".join('<div class="row"><div class="t">%s</div><div><a class="dom" href="%s/s/%s">%s</a> · <a href="%s/m/%s">%s</a> <span class="old">%s</span> → <span class="new">%s</span> %s<div class="sub">%s · $/百万输出</div></div></div>' % (
    c["t"][5:16].replace("T", " "), C, esc(c["vendor"]), esc(c["vendor"]), C, esc(c["model"]), esc(c["model"]), fmt(c["old"]), fmt(c["new"]), "↑" if c["new"] > c["old"] else "↓", "中转站名义价" if c["kind"] == "relay" else "公开参考价") for c in changes) or '<div class="row"><div class="t">今日</div><div class="sub">没有价格变动。变更需连续两次抓取一致才发布。</div></div>'
fam_ref = sum(1 for mod in ("video", "image") for f in MEDIA.get(mod, []) if f.get("ref"))
robo_models = ROBOD.get("models", []); robo_nc = sum(1 for m in robo_models if m.get("commercial_ok") is False); robo_ok = sum(1 for m in robo_models if m.get("commercial_ok") is True)
kpis = [("已确认中转站", st["confirmed"], "", "面板指纹确认 · 每小时探测可达", C + "/sites"), ("实付报价", format(st["quotes"], ","), "", "每天抓一次 · 每条带快照", C + "/"),
        ("实付低于成本下限的站", CL["ultra"], " / %d" % (CL["ultra"] + CL["cheap"] + CL["near"] + CL["high"]), "算术分档 · 不推测成因", C + "/sites#c=ultra"),
        ("图像 / 视频族有官方参考", fam_ref, " / %d" % sum(len(MEDIA.get(k, [])) for k in ("video", "image")), "Seedance · Veo · 可灵 · Vidu · 万相…", C + "/media"),
        ("开源具身模型", len(robo_models), " · %d 本体" % len(ROBOD.get("embodiments", [])), "%d 可商用 · %d 禁商用 · 其余待核实" % (robo_ok, robo_nc), R + "/models")]
kpi_html = "".join('<a class="card kpi rise" style="--i:%s" href="%s"><div class="k">%s</div><div class="v">%s%s</div><div class="n">%s</div></a>' % (2 + i * .4, u, k, v, ('<small>%s</small>' % s) if s else "", n) for i, (k, v, s, n, u) in enumerate(kpis))
home = u"""
<section class="hero rise" style="--i:1"><canvas class="stars" id="stars"></canvas><canvas id="gl"></canvas><div class="scrim"></div>
<div class="txt"><div class="eyebrow">司南实验室 · AI 基础设施的中立测量者</div><h1>看清算力，<br>才好买算力。</h1>
<p>我们把 %d 个模型 API 中转站的实付价，对着官方与公开市场价逐条算成比率；再把开源具身模型的许可证、权重、能上哪些机器人做成可审计的索引。每个数字都能点开看来源。不收任何被测渠道的钱，也不替你判断。</p>
<form class="search" action="%s/sites" method="get" onsubmit="var v=this.q.value.trim();if(!v)return false;location.href='%s/sites#q='+encodeURIComponent(v);return false;"><input name="q" placeholder="查一个中转站（如 toapis.cn）或一个模型（如 DeepSeek V4）"><button type="submit">查</button></form>
<div class="hint">或直接看：<a href="%s/m/deepseek-v4-pro">DeepSeek V4 Pro 在 %d 家中转站的实付</a> · <a href="%s/media/seedance">Seedance 按秒价</a> · <a href="%s/models">开源 VLA 索引</a></div></div>
<div class="stat"><div><b>%s</b><small>条实付报价</small></div><div><b>%d</b><small>个中转站</small></div><div><b>%d</b><small>个具身模型</small></div></div>
<div class="tag">地球影像 NASA BLUE MARBLE · BLACK MARBLE<br>实时大气散射 · 拖动转动地球</div></section>

<div class="kpis">%s</div>

<section class="card board rise" style="--i:4"><div class="bh"><div><h2 class="sec">今天的行情板</h2><p class="lead">最新两代里在卖最多的 %d 个模型：参考价、说得通的最低实付是谁给的、多少家低于成本下限。点模型名看全部中转站。</p></div><span class="r">数据 %s · USD/CNY %.2f</span></div>
<div class="tablewrap"><table><thead><tr><th>模型</th><th class="num">参考价 $/百万输出</th><th class="num">说得通的最低实付</th><th>是参考价的几成</th><th class="num">低于成本下限</th><th class="num"></th></tr></thead><tbody>%s</tbody></table></div>
<div class="tfoot"><span>参考价 = 官方与公开市场最低；实付 = 面板名义价 × 充值比例 ÷ 汇率；"说得通" = 落在常见批量折扣区间。此为算术比值，不构成对任何渠道的指控。</span></div></section>

<div class="prods">
<a class="card prod c rise" style="--i:5" href="%s"><span class="orb"></span><div class="k">Sinan Compute · 司南·算力</div><h3>模型 API 中转站实付比价</h3><p>%d 个站、%s 条报价、%d 个图像视频族。每个站一页事实清单：充值比例、登录方式、24 小时可达率、它卖的每个模型是参考价的几成。</p><ul><li><b>%d</b> 家实付低于成本下限，我们标出来但不推测成因</li><li><b>%d</b> 家计价方式待核，只列名义价不出比率</li><li>每天凌晨自动重抓、重算、重发</li></ul><span class="go">进入 compute.sinanlab.com →</span></a>
<a class="card prod r rise" style="--i:5.5" href="%s"><span class="orb"></span><div class="k">Sinan Robo · 司南·机脑</div><h3>开源具身模型的可审计索引</h3><p>%d 个开源 / 开放权重 VLA、%d 个机器人本体。许可证、权重、代码、参数量每个字段带来源；没核实的写"待核实"，不猜。</p><ul><li><b>%d</b> 个模型许可证明确允许商用，<b>%d</b> 个明确禁止</li><li>模型 × 本体适配矩阵，只给有证据的格子上色</li><li>延迟与每千次推理成本层已就位，等实测填入</li></ul><span class="go">进入 robo.sinanlab.com →</span></a>
</div>

<div class="grid2">
<section class="card pad rise" style="--i:6"><h2 class="sec">登录以后多了什么</h2><p class="lead">所有数据不登录也全看得到。登录只解锁属于你自己的东西，不设密码，GitHub 一键。</p>
<div class="why"><div class="it"><b>关注一个站或模型</b><span>价格变、可达率掉、检测结果变，第一时间提醒你（邮件与飞书 / 钉钉接入中）。</span></div><div class="it"><b>看全部价格历史</b><span>匿名看最近 7 天，登录看从收录第一天起的每一次变价。</span></div><div class="it"><b>提交纠错并署名</b><span>发现数据不对，提交来源链接，审核通过后记入修正日志并署你的名。</span></div></div>
<div style="margin-top:16px;display:flex;gap:10px;flex-wrap:wrap"><a class="btn p" href="%s/api/auth/github/start?return_to=%s/">用 GitHub 登录 →</a><a class="btn o" href="%s/method">先看看我们怎么算的</a></div></section>
<section class="card pad feed rise" style="--i:7"><h2 class="sec">今日价格变动</h2><div style="margin-top:6px">%s</div><div style="margin-top:12px;display:flex;gap:14px;font-size:13px"><a href="%s/weekly" style="color:var(--p-ink)">每周价格周报 →</a><a href="%s/feed.xml" style="color:var(--p-ink)">RSS 订阅</a></div></section>
</div>

<section class="card pad rise" style="margin-top:18px;--i:8"><h2 class="sec">凭什么信我们</h2><ol class="law">
<li><b>不收任何被测渠道的钱</b><span>不做付费认证、不接被测者的广告与赞助。检测页零商业链接。</span></li>
<li><b>排名与判读永不含商业变量</b><span>有返佣与无返佣的渠道同等收录、同等展示；算法里没有佣金这个字段。</span></li>
<li><b>每个数字带证据</b><span>来源 URL、抓取时间、原始快照哈希，永不覆盖。算错了公开更正，原记录保留。</span></li>
<li><b>只说算术，不说人</b><span>"在无补贴假设下数学上不可持续"是算术；指控性词汇在发布管线里被拦下，不靠自觉。</span></li>
</ol><p style="margin-top:12px;font-size:13px;color:var(--ink-3)">全文见 <a href="/constitution" style="color:var(--p-ink)">为什么可信</a> · 原始数据在 <a href="%s/method#data" style="color:var(--p-ink)">这里下载</a></p></section>
""" % (st["confirmed"], C, C, C, next((m["n_relay"] for m in D["models"] if m["id"] == "deepseek-v4-pro"), 0), C, R, format(st["quotes"], ","), st["confirmed"], len(robo_models), kpi_html, len(board_models), GEN, D["fx"]["rate"], board,
       C, st["confirmed"], format(st["quotes"], ","), sum(len(MEDIA.get(k, [])) for k in ("video", "image")), CL["ultra"], CL["held"], R, len(robo_models), len(ROBOD.get("embodiments", [])), robo_ok, robo_nc,
       C, BASE, C, feed, C, C, C)
ld_home = [{"@context": "https://schema.org", "@type": "Organization", "name": "Sinan Lab", "alternateName": "司南实验室", "url": BASE, "logo": BASE + "/favicon.svg", "email": "hello@sinanlab.com", "sameAs": ["https://github.com/sinanlabs"]},
           {"@context": "https://schema.org", "@type": "WebSite", "name": "Sinan Lab", "url": BASE + "/", "inLanguage": "zh-CN", "potentialAction": {"@type": "SearchAction", "target": {"@type": "EntryPoint", "urlTemplate": C + "/sites#q={search_term_string}"}, "query-input": "required name=search_term_string"}}]
page("index.html", "Sinan Lab · 司南实验室 —— 看清算力，才好买算力", "司南实验室：%d 个模型 API 中转站的实付比价与可达性测量，%d 个开源具身模型的可审计索引。每个数字带来源，不收任何被测渠道的钱，不推荐。" % (st["confirmed"], len(robo_models)), home, "index.html", jsonld=ld_home, scripts='<script src="/assets/earth.js?v=%s" defer></script>' % GEN.replace("-", ""))

# ---------------- 其他页 ----------------
page("constitution.html", "为什么可信 · Sinan Lab", "司南实验室对用户的五条承诺：不收被测方一分钱、排名不含商业变量、每个数字可追溯出处、只讲算术不讲情绪、方法与收入公开。", u"""
<div class="rise" style="--i:0;margin-bottom:14px"><div class="eyebrow">为什么可信 · 我们对你的五条承诺</div><h1 style="font-size:30px;margin-top:8px">不收被测方一分钱，每个数字都能查到出处</h1><p class="lead">这五条不是口号，是写进代码的运行规则：排序函数里没有佣金字段，发布管线有禁用词闸门，命中就发不出去。你看到的每一个价格、每一条结论，都可以自己点开验证。</p></div>
<section class="card pad rise" style="--i:1"><ol class="law">
<li><b>排名里永远没有商业变量</b><span>有没有和我们合作，对一个渠道的排序和展示毫无影响。任何带推广的位置都会显著标注"广告"，符合《互联网广告管理办法》。</span></li>
<li><b>不做付费认证</b><span>任何委托测试只收执行费，结果不会被冠以"独立认证"。你看到的"一致"或"不一致"，买不来。</span></li>
<li><b>不收被测方的钱</b><span>广告、赞助、返佣，一律不进入测量页面。目前全站零返佣、零广告、零赞助。</span></li>
<li><b>收入来源按季公开</b><span>每季度公布收入构成；修正日志和方法论版本永久公开，改过什么一目了然。</span></li>
<li><b>先有证据，再有结论</b><span>页面上任何数字都能追回一条原始抓取快照，追不回的不显示。这在数据库层面是硬约束，不是自觉。</span></li>
</ol></section>
<section class="card pad rise" style="margin-top:16px;--i:2"><h2 class="sec">我们怎么说话</h2><div class="two" style="margin-top:12px">
<div class="box ok"><h3>我们会这样写</h3><ul><li>"该端点输出分布与参考端点统计不一致（置信度 92%，n=1,240，2026-08 窗口）"</li><li>"该渠道对该模型的实付价为最低公开渠道价的 7.5%，在无补贴假设下数学上不可持续"</li><li>"本次测量未能复现上月结论，原因待查"</li></ul></div>
<div class="box no"><h3>我们不会这样写</h3><ul><li>"实锤""假模型""套壳""诈骗""降智"</li><li>任何不带样本量与时间窗的质量结论</li><li>任何形式的"推荐榜"。我们给事实清单，判断权交回给你</li></ul></div></div>
<p class="lead" style="margin-top:12px">所有质量类结论必须带样本量、时间窗、置信度，缺一个发布管线直接拦下。点名发布前给渠道方 72 小时预通知与申诉窗口；同一结论要在两个独立时间窗复现才发。</p></section>""", "constitution.html")

page("about.html", "关于 · Sinan Lab", "司南实验室是一个一人加 AI 的小团队，做 AI 基础设施的中立测量：算力与模型渠道（Sinan Compute）、具身智能模型（Sinan Robo）。", u"""
<div class="rise" style="--i:0;margin-bottom:14px"><div class="eyebrow">关于</div><h1 style="font-size:30px;margin-top:8px">一个中立的测量者，不是导航站</h1></div>
<section class="card pad prose rise" style="--i:1"><p>司南是中国最早的指向仪器。我们借这个名字做一件事：在算力与模型这个信息极不对称的市场里，给买方一把可以自己校验的尺。</p>
<h3>我们做什么</h3><p>持续采集官方定价、公开市场价与各渠道的实付价，用统一口径比对；对渠道做可用性与一致性测量；对具身智能的开源模型做可审计的索引。全部结论带证据链，全部方法公开。</p>
<h3>我们不做什么</h3><p>不卖算力，不做中转，不做付费认证，不推荐。不收任何被测渠道的钱。</p>
<h3>怎么运作</h3><p>一人 + AI 的小团队，采集、计算、生成、部署全流程每天自动跑。数据与代码本身即是资产。目前完全免费、不注册也看全部。</p>
<h3>联系</h3><p>渠道方对数据有异议，请通过 <a href="mailto:hello@sinanlab.com">hello@sinanlab.com</a> 提交核对请求，我们按公开的修正流程处理并保留原记录。</p></section>""", "about.html")

page("subscribe.html", "订阅 · Sinan Lab", "订阅司南实验室：价格变动提醒、每周价格周报、机脑行情。RSS 现在可用，邮件接入中。", u"""
<div class="rise" style="--i:0;margin-bottom:14px"><div class="eyebrow">订阅</div><h1 style="font-size:30px;margin-top:8px">价格变了、新站出现了、测量异常了，我们告诉你</h1></div>
<div class="two"><section class="card pad rise" style="--i:1"><h2 class="sec">现在就能用</h2><p class="lead">RSS 每天更新价格变动与新收录；每周一自动生成周报页。</p><div style="margin-top:14px;display:flex;gap:10px;flex-wrap:wrap"><a class="btn p" href="%s/feed.xml">RSS 订阅</a><a class="btn o" href="%s/weekly">价格周报</a></div>
<p class="lead" style="margin-top:14px">想按站、按模型收提醒：登录后在站点页或模型页点"关注"。</p><a class="btn o" style="margin-top:10px" href="%s/api/auth/github/start?return_to=%s/subscribe">用 GitHub 登录 →</a></section>
<section class="card pad rise" style="--i:2"><h2 class="sec">邮件周报</h2><p class="lead" style="margin-top:6px">每周一一封：本周价格变动、新收录的站、每个模型说得通的最低实付。只陈述测量，不含推荐；每封都能一键退订。</p><form id="subf" style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap"><input type="email" id="sube" required placeholder="你的邮箱" autocomplete="email" style="flex:1;min-width:220px;padding:10px 12px;border:1px solid var(--hair);border-radius:10px;font:inherit;font-size:14px"><button class="btn p" type="submit">订阅周报</button></form><div id="subm" class="notice" style="margin-top:12px;display:none"></div><p class="lead" style="margin-top:12px;font-size:13px">想按站、按模型收提醒：用 GitHub 登录 Sinan Compute，在站点页或模型页点"关注"，再到"我的"页面开启邮件提醒。</p></section>
<script>(function(){var f=document.getElementById("subf"),m=document.getElementById("subm");function say(t){m.style.display="block";m.textContent=t;}var st=new URLSearchParams(location.search).get("s");var MS={confirmed:"订阅已确认，下周一见。",unsubscribed:"已退订，不会再发。",expired:"确认链接已过期，请重新提交邮箱。",invalid:"链接无效。"};if(st&&MS[st])say(MS[st]);f.addEventListener("submit",function(e){e.preventDefault();var em=document.getElementById("sube").value.trim();say("发送中…");fetch("https://compute.sinanlab.com/api/subscribe",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email:em,lang:document.documentElement.lang==="en"?"en":"zh"})}).then(function(r){return r.json();}).then(function(x){var R={sent:"确认邮件已发出，去邮箱点一下链接就生效。",already:"这个邮箱已经在订阅列表里。",bad_email:"邮箱格式不对。",mail_not_ready:"邮件服务暂未开放。",send_failed:"发送失败，稍后再试。"};say(R[x.state]||R[x.error]||"发送失败，稍后再试。");}).catch(function(){say("网络错误，稍后再试。");});});})();</script></div>""" % (C, C, C, BASE), "subscribe.html")

for fn, title, body in [
    ("disclosure.html", "收入透明 · Sinan Lab", u'<div class="rise" style="--i:0;margin-bottom:14px"><div class="eyebrow">收入透明</div><h1 style="font-size:30px;margin-top:8px">目前：零返佣、零广告、零赞助</h1></div><section class="card pad prose rise" style="--i:1"><p>截至本页最后更新，本站所有页面不含任何返佣链接、广告位或赞助内容，未从任何被测渠道或第三方获得收入。所有"前往站点"链接不带推广参数，只计点击数。</p><h3>若将来接入</h3><p>只会来自上游官方平台，绝不来自任何被测量的中转渠道；含返佣的位置显著标明"广告"并使用 rel=sponsored；排序与判读永不读取返佣字段；每季度在本页公开收入来源占比。返佣总开关在后台，默认关闭，每次开关都记入审计日志。</p><p style="color:var(--ink-3);font-size:13px">最后更新：2026-09-04</p></section>'),
    ("privacy.html", "隐私政策 · Sinan Lab", u'<div class="rise" style="--i:0;margin-bottom:14px"><div class="eyebrow">隐私政策</div><h1 style="font-size:30px;margin-top:8px">我们几乎不收集什么</h1></div><section class="card pad prose rise" style="--i:1"><p>所有数据不登录也全部可见；不使用 Cookie 追踪；统计使用无 Cookie 的 Cloudflare Web Analytics。</p><h3>账号（可选）</h3><p>登录只解锁关注、提醒、纠错提交等个人化功能。我们不设密码、不存密码。用 GitHub 登录时，我们保存你的 GitHub 用户编号、用户名、头像地址，以及 GitHub 提供的邮箱（用于将来发提醒；查找时只用邮箱的哈希值）。登录状态存在一个名为 sinan_sid 的 Cookie 里，作用域为 sinanlab.com 及其子域，30 天有效，仅服务器可读。</p><h3>你在站内留下的东西</h3><p>关注列表、提醒设置、你提交的纠错。这些只对你自己和站点维护者可见。想删除账号及全部数据，发邮件到 hello@sinanlab.com，我们在 7 天内处理。</p><h3>邮箱</h3><p>仅用于你订阅或开启的提醒，单独存放、不与浏览数据关联，随时一键退订。</p><h3>出站跳转</h3><p>点击"前往站点"经本站中转，仅按天按站累计点击次数，不记录 IP、浏览器标识或来源页。</p><h3>你的 Key</h3><p>任何"用我的 Key 核实"的功能都在你的浏览器本地运行，Key 不上传、不落库、不经过我们的服务器。</p><h3>统计</h3><p>后台只看无个人信息的计数：每日登录数、注册数、关注数、出站点击数。</p><p style="color:var(--ink-3);font-size:13px">最后更新：2026-09-03 · 联系 hello@sinanlab.com</p></section>'),
    ("disclaimer.html", "免责声明 · Sinan Lab", u'<div class="rise" style="--i:0;margin-bottom:14px"><div class="eyebrow">免责声明</div><h1 style="font-size:30px;margin-top:8px">我们给事实，不给推荐</h1></div><section class="card pad prose rise" style="--i:1"><p>本站所有比率、判读均为基于公开信息的算术结果，不构成对任何渠道的指控，也不构成购买建议；不排除存在本站未收录的更低公开来源。</p><h3>数据时效</h3><p>每条数据均标注抓取时间与快照；渠道价格可能随时变化，以渠道方实时展示为准。</p><h3>第三方渠道</h3><p>本站不运营、不担保任何第三方服务。中转渠道存在日志留存、能力裁剪、限流、关站、余额失效及上游合规等风险，请自行评估。</p><h3>更正</h3><p>数据错误请联系 hello@sinanlab.com；我们公开更正并保留原记录。</p><p style="color:var(--ink-3);font-size:13px">最后更新：2026-09-02</p></section>'),
]:
    page(fn, title, "司南实验室 · " + title.split(" ·")[0] + "：不收被测渠道的钱、每个数字带来源、只给事实不给推荐。", body, "")
page("404.html", "没有这个页面 · Sinan Lab", "页面不存在", u'<section class="card pad rise" style="max-width:640px"><div class="eyebrow">404</div><h1 style="font-size:28px;margin-top:8px">没有这个页面。</h1><p class="lead">地址可能拼错了，或者这一页已经搬走。</p><div style="margin-top:16px;display:flex;gap:10px;flex-wrap:wrap"><a class="btn p" href="/">回首页</a><a class="btn o" href="%s">去 Sinan Compute</a><a class="btn o" href="%s">去 Sinan Robo</a></div></section>' % (C, R), "")

io.open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % BASE)
io.open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join('  <url><loc>%s/%s</loc><lastmod>%s</lastmod></url>\n' % (BASE, "" if f == "index.html" else f.replace(".html", ""), GEN) for f in ["index.html", "constitution.html", "about.html", "subscribe.html", "disclosure.html", "privacy.html", "disclaimer.html"]) + "</urlset>\n")
io.open(os.path.join(OUT, "favicon.svg"), "w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="10" fill="#4B36D6"/><circle cx="20" cy="20" r="14" fill="none" stroke="#B9ADFF" stroke-width="1.5" opacity=".6"/><path d="M20 9 L24.5 20 L20 31 Z" fill="#fff"/><path d="M20 9 L15.5 20 L20 31 Z" fill="#B9ADFF"/><circle cx="20" cy="20" r="2.2" fill="#4B36D6" stroke="#fff" stroke-width="1.4"/></svg>')
io.open(os.path.join(OUT, "_redirects"), "w").write("https://www.sinanlab.com/* https://sinanlab.com/:splat 301\n")
io.open(os.path.join(OUT, "_headers"), "w").write("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n/fonts/*\n  Cache-Control: public, max-age=31536000, immutable\n/img/*\n  Cache-Control: public, max-age=2592000\n")
print("母站 v5 生成：", sorted(x for x in os.listdir(OUT) if x.endswith(".html")))
