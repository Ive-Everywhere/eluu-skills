# Deck profiles

Pick exactly one *primary* profile before designing. The profile decides which
proof objects are mandatory and which failure modes are disqualifying — it sits
above any visual score. Add secondary profiles as extra constraints in the claim
spine when more than one applies; when several apply, make the
highest-delivery-risk one primary.

## finance-ir
Earnings, investor, board, operating-review, and financial-analysis decks.
- **Mandatory:** a KPI summary with units and source period; a revenue/mix table
  or bridge; a margin or cash profile; the relevant customer/backlog/outlook
  proof.
- **Rules:** use only reported figures or clearly-labelled calculations from
  them; keep units, fiscal periods, and GAAP/non-GAAP labels visible; build a
  source ledger before charts; prefer table-first and bridge-first slides over
  decorative KPI grids; bridges must reconcile visually and numerically;
  combination charts must make scale logic explicit and keep continuous series
  geometry after render; include a disclosure/source appendix.
- **Fails on:** a pretty chart with unsupported values; a generic "growth is
  strong" title; multiple metrics on one axis for no reason; dual-encoding that
  implies a relationship the figures don't support; missing footnotes on dense
  tables.

## product-platform
SaaS, product, platform, security, workflow, and ecosystem decks.
- **Mandatory:** a platform map or workflow architecture; a use-case or
  customer-journey visual; an adoption/expansion proof; a product-to-financial
  linkage slide; a roadmap when asked.
- **Rules:** show the system, not a feature list; tie each capability to
  adoption, expansion, monetization, efficiency, or customer quality; keep a
  small set of recurring diagram primitives so the deck feels authored; every
  connector/lane/box has explicit semantics.
- **Fails on:** repeated feature-card grids; vague boxes ("AI", "Data",
  "Platform"); product slides disconnected from business outcomes; flow arrows
  that float, cross unrelated objects, or imply an unsupported sequence; boxes
  aligned decoratively that encode no real system.

## gtm-growth
GTM, marketing, consumer growth, subscription ecosystem, mobility, engagement,
and commercialization decks.
- **Mandatory:** a visible growth loop or funnel progression; a segment or
  cohort proof; a monetization bridge; an engagement or retention trend.
- **Rules:** connect reach → activation → engagement → monetization → margin or
  retention; preserve recognizable brand cues without letting brand colour
  overpower data; use verified or user-provided identity assets only — otherwise
  express brand through colour, type, layout, product language, and sourced
  metrics.
- **Fails on:** funnel labels with no movement between stages; brand parody
  instead of business storytelling; unofficial logos/mascots/app-icons used as
  decoration; marketing claims without quantified proof.

## engineering-platform
Developer, AI, infrastructure, data, security, and technical-platform decks.
- **Mandatory:** accurate system diagrams; technical labels that survive
  executive simplification; metrics tied to the architecture.
- **Fails on:** technically vague diagrams; labels stripped of real meaning;
  developer detail that overwhelms the executive story.

## strategy-leadership
Investor-day, board, transformation, and market-strategy decks.
- **Mandatory:** chapter discipline; market framing; explicit strategic bets;
  transition slides that carry the thesis.
- **Fails on:** chapter dividers without thesis movement; a market frame that
  never returns in the operating plan.

## consumer-retail
Lookbooks, clienteling, luxury, consumer-brand, campaign, travel, lifestyle,
food, fashion, beauty, people/places, sports, and playful image-led
storytelling — anywhere the audience must visually inspect the subject.
- **Mandatory:** real assets or explicit asset provenance; image quality;
  editorial hierarchy; client-ready copy.
- **Fails on:** stock-looking imagery; weak crop quality; unverified provenance;
  generic client-outreach copy.

## appendix-heavy
Dense appendices, tables, disclosures, and source packs.
- **Mandatory:** an index / page markers; readable small-type thresholds;
  consistent table grammar; explicit source-density rules.
- **Fails on:** unreadable tables; a missing index; source density that hides
  the answer.

## template-following
A supplied template/source `.pptx` (or existing Slides deck) is the canonical,
editable starting point — clone/edit only. See `template-following.md`.
- **Mandatory:** `template-audit.txt`, `template-frame-map.json`,
  `deviation-log.txt`; every output slide mapped to a duplicated source slide.
- **Rules:** preserve typography, palette, spacing, inherited placeholders, and
  brand chrome; borrow only verified identity assets; add a domain profile (e.g.
  finance-ir) as a secondary gate.
- **Fails on:** rebuilding from blank instead of cloning; inventing lookalike
  marks to fill gaps; restyling the inherited system without being asked.

## targeted-edit-data
Add or edit a single data / comparison slide in an existing deck.
- **Mandatory:** exact calculations before any visual work; a native-looking
  insertion that matches the deck's layout grammar.
- **Fails on:** calculation mistakes; wrong ranking; a slide that looks pasted in
  from another system.

## targeted-edit-media
Add headshots, logos, screenshots, or other media to an existing deck.
- **Mandatory:** identity/source verification; consistent crops; preservation of
  the surrounding layout grammar.
- **Fails on:** unverified identities; inconsistent headshot crops; local layout
  damage.

## Brand-authenticity gate (every profile)
Logos, mascots, app icons, product UI, and partner/customer marks are identity
assets. Do not draw, trace, or approximate an official mark. Use a verified
asset with provenance, a user-supplied asset, or none — and lean on colour,
type, layout, and sourced metrics for brand instead. A fabricated or
approximated official mark, an unverified product screenshot, or a
pseudo-official badge fails the deck regardless of visual score.
