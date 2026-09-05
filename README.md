# Sinan Lab · 司南实验室 — sinanlab.com

Landing site for **Sinan Lab**, neutral measurement for AI infrastructure.
司南实验室母站：产品入口、今日行情板、五条承诺、订阅。

- 🧮 [Sinan Compute](https://compute.sinanlab.com) — effective-price comparison and reachability measurement for model API relay sites ([repo](https://github.com/sinanlabs/compute))
- 🤖 [Sinan Robo](https://robo.sinanlab.com) — auditable index of open embodied (VLA) models ([repo](https://github.com/sinanlabs/robo))
- 📜 [Why trust us](https://sinanlab.com/constitution) · [Revenue transparency](https://sinanlab.com/disclosure) · [Privacy](https://sinanlab.com/privacy)

## Build

```bash
python3 build.py                                  # reads ../compass/site/data_v2.json + ../sinan-robo/data/seed_v0.json → public/
python3 ../compass/site/i18n_apply.py public https://sinanlab.com   # /en/ mirror
```

Static HTML, no framework. Deployed on Cloudflare Pages; `functions/` holds the search-engine verification handlers.

## Contact

hello@sinanlab.com · corrections are logged publicly and originals kept.
