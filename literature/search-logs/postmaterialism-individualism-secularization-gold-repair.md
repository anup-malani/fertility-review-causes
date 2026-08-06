# D.1.a — gold-set repair: citation strings, and what they were costing

`107_` found that 24 of the 68 gold records missing from the v2 corpus store an entire bibliography line where a title belongs — Crossref's `unstructured` field, which `93_`/`96_` fall back to. A3 found 27 of these and did not fully repair them. **Such a row cannot match by title however complete the index is, so it depresses measured Recall(B-only) while saying nothing about coverage.**

## The decision that would have rigged this

Titles are extracted **by parsing the string only**. The obvious alternative — search each citation against OpenAlex and adopt the best match's title — is more accurate per record and is disqualified: it repairs only the rows OpenAlex can confirm, so the repaired gold becomes a set of works OpenAlex is known to hold and the recall it then measures is *guaranteed* to rise. **The measurement would be an artifact of its own repair.** Parsing is provider-independent, so a work whose title we recover but which OpenAlex does not hold correctly stays a miss. Provider lookup runs afterwards and only labels confidence.

- citation-string rows found in Tier B: **24**
- repaired: **23**
- left unrepaired (no year anchor — still counted as misses): **1**
- duplicates the repair exposed and merged: **7**
- Tier-B rows: 400 → **393**

## Re-measured recall against the v2 corpus

| gold set | matched | n | Recall(B-only) |
|---|---|---|---|
| as frozen | 336 | 400 | 84.0% |
| **repaired** | **342** | **393** | **87.0%** |

### On the same basis as the headline recall figures

`103_` reports A-only / B-only / both off `cv.load()`, which drops Tier-B rows overlapping Tier A and dedupes on the normalised title. The raw Tier-B table above is **not** that basis, so this is the comparable one.

| tier | before | after |
|---|---|---|
| A_ONLY | 92.9% (n=14) | **92.3%** (n=13) |
| B_ONLY | 83.2% (n=381) | **86.4%** (n=375) |
| BOTH | 100.0% (n=17) | **100.0%** (n=18) |
| **weighted** | 84.2% (n=412) | **87.2%** (n=406) |

**The denominator moved as well as the numerator** (400 → 393), because merging duplicates removes rows. A recall figure that moved only because rows were deleted would be meaningless, so both are shown.

## Confidence labels — computed AFTER the repair, and they decided nothing

- repaired title found in OpenAlex: **11**
- repaired title not found: **12** — these stay misses, correctly
- unconfirmed (provider refused): 0

## Every repair, for reading

- **Changes in work and family attitudes over birth cohorts and links to childfree ideals in Finnish women**
  - from: `Laamanen VM (2024) Changes in work and family attitudes over birth cohorts and links to childfree ideals in Finnish women. Master’s Thesis University `
- **Three Dimensions of the Relationship between Gender Role Attitudes and Fertility Intentions**
  - from: `Lappegard, T., Neyer, G., & Vignoli, D. (2015). Three Dimensions of the Relationship between Gender Role Attitudes and Fertility Intentions. Stockholm`
- **Postmodern fertility preferences: From changing value orientation to new behavior**
  - from: `van de Kaa, D. J. (2001). Postmodern fertility preferences: From changing value orientation to new behavior. Population and Development Review, 27, 29`
- **Culture, religion, and fertility: a global view**
  - from: `Lutz W (1987) Culture, religion, and fertility: a global view. Genus 15–35`
- **An assessment on the impact of women’s autonomy, education and social participation on childbearing intention **
  - from: `Abbasi-Shavazi, M., & Khajehsalehi, Z. (2020). An assessment on the impact of women’s autonomy, education and social participation on childbearing int`
- **Religion and fertility in India**
  - from: `Jeffery, P., & Jeffery, R. (2000). Religion and fertility in India. Economic and Political Weekly, 35, 3253–3259.`
- **Religion and fertility: Analysis of fertility behavior of Sunni and Shiite religious groups in Galehdar**
  - from: `Mahmoudian, H., & Nobakht, R. (2010). Religion and fertility: Analysis of fertility behavior of Sunni and Shiite religious groups in Galehdar. Fars Pr`
- **Religion, gender equality, and fertility**
  - from: `Jeppsen, C. (2015). Religion, gender equality, and fertility. [Unpublished Doctoral Dissertation]. The Pennsylvania State University. University Park,`
- **Islamism, religiosity and fertility in the Muslim world**
  - from: `Kaufmann, E. (2009). Islamism, religiosity and fertility in the Muslim world. Paper presented at the annual meeting of the International Sociological `
- **How conservative are british attitudes to childbearing**
  - from: `Simons, J. (1986). How conservative are british attitudes to childbearing. Quarterly Journal of Social Affairs, 2, 415–429.`
