# Style Guide

**The single source of truth for colors, typography, and tokens.** Every diagram draws from this — not from hex values inlined in other reference files. If you want to change the visual skin of Diagram Design, change this file.

Default skin follows turbopuffer.com: near-white slate paper, deep navy ink, slate muted tones, one orange accent, JetBrains Mono for every text role, and square corners everywhere. Nodes take the orange fill on hover. Swap the color values (or run [`onboarding.md`](onboarding.md)) and every new diagram inherits the new colors; the font, the square corners, and the hover stay.

To generate your own from a website URL, see [`onboarding.md`](onboarding.md).

---

## Tokens

### Semantic roles

Every token is referred to by **semantic role**, not by its hex value. Type references (`type-*.md`) and SKILL.md say `accent`, not `#f7591f`.

| Role | Purpose | Default (light) | Default (dark) |
|---|---|---|---|
| `paper` | Page background, default node fill | `#f8fafc` (slate-50) | `#0f172a` (navy) |
| `paper-2` | Diagram container bg, secondary fill | `#f1f5f9` | `#1e293b` |
| `ink` | Primary text, primary stroke | `#0f172a` (navy) | `#f8fafc` (slate-50) |
| `ink-strong` | High-contrast text on warm accent fills | `#111111` | `#111111` |
| `muted` | Secondary text, default arrow stroke | `#475569` (slate-600) | `#cbd5e1` (slate-300) |
| `soft` | Sublabels, boundary labels | `#64748b` | `#94a3b8` |
| `rule` | Hairline borders | `rgba(15,23,42,0.12)` | `rgba(248,250,252,0.12)` |
| `rule-solid` | Stronger borders, baselines | `#cbd5e1` | `rgba(203,213,225,0.25)` |
| `accent` | Focal / 1–2 max per diagram | `#c2410c` (orange-700) | `#fdba75` (turbopuffer orange) |
| `accent-tint` | Fill for accent-bordered boxes | `rgba(194,65,12,0.08)` | `rgba(253,186,117,0.10)` |
| `link` | HTTP/API calls, external arrows | `#1d4ed8` | `#93c5fd` |
| `hover-fill` | Node box fill while hovered | `#fdba75` | `rgba(253,186,117,0.22)` |
| `hover-stroke` | Node box stroke while hovered | `#0f172a` | `#fdba75` |
| `hover-ink` | Node text while hovered | `#431307` | `#f8fafc` |

> **Palette source:** turbopuffer.com's CSS tokens: background `hsl(220 33% 98%)`, foreground `hsl(222 47% 11%)`, border `hsl(214 26% 84%)`, muted foreground `hsl(215 16% 47%)`, and the brand orange `hsl(30 97% 73%)` = `#fdba75`. Raw `#fdba75` reads 1.6:1 on `paper`, too faint for a stroke or a label, so the light `accent` is `#c2410c` from the same hue family and the brand orange is kept for fills: the hover fill and the dark-skin accent.

> **Note:** The example HTML files in `assets/` were converted from the upstream skin by a script: colors, fonts, and corners are this skin's, but layouts were sized for the upstream fonts. Treat them as layout references.

### Contrast contract

Every token must clear the threshold for each role it plays, against the background it actually sits on, in both skins. `scripts/verify-contrast.py` computes the WCAG 2.x ratio for every row above against the `paper` of its skin (`ink-strong` against the 0.85 `accent` fill it labels) and fails CI when one falls short.

| Use | Minimum vs. its actual background |
|---|---|
| Regular text, including any `soft`, `link`, or `accent` used as text | 4.5:1 |
| Large text (24px+, or 18.7px+ at weight 600+) | 3:1 |
| Essential non-text marks: lines, arrows, borders, focus outlines, data points | 3:1 against the adjacent color |
| Decorative rules and translucent tints (`rule`, `rule-solid`, `paper-2`, `accent-tint`, fills at opacity) | No minimum, but never the only carrier of meaning |

- **A token used in several roles must pass each one.** `accent` is a stroke in one place and a label in another, so it is held to 4.5:1, not the 3:1 its strokes alone would need. Don't assume a token is non-text because it usually is.
- **Translucent colors are composited first.** An `rgba()` fill or stroke is blended over `paper` before its ratio is measured. A value that clears the bar at full strength can fail at 0.5 opacity.
- **Surfaces other than `paper` cost contrast.** Inside an `accent-tint` box or on `paper-2` every ratio drops. Measure text placed there against that surface, not against `paper`.
- **Current defaults:** light `accent` 4.95:1, `soft` 4.55:1, `link` 6.41:1, `muted` 7.24:1 on `#f8fafc`; dark `accent` 10.59:1, `soft` 6.96:1, `link` 9.90:1 on `#0f172a`. Hover text `#431307` on `#fdba75` is 9.33:1.

