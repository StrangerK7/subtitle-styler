"""
Desi_Captions.py — DaVinci Resolve plugin for Hinglish captions
v2.0 — Custom builder + animations + transcription

Brand: Desi Captions
Target: Indian content creators (reels, devotional, astrology, education)
"""

import sys
import os

# Project path setup
PROJECT_DIR = "/Users/kamil/Code/davinci-tools/subtitle-styler"
sys.path.insert(0, PROJECT_DIR)

from core import (
    get_fusion_and_comp,
    find_text_tools,
    write_text_style,
    backup_text_style,
    load_template,
    template_to_style,
    list_templates,
    disable_all_shading_elements,
    get_timeline_subtitles,
    format_subtitles_text,
    trigger_auto_transcribe,        # ⭐ NEW
)


# ============================================
# Globals
# ============================================

resolve = None
fu = None
comp = None
ui = None
dispatcher = None
win = None
itm = None

# Tab state (0 = Transcribe, 1 = Style, 2 = Animate)
CURRENT_TAB = 1  # Default to Style tab


# ============================================
# UI helpers
# ============================================

def show_message(text, color="#4caf50"):
    """Status label update."""
    if itm and "StatusLabel" in itm:
        itm["StatusLabel"].Text = text
        itm["StatusLabel"].StyleSheet = f"color: {color}; padding: 4px;"
    print(f"[Desi Captions] {text}")


def switch_tab(tab_index):
    """Show specific tab page in Stack."""
    global CURRENT_TAB
    CURRENT_TAB = tab_index
    if itm and "MainStack" in itm:
        itm["MainStack"].CurrentIndex = tab_index
    
    # Update tab button styles (highlight active)
    update_tab_button_styles()


def update_tab_button_styles():
    """Highlight active tab button."""
    if not itm:
        return
    
    active_style = "background-color: #e6e600; color: black; font-weight: bold;"
    inactive_style = "background-color: #333; color: #ccc;"
    
    for i, btn_id in enumerate(["TabTranscribeBtn", "TabStyleBtn", "TabAnimateBtn"]):
        if btn_id in itm:
            itm[btn_id].StyleSheet = active_style if i == CURRENT_TAB else inactive_style


# ============================================
# Tab button handlers
# ============================================

def on_tab_transcribe(ev):
    switch_tab(0)
    show_message("📝 Transcribe tab — coming Week 1 Day 8")


def on_tab_style(ev):
    switch_tab(1)
    show_message("🎨 Style tab — current focus")

    # ============================================
# Transcribe tab handlers
# ============================================

def on_auto_transcribe_clicked(ev):
    """Auto-transcribe button — Resolve ka subtitle creation trigger karo."""
    global resolve
    
    if not resolve:
        show_message("❌ Resolve nahi mila", "#f44336")
        return
    
    show_message("🔄 Transcribing audio... (wait 5-10 sec)", "#2196f3")
    
    try:
        success, msg = trigger_auto_transcribe(resolve)
        
        if success:
            show_message(msg, "#4caf50")
            # Auto-load the new subtitles
            on_read_subtitles_clicked(None)
        else:
            show_message(f"⚠️ {msg}", "#ff9800")
    
    except Exception as e:
        show_message(f"❌ Error: {e}", "#f44336")

def on_read_subtitles_clicked(ev):
    """Timeline ke subtitles read karke UI mein dikhao."""
    global resolve
    
    if not resolve:
        show_message("❌ Resolve nahi mila", "#f44336")
        return
    
    try:
        subtitles = get_timeline_subtitles(resolve)
        
        if not subtitles:
            show_message("⚠️ Timeline mein koi subtitle nahi", "#ff9800")
            if "TranscribedTextEdit" in itm:
                itm["TranscribedTextEdit"].PlainText = (
                    "Subtitle track nahi mila.\n\n"
                    "Resolve mein:\n"
                    "1. Edit page kholo\n"
                    "2. Timeline pe video clip select karo\n"
                    "3. Right-click → 'Create Subtitles from Audio'\n"
                    "4. Language choose karke 'Create' click\n"
                    "5. Wapas yahan aakar 'Read Subtitles' click"
                )
            return
        
        # Format display
        display_text = format_subtitles_text(subtitles)
        if "TranscribedTextEdit" in itm:
            itm["TranscribedTextEdit"].PlainText = display_text
        
        show_message(f"✅ {len(subtitles)} subtitles loaded", "#4caf50")
    
    except Exception as e:
        show_message(f"❌ Error: {e}", "#f44336")


def on_tab_animate(ev):
    switch_tab(2)
    show_message("✨ Animate tab — coming Week 3")


# ============================================
# Action button handlers
# ============================================

