# Consilium brand guidelines

Version 1.4, November 2026. This document records the brand as it exists on
consilium.ng today, so that new pages, reports and cards stay consistent. Where
the live site disagrees with itself, the "To resolve" section at the end says
which value to use going forward.

## 1. Who we are

Consilium is Nigeria's health systems intelligence and advisory firm. We
produce original primary research, analytical tools and decision intelligence
for governments, development partners, investors and healthcare providers.

**Positioning line:** Nigerian health systems intelligence.
**Promise:** Better healthcare decisions begin with better evidence.

**Personality:** rigorous, direct, institutional but not stiff. We sound like a
knowledgeable analyst briefing a decision-maker, not like a marketer.

## 2. Logo

- The mark is four interlocking squares forming a cross, in two tones. Files:
  `assets/consilium-logo.png` (colour) and
  `assets/consilium-logo-white.png` (for dark backgrounds). The nav and footer use these files, never live text beside the mark. The
  favicon is the mark as inline SVG.
- Use the colour logo on light backgrounds and the white logo on Blue or Ink.
- Keep clear space around the mark equal to the width of one square.
- Do not recolour, stretch, rotate, add effects, or place it on busy imagery.
- Minimum size: 24px high on screen.

## 3. Colour

| Role | Name | Hex | Use |
|---|---|---|---|
| Primary | Blue | `#3D35EB` | Hero and key surfaces, primary buttons, links, chips |
| Primary hover | Blue Deep | `#2D28C8` | Hover and pressed states |
| Text and dark surface | Ink | `#123184` | Headings, body text on light, report cover backgrounds |
| Accent | Lime | `#C8F5A0` | Key numbers and highlights on Blue or Ink only |
| Accent (cool) | Sky | `#2CB1F4` | Secondary accent, logo second tone, small highlights |
| Secondary text | Body Grey | `#4A4A63` | Paragraph text on light backgrounds |
| Page background | Mist | `#F4F4F8` | Page and section backgrounds |
| Lines | Border | `#E0E0E8` | Card borders, dividers |
| Chart context | Context | `#BDBDDB` (fills), `#7E7EA6` (lines) | The quiet series in a chart. Never the focus |
| Surface | White | `#FFFFFF` | Cards, text on Blue or Ink |

Rules:

- Blue carries the brand. Ink carries the text. Use Lime sparingly: one or two
  highlights per screen, always on a dark ground. Never use Lime as text on a
  light background.
- Text on Blue or Ink is White, or White at 72% opacity for secondary copy.
- Keep body text at least 4.5:1 contrast against its background.
- Status colours (amber for caution, red for error) are for interactive tools
  and data only, never for decoration.

## 4. Typography (v1.2)

| Role | Typeface | Notes |
|---|---|---|
| Headlines | Fraunces (700, optical size on) | Tight tracking (-0.02em), line height 1.0 to 1.1 |
| Body, interface and figures | Hanken Grotesk (300 to 600) | Body 16px, line height 1.7 |
| Quotations | Newsreader Italic | Article pull-quotes only |

Big numbers (key figures, proof strip, stat tiles) use Hanken Grotesk at weight
300, letter spacing -0.035em to -0.045em, with tabular figures. Bebas Neue and
Plus Jakarta Sans are retired. The US-Nigeria MOU explainer page still carries
its own font stack and should be moved over when next edited.

Scale in use: hero heading `clamp(38px, 5vw, 64px)`, section heading
`clamp(28px, 3.5vw, 44px)`, body 16px, labels 11px.

Eyebrow labels: Hanken Grotesk 11px, 600, uppercase, 2px letter spacing, with a
small dot before the text.

## 5. Shape, space and motion

Corner scale (v1.1). An inner corner is always smaller than the corner around it.

| Step | Radius | Use |
|---|---|---|
| Small | 8px | Chips, chart bars, small controls |
| Card | 16px | Cards and tiles inside a panel |
| Panel | 24px | Panels, featured cards, inputs |
| Pill | fully rounded | Buttons, prompts, source tags |