- **Losing my Religion (or Maybe not): Religion and Fertility Patterns in Africa**
  - from: `Ishak, P. W., and Gradstein, M. 2022. Losing my Religion (or Maybe not): Religion and Fertility Patterns in Africa.`
- **Religion and Reproductive Behavior in Sub-Saharan Africa**
  - from: `Westoff, C. F., and Bietsch, K. 2015. Religion and Reproductive Behavior in Sub-Saharan Africa. DHS Analytical Studies. 48. Rockville, Maryland, USA: `
- **Fruktsamhetsmönster, produktionsstruktur och sekularisering: en jämförelse mellan 69 härader vid 1800-talets s**
  - from: `Larsson, M. (1984). Fruktsamhetsmönster, produktionsstruktur och sekularisering: en jämförelse mellan 69 härader vid 1800-talets slut[Fertility patter`
- **Modes of production secularization and the pace of the fertility decline in Western Europe 1870–1930**
  - from: `Lesthaeghe, R. & Wilson, C. (1986). Modes of production secularization and the pace of the fertility decline in Western Europe 1870–1930. In A. J. Coa`
- **Secularization in Europe: Religious change between and within birth cohorts**
  - from: `Voas, D., & Doebler, S. (2011). Secularization in Europe: Religious change between and within birth cohorts. Religion and Society in Central and Easte`
- **The multidimensional impact of religion on childbearing preferences and behavior in Nepal**
  - from: `Pearce, L. D. (2000). The multidimensional impact of religion on childbearing preferences and behavior in Nepal. Ph.D., United States -- Pennsylvania:`
- **Socio-cultural dynamics of first birth intervals in Nepal**
  - from: `Suwal, J. V. (2001). Socio-cultural dynamics of first birth intervals in Nepal. Contribution to Nepalese Studies, 28(1), 11–33.`
- **The value and cost of children: Converging theory and research**
  - from: `Fawcett, J.T. ( 1976). The value and cost of children: Converging theory and research. In L. T. Ruzicka (Ed.), The economic and social supports for hi`
- **Changing value of children: An action theory of fertility behavior and intergenerational relationships in cros**
  - from: `Nauck, B. ( 2005). Changing value of children: An action theory of fertility behavior and intergenerational relationships in cross-cultural comparison`
- **The relationship between religion and fertility: Evidence for Austria**
  - from: `Heineck, G. (2006). The relationship between religion and fertility: Evidence for Austria. PER Working Paper 06-01.`
  - OpenAlex holds: *The relationship between religion and fertility : Evidence from Austria*
- **Postmodern fertility preferences: From changing value orientation to new behaviour**
  - from: `van de Kaa, D. (1998). Postmodern fertility preferences: From changing value orientation to new behaviour. Working Papers in Demography, No. 74, Resea`
- **Causality between religiosity and childbearing: Evidence from a Dutch panel study**
  - from: `Berghammer, C. (2009). Causality between religiosity and childbearing: Evidence from a Dutch panel study. Paper presented at the IUSSP conference, Mar`
- **Report on analysis of ESS data on cross-national differences in perceived norms concerning fertility-related b**
  - from: `Liefbroer, A. C., & Merz, E.-M. (2009). Report on analysis of ESS data on cross-national differences in perceived norms concerning fertility-related b`
  - OpenAlex holds: *Reproductive decision-making in a macro-micro perspective: report on analysis of ESS data on cross-national di*

## Left unrepaired — no year anchor to parse from

Left exactly as found and still counted as misses. A low repair rate is the correct outcome when the strings cannot be parsed; relaxing the rule to lift it is how the OAS run acquired a 40%-ghost Tier B.

- `B Arpino G Esping-Andersen L Pessin The diffusion of gender egalitarian values and fertility. The Fertility Gap in Europe: Singularities of the Spanis`

## Duplicates exposed by the repair

- kept *Postmodern fertility preferences: from changing value orientation to new behaviour* / dropped *Postmodern fertility preferences: From changing value orientation to new behavior*
- kept *Postmodern fertility preferences: from changing value orientation to new behaviour* / dropped *Postmodern fertility preferences: From changing value orientation to new behavior*
- kept *Fertility and Faith: The Demographic Revolution and the Transformation of World Religions * / dropped *Fertility and Faith: The Demographic Revolution and the Transformation of World Religions*
- kept *Secularization in Europe: religious change between and within birth cohorts* / dropped *Secularization in Europe: Religious change between and within birth cohorts*
- kept *Postmodern fertility preferences: from changing value orientation to new behaviour* / dropped *Postmodern fertility preferences: From changing value orientation to new behaviour*
- kept *Islamism, religiosity and fertility in the Muslim world* / dropped *Islamism, Religiosity and Fertility in the Muslim World*
- kept *Report on analysis of ESS data on cross-national differences in perceived norms concerning* / dropped *Report on analysis of ESS data on cross-national differences in perceived norms concerning*
