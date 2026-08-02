# Social-Voice Exemplar Bank — Anup Malani — EXPLAINER REGISTER

**What this is.** A curated bank of paragraphs from Anup Malani's Substack (*Research Notes*, `anupmalani.substack.com`) that exemplify his **explainer register**: the systematic, pedagogical writing of his law-and-economics teaching series. The signature move is **define → derive → worked example**, addressed to "you," building a concept from primitives for a beginner. These are meant to be injected live into an LLM's context as models to imitate (exemplar-in-context). The north star is the **dinner-table test**: would you say this sentence to a smart non-expert across a table?

This file is one of two register-specific banks split from the original combined `social.md`. Its sibling is `social-essay.md` (his essayistic, argument-driven register — re-anchoring the reader's wrong comparison). This register was **under-sampled** in the original bank, so it is deliberately rich here. If you are explaining a concept from primitives to a beginner, inject from this file; if you are drafting an argument-driven essay, inject from the essay bank.

**Status.** Date assembled: 2026-07-25. These are **SHORTLISTS the user finalizes.** The file is two tiers: a **CORE** set (the tightest five, one per distinct archetype — the default injection) and an **EXTENDED** set (additional non-redundant paragraphs worth keeping, for CORE+relevant injection). Source corpus: 30 posts at `/Users/amalani/UChicago Law Dropbox/Anup Malani/assistants/research-manager/projects/style-analysis/corpus/substack/`. **Systematic/distinct curation pass: 2026-07-27** — mapped all eleven entries to their systematic move; X6 moved to Deprecated as a near-duplicate of X4 (same short-deductive-chain technique, different content domain); Move notes tightened to name the technique first. See "Coverage notes" below the entries.

**Transcription notes (read before using).** Quotes are **verbatim in wording**. I have only: (a) normalized double-spaces-after-periods to single spaces; (b) removed inline footnote-anchor markers, figure references ("see figure below"), and interspersed student-query blocks; (c) stripped Substack's bold/italic emphasis markup on defined terms; (d) normalized escaped dollar signs (`\$` → `$`); (e) where noted, trimmed a leading stage-direction and flagged it. Small authorial typos are preserved and flagged inline. Nothing else is changed, added, or paraphrased. Verify any paragraph against its source file before it goes into production, since these get imitated.

**Register note on the AI-tell blocklist.** Screen against `~/.claude/refs/ai-tells.md`, but this teaching voice legitimately uses em-dashes (§9) and, as a section pivot, the occasional rhetorical question (§6). Do not exclude an otherwise-best exemplar for that alone; it is **included and flagged inline**, because the user is deciding whether the social register earns an exception. Voice fidelity is the priority for this bank.

---

## CORE (default injection — one per distinct archetype)

### 1. Defines a field from primitives (a whole discipline in five sentences)
*Source: "What is economics?," 2024-12-25 — https://anupmalani.substack.com/p/what-is-economics*

> Scarcity is central to economics. To "economize" is to make the best use of limited resources. If there were bountiful resources, predicting human behavior would be simple: people would do whatever they want. But when humans have limited resources, they have to figure out who gets what at the group level. And, at the individual level, they face trade-offs when deciding when to engage in one activity or another, to consume one good or another.

**Anchor:** *Move: define an entire field from one primitive, using a counterfactual to make it land.* Defines the whole discipline of economics in five sentences a non-expert follows ("if there were bountiful resources..."). The "start from the primitive" opening of the teaching register.

---

### 2. Worked example from a producer's primitives → derives a curve
*Source: "What is supply?," 2024-12-25 — https://anupmalani.substack.com/p/what-is-supply*

> One challenge with production is that, as a firm makes more output, at some point its cost per unit of output rises. Increasing the number of cakes produced per week requires not just proportionally more kitchen appliances and employees, but also more layers of management or the fixed costs of a new store. Eventually, these extra costs rise faster than output, so that the cost of each cake increases. If the price of cakes is fixed, maybe the firm makes some profit producing a small amount of cakes; but as output increases, the cost of producing cakes exceeds the price of cakes. Since the bakery will only produce an additional cake if its price can cover the marginal cost of that cake, it will stop producing when the price of cakes equals the marginal cost of cakes. However, if the price of cakes rises, the firm will produce some more cakes, because a few more cakes will be profitable. This generates what is called an individual firm's supply curve: an upward-sloping line that indicates how much quantity (on the x-axis) a firm produces as price (y-axis) rises.

**Anchor:** *Move: derive an abstraction from a concrete, narrative worked example, naming the concept only once it falls out.* Builds the supply curve out of a concrete producer (a bakery and its cakes), reasoning one step at a time. The archetypal define → derive → worked-example arc.

---

### 3. Addresses "you," builds the concept from your own day
*Source: "What is demand?," 2024-12-25 — https://anupmalani.substack.com/p/what-is-demand*

> Budgets apply to time too. You have 24 hours in a day. If you sleep 8, then you have 16 left over to do other things. If you sleep more, say 12, then you have just 12 hours for other things. Sleep has a time cost: you can do fewer other things. Suppose you finish dinner tonight at 10pm and have to be at work by 9am tomorrow, but your friends suggest going to a bar til 2am. If you go to the bar, you have 7 hours to sleep and get ready for work; if you don't, you have 11. The bar visit costs you not just money, but time. You lose the opportunity to sleep more. Economists call opportunities you lose when you engage in action Z the opportunity cost of Z. Usually opportunity costs refer to costs denominated in time, but are general enough to encompass costs denominated in other things, including money.

**Anchor:** *Move: address the reader as "you" and use their own life as the worked example.* Teaches opportunity cost by walking the reader through their own night (dinner, bar, sleep, work), naming the concept only after the reader has felt it.

---

### 4. Corrects a confusion people constantly make (one worked example)
*Source: "What is demand?," 2024-12-25 — https://anupmalani.substack.com/p/what-is-demand*

> The monetary cost of something you can buy with money is called the price of that thing. Do not confuse the price of a thing with its value to you. If the price of a ticket to a concert is $150, but you only value the concert at $50 because you don't like the band, then you won't go. You will only go to the concert if you value seeing the band live more than $150. But however much you value the band, the price remains $150.

**Anchor:** *Move: name a confusion people constantly make, then dissolve it with a single worked example.* Here: price ≠ value, made concrete with one $150 concert ticket. No jargon.

---

### 5. Wonder at the machine (why the mechanism is remarkable, with wit)
*Source: "Market equilibrium," 2024-12-30 — https://anupmalani.substack.com/p/market-equilibrium*

> While we all take prices for granted, they are—honestly—somewhat magical. First, they are very efficient at conveying information. The price of a good is a number, denominated in some currency, that tells consumers whether they ought to buy a good, and producers whether they should supply a good. Just 1 number. It doesn't matter whether I am going to use eggs to make breakfast, and you are going to use eggs to make a cake. If the price is $5, either of us will only buy if the value of the eggs in breakfast or the eggs in cake is worth more than $5 to us. Likewise, it doesn't matter if a producer is located in the US or in Mexico, or whether it uses factory farming to mass produce eggs or is a small family farm. It will not supply eggs (including shipping costs) unless its costs per carton are less than $5. Once we have prices, we don't need anything more to allocate goods.
>
> Second, a market sets a price without centralized control, without help from a divine entity or an alien race, even without ChatGPT or Claude! And it does so in a manner that ensures the price conveys how much the lowest cost producers can supply the good at, and how much the highest valued users are willing to pay for the good.

**Anchor:** *Move: make the reader marvel at an ordinary mechanism by isolating exactly what it does.* Isolates what a price does ("Just 1 number"), then lands the wit ("without a divine entity or an alien race, even without ChatGPT or Claude!"). *Flag: em-dashes in "they are—honestly—somewhat magical" (§9), and an exclamation for genuine delight — both authentically his.*

---

## EXTENDED (add when the draft calls for the specific move)

### X1. Grounds a primitive in a personal example (dog → rats → humans)
*Source: "What is demand?," 2024-12-25 — https://anupmalani.substack.com/p/what-is-demand*

> This lesson applies even to animals. I have a dog; his name is Clark (see photo below). He is very food motivated, i.e., he like treats. If I offer him a treat to turn around in a circle, he will do so. Many research labs at universities study rats. Rats like sugar water. If you offer rats some sugar water to press a button or to navigate through a maze, they will do so. Animals care about incentives, much as humans do.

**Anchor:** *Move: ground a primitive in a first-person anecdote, then generalize outward.* Takes "incentives matter" and grounds it in his own dog, then rats, then lands the general claim — a distinct addressing mode from CORE #3 (anecdote-then-generalize, vs. direct second-person immersion). Warm, first-person, concrete, dry. Moved here from the old combined bank's essay slot because it teaches a primitive to a beginner (explainer pedagogy), not an argument. *Flag: "he like treats" is a small typo in the original ("likes"). Fix on use, or accept as-is.*

---

### X2. Re-anchors what the reader actually values (essay move, explainer key)
*Source: "A framework for studying law and economics," 2025-01-07 — https://anupmalani.substack.com/p/a-framework-for-studying-law-and*

> People do not intrinsically value the legal system (legislature and courts combined) or lawyers. These two things are instrumental to producing things that are closer to what people ultimately value. People value things like food, housing, companionship and entertainment. They indirectly value inputs into producing those things. This includes things like seeds and fertilizer for food, bricks and insurance for housing, a community to find friends and mates, and wifi and laptops for entertainment. This should not come as a surprise. But producing consumer goods also requires contracts, legal rules, which require legislatures and courts, which in turn require lawyers. In other words, the legal system and lawyers are an input into the production of goods that our economy demands.

**Anchor:** *Move: re-anchor what the reader actually values, imported from the essay register.* You think you value courts and lawyers; actually you value food and housing, and law is just an input into producing them. Shows the two registers are one voice: the re-anchor here opens a framework rather than winning an argument.

---

### X3. Numeric iteration to derive equilibrium (walk the prices)
*Source: "Market equilibrium," 2024-12-30 — https://anupmalani.substack.com/p/market-equilibrium*
*[Setup for context: in the example, farms can supply the nth carton at a cost of $n, and consumers are arranged so that supply plus demand equals 10 at every price.]*

> To see how a market sets a price, arbitrarily pick a price, say 3. At this price, producers will supply 3 cartons of eggs per week. But consumers will want 7. But this means that there is excess demand: consumers want more eggs than producers supply. What if one farm increases price to 4? Some consumer will buy at that price because 6 people would purchase at a price of 4, more cartons than the other producers supply at 3. Other producers will realize that and match the first producer's price of 4. But there will still be excess demand, because producers will supply 4 at a price of 4, but consumers want 6 at that price. But if the same process of changing price raises price to 5, producers can supply exactly the same amount consumers want: 5. So that price equates supply with demand—no excess demand! What if we increase price to 6? Now farms want to supply 6, but consumers only want 4. We have the opposite problem as before: excess supply. So, the farm that risks raising its price from 5 to 6 will lose sales to other farms. Ultimately, whether you start with a price below or above 5, the price will adjust until it equates supply and demand, which happens at a price of 5.

**Anchor:** *Move: derive an equilibrium by iterating through concrete numbers until they converge.* Walks prices 3, 4, 5, 6 to convergence — a distinct rhetorical shape from the bakery's narrative derivation (CORE #2): here the reader watches the mechanism settle rather than watching a curve get built. *Flag: em-dash in "5—no excess demand!" (§9); figure/setup parentheticals removed.*

---

### X4. Counterintuitive institution (the producer trying to close itself down)
*Source: "The market for dispute resolution," 2024-12-21 — https://anupmalani.substack.com/p/the-market-for-dispute-resolution*

> [A]lthough the government is a privileged producer in this market, in a well-functioning legal system, the government producer is trying to put itself out of business. Over time, the judiciary should be trying to clarify legal rights and statutes so that later litigants can resolve conflicts privately, through settlement. Since settlement is a substitute for government resolution of litigation, this means that good judicial decisions reduce demand for judicial supply of dispute resolution.

**Anchor:** *Move: derive a counterintuitive institutional claim through a short deductive chain, built entirely from primitives taught earlier in the piece.* Here: a good court is a producer working to shrink demand for its own product. This is the bank's clearest exemplar of the move — see Deprecated below for a second (public-goods) instance folded out as duplicative. *Flag: a leading stage-direction ("Let me conclude this section … is that,") was trimmed for a cleaner exemplar; the bracketed [A] marks the trim.*

---

### X5. Concrete grounding of an abstraction + named authority
*Source: "What is supply?," 2024-12-25 — https://anupmalani.substack.com/p/what-is-supply*

> An important qualifier to this statement is that, in the long run, supply curves become more flat. If we think in terms of percentage changes, the claim is that in the long run supply is very elastic. If price rises, in time more firms enter the market and people come up with innovations to reduce costs. We can see evidence for this everywhere. In 2010, cellular data was expensive. That signalled demand for more speed. Now we all get 5G speeds on mobile data for pretty cheap. In 2010, the green transition was daunting because solar cells were expensive. The high price signalled demand, and technology drove down costs tremendously. Humans are remarkable, and one place we see it is supply elasticity. So, as Tyler Cowen says, never underestimate supply elasticity.

**Anchor:** *Move: prove an abstraction with recent, checkable history, and attribute the takeaway to a named source.* Grounds long-run supply elasticity in two datable cases (5G, solar) and cites Tyler Cowen by name — the properly-sourced counter to ai-tells §19's unnamed "experts say."

---

## Deprecated (systematic/distinct pass, 2026-07-27)

Kept verbatim for the record; out of the active bank.

### X6 (old). Derives why the market fails, from primitives — *deprecated (duplicative; same move as X4)*
*Source: "Market failures: Public goods," 2025-01-20 — https://anupmalani.substack.com/p/market-failures-public-goods*

> Why do we care whether goods are excludable or rivalrous? Producers care if goods are excludable. If they are not, then producers cannot ensure that customers pay before they consume a good. And without pay, producers have less revenue. Since profit is revenue minus costs, non-excludable goods are less profitable. This gives us our initial intuition for why non-excludable goods might not be adequately supplied.

*Why:* same technique as X4 — a short deductive chain, built on primitives taught earlier in the piece, landing a counterintuitive institutional/market claim. X4's court/dispute-resolution version is the crisper exemplar (a cleaner payoff line, and it doesn't open on the rhetorical-question tell this one does). Restore as a second exemplar if the point being made is specifically that the technique recurs across lessons, not just once.

---

## Coverage notes (curation pass, 2026-07-27)

No entry shows him narrowing an over-broad claim or conceding a limit on his own account (appellate's T6 "cabin the claim" / D3 "concede your own limits"). Flagged as a possible gap, not filled with a fabricated exemplar — if a good instance of this move exists in the source corpus, it wasn't captured in the original mining pass.

---

## Through-line of the explainer register

He **builds a concept from primitives for a beginner**: start from one atom (scarcity, incentives, excludability), add one checkable step at a time, and name the concept only after the reader has already felt it. Around that spine sit four habits: he addresses "you" and uses the reader's own life as the worked example (your 24-hour day, a $150 concert ticket); he grounds every abstraction in something concrete (a bakery's cakes, a carton of eggs, his dog Clark); he sources authority by name (Tyler Cowen, not "experts"); and he lets himself marvel at the ordinary machine ("prices are somewhat magical"). The strongest paragraphs came from **"What is demand?"** (dog Clark, the time-budget day, price ≠ value), **"What is supply?"** (the bakery → supply-curve derivation, supply elasticity), **"Market equilibrium"** ("prices are magical," the numeric walk to a clearing price), and **"A framework for studying law and economics"** (the legal-system-as-input re-anchor).
