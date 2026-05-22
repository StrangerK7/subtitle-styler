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