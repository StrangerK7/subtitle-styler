# Subtitle Styler — Development Log

## Phase 3 begins — Day 1

### Context
- Phase 1 (template-manager) shipped v1.0
- Phase 2 (node-cleanup) shipped v7.1 (graph algorithms)
- Both production-ready in Resolve menu

### Today's goal
- Project setup
- Explore Fusion Text+ tool API
- Identify key parameters for subtitle styling
- First exploration script
## Day 1 — Phase 3 Foundation ✅ COMPLETE

### Achievements
1. ✅ Project setup (folder, GitHub repo, initial docs)
2. ✅ Text+ API exploration (309 parameters discovered)
3. ✅ Naming convention identified (spaces + title case)
4. ✅ Style read function (core.py)
5. ✅ Style write function (core.py)
6. ✅ Backup system (auto-JSON before write)
7. ✅ **HINDI + DEVANAGARI FONT TEST PASSED** 🇮🇳

### Critical discoveries
1. Fusion parameter names use SPACES (e.g., "Styled Text", "Red 1", "Alpha 1")
2. Text+ has 309 parameters — most complex Fusion tool
3. "Styled Text" parameter holds actual text content
4. "Font" parameter accepts font family name string (e.g., "Kohinoor Devanagari")
5. Color via 4 separate params: "Red 1", "Green 1", "Blue 1", "Alpha 1"
6. Style modifier separate ("Bold", "Regular", "Italic")
7. Size in normalized units (0.08 = roughly 80px equivalent)

### Mac fonts available (verified)
- Kohinoor Devanagari (premium Apple)
- ITF Devanagari + Marathi variant
- Hind (Google Fonts)
- Devanagari MT, Shree Devanagari 714
- .SF Devanagari (Apple system)

### Files created
- core.py (foundation: read/write/backup)
- experiments/explore_textplus.py (full param dump)
- experiments/read_textstyle.py (current state reader)
- experiments/write_hindi.py (Hindi+font test) ⭐
- experiments/textplus_dump.json (reference)

### Stats
- Lines added: ~250
- Time: ~3 hours
- API discoveries: 7
- Working capabilities: 5
- Bugs encountered + fixed: 1 (FindInput None — pivoted to iteration)

### Day 2+ ideas (in IDEAS.md)
- Template system (style as JSON template)
- Hinglish Badge style implementation
- Shading layers (outline, shadow, glow)
- Animation modifiers exploration
- Multi-line subtitle handling
## Day 2 — Pill Badge + Template System ✅ COMPLETE

### Block 1: Shading exploration
- 56 params per element discovered
- "Level N" parameter found: {Text/Line/Word/Character}
- "Appearance N" parameter found: 4 modes (Fill/Outline/BG/Hollow-BG)
- "Round N", "Extend Horizontal/Vertical N" — pill controls

### Block 2: First pill badge code
- `make_text_fill_style()` helper
- `make_pill_background_style()` helper
- `hex_to_rgb()` color converter
- 20 params applied successfully

### Block 3: Visual quality fixes
- **CRITICAL FIX**: "Level 5" was at Word (3.0), needed Text (1.0)
- Single pill around full text vs fragmented per-word pills
- User insight: "border character level pe lag raha hai"
- Resolved with ComboControl value mapping discovered

### Block 4: Template JSON system
- 3 templates created:
  - hinglish_badge.json (Clickastro orange pill)
  - corporate_clean.json (minimal white)
  - reel_pop.json (Instagram green pill)
- `load_template()`, `template_to_style()`, `list_templates()`
- LEVEL_MAP for human-readable level values
- `disable_all_shading_elements()` for clean slate

### Block 4b: State leak fix
- Bug: Previous template's element 5 stayed enabled
- Fix: Disable all 8 elements before applying new template
- Production pattern: idempotent template application

### Tests passed
- Corporate Clean: white text only, no pill ✅
- Hinglish Badge: orange pill + text ✅
- Reel Pop: green text + dark pill ✅
- All 3 with same Text1 node — no state leak ✅

### Encoding fix
- Hindi/Devanagari text needs `encoding="utf-8"` in JSON
- Backup function now handles non-ASCII content

### Files
- core.py — expanded ~150 lines (helpers + template loader)
- templates/ — 3 JSON files
- experiments/test_pill_badge.py
- experiments/test_templates.py

### Stats
- Lines added: ~250
- Time: ~3 hours
- Templates working: 3
- Connection types handled: text, color, pill background
- Bugs fixed: 3 (FindInput None, encoding, state leak)

### Day 3+ ideas
- UIManager UI (template dropdown + text input + apply button)
- More templates (Karaoke highlight, Podcast lower-third)
- Animation modifiers exploration
- SRT file import (batch subtitle styling)
- Color picker helper