def on_apply_clicked(ev):
    """Main Apply to Timeline button."""
    global comp
    
    if not comp:
        show_message("❌ Fusion comp nahi mila", "#f44336")
        return
    
    text_tools = find_text_tools(comp)
    if not text_tools:
        show_message("⚠️ Koi Text+ node nahi mila", "#ff9800")
        return
    
    # For now, use Style tab logic (existing template behavior)
    if CURRENT_TAB == 1:  # Style tab
        apply_style_tab()
    elif CURRENT_TAB == 0:  # Transcribe tab
        show_message("📝 Transcribe feature coming Week 1 Day 8", "#2196f3")
    elif CURRENT_TAB == 2:  # Animate tab
        show_message("✨ Animation feature coming Week 3", "#2196f3")


def apply_style_tab():
    """Apply selected template (preset mode)."""
    if "TemplateDropdown" not in itm or "SubtitleTextEdit" not in itm:
        show_message("⚠️ UI not ready", "#ff9800")
        return
    
    idx = itm["TemplateDropdown"].CurrentIndex
    templates = list_templates()
    if idx < 0 or idx >= len(templates):
        show_message("⚠️ Template select karo", "#ff9800")
        return
    
    template_name = templates[idx]
    text = itm["SubtitleTextEdit"].PlainText.strip()
    if not text:
        show_message("⚠️ Subtitle text daal pehle", "#ff9800")
        return
    
    text_tools = find_text_tools(comp)
    idx_tool, name, tool = text_tools[0]
    
    try:
        template_data = load_template(template_name)
        style = template_to_style(template_data, text=text)
        
        backup_text_style(tool, comp, name_prefix=f"pre_{template_name}")
        disable_all_shading_elements(tool, comp)
        applied, failed = write_text_style(tool, comp, style)
        
        if failed:
            show_message(f"⚠️ Applied {applied}, {len(failed)} failed", "#ff9800")
        else:
            show_message(f"✅ '{template_data.get('name', template_name)}' applied", "#4caf50")
    
    except Exception as e:
        show_message(f"❌ Error: {e}", "#f44336")


def on_close_clicked(ev):
    dispatcher.ExitLoop()


# ============================================
# UI Build
# ============================================

