#!/usr/bin/env python3
"""
51_build_ra_gate.py — assemble the interactive RA-gate review sheet.

Joins the LLM screen verdicts (screen-tiers.json) with paper abstracts/metadata
(temp/screen/batch_*.json) and the estimand-ready pooling set
(estimand-ready-set.json) into a single self-contained HTML page that the RA
works through in the browser. Two review streams:

  1. POOLING SET (61) — precision spot-check. The automated estimand gate ran
     more permissive than the pilot (37% PRIMARY vs 23%), so the RA confirms or
     demotes each paper's "identifies the primary cell (OAS-motive -> fertility,
     forward, fertility-outcome)" call.
  2. UNCERTAINS (88) — the screen's UNCERTAIN verdicts, resolved by the RA to
     RELEVANT / NOT_RELEVANT (corpus membership; upstream of cell routing).

Output: output/old-age-security-pension-crowdout-ra-gate.html (open in browser).
Decisions persist to the browser's localStorage and export to JSON/CSV, which
step 52 folds back into the pipeline. No abstracts are re-fetched; this step is
LLM/OpenAlex-free and deterministic.
"""
import json, glob, html, os, urllib.parse

SLUG = "old-age-security-pension-crowdout"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # repo root (source/build/goldset/ -> repo)
def rp(*a): return os.path.join(ROOT, *a)

tiers = json.load(open(rp("output", f"{SLUG}-screen-tiers.json")))
pool  = json.load(open(rp("output", f"{SLUG}-estimand-ready-set.json")))
pool_ids = {r["paperId"] for r in pool}

# abstract / metadata index from the screen input batches
absidx = {}
for f in glob.glob(rp("temp", "screen", "batch_*.json")):
    for r in json.load(open(f)):
        absidx[r["paperId"]] = r

def scholar(title):
    return "https://scholar.google.com/scholar?q=" + urllib.parse.quote(title or "")

def record(r, group):
    meta = absidx.get(r["paperId"], {})
    return {
        "id": r["paperId"],
        "group": group,
        "title": r.get("title") or meta.get("title") or "(untitled)",
        "year": meta.get("year"),
        "venue": meta.get("venue"),
        "authors": meta.get("authors"),
        "abstract": meta.get("abstract"),
        "is_gold": bool(r.get("is_gold")),
        "tier": r.get("tier"),
        "evidence_type": r.get("evidence_type"),
        "cell": r.get("cell"),
        "outcome": r.get("outcome"),
        "mechanism": r.get("mechanism"),
        "direction": r.get("direction"),
        "reason": r.get("reason"),
        "snow_reason": meta.get("snow_reason"),
        "scholar": scholar(r.get("title") or meta.get("title")),
    }

pooling  = [record(r, "pooling") for r in pool]
uncertain = [record(r, "uncertain")
             for r in tiers if r["verdict"] == "UNCERTAIN"]

# sort: gold first within pooling (the anchors), then by title; uncertain by title
pooling.sort(key=lambda x: (not x["is_gold"], x["title"].lower()))
uncertain.sort(key=lambda x: x["title"].lower())

DATA = {"slug": SLUG, "pooling": pooling, "uncertain": uncertain}
data_json = json.dumps(DATA, ensure_ascii=False)

TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RA gate — old-age-security / pension-crowdout</title>
<style>
:root{
  --bg:#f7f7f5; --card:#fff; --ink:#1a1a1a; --muted:#6b6b6b; --line:#e3e3e0;
  --accent:#2d6a4f; --accent2:#1d3557; --warn:#9a3412; --gold:#8a6d1f; --goldbg:#fbf3d5;
  --ok:#166534; --okbg:#dcfce7; --no:#991b1b; --nobg:#fee2e2; --skip:#475569; --skipbg:#e2e8f0;
  --shadow:0 1px 3px rgba(0,0,0,.08),0 6px 20px rgba(0,0,0,.05);
}
@media (prefers-color-scheme:dark){
  :root{--bg:#16171a;--card:#212327;--ink:#e9e9e7;--muted:#9a9a97;--line:#33353a;
    --accent:#4ade80;--accent2:#7aa2e0;--gold:#d8b84a;--goldbg:#2e2915;
    --ok:#4ade80;--okbg:#0f2e1a;--no:#f87171;--nobg:#2e1414;--skip:#94a3b8;--skipbg:#1e242c;
    --shadow:0 1px 3px rgba(0,0,0,.4),0 6px 24px rgba(0,0,0,.3);}
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
header{position:sticky;top:0;z-index:10;background:var(--bg);border-bottom:1px solid var(--line);
  padding:12px 20px 8px;}
h1{font-size:15px;margin:0 0 8px;font-weight:600;letter-spacing:.01em}
h1 span{color:var(--muted);font-weight:400}
.tabs{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.tab{border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:999px;
  padding:5px 14px;font-size:13px;cursor:pointer;font-weight:500}
.tab.active{background:var(--accent2);color:#fff;border-color:var(--accent2)}
.tab .n{opacity:.7;font-weight:400}
.spacer{flex:1}
.btn{border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:8px;
  padding:5px 11px;font-size:12.5px;cursor:pointer}
.btn:hover{border-color:var(--muted)}
.progress{height:4px;background:var(--line);border-radius:3px;margin-top:9px;overflow:hidden}
.progress i{display:block;height:100%;background:var(--accent);width:0;transition:width .2s}
.counts{font-size:12px;color:var(--muted);margin-top:6px;display:flex;gap:14px;flex-wrap:wrap}
.counts b{color:var(--ink);font-weight:600}
main{max-width:860px;margin:20px auto 120px;padding:0 20px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow);
  padding:22px 24px;}
.cardhead{display:flex;align-items:baseline;gap:10px;margin-bottom:2px}
.pos{font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums;white-space:nowrap}
.gold{background:var(--goldbg);color:var(--gold);border:1px solid var(--gold);border-radius:5px;
  font-size:10.5px;padding:1px 6px;font-weight:700;letter-spacing:.04em;text-transform:uppercase}
.decided{font-size:11px;padding:1px 8px;border-radius:5px;font-weight:600}
.ttl{font-size:19px;line-height:1.35;font-weight:650;margin:6px 0 4px}
.ttl a{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--line)}
.ttl a:hover{border-color:var(--accent)}
.meta{font-size:12.5px;color:var(--muted);margin-bottom:14px}
.gatebox{background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin-bottom:14px}
.gatebox .lab{font-size:10.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);
  font-weight:700;margin-bottom:7px}
.axes{display:grid;grid-template-columns:auto 1fr;gap:3px 12px;font-size:13.5px}
.axes dt{color:var(--muted);font-weight:600}
.axes dd{margin:0}
.gatereason{margin-top:8px;font-size:13px;font-style:italic;color:var(--ink);opacity:.85}
.cellpill{display:inline-block;font-size:10.5px;font-weight:700;padding:1px 7px;border-radius:5px;
  margin-left:6px;vertical-align:middle}
.cell-PRIMARY{background:var(--okbg);color:var(--ok)}
.cell-OFF{background:var(--nobg);color:var(--no)}
.cell-THEORY,.cell-null{background:var(--skipbg);color:var(--skip)}
.abstract{font-size:14.5px;line-height:1.6;max-height:340px;overflow:auto;
  padding-right:6px;white-space:pre-wrap}
.noabs{color:var(--muted);font-style:italic}
.decisionbar{position:fixed;bottom:0;left:0;right:0;background:var(--card);border-top:1px solid var(--line);
  box-shadow:0 -2px 12px rgba(0,0,0,.06);padding:12px 20px}
