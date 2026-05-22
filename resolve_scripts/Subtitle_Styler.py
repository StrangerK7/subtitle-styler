"""
Subtitle_Styler.py — Resolve menu UI for Subtitle Styler
Day 3, Phase 3 — UIManager UI

Workspace → Scripts → Utility → Subtitle Styler
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
# Globals (UIManager pattern)
# ============================================

resolve = None
fu = None
comp = None

ui = fu.UIManager if fu else None
dispatcher = None
win = None
itm = None


# ============================================
# UI helpers
# ============================================

def show_message(text, color="white"):
    """Status label update karo."""
    if itm and "StatusLabel" in itm:
        itm["StatusLabel"].Text = text
    print(f"[Subtitle Styler] {text}")


def get_selected_template():
    """Dropdown se chosen template ka name return karo."""
    if itm and "TemplateDropdown" in itm:
        idx = itm["TemplateDropdown"].CurrentIndex
        templates = list_templates()
        if 0 <= idx < len(templates):
            return templates[idx]
    return None


def get_subtitle_text():
    """Text input se subtitle text return karo."""
    if itm and "SubtitleTextEdit" in itm:
        return itm["SubtitleTextEdit"].PlainText
    return ""


# ============================================
# Button handlers
# ============================================

def on_backup_clicked(ev):
    """Backup button — current Text+ state save karo."""
    global comp
    
    if not comp:
        show_message("❌ Fusion comp nahi mila")
        return
    
    text_tools = find_text_tools(comp)
    if not text_tools:
        show_message("⚠️ Koi Text+ node nahi mila comp mein")
        return
    
    idx, name, tool = text_tools[0]
    backup_path = backup_text_style(tool, comp, name_prefix="manual")
    show_message(f"💾 Backup saved: {backup_path.name}")


def on_apply_clicked(ev):
    """Apply button — chosen template + text apply karo."""
    global comp
    
    if not comp:
        show_message("❌ Fusion comp nahi mila")
        return
    
    text_tools = find_text_tools(comp)
    if not text_tools:
        show_message("⚠️ Koi Text+ node nahi mila comp mein")
        return
    
    template_name = get_selected_template()
    if not template_name:
        show_message("⚠️ Template select karo")
        return
    
    text = get_subtitle_text().strip()
    if not text:
        show_message("⚠️ Subtitle text daal pehle")
        return
    
    idx, name, tool = text_tools[0]
    
    try:
        # Load template
        template_data = load_template(template_name)
        style = template_to_style(template_data, text=text)
        
        # Auto-backup before apply
        backup_path = backup_text_style(tool, comp, name_prefix=f"pre_{template_name}")
        
        # Clean slate
        disable_all_shading_elements(tool, comp)
        
        # Apply
        applied, failed = write_text_style(tool, comp, style)
        
        if failed:
            show_message(f"⚠️ Applied {applied}, {len(failed)} failed")
        else:
            show_message(f"✅ '{template_data.get('name', template_name)}' applied ({applied} params)")
    
    except Exception as e:
        show_message(f"❌ Error: {e}")


def on_close_clicked(ev):
    """Close button."""
    dispatcher.ExitLoop()


# ============================================
# UI Layout
# ============================================

def build_ui():
    global win, itm, dispatcher, ui
    
    dispatcher = bmd.UIDispatcher(ui)
    
    # Window
    win = dispatcher.AddWindow(
        {
            "ID": "SubtitleStylerWin",
            "WindowTitle": "📝 Subtitle Styler",
            "Geometry": [500, 300, 480, 420],
        },
        [
            ui.VGroup([
                # Header
                ui.Label({
                    "Text": "Subtitle Styler",
                    "Weight": 0.05,
                    "Alignment": {"AlignHCenter": True},
                    "StyleSheet": "font-size: 16px; font-weight: bold;"
                }),
                
                # Spacer
                ui.Label({"Text": "", "Weight": 0.02}),
                
                # Template dropdown section
                ui.Label({
                    "Text": "Choose Template:",
                    "Weight": 0.05,
                    "StyleSheet": "font-weight: bold;"
                }),
                ui.ComboBox({
                    "ID": "TemplateDropdown",
                    "Weight": 0.08,
                }),
                
                # Spacer
                ui.Label({"Text": "", "Weight": 0.02}),
                
                # Subtitle text input section
                ui.Label({
                    "Text": "Subtitle Text (Hindi/English):",
                    "Weight": 0.05,
                    "StyleSheet": "font-weight: bold;"
                }),
                ui.TextEdit({
                    "ID": "SubtitleTextEdit",
                    "Weight": 0.35,
                    "PlaceholderText": "Type your subtitle here...",
                }),
                
                # Spacer
                ui.Label({"Text": "", "Weight": 0.02}),
                
                # Buttons row
                ui.HGroup([
                    ui.Button({
                        "ID": "BackupBtn",
                        "Text": "💾 Backup",
                        "Weight": 0.3,
                    }),
                    ui.Button({
                        "ID": "ApplyBtn",
                        "Text": "🎨 Apply Style",
                        "Weight": 0.5,
                    }),
                    ui.Button({
                        "ID": "CloseBtn",
                        "Text": "Close",
                        "Weight": 0.2,
                    }),
                ], {"Weight": 0.1}),
                
                # Spacer
                ui.Label({"Text": "", "Weight": 0.02}),
                
                # Status label
                ui.Label({
                    "ID": "StatusLabel",
                    "Text": "Ready",
                    "Weight": 0.05,
                    "StyleSheet": "color: #4caf50; padding: 4px;"
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
    
    # Wire buttons
    win.On.BackupBtn.Clicked = on_backup_clicked
    win.On.ApplyBtn.Clicked = on_apply_clicked
    win.On.CloseBtn.Clicked = on_close_clicked
    win.On.SubtitleStylerWin.Close = on_close_clicked
    
    # Pre-fill with sample text
    itm["SubtitleTextEdit"].PlainText = "Sample subtitle text"
    
    win.Show()
    dispatcher.RunLoop()
    win.Hide()


# ============================================
# Entry point
# ============================================

def main():
    global resolve, fu, comp, ui
    
    # Resolve handle (Fusion menu se script chalega — resolve ready hoga)
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
        print("⚠️ Fusion page khol pehle — koi active comp nahi")
        return
    
    ui = fu.UIManager
    
    text_tools = find_text_tools(comp)
    if not text_tools:
        print("⚠️ Comp mein Text+ node banao pehle")
        # Continue anyway — user might add it later
    
    build_ui()


main()