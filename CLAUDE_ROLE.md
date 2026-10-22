# Who did what: the human and Claude

This project extended OEIS [A072503](https://oeis.org/A072503) (shoe lacings
with no horizontal connection) from a(9) to a(400). It was carried out in one
session of **Claude Code on the web** (Anthropic's coding agent, running in a
cloud sandbox), started from the Claude mobile app. This page describes, as
precisely as possible, which parts were done by the human and which by Claude
and its subagents. Every claim here can be checked against the files and the
commit history.

## The human (repository owner)

* **Posed the problem.** Chose the sequence and made a(10) the main target.
* **Supplied the data.** oeis.org was not reachable from the sandbox, so the
  task statement included the OEIS name, the known terms a(3..9), Pfoertner's
  numbering, Sean A. Irvine's 2024 clarifications of the rules, the n = 3
  example and the related sequences.
* **Designed the verification protocol.** The task statement fixed the rules
  of the work in advance:
  1. first check (via a sparse checkout of github.com/oeis/oeisdata) that
     nobody had published a(10) yet;
  2. reconstruct the definition with a brute force that must reproduce the
     six n = 3 lacings and the known terms;
  3. build at least two independent fast exact methods, written by different
     agents that do not see each other's code, each of which must reproduce
     all 7 known terms;
  4. only then compute new terms, in C/C++ or with exact integers, in chunks
     of at most 25 minutes with checkpoints and progress logs;
  5. accept a new term only if both independent methods agree, and have a
     separate reviewer agent try to find errors;
  6. mark clearly what is proved and what is only checked.
* **Delegated all decisions.** The human did not watch the run and asked Claude
  to resolve ambiguities itself and log every decision (`a072503/DECISIONS.md`).
* **Reviewed and merged** the result into the repository. The OEIS submission is
  to be made by the human, under their own name, after studying the
  explanation (`a072503/explanation.md`). In line with the OEIS guideline on
  AI use, the human writes the text of the OEIS edit (comments, formula,
  messages to the editors) in their own words. Claude's drafts in
  `a072503/oeis_draft.txt` are only reference material. Nothing was sent to
  OEIS by Claude.

## Claude

Claude worked as a **coordinator** (the main session) that wrote the
reference code itself and ran three **subagents**, plus translation agents
for this English version.

### Coordinator (main session)

* Checked oeisdata: the A072503 file at commit `f72d165` (2026-10-20) ends at
  a(9) and is still marked `more`.
* Read Irvine's Java program (jOEIS) to see which reading of the rules
  produced a(9).
* Tested three readings of "three consecutive eyelets on the same side" by
  literal enumeration of all orderings (`a072503/brute/interpretations.py`).
  Only one gives the known a(4) = 45 and a(5) = 1824. As a check of the model,
  another reading reproduces the sister sequence A078602 (checked for n = 3..5).
* Wrote the literal enumerator `brute/brute_dfs.c` (C/OpenMP; reproduces
  a(3..8); n = 8 is 2.3·10^9 lacings in about 59 s) and the exact subset DP
  `brute/subset_dp.c` (no symmetry used; 128-bit integers, or two moduli plus
  CRT). The subset DP produced a(10)…a(13) as a reference **before** the fast
  methods were finished. These values were deliberately not given to the
  method agents.
* Wrote the formal definition `DEFINITION.md` (including the proof that no
  lacing is its own mirror image) and the briefs for the method agents: one
  method family each, following the human's suggestion, with strict isolation
  rules (each agent may read only `DEFINITION.md` and its own folder).
* Compared the results (`compare.py` → `accepted_terms.txt`). Then it wrote the
  b-file, the short Python program for OEIS, the README, the Russian
  explanation, the OEIS draft, an empirical recurrence search
  (`recurrence/`, labelled conjectural) and the documentation fixes after the
  review.

### Subagent "method 1" (`a072503/method_dp/`)

* Derived a dynamic program over **counts of row statuses**: rows untouched,
  only left eyelet used, only right eyelet used, plus a few bits of local
  state. About n³ states instead of (2n−2)! orderings.
* Proved the "lumping" lemma that makes the counts exact. Reproduced a(3..9)
  and computed n = 3..400 with exact integers (4 minutes).

### Subagent "method 2" (`a072503/method_ie/`)

* Derived an **inclusion–exclusion formula over side patterns**:
  `2a(n) = (n−1)! Σ_k (−1)^k (n−1−k)! N(n,k)`. It also derived an explicit
  6-fold binomial sum and a fast DP for N(n,k).
* Reproduced a(3..9) and computed n = 3..500 (under 1 minute).
* Both method agents were instructed to read only `DEFINITION.md` and their
  own folder, and were not given the coordinator's numbers. This cannot be
  checked from the files; the reviewer found no sign of copying. Their
  results agree for **every n = 3..400**.

### Subagent "reviewer" (`a072503/review/`)