### Inversion rule (light → dark)

Any `rgba(15,23,42, X)` in light becomes `rgba(248,250,252, X)` in dark. Same opacities, RGB flipped. The accent gets a slight hue-shift brighter to read on dark paper.

### Series palette (multi-series chart types only)

A small set of desaturated, editorial-tone colors for chart types that genuinely need to distinguish multiple overlapping entities (currently: **radar**). The "1-focal" rule still holds — `accent` is reserved for the focal series; the palette below covers the rest.

| Token | Light | Dark | Notes |
|---|---|---|---|
| `series-1` | `#7c8f6f` (sage) | `#9caf8f` | Non-focal series |
| `series-2` | `#5e7a9b` (dusty-blue) | `#82a0c0` | Non-focal series |
| `series-3` | `#b8915a` (mustard) | `#d3ad7a` | Non-focal series |
| `series-4` | `#9c6b50` (rust-brown) | `#b88670` | Non-focal series |
| `series-5` | `#6e6479` (slate) | `#8d8298` | Non-focal series |

Fills sit at `0.18` opacity light, `0.22` dark; strokes use the full color. **Don't backfill these tokens to non-chart types** — architecture, swimlane, etc. continue to use muted-ink variants. The series palette is opt-in for diagrams where overlapping shapes demand distinguishable color, not a license to add color elsewhere.

### Terminal skin (opt-in alternate)

A self-contained palette for the terminal-window primitive (see [primitive-terminal.md](primitive-terminal.md)) — a CLI-chrome register for dev-tool posts and technical social cards. It does not replace the default skin above and isn't affected by onboarding; it's a second, fixed skin you opt into per-diagram.

| Token | Hex | Purpose |
|---|---|---|
| `terminal-page` | `#0a0a0a` | Page background behind the window |
| `terminal-paper` | `#141414` | Window body, node fill |
| `terminal-bar` | `#1b1b1b` | Titlebar strip |
| `terminal-border` | `#2b2b2b` | Window border, hairlines |
| `terminal-ink` | `#f8fafc` | Primary text, primary stroke (same white-smoke as default `ink`) |
| `terminal-muted` | `#9a9a9a` | Secondary text, sublabels, ring stroke |
| `terminal-soft` | `#5c5c5c` | Tertiary — inactive dots, spokes |
| `terminal-accent` | `#ff5a36` | The one accent — focal station, prompt sign, active dot |
| `terminal-accent-tint` | `rgba(255,90,54,0.12)` | Fill for accent-bordered boxes |

**1-accent rule still holds.** Everything that isn't `terminal-ink` or `terminal-muted`/`terminal-soft` should be `terminal-accent` — never introduce a second hue.

---

## Typography

| Role | Family | Size | Weight | Usage |
|---|---|---|---|---|
| `title` | JetBrains Mono | 1.75rem | 600, tracked -0.02em | Page H1 |
| `node-name` | JetBrains Mono | 12px | 600 | Human-readable labels |
| `sublabel` | JetBrains Mono | 9px | 400 | Port, protocol, URL, field type |
| `eyebrow` | JetBrains Mono | 7–8px | 500, tracked 0.18em, uppercase | Type tags, axis labels |
| `arrow-label` | JetBrains Mono | 8px | 400, tracked 0.06em | Arrow annotations |
| `callout` | JetBrains Mono *italic* | 13px | 400 | Editorial asides only |

Every role resolves to the same stack:

```css
font-family: 'JetBrains Mono', 'Noto Sans KR', 'Noto Sans TC', ui-monospace, monospace;
```

### Font stack

```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Noto+Sans+KR:wght@400;500;600&family=Noto+Sans+TC:wght@400;500;600&display=swap" rel="stylesheet">
```

### Font source

The font source decides whether a diagram makes any network request. It is a skin setting, so a saved profile carries it too.

Font source: `web`

| Value | What ships | Network |
|---|---|---|
| `web` (default) | The Google Fonts `<link>` above; text renders in JetBrains Mono | One stylesheet request to `fonts.googleapis.com`, plus the font files |
| `system` | No font `<link>`; every family stack falls through to the platform's own serif, sans, and monospace faces | None |

Use `system` when the user asks for offline output, system fonts, or no Google Fonts, or when this line says `system`. In `system` mode:

- Omit the font `<link>` (and the export `@import`) entirely. Keep every `font-family` stack as written: each one already ends in `ui-monospace, monospace`, so a viewer who has JetBrains Mono installed still gets it and everyone else gets their system face.
- Fallback mono faces differ slightly from JetBrains Mono, so keep the 8px label padding intact rather than trimming boxes to the JetBrains Mono measurement.
- Export with `python3 scripts/export_svg.py <file> --system-fonts`, and verify with `python3 scripts/self_check.py --offline <file>`, which fails if the Google Fonts link is still present.

