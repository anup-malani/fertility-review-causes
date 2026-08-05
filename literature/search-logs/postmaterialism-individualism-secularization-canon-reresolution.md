# D.1.a — channel-2 canon re-resolution, off Crossref and Semantic Scholar

Run 2026-08-04 by `95_d1a_canon_reresolve.py`. Supersedes the OpenAlex resolution in `92_`
for seeding purposes; 92's output is kept as the record of what OpenAlex answered while the
free tier could still answer. Every row is re-resolved against BOTH providers, including the
four 92 had already marked RESOLVED, because two independently-sourced resolvers agreeing on
an identifier is better evidence than one asserting it.

- rows re-resolved: **16**
- both providers resolved and agree: **6**
- same work, two registered DOIs, citations split (`TWIN_DOI`, seed both): **1**
- one provider resolved, the other did not: **4**
- neither provider resolved: **5**
- rescued by the subtitle-drop fallback that Jaccard alone false-negatived: **1**
- carry a seedable identifier from a provider that actually resolved: **11**

`RESOLVED_DISCREPANT` rows are NOT seedable and are not counted above: the provider matched a
title but the author or year disagrees, which means it resolved to *something*, not
necessarily to the right thing.

| label | v5? | Crossref | S2 | agreement | 92 (OpenAlex) | seed id |
|---|---|---|---|---|---|---|
| Lesthaeghe 1983 | yes | RESOLVED | RESOLVED | AGREE | RESOLVED | `84b141676afad54cd636bb0bec5188cb4f636ba6` |
| van de Kaa 1987 | yes | UNRESOLVED | RESOLVED | SINGLE_PROVIDER | RESOLVED | `a4625dbdaceb56b742cb921a1993332a78174f3c` |
| Lesthaeghe and van de Kaa 1986 | yes | UNRESOLVED | UNRESOLVED | NEITHER | UNRESOLVED | `—` |
| Lesthaeghe and Surkyn 1988 | yes | RESOLVED | RESOLVED | AGREE | RESOLVED | `7a6c35241f4f2ae0f62795670afdd5dd428613fa` |
| Inglehart 1977 | yes | UNRESOLVED | RESOLVED | SINGLE_PROVIDER | RESOLVED_DISCREPANT | `db00dde1e9630e3bbf2bfb6d9314aa6f9c525591` |
| Norris and Inglehart 2004 | yes | UNRESOLVED | RESOLVED | SINGLE_PROVIDER | RESOLVED | `bdd32ed2f77aceb744bf2512ddc0ac56028c906a` |
| Frejka and Westoff 2008 | yes | RESOLVED | RESOLVED | AGREE | UNCONFIRMED | `11163f3b53cbcad80df57566f05f9a0718e6c34b` |
| Hagestad and Call 2007 | yes | RESOLVED_SUBTITLE | UNRESOLVED | SINGLE_PROVIDER | UNRESOLVED | `10.1177/0192513x07303836` |
| Inglehart 1997 |  | RESOLVED_DISCREPANT | UNRESOLVED | NEITHER | UNCONFIRMED | `—` |
| Inglehart and Baker 2000 |  | RESOLVED | RESOLVED | TWIN_DOI | UNCONFIRMED | `7d0e7ec4f0706b57fec51cbc45413acb5abbb720` |
| Schwartz 1992 |  | RESOLVED_DISCREPANT | UNRESOLVED | NEITHER | RESOLVED_DISCREPANT | `—` |
| Hofstede 1980 |  | RESOLVED_DISCREPANT | RESOLVED_DISCREPANT | NEITHER | RESOLVED_DISCREPANT | `—` |
| Alesina and Giuliano 2015 |  | RESOLVED_DISCREPANT | UNRESOLVED | NEITHER | UNCONFIRMED | `—` |
| Enke 2019 |  | RESOLVED | RESOLVED | AGREE | UNCONFIRMED | `0a3f69f8fd10ed07d533ef9f33756b8de16080b6` |
| Voas 2009 |  | RESOLVED | RESOLVED | AGREE | UNCONFIRMED | `e7c2d7e77318d9b1cdb829ecd1103ff2d7cad8bc` |
| McQuillan 2004 |  | RESOLVED | RESOLVED | AGREE | UNCONFIRMED | `9d9d783e336c6fbfba67e40bd31a36f3eea7b1d9` |