* Was asked to try to break the definition, the code and the results.
* Re-ran everything from scratch: both result files were rebuilt
  byte-identically.
* Tested eight further variants of the rules (`a072503/review/alt_readings.py`):
  seven do not fit the known terms, and one (starting at either top eyelet)
  gives exactly four times the same count. It also re-ran reading B (no fit)
  and showed that a cyclic version of the side rule is equivalent to the
  chosen reading. Found that the chosen reading without the horizontal ban
  gives Pfoertner's sister sequence A078698.
* Wrote its own checks:
  * a literal enumeration of "canonical" lacings that gives a(3..11) directly;
  * a third fast method that agrees up to n = 500;
  * a test of method 1's key lemma on 882 321 real prefixes;
  * a per-side-word test of method 2 up to n = 9.
* Found **no error** in the definition, code or numbers. Its remarks
  concerned the strength of some checks and the documentation; each was
  either fixed or documented (`DECISIONS.md`, D5).

### Translation agents (English version)

The Russian documents were translated by subagents. A separate checker agent
compared them with the originals: numbers, commands, file names and claims.
The Russian originals are kept as `a072503/README_ru.md`,
`a072503/explanation_ru.md` and `a072503/oeis_draft_ru.txt`.

## Later additions (2026-10-21/22)

After the run, the work continued in the same session, through pull
requests #2–#5 and a final audit.

* **Claude:**
  * the English translation of the documents and its check by a separate
    agent (see above), and this page, `CLAUDE_ROLE.md` (PR #2);
  * the header of `a072503/oeis_draft.txt` on the OEIS rules on AI and the
    program walkthrough in `a072503/explanation.md`, section 5.5 (first
    version on 2026-10-20 at 22:35 UTC, together with the b-file trim to
    n = 3..233; see `a072503/DECISIONS.md`, D6), and a step-by-step guide to
    submitting the edit, written for the human (not in the repository);
  * the figure `assets/lacing_n3.svg`, the social preview image
    `assets/social_preview.*`, the script `assets/make_figures.py` that
    generates them, `LICENSE`, `LICENSING-docs.md` and `CITATION.cff` (PR #3);
  * the Zenodo-compatible fix of `CITATION.cff` (PR #4);
  * the DOI badge and the "How to cite" section of `README.md` (PR #5);
  * a general audit of the repository (2026-10-22): six auditor agents and
    six verifier agents; of 54 findings, 45 were confirmed, none of them an
    error in a computed term. The fixes are listed in `a072503/DECISIONS.md`,
    D6.
* **The human** (on GitHub and Zenodo; this is not visible in the files):
  set the repository's About text and topics, enabled archiving on Zenodo
  and created the GitHub releases v1.0.1 and v1.0.2 (all versions:
  [doi:10.5281/zenodo.23553325](https://doi.org/10.5281/zenodo.23553325)),
  and reviewed and merged the pull requests.

## Timeline (2026-10-20, UTC)

| time | step |
|---|---|
| 18:56 | task received |
| 18:58 | oeisdata checked: a(10) not yet published |
| 19:00 | rules reading fixed (only one of three readings fits a(4), a(5)) |
| 19:02 | brute force reproduces a(3..8) |
| 19:03 | method agents 1 and 2 started in parallel |
| 19:06 | subset DP gives reference values a(3..13) |
| 19:22 | method 1 finished (n ≤ 400) |
| 19:31 | method 2 finished (n ≤ 500); both agree for n = 3..400 |
| 19:33 | reviewer started |
| 19:48 | README, explanation, OEIS draft, b-file written |
| 20:10 | review finished (no errors found) |
| 20:15 | documentation fixes committed |

About 1 h 20 min from the task to the reviewed result. The machine time for
the new terms themselves is a few minutes.

## What is and is not claimed

* **New:** a(10) = 36441019601280 and the terms up to a(400), established by
  two independent exact methods. The earlier terms came from exhaustive
  search (Pfoertner's FORTRAN program; Irvine's DFS for a(9), about 3.6·10^11
  lacings). The new methods are polynomial-time: all terms up to n = 500 take
  under a minute.
* **Techniques:** these are standard combinatorial tools (symmetry reduction,
  dynamic programming, inclusion–exclusion), applied to this problem. No deep
  new mathematics is claimed.
* **Proved** (proofs written by the agents and checked by the reviewer agent,
  not yet by an independent human expert):
  * the inclusion–exclusion formula;
  * the exactness of method 1;
  * no lacing is its own mirror image;
  * 2a(n) is divisible by (n−1)!.
* **Not proved:** the order-18 recurrence in `recurrence/` (empirical only).
* **A choice, not a theorem:** the reading of the OEIS rules. It is the
  only one of the readings tested that reproduces all known terms, and it is
  the reading implemented in Irvine's program.
* **Not checked:** Pfoertner's original FORTRAN program could not be
  downloaded (the host did not resolve). Its published values a(3..8) are
  reproduced.