The render linter's default run (`lint-render.py` with network blocked) measures exactly this fallback rendering, so every shipped template and example is already checked in system-font mode.

To keep the face with no network at all, install JetBrains Mono locally (SIL Open Font License) and use `system`: the stacks resolve to the installed faces first.

### Korean labels

JetBrains Mono carries no Hangul. A Korean `<text>` element extends its own family — never swap the skin:

```svg
<text font-family="'JetBrains Mono', 'Noto Sans KR', 'Apple SD Gothic Neo', 'Malgun Gothic', ui-monospace, monospace">결제 서비스</text>
```

Both Noto faces ship in the font link above, so the web font resolves before any locally installed one and the same file renders identically on macOS, Windows, and a reviewer's browser. The local families follow it for offline viewing. Page titles use the same stack. Google's `css2` endpoint slices Korean by unicode-range, so a diagram with a handful of Korean labels downloads only the slices it touches. The four templates carry both faces because a new diagram may contain Hangul; the shipped Latin-only examples keep the shorter link, since a file with no Hangul has nothing to resolve.

**Width budget.** Measure per character, not per script: **every Unicode wide or full-width character costs 1em, every other character costs its face's Latin advance** (0.60em for JetBrains Mono), and nonspacing/enclosing marks cost nothing. Sum over the string and multiply by the font size for the text width, then add padding and round the box up to the next multiple of 4. `verify-treemap.py` enforces exactly this text width for treemap cell labels; the padding and rounding are authoring convention, and no other type carries an automatic check, so on those the budget is yours to hold.

Counting by script is the trap. `주문 v2.1` is two full-width syllables and five narrow characters; a formula that tallies Hangul, Latin letters, and spaces silently drops `2`, `.`, and `1` and sizes the box for four of its seven characters. Every rendered character costs something — measure per character, never per script.

Three rules follow from Hangul metrics:

- **Sublabels stay Latin.** Ports, protocols, field types, and URLs are Latin anyway — keep `JetBrains Mono` there and don't translate them. Hangul in a 9px mono sublabel is unreadable and has no mono face to fall back to.
- **Floor of 12px.** Hangul goes muddy below 12px. If a Korean name doesn't fit at 12px, cut the name — don't shrink the type.
- **Arrow labels, eyebrows, and legend text switch register.** Those slots are 7–8px JetBrains Mono, uppercase and tracked, which Hangul has neither a face nor legibility for. A Korean label in one of those slots becomes 12px sans at weight 500 with no tracking and no uppercase transform, and its mask rect grows to match (16px tall, width from the budget above, still rounded to a multiple of 4). Latin labels in the same diagram keep the mono treatment.

**Load-bearing rule:** JetBrains Mono for every role. Hierarchy comes from size, weight, case, and tracking. Italic JetBrains Mono is reserved for annotation callouts (see [primitive-annotation.md](primitive-annotation.md)). Never add a second family.

### Traditional Chinese labels

JetBrains Mono carries no Han. A Traditional Chinese `<text>` element extends its own family — never swap the skin:

```svg
<text font-family="'JetBrains Mono', 'Noto Sans TC', 'PingFang TC', 'Microsoft JhengHei', ui-monospace, monospace">請求項比對</text>
```

Both Noto TC faces ship in the font link above, so the web font resolves before any locally installed one and the same file renders identically on macOS, Windows, and a reviewer's browser. The local families follow it for offline viewing. Page titles use the same stack. Google's `css2` endpoint slices Chinese by unicode-range, so a diagram with a handful of Chinese labels downloads only the slices it touches.

**Width budget.** The per-character contract above is unchanged: every Unicode wide or full-width character costs 1em, every other character costs its face's Latin advance, and nonspacing marks cost nothing. Full-width punctuation — `（）「」，。：` — is wide and costs 1em as well, which is the part most often dropped.

Counting by script is the trap. `請求項 v2.1` is three full-width characters and five narrow ones; a formula that tallies Han and Latin letters silently drops `2`, `.`, and `1` and sizes the box for six of its nine characters.

Three rules follow from Han metrics, mirroring the Hangul ones:

- **Sublabels stay Latin.** Ports, protocols, field types, and URLs are Latin anyway — keep `JetBrains Mono` there and don't translate them. Han in a 9px mono sublabel is unreadable and has no mono face to fall back to. A sublabel that is prose rather than a value may be Chinese, but it then switches register by the third rule below.
- **Floor of 12px.** Han packs more strokes than Hangul into the same em box, so the 12px floor binds at least as hard here. If a Chinese name doesn't fit at 12px, cut the name — don't shrink the type.
- **Arrow labels, eyebrows, and legend text switch register.** Those slots are 7–8px JetBrains Mono, uppercase and tracked, which Han has neither a face nor legibility for. A Chinese label in one of those slots becomes 12px sans at weight 500 with no tracking and no uppercase transform, and its mask rect grows to match (16px tall, width from the budget above, still rounded to a multiple of 4). Latin labels in the same diagram keep the mono treatment.

