# Subtitle Styler — Ideas Board

## Style templates planned (Phase 3 deliverables)
1. **Hinglish Badge** — pill-shape orange badge, white bold (Clickastro ad style)
2. **Corporate Clean** — minimal, white text, subtle shadow
3. **Reel Pop** — large bold, neon colors, bounce animation
4. **Podcast Lower-third** — name + title block
5. **Karaoke Highlight** — word-by-word color reveal

## Technical patterns to explore
- Text+ parameter mapping (StyledText, Font, Color, Size, Outline, Shadow)
- TextAnim modifiers for animations
- Devanagari font handling quirks
- Render preview vs final quality

## Future
- Subtitle file (SRT) import
- AI-generated subtitle text (Whisper integration?)
- Word timing extraction
## Day 1 Discoveries → Day 2 Plans

### Confirmed capabilities (ready to build on)
- ✅ Read any Text+ parameter
- ✅ Write any Text+ parameter
- ✅ Devanagari font selection
- ✅ Hindi text content
- ✅ Color (4-channel)
- ✅ Size, Style, Font family

### Templates to build next
Each template = JSON file with key params

**Template 1: Hinglish Pill Badge** (Clickastro style)
```json
{
  "Styled Text": "(user input)",
  "Font": "Poppins",
  "Style": "ExtraBold",
  "Size": 0.04,
  "Red 1": 1.0, "Green 1": 1.0, "Blue 1": 1.0,
  "Shading Element 1 Type": "Background",
  "Background Color": "(orange #E8622A)"
}
```

**Template 2: Hindi Reel Title**
- Kohinoor Devanagari Bold
- Large size (0.12)
- White text with shadow

**Template 3: Corporate Lower-third**
- Open Sans
- Smaller (0.05)
- Subtle shadow

### Technical unknowns to explore Day 2
- Shading elements (outline, shadow, background pill)
- Multi-character layouts (line breaks, alignment)
- Color picker → RGB conversion helper
- Animation modifiers (TextScramble, fade-in)
## Day 2 Discoveries → Day 3+ Plans

### Confirmed production capabilities
- ✅ Template JSON → Text+ style pipeline
- ✅ Clean state management (no element leaks)
- ✅ Multi-language text (Hindi/English)
- ✅ Multiple shading elements (text + background)

### Day 3 mission
**UIManager UI** — Phase 1+2 pattern reuse:
- Template dropdown (lists from templates/ folder)
- Text input field (multi-line)
- Apply button
- Live preview hint
- Backup/restore buttons

### Templates pipeline
Current: 3 hardcoded templates (corporate, badge, reel)
Day 3-4: Add 3-5 more templates
- Karaoke highlight (yellow text on dark BG)
- Podcast lower-third (name + title format)
- News ticker (white text on blue strip)
- Bollywood title (large bold with shadow)
- Cooking show (warm tones with outline)

### Future enhancements
- SRT/VTT subtitle file import
- Whisper integration for auto-transcription
- Per-word timing animations
- Color picker for custom templates
- Save user-customized templates