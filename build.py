# -*- coding: utf-8 -*-
"""sinanlab.com 母站：五页静态 HTML。无框架，python3 build.py 生成到 public/。"""
import io, os
import shutil
OUT = "public"; os.makedirs(OUT, exist_ok=True)
shutil.copytree("fonts", os.path.join(OUT, "fonts"), dirs_exist_ok=True)
FONT_CSS = '@font-face{font-family:"Instrument Serif";font-style:normal;font-weight:400;font-display:swap;src:url(/fonts/InstrumentSerif-latin.woff2) format("woff2");unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}@font-face{font-family:"Instrument Serif";font-style:italic;font-weight:400;font-display:swap;src:url(/fonts/InstrumentSerif-italic-latin.woff2) format("woff2")}@font-face{font-family:"JetBrains Mono";font-style:normal;font-weight:400 600;font-display:swap;src:url(/fonts/JetBrainsMono-latin.woff2) format("woff2")}@font-face{font-family:"IBM Plex Sans";font-style:normal;font-weight:400 600;font-display:swap;src:url(/fonts/IBMPlexSans-latin.woff2) format("woff2")}'
CSS = """
:root{--ground:#0B0F14;--surface:#10161E;--hair:#1F2A36;--hair2:#2A3644;--ink:#E8EEF3;--ink2:#A3B1BE;--ink3:#64768A;--accent:#4FD1D9;--robo:#E0AE4A}
*{box-sizing:border-box}body{margin:0;background:var(--ground);color:var(--ink);font-family:"IBM Plex Sans","PingFang SC","Noto Sans SC",system-ui,sans-serif;font-size:15px;line-height:1.65;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}a:hover{color:#8AE3E8}h1,h2,h3{margin:0;font-weight:400}
.serif{font-family:"Instrument Serif","Noto Serif SC","Songti SC",Georgia,serif}.mono{font-family:"JetBrains Mono","IBM Plex Mono",ui-monospace,Menlo,monospace}
.wrap{max-width:1040px;margin:0 auto;padding:0 32px}
header{border-bottom:1px solid var(--hair)}.bar{display:flex;align-items:center;gap:26px;padding:22px 0}.bar nav{display:flex;gap:22px;font-size:14px;margin-left:auto}.bar nav a{color:var(--ink2)}.bar nav a.on{color:var(--ink);border-bottom:1px solid var(--accent);padding-bottom:2px}
.brand{display:flex;align-items:center;gap:12px;color:var(--ink)}.brand h1{font-family:"Instrument Serif","Noto Serif SC",serif;font-size:22px;line-height:1}.brand .sub{font-family:"JetBrains Mono",monospace;font-size:10px;letter-spacing:.22em;color:var(--ink3);text-transform:uppercase;margin-top:3px}
main{padding:56px 0 80px}.eyebrow{font-family:"JetBrains Mono",monospace;font-size:11px;letter-spacing:.22em;color:var(--accent);text-transform:uppercase}
h2.big{font-family:"Instrument Serif","Noto Serif SC",serif;font-size:52px;line-height:1.06;letter-spacing:-.01em;text-wrap:balance;margin:14px 0 0}h2.big em{color:var(--accent)}
p.lead{font-size:17px;color:var(--ink2);max-width:640px;margin:18px 0 0}
.cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:44px}
.card{background:var(--surface);border:1px solid var(--hair);border-radius:16px;padding:26px 28px;display:flex;flex-direction:column;gap:10px;color:var(--ink)}
.card .k{font-family:"JetBrains Mono",monospace;font-size:11px;letter-spacing:.2em;text-transform:uppercase}.card h3{font-family:"Instrument Serif","Noto Serif SC",serif;font-size:28px}.card p{margin:0;color:var(--ink2);font-size:14px}
.card .cta{margin-top:auto;display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:600}
.card.compute .k,.card.compute .cta{color:var(--accent)}.card.robo .k,.card.robo .cta{color:var(--robo)}
.card.soon{opacity:.85}.badge{display:inline-block;font-family:"JetBrains Mono",monospace;font-size:10.5px;padding:2px 8px;border-radius:999px;border:1px solid var(--hair2);color:var(--ink3);margin-left:8px;vertical-align:middle}
.sec{margin-top:56px}.sec h2{font-family:"Instrument Serif","Noto Serif SC",serif;font-size:30px;margin-bottom:14px}
ol.law{counter-reset:c;list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:14px}ol.law li{display:grid;grid-template-columns:44px minmax(0,1fr);gap:14px;padding:18px 20px;background:var(--surface);border:1px solid var(--hair);border-radius:12px}ol.law li::before{counter-increment:c;content:counter(c,decimal-leading-zero);font-family:"JetBrains Mono",monospace;color:var(--accent);font-size:13px;padding-top:3px}ol.law b{display:block;font-size:16px;margin-bottom:4px;font-weight:500}ol.law span{color:var(--ink2);font-size:14px}
.two{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.box{background:var(--surface);border:1px solid var(--hair);border-radius:12px;padding:18px 20px}.box h3{font-size:16px;margin-bottom:8px;font-weight:500}.box.ok{border-color:rgba(76,195,138,.4)}.box.no{border-color:rgba(228,97,76,.4)}.box ul{margin:0;padding-left:18px;color:var(--ink2);font-size:14px}
.prose{max-width:720px;color:var(--ink2)}.prose h3{color:var(--ink);font-size:18px;margin:26px 0 8px;font-weight:500}.prose p{margin:10px 0}
form.sub{display:flex;gap:10px;margin-top:18px;max-width:520px}form.sub input{flex:1;height:44px;border:1px solid var(--hair2);border-radius:9px;background:var(--surface);color:var(--ink);padding:0 14px;font:inherit}form.sub button{height:44px;border:0;border-radius:9px;background:var(--accent);color:#06181B;font:inherit;font-weight:600;padding:0 18px;cursor:pointer}
footer{border-top:1px solid var(--hair)}footer .wrap{display:flex;flex-wrap:wrap;gap:20px;padding:22px 32px;font-size:12.5px;color:var(--ink3)}footer a{color:var(--ink3)}
@media(max-width:800px){.cards,.two{grid-template-columns:1fr}h2.big{font-size:38px}.bar nav{display:none}}
"""
LOGO='<svg width="30" height="30" viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="17.5" fill="none" stroke="#2A3644" stroke-width="1.2"/><path d="M20 5v4M20 31v4M5 20h4M31 20h4" stroke="#64768A" stroke-width="1.2" stroke-linecap="round"/><path d="M20 9 L24.5 20 L20 31 Z" fill="#4FD1D9"/><path d="M20 9 L15.5 20 L20 31 Z" fill="#2A3644"/><circle cx="20" cy="20" r="2.2" fill="#0B0F14" stroke="#4FD1D9" stroke-width="1.4"/></svg>'
NAV=[("index.html","首页"),("constitution.html","中立宪法"),("about.html","关于"),("subscribe.html","订阅")]
def page(fn, title, desc, body, active):
    nav="".join('<a href="%s"%s>%s</a>' % (h, ' class="on"' if h==active else "", t) for h,t in NAV)
    html=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title><meta name="description" content="{desc}"><meta property="og:site_name" content="Sinan Lab"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><link rel="canonical" href="https://sinanlab.com/{'' if fn=='index.html' else fn}"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><meta name="theme-color" content="#0B0F14"><style>{FONT_CSS}</style><style>{CSS}</style></head><body>
