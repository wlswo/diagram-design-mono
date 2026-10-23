# Writing for the reader

Routed from SKILL.md §5. A diagram is read by someone who did not write the system: a new teammate, a reviewer, a manager, a blog reader. Every word on the page is for them. SKILL.md keeps the five rules in one line each; this file holds the long form and examples.

## 1. No separator dots

Never join two facts with a dot. The ban covers `·` (U+00B7), `•` (U+2022), `・` (U+30FB), `∙` (U+2219), and the entities `&middot;` / `&#183;`, in every visible text role: page title, eyebrow, subtitle, captions, zone labels, node names, sublabels, type tags, arrow labels, legend, cards, and footer.

A dot-joined label is usually two labels pretending to be one. Fix it in this order:

1. **Delete the weaker fact.** Most second halves are noise (`MASTER · COORDINATORSERVICE` → `MASTER`).
2. **Split into two lines.** A node has room for a second sublabel line 13px below the first.
3. **Use a comma** for a list of peers (`HDFS, S3, Local`).
4. **Use ` / `** for alternatives or a path (`Doris / Iceberg`, `ingest / transform`).

| Instead of | Write |
|---|---|
| `HDFS · S3 · LocalFile` | `HDFS, S3, LocalFile` |
| `JobMaster · 1 per job` | line 1 `JobMaster`, line 2 `one per job` |
| `MASTER · COORDINATORSERVICE` | `MASTER` |
| `01 · 클러스터` | `01 클러스터` |
| `Architecture · 2026-10-23` | eyebrow `Architecture`, date in the footer |
| `ACK · STATE` | `SEND STATE` |

`scripts/self_check.py` fails any file whose visible text contains one of these characters. Math in HTML comments (`r = 1.4·√v`) is not visible text and is allowed.

## 2. Plain words

Name things by **what they do for the reader**, not by what the code calls them.

| Code-speak | Plain |
|---|---|
| `JobMaster` | `작업 관리자` / `Job manager` |
| `CoordinatorService` | `작업 접수` / `Job intake` |
| `ResourceManager` | `자원 배분` / `Resource allocator` |
| `SourceSplitEnumerator` | `읽을 범위 나누기` / `Work splitter` |
| `SinkAggregatedCommitter` | `최종 확정` / `Final commit` |
| arrow `APPLY SLOTS` | `자원 요청` / `REQUEST SLOTS` |
| arrow `prepareCommit` | `확정 준비` / `READY TO COMMIT` |

Rules:

- **Node name = role in everyday words.** If the reader will search for the real identifier (a class to open in the IDE, a product to install), put it in the sublabel.
- **Product and technology names stay as they are** (`Kafka`, `MySQL`, `Kubernetes`). They are what the reader searches for, and they usually get an icon ([primitive-techicon.md](primitive-techicon.md)).
- **No unexplained abbreviations.** `RM`, `CP`, `XFRM`, `WRTE`, `ENUM` are fails. Spell it out, replace it with a word, or replace the type tag with an icon. Widely known ones (`API`, `DB`, `SQL`, `HTTP`) are fine.
- **Arrow labels are verb + object** in everyday words: `SEND JOB`, `SAVE STATE`, `작업 보내기`, `상태 저장`. Never an RPC, method, or event-class name.
- **Captions and cards use short sentences**, one idea each. Say *why* something happens, not only *what*. Define an unavoidable term in parentheses the first time it appears: `체크포인트(중간 저장 지점)`.

### Korean

- Prefer a natural Korean word over a transliterated one when a common word exists: `잡` → `작업`, `코디네이터` → `조정자` or `관리자`, `스플릿` → `조각`, `배리어` → `체크포인트 신호`, `커밋` → `확정`. When the reader needs the original term to search for it, give it once in parentheses: `확정(커밋)`.
- Keep product names in their own spelling (`Kafka`, not `카프카`).
- A Korean explanation that does not fit a node name belongs in the caption or a card. Hangul in a 9px sublabel is unreadable ([style-guide.md § Korean labels](style-guide.md#korean-labels)), and Korean arrow labels switch to the 12px register described there.

## 3. Audience dial

| Audience | Code identifiers | Technical terms | Abbreviations |
|---|---|---|---|
| `executive` | none | replaced with outcomes | none |
| `mixed` (default) | sublabels only, when searchable | defined once in prose | common ones only |
| `engineer` | sublabels | allowed | common ones only, others spelled out |

The separator-dot ban and the abbreviation rule hold for every audience.

## 4. The read-aloud test

Before output, read every label aloud as if explaining the diagram to a new teammate. Any label you would have to expand, translate, or apologise for gets rewritten.