Simplified Chinese takes the same three rules with the Simplified stack (`'Noto Sans SC'`, `'PingFang SC'`, `'Microsoft YaHei'`). That face does not ship in the link, so Simplified labels still resolve through whatever the viewer has locally.

### Cyrillic labels

JetBrains Mono ships Cyrillic (`cyrillic` and `cyrillic-ext` on Google Fonts), so names, sublabels, arrow labels, eyebrows, legend text, and titles in Bulgarian, Russian, Ukrainian, or Serbian keep the Latin treatment: same face, sizes, tracking, and uppercase. There is no register switch and no fallback face.

**Width budget.** Every character costs the mono advance (0.60em for JetBrains Mono): a Cyrillic glyph advances exactly as far as a Latin one, so every label and mask rect is sized as for Latin.

Counting by script is still the trap. `Шкаф ODF-2` is four Cyrillic letters, a space, three Latin letters, a hyphen, and a digit; a formula that tallies Cyrillic letters, Latin letters, and spaces silently drops `-` and `2` and sizes the box for eight of its ten characters.

**Preserve printed labels.** A label the reader matches against a physical thing — a cabinet, a splice closure, a port map — carries the exact printed string. Don't transliterate it and don't re-case it; if one has to sit in an uppercase slot such as an eyebrow, drop the transform for that label rather than re-case the printed string. `Шкаф ODF-2` stays `Шкаф ODF-2`, not `Shkaf ODF-2`.

---

## Stroke, radius, spacing

| Token | Value | Use |
|---|---|---|
| `stroke-thin` | `0.8` | Tag-box outlines, leaf nodes |
| `stroke-default` | `1` | Most strokes |
| `stroke-strong` | `1.2` | Emphasis strokes |
| `radius` | `0` | Every rect and CSS box: nodes, tags, chips, containers, cards. No `rx`, no `ry` |
| `elbow` | `8` | Connector bends only (`r=6` in tight layouts). Connectors stay rounded |
| `grid` | `4` | Every coord, size, and gap is divisible by 4 (hard rule) |

---

## Node type → treatment

Semantic role combinations — reference these by name in type specs.

| Type | Fill | Stroke |
|---|---|---|
| `focal` (1–2 max) | `accent-tint` | `accent` |
| `backend` | `#ffffff` (white) | `ink` |
| `store` | `ink @ 0.05` | `muted` |
| `external` | `ink @ 0.03` | `ink @ 0.30` |
| `input` | `muted @ 0.10` | `soft` |
| `optional` | `ink @ 0.02` | `ink @ 0.20` dashed `4,3` |
| `security` | `accent @ 0.05` | `accent @ 0.50` dashed `4,4` |

---

## Customizing the skin

Four options:

1. **Run onboarding** — see [`onboarding.md`](onboarding.md). Drop a URL; the skill extracts the palette + fonts and rewrites this file.
2. **Edit by hand** — change the hex values in the tables above. Run the pre-output taste gate afterward to verify the accent still reads as "focal" against the new paper color.
3. **Brand handoff** — paste your existing design-token JSON into a new section here and map its tokens to the semantic roles above.
4. **Client profiles** — save and switch named skins, or bind one to a project, using [`profiles.md`](profiles.md).

### Constraints (don't break these)

- **Contrast**: every text token (`ink`, `muted`, `soft`, `link`, and `accent`) must clear 4.5:1 on `paper`, in both skins. See the [contrast contract](#contrast-contract); `scripts/verify-contrast.py` checks it.
- **One accent**: pick one color for `accent`. Two accents erases the focal signal.
- **No rainbow palette**: if your brand ships 8 colors, pick 3 (paper, ink, accent). The rest become `muted` variants.
- **One family**: JetBrains Mono for every role, whatever the brand ships. Brand fonts are not imported.
- **Square corners**: brand radius tokens are ignored; every box stays square.
- **Paper is cool-neutral, not pure white**: `#f8fafc` keeps a hint of slate so white `backend` nodes still separate from the page.
- **Dot pattern is optional, not default**: the 22×22 dot pattern is an opt-in "dotted paper" variant (good for long-form editorial hero diagrams). The default background is a clean `paper` fill, no pattern. When the pattern is enabled, it should sit at ~10% opacity of `ink` on `paper` — visible but quiet.
- **Container is clean by default**: the diagram sits directly on the page paper, no secondary container background or border. A framed variant (`paper-2` bg + `rule` border + square corners + padding) is available as an opt-in for card-heavy layouts, but don't reach for it by default — the extra chrome fights the figure.
