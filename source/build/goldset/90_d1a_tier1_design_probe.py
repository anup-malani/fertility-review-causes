#!/usr/bin/env python3
"""
90_d1a_tier1_design_probe.py — D.1.a, stage A3 continued. HUNT TIER 1 BY DESIGN, NOT BY TOPIC.

Why this exists. The channel-1 probe (89) surfaced thirteen S3 anchor candidates and **not one is a
natural experiment** — every one is Tier 3 or Tier 4 under scope Ruling 3 on the face of its title.
A topical probe ranks by citation and returns the field's canon, and this field's canon is
cross-sectional. The Tier 1 material the chapter needs to rate anything above Very Low has to be
sought by the vocabulary of the DESIGN and by the NAMES OF THE SHOCKS, which is what this does.

Two constraints carried from 89, both learned the hard way that day:

  * **OpenAlex throttles boolean searches above five OR/AND/NOT operators** and answers with a
    rate-limit error rather than a result. Every probe below is therefore deliberately NARROW — a
    compact outcome disjunction plus a small treatment clause — and the union is assembled
    client-side. This is the pattern the production query will have to use too; one wide boolean is
    not available.
  * **The outcome axis collides with clinical medicine** (fertility as IVF, birth as birth weight).
    Handled here by demographic outcome vocabulary plus, where a probe is topically broad, the
    four-field social-science restriction. Narrow probes (named shocks) run UNRESTRICTED, because a
    named shock like "blue laws" carries no clinical sense and the restriction would only cost recall.

Nothing here asserts a DOI or a title from memory: every record printed is live API output, and a hit
is a CANDIDATE until it clears the Crossref + doi.org existence gate.

Output: temp/d1a/tier1-design-probe.json
        temp/d1a/tier1-design-probe.md
"""
import json, os, subprocess, sys, time, urllib.parse

SLUG = "postmaterialism-individualism-secularization"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUTDIR = os.path.join(ROOT, "temp", "d1a")
os.makedirs(OUTDIR, exist_ok=True)
OUT_JSON = os.path.join(OUTDIR, "tier1-design-probe.json")
OUT_MD = os.path.join(OUTDIR, "tier1-design-probe.md")
API = "https://api.openalex.org/works"

FIELDS = "primary_topic.field.id:fields/33|fields/20|fields/32|fields/12"
FERT = "(fertility OR childbearing OR births)"          # 2 operators, leaves 3
FERT1 = "fertility"                                      # 0 operators, leaves 5

