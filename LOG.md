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
## Day 3 — Production UI ✅ COMPLETE (in 30 min!)

### Achievement
UI Manager-based clickable interface deployed in Resolve menu.
**Time: 30 minutes** (3-hour budget — way under).

### Reason: Phase 1+2 pattern reuse
Template Manager + Node Cleanup ki UIManager patterns directly adapted:
- Window setup, layout structure
- Dropdown, button wiring
- Status label for user feedback
- Backup integration

### Files
- resolve_scripts/Subtitle_Styler.py (UIManager interface)
- Symlink: /Users/kamil/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/Subtitle_Styler.py

### UI Features
1. Template dropdown (auto-populated from templates/ folder)
2. Multi-line text input (Hindi/English support)
3. Backup button (manual safety net)
4. Apply Style button (one-click template application)
5. Close button (clean exit)
6. Status label (real-time feedback)
7. 📝 emoji in title (renders correctly!)

### Tests passed (3/3)
- Corporate Clean: white text, 10 params ✅
- Hinglish Pill Badge: orange pill, 21 params ✅
- Reel Pop: green + dark pill, 21 params ✅
- Empty text validation: warning shown, no crash ✅

### Key insights
- UIManager works with Hindi/English text input
- Emoji in window titles works in DaVinci Resolve Studio 21
- TextEdit widget handles multi-line natively
- ComboBox dropdown smooth, no flicker
- Status label color (StyleSheet) render
## Day 4 — 3 new templates ✅ COMPLETE

### Templates added
1. **Karaoke Highlight** (karaoke_highlight.json)
   - Yellow text (#FFD600), dark navy pill (#1A237E)
   - Full round corners, larger padding
   - Lyrics video / music content use case
   
2. **News Ticker** (news_ticker.json)
   - White bold text, sharp blue rectangle (#1565C0)
   - SHARP corners (round: 0.0) — formal news look
   - Wide horizontal padding
   
3. **Podcast Lower-third** (podcast_lower_third.json)
   - White SemiBold, dark gray pill (#212121)
   - Slight rounded corners (0.15)
   - Interview/podcast use case

### Stats
- 3 templates → 6 templates (100% increase)
- Lines added: ~50 (just JSON, no code change!)
- Time: ~45 min (templates created + tested)
- Bug count: 0 (smooth as butter)

### Insight: Architecture proven scalable
Day 2 mein build kiya template system. Day 4 mein 3 new templates **without ANY code changes** — sirf JSON files add. **Yeh proper engineering** hai.

### Day 5 plan
- Edge cases (no Text+, multiple Text+, invalid template)
- Better error messages
- Font fallback system
- Multi-Text+ node batch apply