The live site still uses 16px cards, 6px chips and 48px pills. Move to the scale
above when the components are next touched.

- Cards: 1px Border line, White fill. Border turns Blue on hover.
- Buttons and pills: 14px semibold, 12px by 24px padding (small: 13px, 9px by 18px).
- Page content width 1140px. Sections breathe: 80 to 128px vertical padding.
- Transitions are 0.22s ease. Respect reduced-motion settings.
- On phones, tap targets are at least 44px.

## 6. Components

**Buttons.** Primary: Blue fill, White text. Secondary: transparent with Border
outline and Ink text. On Blue backgrounds: White fill with Blue text, or a White
outline. One primary button per section.

**Report and tool cards.** A 24px white card with an 8px inset. Inside it, a
16px brand-glow cover (Ink base with Blue, Sky and a hint of Lime glows; Blue Deep
base for policy briefs): year and type tags at top left, the key figure large and
light in Lime at bottom left, with one short line saying what it means. Below the
cover: the title once in Fraunces, one line of description, then metadata and
pill buttons. The title never appears on the cover. Each report supplies a key
figure and its meaning in the CMS.

**Statistics.** Large Bebas Neue numerals in Lime on Blue or Ink, with a small
uppercase label beneath.

**Data panel (v1.1).** One large 24px panel holds a question in a pill, a
one-sentence answer, a row of number tiles (16px), one chart, and source tags
at the bottom ("HCW Report 2025", "Not nationally representative"). Dark version
(Ink ground, Lime highlight) for tools and data pages. Light version (White
ground, Blue highlight) for reports and reading pages. Same structure in both.

## 7. Voice and writing

- Lead with the evidence. Say what we found, how many people, which states.
- Plain, concrete sentences. Prefer specific numbers to adjectives.
- Name the audience: governments, investors, development partners, healthcare
  providers.
- Say "Nigerian healthcare" and "health systems", not "the African market".
- Headlines are sentence case and end with a full stop when they are
  statements ("Better healthcare decisions begin with better evidence.").
- Report titles name the subject and year. State the limits of the data
  (sample, dates, "not nationally representative") next to the finding.
- Avoid hype words such as "revolutionary", "cutting-edge" and "game-changing".

## 7b. Firm first, studies second

The brand is Consilium, the firm. A report is evidence of what the firm does, not
the brand itself. Rules for every page that represents the whole firm (home page,
nav, footer, social profiles, pitch material):

- Lead with what the firm does and who it serves. No single report in the hero
  headline or as the only call to action.
- Primary calls to action are "Explore our work" and "Commission research". A
  report link is a secondary item in a list of work.
- Proof figures describe the firm (studies published or in the field, topic
  areas, reach, years publishing), not one study's sample.
- Show the range: workforce, policy, markets and commissioned studies, with the
  latest item in each.
- Each study may carry its own sub-brand (for example hcw25.consilium.ng) but
  always with a "A Consilium study" line and the Consilium mark.
- What a page features should come from the CMS (a "featured" flag), so changing
  the lead is an edit, not a code change.

## 8. Imagery and data

- Prefer our own charts, maps and figures over stock photography.
- Charts use Blue and Ink as main series colours, Lime and Sky for emphasis, on
  White or Mist. Always show the source and date.
- Social preview image: `og-image.png`, 1200 by 630.

## 9. Interaction patterns (v1.3)

- **Newsletter opt-ins** (contact form, report download gate, footer): ticking the
  box opens Substack's own confirmation page in a new tab, because browsers block
  quiet background sign-ups. The success message says a Substack tab has opened.
- **Footer and navigation** show firm-level content only: latest work and the
  three kinds of output (research, policy analysis, data tools). Never quote one
  study's figures there.

## 10. Data visualisation (v1.4)

**Colour rules for every chart**

| Role | Colour | Use |
|---|---|---|
| Focus series | Blue `#3D35EB` | The one thing the chart is about |
| Context series | `#BDBDDB` fills, `#7E7EA6` lines | Everything else |
| Second series | Sky `#2CB1F4` | Only when two series need equal weight |
| Highlight on dark | Lime `#C8F5A0` | The focus series and key numbers on Ink or glow grounds |
| Highlight on light | Lime as a marker-pen background behind Ink text | Key phrases and figures, never Lime as text |

