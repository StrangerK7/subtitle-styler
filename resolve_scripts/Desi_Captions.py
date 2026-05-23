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
                            "Text": "Auto-Transcribe (Coming Week 1 Day 8)",
                            "Weight": 0.1,
                            "StyleSheet": "font-weight: bold; padding: 8px;"
                        }),
                        ui.Label({
                            "Text": "DaVinci Resolve ka built-in 'Create Subtitles from Audio' use karega.\nSupports Hindi, English, Hinglish + 16 more languages.",
                            "Weight": 0.3,
                            "StyleSheet": "color: #999; padding: 8px;"
                        }),
                        ui.Button({
                            "ID": "TranscribeBtn",
                            "Text": "🎤 Auto-Transcribe (placeholder)",
                            "Weight": 0.1,
                        }),
                        ui.TextEdit({
                            "ID": "TranscribedTextEdit",
                            "Weight": 0.5,
                            "PlaceholderText": "Transcribed text will appear here for editing...",
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
    
    # Wire action buttons
    win.On.ApplyBtn.Clicked = on_apply_clicked
    win.On.CloseBtn.Clicked = on_close_clicked
    win.On.DesiCaptionsWin.Close = on_close_clicked
    
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