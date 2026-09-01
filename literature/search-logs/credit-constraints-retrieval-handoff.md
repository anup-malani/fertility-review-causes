# Full-text retrieval handoff — C.3.e (TICK-077)

**2026-09-01 · Shravan.** Eight studies the automated ladder could not fetch. Split by cause,
because a blocked route is not a paywall and the two need different fixes.

- **browser-job** — the URL is OPEN. A 403 from bot defence killed the scripted fetch; opening
  the DOI in a normal browser session and saving the PDF is enough.
- **proxy-job** — no open copy exists at any rung. Needs Zotero + the UChicago proxy.

**Save into `temp/c3e-handoff/` using the `key` as the filename** (e.g. `desai-tarozzi-2011.pdf`).
Hand-retrieved PDFs arrive publisher-named, and a wrong pairing corrupts the extraction table
silently, so `284` re-checks each PDF's own text against the record's title before installing it.


## Priority 1 — these decide whether the composite stratum has an identified estimate

| Key | DOI | Job | Study | Why it matters |
|---|---|---|---|---|
| `desai-tarozzi-2011` | `10.1007/s13524-011-0029-0` | **browser** | Microcredit, Family Planning Programs, and Contraceptive Behavior: Evi (2011, Demography) | BOUNDARY-SPANNING candidate: financial-access exposure x fertility outcome |
| `steele-amin-naved-1998` | `10.31899/pgy6.1016` | **browser** | The impact of an integrated micro-credit programme on women's empowerm (1998, n/a) | BOUNDARY-SPANNING candidate: financial-access exposure x fertility outcome |
| `kuchler-2012` | `10.1353/jda.2012.0037` | **proxy** | Do Microfinance Programs Change Fertility?: Evidence Using Panel Data  (2012, The Journal of developing areas) | BOUNDARY-SPANNING candidate: financial-access exposure x fertility outcome |

## Priority 2 — the remaining probes

| Key | DOI | Job | Study | Why it matters |
|---|---|---|---|---|
| `attanasio-2015-mongolia` | `10.1257/app.20130489` | **browser** | The Impacts of Microfinance: Evidence from Joint-Liability Lending in  (2015, American Economic Journal Applied Economics) | composite/savings probe - does it estimate a fertility outcome? |
| `bruhn-2014-mexico` | `10.1111/jofi.12091` | **browser** | The Real Impact of Improved Access to Finance: Evidence from Mexico (2013, The Journal of Finance) | composite/savings probe - does it estimate a fertility outcome? |
| `guinnane-credit-cooperatives` | `10.1017/s0022050701028042` | **proxy** | COOPERATIVES AS INFORMATION MACHINES: GERMAN RURAL CREDIT COOPERATIVES (2001, The Journal of Economic History) | composite/savings probe - does it estimate a fertility outcome? |
| `lan-pan-yu-2023` | `10.1080/00036846.2023.2244249` | **proxy** | The role of digital financial inclusion in increasing fertility intent (2023, Applied Economics) | BOUNDARY-SPANNING candidate: financial-access exposure x fertility outcome |
| `prina-2015-banking-the-poor` | `10.1016/j.jdeveco.2015.01.004` | **proxy** | Banking the poor via savings accounts: Evidence from a field experimen (2015, Journal of Development Economics) | composite/savings probe - does it estimate a fertility outcome? |

## What each one is being read for

**Priority 1.** Desai and Tarozzi randomly allocated areas across credit and family-planning arms with
fertility among the outcomes: the question is whether a **credit arm is separately identified from the
family-planning arm**. If it is, that is a clean identified estimate of a composite financial-access
exposure on fertility, and it carries a stratum that otherwise has none. Steele and Küchler are the same
question with weaker designs (quasi-experimental panel; DiD with an instrument).

**Priority 2.** The four remaining probes are read for one binary: **does a fertility or birth variable
appear on the left-hand side of any estimate?** Their abstracts say no. Six of their siblings said no in
full text too. These four close the bound — until they are read, the finding is "6 of 10 checked, 0
positive", not "the cell is empty".