def build_ui():
    global win, itm, dispatcher, ui
    
    dispatcher = bmd.UIDispatcher(ui)
    
    win = dispatcher.AddWindow(
        {
            "ID": "DesiCaptionsWin",
            "WindowTitle": "🎬 Desi Captions",
            "Geometry": [400, 200, 560, 580],
        },
        [
            ui.VGroup([
                # Header
                ui.Label({
                    "Text": "🎬 Desi Captions",
                    "Weight": 0.05,
                    "Alignment": {"AlignHCenter": True},
                    "StyleSheet": "font-size: 18px; font-weight: bold; color: #e6e600; padding: 4px;"
                }),
                
                # Tagline
                ui.Label({
                    "Text": "Hinglish captions for DaVinci Resolve",
                    "Weight": 0.03,
                    "Alignment": {"AlignHCenter": True},
                    "StyleSheet": "color: #888; font-size: 11px;"
                }),
                
                # Tab buttons row
                ui.HGroup([
                    ui.Button({
                        "ID": "TabTranscribeBtn",
                        "Text": "📝 Transcribe",
                        "Weight": 0.33,
                    }),
                    ui.Button({
                        "ID": "TabStyleBtn",
                        "Text": "🎨 Style",
                        "Weight": 0.33,
                    }),
                    ui.Button({
                        "ID": "TabAnimateBtn",
                        "Text": "✨ Animate",
                        "Weight": 0.33,
                    }),
                ], {"Weight": 0.08}),
                
                # MAIN STACK (3 tabs)
                ui.Stack({
                    "ID": "MainStack",
                    "Weight": 0.65,
                    "CurrentIndex": 1,  # Default to Style tab
                }, [
                    # ============ PAGE 0: TRANSCRIBE ============
ui.VGroup([
    ui.Label({
        "Text": "📝 Auto-Transcribe + Reader (Day 7+8)",
        "Weight": 0.06,
        "StyleSheet": "font-weight: bold; padding: 8px; font-size: 13px;"
    }),
    ui.Label({
        "Text": "Step 1: Audio se subtitles auto-generate karo\nStep 2: UI mein read karke preview karo",
        "Weight": 0.08,
        "StyleSheet": "color: #999; padding: 4px;"
    }),
    
    # Auto-transcribe button (NEW)
    ui.Button({
        "ID": "AutoTranscribeBtn",
        "Text": "🎤 Auto-Transcribe Audio",
        "Weight": 0.08,
        "StyleSheet": "background-color: #e6e600; color: black; font-weight: bold;"
    }),
    
    # Read button (existing)
    ui.Button({
        "ID": "ReadSubtitlesBtn",
        "Text": "📥 Read Subtitles from Timeline",
        "Weight": 0.08,
        "StyleSheet": "background-color: #2196f3; color: white; font-weight: bold;"
    }),
    
    ui.Label({
        "Text": "Transcribed text (preview):",
        "Weight": 0.04,
        "StyleSheet": "color: #ccc; padding-top: 8px;"
    }),
    ui.TextEdit({
        "ID": "TranscribedTextEdit",
        "Weight": 0.55,
        "PlaceholderText": "Click Auto-Transcribe ya Read Subtitles to load...",
    }),
    ui.Label({
        "Text": "💡 Edit karna ho to abhi Resolve mein direct karo. Python edit Day 9-10 mein add hoga.",
        "Weight": 0.04,
        "StyleSheet": "color: #888; font-size: 10px;"
    }),
]),
                    
                    # ============ PAGE 1: STYLE (default) ============
                    ui.VGroup([
                        ui.Label({
                            "Text": "Choose Template:",
                            "Weight": 0.05,
                            "StyleSheet": "font-weight: bold;"
                        }),
                        ui.ComboBox({
                            "ID": "TemplateDropdown",
                            "Weight": 0.08,
                        }),
                        
                        ui.Label({"Text": "", "Weight": 0.02}),
                        
                        ui.Label({
                            "Text": "Subtitle Text (Hindi/English):",
                            "Weight": 0.05,
                            "StyleSheet": "font-weight: bold;"
                        }),
                        ui.TextEdit({
                            "ID": "SubtitleTextEdit",
                            "Weight": 0.4,
                            "PlaceholderText": "Type your subtitle here...",
                        }),
                        
                        ui.Label({
                            "Text": "💡 Custom builder coming Week 2 (Day 13)",
                            "Weight": 0.05,
                            "StyleSheet": "color: #888; font-size: 10px;"
                        }),
                    ]),
                    
                    # ============ PAGE 2: ANIMATE ============
                    ui.VGroup([
                        ui.Label({
                            "Text": "Animation (Coming Week 3 - Day 20)",
                            "Weight": 0.1,
                            "StyleSheet": "font-weight: bold; padding: 8px;"
                        }),
                        ui.Label({
                            "Text": "Coming animations:\n\n• Karaoke Highlight (word color change)\n• Word-by-Word Reveal\n• Kinetic Captions (scale/slide entry)\n• Dynamic Captions (per-emphasis effects)",
                            "Weight": 0.5,
                            "StyleSheet": "color: #999; padding: 8px;"
                        }),
                        ui.Label({"Text": "", "Weight": 0.3}),
                    ]),
                ]),
                
                # Action buttons
                ui.HGroup([
                    ui.Button({
                        "ID": "ApplyBtn",
                        "Text": "🎨 Apply to Timeline",
                        "Weight": 0.7,
                        "StyleSheet": "background-color: #e6e600; color: black; font-weight: bold;"
                    }),
                    ui.Button({
                        "ID": "CloseBtn",
                        "Text": "Close",
                        "Weight": 0.3,
                    }),
                ], {"Weight": 0.08}),
                
                # Status
                ui.Label({
                    "ID": "StatusLabel",
                    "Text": "Ready • Desi Captions v2.0",
                    "Weight": 0.04,
                    "StyleSheet": "color: #4caf50; padding: 4px; font-size: 11px;"
                }),
            ])
        ]
    )
    
    itm = win.GetItems()
    
    # Populate template dropdown
    templates = list_templates()
    for t in templates:
        td = load_template(t)
        display_name = td.get("name", t)
        itm["TemplateDropdown"].AddItem(display_name)
    
    # Wire tab buttons
    win.On.TabTranscribeBtn.Clicked = on_tab_transcribe
    win.On.TabStyleBtn.Clicked = on_tab_style
    win.On.TabAnimateBtn.Clicked = on_tab_animate
    win.On.ReadSubtitlesBtn.Clicked = on_read_subtitles_clicked     # ⭐ NEW LINE

    # Wire action buttons
    win.On.ApplyBtn.Clicked = on_apply_clicked
    win.On.CloseBtn.Clicked = on_close_clicked
    win.On.DesiCaptionsWin.Close = on_close_clicked
    win.On.AutoTranscribeBtn.Clicked = on_auto_transcribe_clicked   # ⭐ NEW
    win.On.ReadSubtitlesBtn.Clicked = on_read_subtitles_clicked
    
    # Initial tab style
    update_tab_button_styles()
    
    win.Show()
    dispatcher.RunLoop()
    win.Hide()


# ============================================
# Entry point
# ============================================

def main():
    global resolve, fu, comp, ui
    
    if "resolve" not in globals() or resolve is None:
        try:
            resolve = bmd.scriptapp("Resolve")
        except:
            pass
    
    if not resolve:
        print("❌ Resolve nahi mila")
        return
    
    fu = resolve.Fusion()
    comp = fu.GetCurrentComp()
    
    if not comp:
        print("⚠️ Fusion page khol pehle")
        return
    
    ui = fu.UIManager
    
    build_ui()


main()