# (probe_id, pair, search_string, restrict_fields, note)
# Operator budget is annotated on every line and must stay <= 5.
PROBES = [
    # --- S3, named institutional shocks. Unrestricted: these phrases have no clinical sense. ---
    ("shock_church_tax", "S3", f'"church tax" AND {FERT}', False, "German/Nordic church-tax and opt-out reforms"),
    ("shock_blue_laws", "S3", f'("blue laws" OR "Sunday trading" OR "Sunday closing") AND {FERT1}', False,
     "US blue-law repeal; the Gruber-Hungerman design family"),
    ("shock_state_atheism", "S3", f'("state atheism" OR antireligious OR "anti-religious") AND {FERT1}', False,
     "Soviet, Albanian, and Chinese campaigns against religious practice"),
    ("shock_deregulation", "S3", f'("religious market" OR "religious deregulation") AND {FERT1}', False,
     "religious-market structure and competition"),
    ("shock_scandal", "S3", f'(scandal OR "abuse crisis") AND religiosity AND {FERT1}', False,
     "clergy-scandal shocks to attendance"),
    ("shock_missionary", "S3", f'(missionary OR missions) AND {FERT} AND historical', False,
     "historical religious-exposure variation"),
    ("shock_quiet_revolution", "S3", f'("Quiet Revolution" OR dechristianization OR déchristianisation) AND {FERT1}',
     False, "Quebec and French secularization episodes"),
    ("shock_schooling_secular", "S3", f'("compulsory schooling" OR "school reform") AND religiosity AND {FERT1}',
     False, "secular schooling exposure as a religiosity shock"),

    # --- S3, design vocabulary against the topical core. ---
    ("design_natexp", "S3", f'religiosity AND {FERT1} AND ("natural experiment" OR "quasi-experimental")', False,
     "self-described identification"),
    ("design_iv", "S3", f'(religion OR religiosity) AND {FERT1} AND (instrument OR instrumental)', False,
     "IV designs"),
    ("design_did_rd", "S3", f'religion AND {FERT1} AND ("difference-in-differences" OR "regression discontinuity")',
     False, "DiD and RD designs"),
    ("design_causal_effect", "S3", f'(secularization OR religiosity) AND {FERT1} AND (causal OR exogenous)', False,
     "explicit causal framing"),

    # --- S3, denominational and high-fertility-group variation. ---
    ("group_high_fertility_sects", "S3", f'(Amish OR Hutterite OR Haredi OR Mormon) AND {FERT1}', False,
     "denominational fertility differentials; PM/FDT-era baseline material"),
    ("group_conversion", "S3", f'(conversion OR "religious switching" OR apostasy) AND {FERT1}', False,
     "within-person religiosity change"),

    # --- S3, panel / ex-ante measurement (the Tier 2 PRIMARY_VALUE_EX_ANTE cell). ---
    ("exante_panel", "S3", f'religiosity AND {FERT1} AND (panel OR longitudinal OR prospective)', True,
     "value measured before the outcome"),

    # --- S1 / S2, the economics-of-culture design family (Tier 2, epidemiological approach). ---
    ("culture_immigrants", "S1S2", f'culture AND {FERT1} AND (immigrants OR "second generation")', True,
     "epidemiological approach -- Wall 5 routes on proxy content"),
    ("culture_kinship", "S2", f'("kinship intensity" OR "kin networks" OR clan) AND {FERT1}', True,
     "Enke-family kinship-structure measures"),
    ("culture_individualism_econ", "S2", f'individualism AND {FERT1} AND (culture OR cultural)', True,
     "individualism indices in economics; NOTE the individualiSED stemming trap"),
    ("s1_postmat_direct", "S1", f'(postmaterialism OR postmaterialist) AND {FERT1}', False,
     "does ANY postmaterialism-fertility estimate exist"),
    ("s1_value_orientations", "S1", f'"value orientations" AND {FERT} AND (Inglehart OR survey)', True,
     "Inglehart-battery studies with a fertility outcome"),
    ("s5_material_values", "S5", f'("material values" OR materialism) AND (childbearing OR childlessness)', True,
     "consumer-psychology materialism, the polysemic pole"),

    # --- Routing decoys, deliberately included so the anchor set tests routing (scope: decoy rule). ---
    ("decoy_media_a20", "DECOY", f'(television OR soap OR media) AND {FERT1} AND exposure', True,
     "A.20 channel-exposure decoys"),
    ("decoy_gender_d2a", "DECOY", f'"gender role attitudes" AND {FERT1}', True, "D.2.a decoys"),
    ("decoy_contraceptive_stigma_a6", "DECOY", f'(stigma OR legitimation) AND contraception AND {FERT1}', True,
     "A.6 decoys"),
]


def fetch(search, restrict, per=15, tries=4):
    """Three-state: OK / UNCONFIRMED (transport) / ERROR (API refused, e.g. operator cap)."""
    filt = f"title_and_abstract.search:{search}"
    if restrict:
        filt += "," + FIELDS
    url = API + "?" + urllib.parse.urlencode(
        {"filter": filt, "per-page": per, "sort": "cited_by_count:desc", "mailto": MAILTO})
    last = None
    for attempt in range(tries):
        try:
            out = subprocess.run(["curl", "-s", "-m", "45", "-A", UA, url],
                                 capture_output=True, text=True)
            if out.returncode != 0:
                last = f"curl exit {out.returncode}"
            else:
                data = json.loads(out.stdout)
                if "results" in data:
                    return url, data, None, "OK"
                if "error" in data:  # API refused -- do NOT retry, it will refuse identically
                    return url, None, f"{data.get('error')}: {str(data.get('message'))[:160]}", "ERROR"
                last = f"unexpected payload: {out.stdout[:160]}"
        except Exception as e:  # noqa: BLE001
            last = f"{type(e).__name__}: {e}"
        time.sleep(2 * (attempt + 1))
    return url, None, last, "UNCONFIRMED"