<header><div class="wrap bar"><a class="brand" href="/">{LOGO}<div><h1>Sinan Lab</h1><div class="sub">司南实验室 · AI 基础设施的中立测量者</div></div></a><nav>{nav}<a href="https://compute.sinanlab.com">Sinan Compute</a><a href="https://robo.sinanlab.com">Sinan Robo</a></nav></div></header>
<main><div class="wrap">{body}</div></main>
<footer><div class="wrap"><span>© 2026 Sinan Lab · 司南实验室</span><a href="/constitution.html">中立宪法</a><a href="/disclosure.html">返佣披露</a><a href="/privacy.html">隐私政策</a><a href="/disclaimer.html">免责声明</a><a href="mailto:hello@sinanlab.com">hello@sinanlab.com</a><span style="margin-left:auto">每个数字可追溯来源 · 不收任何被测渠道的钱</span></div></footer></body></html>'''
    io.open(os.path.join(OUT,fn),"w",encoding="utf-8").write(html)

page("index.html","Sinan Lab · 司南实验室 —— AI 基础设施的中立测量者","司南实验室：对 GPU 租赁、模型 API 渠道与具身智能模型做中立测量。每个数字可追溯来源，不收任何被测渠道的钱。",f'''
<div class="eyebrow">Sinan Lab · 司南实验室</div>
<h2 class="big">看清算力，才好买算力。<br><em>AI 基础设施的中立测量者。</em></h2>
<p class="lead">我们不卖算力、不做中转、不收被测者的钱。我们只做一件事：把官方价、公开市场价和渠道实付价放在同一把尺上，把每个数字的来源、抓取时间和快照留下来，让你自己判断。</p>
<div class="cards">
  <a class="card compute" href="https://compute.sinanlab.com"><div class="k">Sinan Compute · 司南·算力</div><h3>GPU 与模型 API 的中立比价与质量测量</h3><p>306 个已确认渠道、1.3 万条实付报价、图像与视频按秒/按张比对。每一行一把"罗盘尺"：官方价在 100% 中线，渠道实付是尺上的指针。</p><span class="cta">进入 compute.sinanlab.com →</span></a>
  <a class="card robo soon" href="https://robo.sinanlab.com"><div class="k">Sinan Robo · 司南·机脑 <span class="badge">即将上线</span></div><h3>开源具身模型（VLA）的可审计索引</h3><p>模型 × 本体适配矩阵、硬件延迟与推理成本、方法论公开。首批 11 个模型、7 个本体已录入，未核实字段一律标"待核实"，不猜。</p><span class="cta">看首批预览 →</span></a>