**Story chart template.** Every published chart follows this order:

1. Topic tag and period chip.
2. A headline that states the finding, with one phrase highlighted.
3. One summary sentence.
4. The chart: direct labels (pills on line ends instead of a legend), a shaded gap
   between lines, a dashed ring on the key moment, and numbered markers (seven at
   most) with a dated note for each beneath the chart.
5. A takeaway box with the key figures highlighted.
6. A strip of four key figures.
7. A source and method line with the Consilium mark. Show the arithmetic behind
   any figure we calculate ourselves.

**Share-of-total data** uses cells: one rounded cell is a fixed amount (for
example $5 of every $100). Focus cells are Blue (Lime on dark), context cells are
grey-lilac.

## 11. Data tools: the command panel (v1.4)

A 24px Ink panel with a data-driven glow.

- Top: the question in a sentence ("Who funds the MOU in 2027?"), with any scenario
  toggle at the right.
- Year or option pills below it (the selected pill is Lime with Ink text).
- Two large light figures in frosted 16px tiles. The focus figure is Lime.
- A cell grid for the focus share, beside a line chart with the selected point marked.
- A source line.

**The glow tied to the data.** Three blurred blobs (Sky, Blue and a Lime hint) sit
behind the focus figure. Their size and brightness grow with the focus share, so
the light spreads as the story builds. The glow is decoration only: every value
is also in text, a live readout line announces changes to screen readers, and
the glow holds still under reduced-motion settings. Implemented in the MOU
explainer (`reports/us-nigeria-mou/index.html`).

## 12. Social graphics (v1.4)

Format 4:5 portrait, 1080 by 1350, for LinkedIn and Instagram. X uses the same
design cropped to 16:9. The standard layout is **number first**:

1. Topic tag chip, top left.
2. One giant light figure in Lime on the brand glow ground.
3. One caption line, 12 words or fewer, saying what the figure means.
4. A 50-cell strip beneath it as visual proof (focus cells Lime, others faint).
5. Footer: Consilium logo at left, consilium.ng at right.

One figure per post. Source and date go in the caption text of the post.
Grid-first (100 cells for "Of every $100...") is the alternative for share-of-total
stories.

## 13. Social video (v1.4)

Format 9:16 vertical, 15 seconds, silent-first with burned-in captions. It
combines the number reveal and the cell fill, so the number counts up while the
grid fills.

| Time | Frame |
|---|---|
| 0 to 2s | The question types in on Ink |
| 2 to 5s | First year appears, the figure counts up, the first cells light |
| 5 to 8s | Cells keep filling, a year chip steps forward |
| 8 to 11s | Fill continues to the last year |
| 11 to 15s | The final figure lands, the glow blooms, logo and consilium.ng |

One figure and one grid per video. Use the same Lime-on-glow treatment as the
social graphic.

## 14. Headline typeface

Headlines stay in Fraunces. Instrument Serif and Bricolage Grotesque were tried
as alternatives for data pages and are not adopted. Revisit only with a full
page mockup in hand.

## Decisions (November 2026)

These were open inconsistencies on the live site. Each is now settled.

1. **Spelling:** British. The home page copy now reads "organisations". Proper
   names keep their own spelling, for example "Center for Global Development".
2. **Secondary text grey:** `#4A4A63` everywhere. The MOU explainer was changed
   to match.
3. **Darks:** Ink `#123184` is the only dark, for text and surfaces. Night
   `#0D0D2B` is retired. Charts separate their two series with Blue (focus) and
   Context grey-lilac instead (see section 10). The MOU explainer was updated.
4. **Amber `#F5A623` and red `#C0392B`:** status colours for tools and data only.
5. **Newsreader Italic:** kept, for pull-quotes. Article block quotes already
   use it.
6. **Footer year:** now generated at build time (`buildYear` in
   `eleventy.config.js`).