.dbinner{max-width:860px;margin:0 auto;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.dbtn{border:1.5px solid var(--line);background:var(--card);color:var(--ink);border-radius:9px;
  padding:9px 16px;font-size:14px;font-weight:600;cursor:pointer;display:flex;align-items:center;gap:8px}
.dbtn kbd{font:11px ui-monospace,monospace;background:var(--bg);border:1px solid var(--line);
  border-radius:4px;padding:1px 5px;color:var(--muted)}
.dbtn.ok{border-color:var(--ok);color:var(--ok)} .dbtn.ok:hover{background:var(--okbg)}
.dbtn.no{border-color:var(--no);color:var(--no)} .dbtn.no:hover{background:var(--nobg)}
.dbtn.skip{border-color:var(--skip);color:var(--skip)} .dbtn.skip:hover{background:var(--skipbg)}
.dbtn.sel{color:#fff}
.dbtn.ok.sel{background:var(--ok);border-color:var(--ok)}
.dbtn.no.sel{background:var(--no);border-color:var(--no)}
.dbtn.skip.sel{background:var(--skip);border-color:var(--skip)}
.nav{margin-left:auto;display:flex;gap:8px;align-items:center}
.extra{max-width:860px;margin:10px auto 0;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
select,input[type=text]{font:13px inherit;padding:6px 8px;border:1px solid var(--line);
  border-radius:7px;background:var(--card);color:var(--ink)}
input[type=text]{flex:1;min-width:180px}
.hint{font-size:11.5px;color:var(--muted)}
.hide{display:none!important}
/* summary */
#summary table{width:100%;border-collapse:collapse;font-size:13px}
#summary th,#summary td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line);vertical-align:top}
#summary th{color:var(--muted);font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:.04em}
#summary tr{cursor:pointer}
#summary tr:hover td{background:var(--bg)}
.tag{font-size:11px;padding:1px 7px;border-radius:5px;font-weight:600;white-space:nowrap}
.dot{width:8px;height:8px;border-radius:50%;display:inline-block;margin-right:6px}
</style>
</head>
<body>
<header>
  <h1>RA gate <span>· old-age-security / pension-crowdout · verdicts you make here feed step 52</span></h1>
  <div class="tabs">
    <button class="tab active" data-mode="pooling">Pooling set — spot-check <span class="n">(<span id="pc">0</span>)</span></button>
    <button class="tab" data-mode="uncertain">UNCERTAINs — relevance <span class="n">(<span id="uc">0</span>)</span></button>
    <button class="tab" data-mode="summary">Summary</button>
    <div class="spacer"></div>
    <button class="btn" id="exportJson">Export JSON</button>
    <button class="btn" id="exportCsv">Export CSV</button>
    <button class="btn" id="importBtn">Import…</button>
    <input type="file" id="importFile" accept="application/json" class="hide">
  </div>
  <div class="progress"><i id="bar"></i></div>
  <div class="counts" id="counts"></div>
</header>

<main>
  <div id="reviewer"><div class="card" id="card"></div></div>
  <div id="summary" class="hide"></div>
</main>

<div class="decisionbar" id="decisionbar">
  <div class="dbinner" id="dbtns"></div>
  <div class="extra" id="demoteRow" style="display:none">
    <label class="hint">Off-cell reason:</label>
    <select id="bucket">
      <option value="">— choose —</option>
      <option value="outcome-not-fertility">outcome is not fertility</option>
      <option value="different-cause">different cause / treatment</option>
      <option value="fertility-is-cause">fertility is the cause (RHS)</option>
      <option value="different-channel">different channel (e.g. grandparental care)</option>
      <option value="reverse-direction">reverse direction (children -> pension)</option>
      <option value="not-oas">not about old-age security</option>
      <option value="other">other</option>
    </select>
  </div>
  <div class="extra">
    <input type="text" id="note" placeholder="Optional note (saved with your verdict)…">
    <span class="hint">keys: <b>1</b>/<b>2</b>/<b>3</b> verdict · <b>&larr;</b>/<b>&rarr;</b> or <b>j</b>/<b>k</b> nav · <b>u</b> undo</span>
  </div>
</div>

<script>
const DATA = __DATA_JSON__;
const KEY = "ra-gate:" + DATA.slug;
const ALL = {pooling: DATA.pooling, uncertain: DATA.uncertain};
const BYID = {}; [...DATA.pooling, ...DATA.uncertain].forEach(r=>BYID[r.id]=r);

let state = load();               // {decisions:{id:{v,bucket,note,ts}}, pos:{pooling,uncertain}, mode}
let mode = state.mode || "pooling";

function load(){
  try{ const s = JSON.parse(localStorage.getItem(KEY)); if(s&&s.decisions) return s; }catch(e){}
  return {decisions:{}, pos:{pooling:0,uncertain:0}, mode:"pooling"};
}
function save(){ state.mode=mode; localStorage.setItem(KEY, JSON.stringify(state)); }

// verdict configs per mode
const VCFG = {
  pooling:  [ {v:"confirm", label:"Confirm in-cell", cls:"ok",  key:"1"},
              {v:"demote",  label:"Demote off-cell", cls:"no",  key:"2"},
              {v:"unsure",  label:"Unsure",          cls:"skip",key:"3"} ],
  uncertain:[ {v:"relevant",label:"Relevant",        cls:"ok",  key:"1"},
              {v:"not",     label:"Not relevant",     cls:"no",  key:"2"},
              {v:"unsure",  label:"Unsure",          cls:"skip",key:"3"} ]
};
const VLABEL = {confirm:"in-cell",demote:"off-cell",relevant:"relevant",not:"not relevant",unsure:"unsure"};
const VCLS = {confirm:"okbg",demote:"nobg",relevant:"okbg",not:"nobg",unsure:"skipbg"};

function list(){ return ALL[mode]; }
function pos(){ return Math.max(0, Math.min(state.pos[mode]||0, list().length-1)); }
function setPos(p){ state.pos[mode]=Math.max(0,Math.min(p,list().length-1)); save(); render(); }

function esc(s){ return (s==null?"":String(s)).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }

function render(){
  document.getElementById("pc").textContent = ALL.pooling.length;
  document.getElementById("uc").textContent = ALL.uncertain.length;
  document.querySelectorAll(".tab").forEach(t=>t.classList.toggle("active", t.dataset.mode===mode));
  const isSummary = mode==="summary";
  document.getElementById("reviewer").classList.toggle("hide", isSummary);
  document.getElementById("summary").classList.toggle("hide", !isSummary);
  document.getElementById("decisionbar").classList.toggle("hide", isSummary);
  renderCounts();
  if(isSummary){ renderSummary(); return; }
  renderCard();
}

function renderCounts(){
  const el=document.getElementById("counts");
  function tally(arr){ const t={done:0,total:arr.length}; arr.forEach(r=>{ if(state.decisions[r.id]) t.done++; }); return t; }
  const p=tally(ALL.pooling), u=tally(ALL.uncertain);
  // pooling breakdown
  const pv={confirm:0,demote:0,unsure:0}; ALL.pooling.forEach(r=>{const d=state.decisions[r.id];if(d)pv[d.v]++;});
  const uv={relevant:0,not:0,unsure:0}; ALL.uncertain.forEach(r=>{const d=state.decisions[r.id];if(d)uv[d.v]++;});
  el.innerHTML =
    `<span>Pooling: <b>${p.done}/${p.total}</b> · in-cell ${pv.confirm} · off-cell ${pv.demote} · unsure ${pv.unsure}</span>`+
    `<span>UNCERTAINs: <b>${u.done}/${u.total}</b> · relevant ${uv.relevant} · not ${uv.not} · unsure ${uv.unsure}</span>`+
    `<span>Confirmed pooling set → <b>${pv.confirm}</b> studies</span>`;
  const arr=list();
  if(mode!=="summary"){
    const done = arr.filter(r=>state.decisions[r.id]).length;
    document.getElementById("bar").style.width = (arr.length? (done/arr.length*100):0)+"%";
  }
}

function renderCard(){
  const arr=list(), i=pos(), r=arr[i];
  if(!r){ document.getElementById("card").innerHTML="<p>Nothing to review.</p>"; return; }
  const d = state.decisions[r.id];
  const meta = [r.year, r.venue, r.authors].filter(Boolean).join(" · ");
  const cellcls = "cell-"+(r.cell||"null");
  let gate;
  if(mode==="pooling"){
    gate = `<div class="lab">Gate's call — does this identify the primary cell?
        <span class="cellpill ${cellcls}">${esc(r.cell||"?")}</span></div>
      <dl class="axes">
        <dt>outcome</dt><dd>${esc(r.outcome||"—")}</dd>
        <dt>mechanism</dt><dd>${esc(r.mechanism||"—")}</dd>
        <dt>direction</dt><dd>${esc(r.direction||"—")}</dd>
      </dl>
      ${r.reason?`<div class="gatereason">"${esc(r.reason)}"</div>`:""}`;
  } else {
    gate = `<div class="lab">Screen said UNCERTAIN
        <span class="cellpill ${cellcls}">cell: ${esc(r.cell||"?")}</span>
        ${r.evidence_type?`<span class="cellpill cell-null">${esc(r.evidence_type)}</span>`:""}</div>
      ${r.reason?`<div class="gatereason">"${esc(r.reason)}"</div>`:""}
      ${r.snow_reason?`<div class="hint" style="margin-top:6px">discovery note: ${esc(r.snow_reason)}</div>`:""}`;
  }
  const absHtml = r.abstract
    ? `<div class="abstract">${esc(r.abstract)}</div>`
    : `<div class="abstract noabs">No abstract on file — <a href="${esc(r.scholar)}" target="_blank" rel="noopener">open in Google Scholar</a> to read.</div>`;
  const decided = d ? `<span class="decided" style="background:var(--${VCLS[d.v]})">your call: ${VLABEL[d.v]}${d.bucket?" ("+d.bucket+")":""}</span>` : "";
  document.getElementById("card").innerHTML = `
    <div class="cardhead">
      <span class="pos">${i+1} / ${arr.length}</span>
      ${r.is_gold?'<span class="gold">gold anchor</span>':''}
      ${decided}
    </div>
    <div class="ttl"><a href="${esc(r.scholar)}" target="_blank" rel="noopener">${esc(r.title)}</a></div>
    <div class="meta">${esc(meta)||"&nbsp;"}</div>
    <div class="gatebox">${gate}</div>
    ${absHtml}`;
  renderButtons(d);
  // restore demote UI + note
  const nb=document.getElementById("note"); nb.value = d&&d.note?d.note:"";
  const dr=document.getElementById("demoteRow");
  dr.style.display = (mode==="pooling" && d && d.v==="demote") ? "flex":"none";
  if(d&&d.bucket) document.getElementById("bucket").value=d.bucket;
  else document.getElementById("bucket").value="";
}

function renderButtons(d){
  const box=document.getElementById("dbtns");
  const cfg=VCFG[mode];
  box.innerHTML = cfg.map(c=>
    `<button class="dbtn ${c.cls} ${d&&d.v===c.v?'sel':''}" data-v="${c.v}">${c.label} <kbd>${c.key}</kbd></button>`
  ).join("") +
   `<div class="nav">
      <button class="btn" data-nav="-1">&larr; Prev</button>
      <button class="btn" data-nav="1">Next &rarr;</button>
    </div>`;
}

function decide(v){
  const arr=list(), r=arr[pos()];
  if(!r) return;
  const prev = state.decisions[r.id]||{};
  const note = document.getElementById("note").value.trim();
  const bucket = (mode==="pooling"&&v==="demote") ? document.getElementById("bucket").value : "";
  state.decisions[r.id] = {v, bucket, note, ts:Date.now()};
  save();
  const dr=document.getElementById("demoteRow");
  if(mode==="pooling"&&v==="demote"){
    dr.style.display="flex"; renderCard();          // stay so RA can pick a bucket
    return;
  }
  // auto-advance to next undecided (fallback: next)
  advance();
}
function advance(){
  const arr=list(); let p=pos();
  let n=p+1;
  while(n<arr.length && state.decisions[arr[n].id]) n++;   // skip already-done
  if(n>=arr.length) n=Math.min(p+1,arr.length-1);
  setPos(n);
}
function undo(){
  const r=list()[pos()]; if(r){ delete state.decisions[r.id]; save(); render(); }
}

function renderSummary(){
  const el=document.getElementById("summary");
  function tbl(title, arr, cols){
    let h=`<h2 style="font-size:14px;margin:18px 0 8px">${title}</h2><table><thead><tr>
      <th>#</th><th>your call</th><th>title</th>${cols}</tr></thead><tbody>`;
    arr.forEach((r,i)=>{
      const d=state.decisions[r.id];
      const call = d?`<span class="tag" style="background:var(--${VCLS[d.v]})">${VLABEL[d.v]}${d.bucket?"·"+d.bucket:""}</span>`:'<span class="hint">—</span>';
      h+=`<tr data-mode="${r.group}" data-id="${r.id}"><td>${i+1}</td><td>${call}</td>
        <td>${r.is_gold?'<span class="gold">gold</span> ':''}${esc(r.title)}</td>
        ${r.group==='pooling'
          ? `<td><span class="cellpill cell-${r.cell||'null'}">${esc(r.cell||'?')}</span></td>`
          : `<td>${esc(r.evidence_type||'')}</td>`}</tr>`;
    });
    return h+"</tbody></table>";
  }
  el.innerHTML = tbl("Pooling set (61) — spot-check", ALL.pooling, "<th>gate cell</th>")
              + tbl("UNCERTAINs (88) — relevance", ALL.uncertain, "<th>type</th>");
  el.querySelectorAll("tr[data-id]").forEach(tr=>tr.addEventListener("click",()=>{
    mode=tr.dataset.mode;
    const idx=list().findIndex(r=>r.id===tr.dataset.id);
    setPos(idx); render();
  }));
}

// ---- exports ----
function download(name, text, type){
  const blob=new Blob([text],{type}); const url=URL.createObjectURL(blob);
  const a=document.createElement("a"); a.href=url; a.download=name; a.click();
  setTimeout(()=>URL.revokeObjectURL(url), 500);
}
function exportRows(){
  const rows=[];
  [...ALL.pooling,...ALL.uncertain].forEach(r=>{
    const d=state.decisions[r.id];
    rows.push({group:r.group, id:r.id, title:r.title, is_gold:r.is_gold,
      gate_cell:r.cell, verdict:d?d.v:"", ra_label:d?VLABEL[d.v]:"",
      off_cell_bucket:d?d.bucket:"", note:d?d.note:""});
  });
  return rows;
}
document.getElementById("exportJson").onclick=()=>{
  download(DATA.slug+"-ra-gate-decisions.json",
    JSON.stringify({slug:DATA.slug, exported:Date.now(), decisions:state.decisions, rows:exportRows()}, null, 2),
    "application/json");
};
document.getElementById("exportCsv").onclick=()=>{
  const rows=exportRows(); const cols=Object.keys(rows[0]);
  const q=s=>'"'+String(s==null?"":s).replace(/"/g,'""')+'"';
  const csv=[cols.join(",")].concat(rows.map(r=>cols.map(c=>q(r[c])).join(","))).join("\n");
  download(DATA.slug+"-ra-gate-decisions.csv", csv, "text/csv");
};
document.getElementById("importBtn").onclick=()=>document.getElementById("importFile").click();
document.getElementById("importFile").onchange=(e)=>{
  const f=e.target.files[0]; if(!f) return;
  const rd=new FileReader();
  rd.onload=()=>{ try{ const j=JSON.parse(rd.result);
    if(j.decisions){ state.decisions=Object.assign(state.decisions,j.decisions); save(); render();
      alert("Imported "+Object.keys(j.decisions).length+" decisions."); }
    else alert("No decisions field found."); }catch(err){ alert("Bad JSON: "+err); } };
  rd.readAsText(f);
};

// ---- events ----
document.querySelectorAll(".tab").forEach(t=>t.onclick=()=>{ mode=t.dataset.mode; save(); render(); });
document.addEventListener("click",e=>{
  const b=e.target.closest("[data-v]"); if(b){ decide(b.dataset.v); return; }
  const n=e.target.closest("[data-nav]"); if(n){ setPos(pos()+ (+n.dataset.nav)); return; }
});
document.getElementById("bucket").onchange=()=>{
  const r=list()[pos()], d=state.decisions[r.id];
  if(d){ d.bucket=document.getElementById("bucket").value; save(); }
};
document.getElementById("note").addEventListener("blur",()=>{
  const r=list()[pos()], d=state.decisions[r.id];
  if(d){ d.note=document.getElementById("note").value.trim(); save(); }
});
document.addEventListener("keydown",e=>{
  if(mode==="summary") return;
  const t=e.target.tagName;
  if(t==="INPUT"||t==="SELECT"||t==="TEXTAREA") return;
  const cfg=VCFG[mode];
  const hit=cfg.find(c=>c.key===e.key);
  if(hit){ e.preventDefault(); decide(hit.v); return; }
  if(e.key==="ArrowRight"||e.key==="j"){ e.preventDefault(); setPos(pos()+1); }
  else if(e.key==="ArrowLeft"||e.key==="k"){ e.preventDefault(); setPos(pos()-1); }
  else if(e.key==="u"){ e.preventDefault(); undo(); }
});

render();
</script>
</body>
</html>
"""

out_html = TEMPLATE.replace("__DATA_JSON__", data_json)
out_path = rp("output", f"{SLUG}-ra-gate.html")
with open(out_path, "w") as f:
    f.write(out_html)

print(f"wrote {out_path}")
print(f"  pooling spot-check: {len(pooling)} ({sum(r['is_gold'] for r in pooling)} gold)")
print(f"  uncertain relevance: {len(uncertain)}")
print(f"  abstracts inline: pooling {sum(1 for r in pooling if r['abstract'])}/{len(pooling)}, "
      f"uncertain {sum(1 for r in uncertain if r['abstract'])}/{len(uncertain)}")