</div>
<section class="sec"><h2>我们凭什么让你信</h2>
<ol class="law">
<li><b>排名与判读永不含商业变量</b><span>有返佣与无返佣的渠道同等收录、同等展示；算法里没有佣金这个字段。</span></li>
<li><b>不收任何被测渠道的钱</b><span>不做付费认证、不接被测者的广告与赞助。检测页零商业链接。</span></li>
<li><b>每个数字带证据</b><span>来源 URL、抓取时间、原始快照哈希，永不覆盖。算错了公开更正，原记录保留。</span></li>
<li><b>只说算术，不说人</b><span>"在无补贴假设下数学上不可持续"是算术；"假模型""诈骗"不是。指控性词汇在发布管线里被拦下，不靠自觉。</span></li>
<li><b>方法论与收入占比公开</b><span>方法版本永久公开；一旦有收入，每季度公开来源占比。</span></li>
</ol><p style="margin-top:14px;font-size:14px;color:var(--ink3)">全文见 <a href="/constitution.html">中立宪法</a>。</p></section>
''', "index.html")

page("constitution.html","中立宪法 · Sinan Lab","司南实验室的中立宪法与措辞宪法全文：不收被测者的钱、排名不含商业变量、每个数字带证据、只说算术不说人、方法与收入公开。",'''
<div class="eyebrow">中立宪法 · 不可协商</div><h2 class="big">五条写进网站、写进代码的<em>约束。</em></h2>
<p class="lead">这不是价值宣言，是产品的运行规则。其中第一、四条已经是代码：排序函数里没有佣金字段；发布管线里有一道禁用词闸门。</p>
<section class="sec"><ol class="law">
<li><b>排名与推荐算法永不含佣金变量</b><span>有返佣与无返佣渠道同等收录、同等展示。任何含返佣的位置按《互联网广告管理办法》显著标明"广告"。</span></li>
<li><b>不做付费认证</b><span>任何受托测试只收执行费，结果绝不冠以"独立认证"名义。</span></li>
<li><b>不接受被测量渠道的任何资金</b><span>广告、赞助、返佣，一律不得进入质量测量层页面。</span></li>
<li><b>每季度公开收入来源占比</b><span>修正日志与方法论版本永久公开。</span></li>
<li><b>证据先于结论</b><span>展示层任何数字都必须能追回一条原始快照；追不回的不予显示——这条在数据库层是断言，不是约定。</span></li>
</ol></section>
<section class="sec"><h2>措辞宪法</h2><div class="two">
<div class="box ok"><h3>可以这么写</h3><ul><li>"该端点输出分布与参考端点统计不一致（置信度 92%，n=1,240，2026-08 窗口）"</li><li>"该渠道对该模型的实付价为最低公开渠道价的 7.5%，在无补贴假设下数学上不可持续"</li><li>"本次测量未能复现上月结论，原因待查"</li></ul></div>
<div class="box no"><h3>永不这么写</h3><ul><li>"实锤""假模型""套壳""诈骗""降智"</li><li>任何不带样本量与时间窗的质量结论</li><li>任何形式的"推荐榜"——我们给事实清单，判断权交回给你</li></ul></div></div>
<p style="margin-top:14px;font-size:14px;color:var(--ink3)">所有质量类结论必须同时带样本量、时间窗、置信度三个字段，缺一个发布管线直接拦下。具名发布前有 72 小时预通知与申诉窗口；同一结论须在两个独立时间窗复现；对照端点误报率 &lt;5% 的指标才启用。</p></section>
''', "constitution.html")

page("about.html","关于 · Sinan Lab","司南实验室是一个一人加 AI 的小团队，做 AI 基础设施的中立测量：算力与模型渠道（Sinan Compute）、具身智能模型（Sinan Robo）。",'''
<div class="eyebrow">关于</div><h2 class="big">一个中立的<em>测量者</em>，不是导航站。</h2>
<div class="prose"><p class="lead">司南是中国最早的指向仪器。我们借这个名字做一件事：在算力与模型这个信息极不对称的市场里，给买方一把可以自己校验的尺。</p>
<h3>我们做什么</h3><p>持续采集官方定价、公开市场价与各渠道的实付价，用统一口径比对；对渠道做可用性与一致性测量；对具身智能的开源模型做可审计的索引。全部结论带证据链，全部方法公开。</p>
<h3>我们不做什么</h3><p>不卖算力，不做中转，不做付费认证，不推荐。不收任何被测渠道的钱。</p>
<h3>怎么运作</h3><p>一人 + AI 的小团队，全流程 Runbook 化。数据与代码本身即是资产。目前完全免费、免注册。</p>
<h3>联系</h3><p>渠道方对数据有异议，请通过 <a href="mailto:hello@sinanlab.com">hello@sinanlab.com</a> 提交核对请求，我们按公开的修正流程处理并保留原记录。</p></div>
''', "about.html")

page("subscribe.html","订阅 · Sinan Lab","订阅司南实验室：算力价格周报与机脑行情。邮箱或 RSS，不强制注册，随时一键退订。",'''
<div class="eyebrow">订阅</div><h2 class="big">价格变了、新站出现了、测量异常了——<em>我们告诉你。</em></h2>
<p class="lead">每周一封。邮箱单独存放、不与任何数据关联、随时一键退订。</p>
<form class="sub" action="https://buttondown.com/api/emails/embed-subscribe/sinanlab" method="post" target="_blank"><input type="email" name="email" placeholder="you@company.com" required aria-label="邮箱"><button type="submit">订阅周报</button></form>
<p style="margin-top:10px;font-size:13px;color:var(--ink3)">订阅服务接入中：表单地址上线前会替换为正式地址。也可以用 RSS：<span class="mono">https://compute.sinanlab.com/feed.xml</span>（即将开通）。</p>
<section class="sec"><h2>两栏内容</h2><div class="two"><div class="box"><h3>算力价格周报 · Sinan Compute</h3><ul><li>本周官方与公开市场价变动</li><li>新收录渠道与消失的渠道</li><li>实付价异常与一致性测量摘要</li></ul></div><div class="box"><h3>机脑行情 · Sinan Robo</h3><ul><li>开源 VLA 模型新发布与许可证变化</li><li>模型 × 本体适配矩阵更新</li><li>硬件延迟与推理成本实测</li></ul></div></div></section>
''', "subscribe.html")

for fn,title,body in [
 ("disclosure.html","返佣披露 · Sinan Lab",'<div class="eyebrow">返佣披露</div><h2 class="big">目前：<em>零返佣、零广告、零赞助。</em></h2><div class="prose"><p class="lead">截至本页最后更新，本站所有页面不含任何返佣链接、广告位或赞助内容，未从任何被测渠道或第三方获得收入。</p><h3>若将来接入</h3><p>只会来自上游官方平台，绝不来自任何被测量的中转渠道；含返佣的位置显著标明"广告"；排序与判读永不读取返佣字段；每季度在本页公开收入来源占比。</p><p style="color:var(--ink3);font-size:13px">最后更新：2026-09-02</p></div>'),
 ("privacy.html","隐私政策 · Sinan Lab",'<div class="eyebrow">隐私政策</div><h2 class="big">我们几乎<em>不收集</em>什么。</h2><div class="prose"><p class="lead">不强制注册；不使用 Cookie 追踪；统计使用无 Cookie 的 Cloudflare Web Analytics。</p><h3>邮箱</h3><p>仅用于发送你订阅的周报，单独存放、不与任何浏览数据关联，随时一键退订即删除。</p><h3>出站跳转</h3><p>点击"前往站点"经本站中转，仅累计按站点击数，不记录 IP、浏览器标识或来源页。</p><h3>你的 Key</h3><p>任何"用我的 Key 核实"的功能都在你的浏览器本地运行，Key 不上传、不落库、不经过我们的服务器。</p><p style="color:var(--ink3);font-size:13px">最后更新：2026-09-02 · 联系 hello@sinanlab.com</p></div>'),
 ("disclaimer.html","免责声明 · Sinan Lab",'<div class="eyebrow">免责声明</div><h2 class="big">我们给事实，<em>不给推荐。</em></h2><div class="prose"><p class="lead">本站所有比率、判读均为基于公开信息的算术结果，不构成对任何渠道的指控，也不构成购买建议；不排除存在本站未收录的更低公开来源。</p><h3>数据时效</h3><p>每条数据均标注抓取时间与快照；渠道价格可能随时变化，以渠道方实时展示为准。</p><h3>第三方渠道</h3><p>本站不运营、不担保任何第三方服务。中转渠道存在日志留存、能力裁剪、限流、关站、余额失效及上游合规等风险，请自行评估。</p><h3>更正</h3><p>数据错误请联系 hello@sinanlab.com；我们公开更正并保留原记录。</p><p style="color:var(--ink3);font-size:13px">最后更新：2026-09-02</p></div>'),
]:
    page(fn,title,"司南实验室 · "+title.split(" ·")[0],body,"")
io.open(os.path.join(OUT,"robots.txt"),"w").write("User-agent: *\nAllow: /\nSitemap: https://sinanlab.com/sitemap.xml\n")
io.open(os.path.join(OUT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join("  <url><loc>https://sinanlab.com/%s</loc></url>\n" % ("" if f=="index.html" else f) for f in ["index.html","constitution.html","about.html","subscribe.html","disclosure.html","privacy.html","disclaimer.html"])+"</urlset>\n")
io.open(os.path.join(OUT,"favicon.svg"),"w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="8" fill="#0B0F14"/><circle cx="20" cy="20" r="14" fill="none" stroke="#2A3644" stroke-width="1.5"/><path d="M20 9 L24.5 20 L20 31 Z" fill="#4FD1D9"/><path d="M20 9 L15.5 20 L20 31 Z" fill="#2A3644"/><circle cx="20" cy="20" r="2.2" fill="#0B0F14" stroke="#4FD1D9" stroke-width="1.4"/></svg>')
io.open(os.path.join(OUT,"_redirects"),"w").write("https://www.sinanlab.com/* https://sinanlab.com/:splat 301\n")
print("母站生成：", sorted(os.listdir(OUT)))