def op_count(s):
    """Count OR/AND/NOT tokens -- the quantity OpenAlex caps at five."""
    return sum(s.split().count(t) for t in ("OR", "AND", "NOT"))


def invert(inv):
    if not inv:
        return ""
    pos = {}
    for w, idxs in inv.items():
        for i in idxs:
            pos[i] = w
    return " ".join(pos[i] for i in sorted(pos))


def slim(w):
    s = (w.get("primary_location") or {}).get("source") or {}
    return {"work_id": (w.get("id") or "").rsplit("/", 1)[-1],
            "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
            "title": w.get("title") or "", "year": w.get("publication_year"),
            "type": w.get("type"), "venue": s.get("display_name") or "",
            "cited_by": w.get("cited_by_count"),
            "authors": [a["author"]["display_name"] for a in (w.get("authorships") or [])[:5]],
            "abstract_head": invert(w.get("abstract_inverted_index"))[:260]}


def main():
    out = {"slug": SLUG, "probe": "Tier-1 by design vocabulary and named shocks", "probes": {}}
    seen = {}
    for pid, pair, search, restrict, note in PROBES:
        ops = op_count(search)
        flag = "" if ops <= 5 else f"  !! {ops} OPERATORS, OVER CAP"
        url, data, err, status = fetch(search, restrict)
        rec = {"pair": pair, "search": search, "operators": ops, "field_restricted": restrict,
               "note": note, "url": url, "status": status}
        if data is None:
            rec["error"] = err
            print(f"{pid:32s} {status}: {err}{flag}", file=sys.stderr)
        else:
            hits = [slim(w) for w in data.get("results", [])]
            rec["total_count"] = data["meta"]["count"]
            rec["hits"] = hits
            for h in hits:
                key = h["doi"] or h["title"].lower()[:60]
                seen.setdefault(key, {"record": h, "probes": []})["probes"].append(pid)
            print(f"{pid:32s} ops={ops} count={rec['total_count']:>6} returned={len(hits)}{flag}",
                  file=sys.stderr)
        out["probes"][pid] = rec
        time.sleep(0.4)

    out["union_size"] = len(seen)
    out["union"] = [{"probes": v["probes"], **v["record"]} for v in seen.values()]
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)

    lines = ["# D.1.a — Tier-1 design probe, raw results", "",
             "Live OpenAlex via `90_d1a_tier1_design_probe.py`. Candidates, not anchors: nothing here",
             "has cleared the existence gate.", "",
             f"Union across all probes: **{len(seen)}** distinct records.", ""]
    for pid, rec in out["probes"].items():
        head = f"## {pid} [{rec['pair']}] — {rec['status']}"
        if rec["status"] == "OK":
            head += f", total {rec['total_count']}"
        lines += [head, "", f"*{rec['note']}*", "", f"`{rec['search']}`  ({rec['operators']} operators"
                  + (", field-restricted)" if rec["field_restricted"] else ")"), ""]
        if rec["status"] != "OK":
            lines += [f"**{rec.get('error')}**", ""]
            continue
        if not rec["hits"]:
            lines += ["*(no hits)*", ""]
        for h in rec["hits"]:
            lines.append(f"- [{h['cited_by']}c, {h['year']}] {h['title']} — *{h['venue']}* — "
                         f"`{h['doi'] or 'NO-DOI'}`")
        lines.append("")
    with open(OUT_MD, "w") as f:
        f.write("\n".join(lines))
    print(f"\nunion={len(seen)}\nwrote {OUT_JSON}\nwrote {OUT_MD}", file=sys.stderr)


if __name__ == "__main__":
    main()
