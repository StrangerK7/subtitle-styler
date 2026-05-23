"""
core.py — Subtitle Styler shared logic
Phase 3 Day 1 — Foundation
"""

import sys
import json
from pathlib import Path


# ============================================
# Constants
# ============================================

PROJECT_DIR = Path("/Users/kamil/Code/davinci-tools/subtitle-styler")
TEMPLATES_DIR = PROJECT_DIR / "templates"
BACKUPS_DIR = Path.home() / "Documents" / "SubtitleStyler" / "_backups"

# Resolve API path
RESOLVE_SCRIPT_API = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"


# ============================================
# Setup
# ============================================

def get_resolve_terminal():
    sys.path.insert(0, f"{RESOLVE_SCRIPT_API}/Modules")
    import DaVinciResolveScript as dvr_script
    return dvr_script.scriptapp("Resolve")


def get_fusion_and_comp(resolve):
    fu = resolve.Fusion()
    comp = fu.GetCurrentComp()
    return fu, comp


# ============================================
# Text+ node finding
# ============================================

def find_text_tools(comp, selected_only=False):
    """Saare Text+ nodes return karo.
    
    Returns: list of (idx, name, tool)
    """
    tools = comp.GetToolList(selected_only)
    
    text_tools = []
    for idx, tool in tools.items():
        reg_id = tool.GetAttrs().get("TOOLS_RegID", "")
        if reg_id == "TextPlus":
            name = tool.GetAttrs().get("TOOLS_Name", "")
            text_tools.append((idx, name, tool))
    
    return text_tools


def find_input_by_name(tool, target_name):
    """Tool ke input list mein specific naam ka parameter dhoondho.
    
    Returns: input object or None
    """
    inputs = tool.GetInputList()
    for in_idx, inp in inputs.items():
        pname = inp.GetAttrs().get("INPS_Name", "")
        if pname == target_name:
            return inp
    return None


# ============================================
# Read style from Text+ node
# ============================================

# Key parameters jo style ke liye matter karte hain
STYLE_PARAMS = [
    "Styled Text",
    "Font",
    "Style",
    "Size",
    "Red 1",
    "Green 1",
    "Blue 1",
    "Alpha 1",
    "Line Spacing",
    "Character Spacing",
]


def read_text_style(tool, comp):
    """Text+ node ka complete style read karo.
    
    Returns: dict {param_name: value}
    """
    style = {}
    time = comp.CurrentTime
    
    for param_name in STYLE_PARAMS:
        inp = find_input_by_name(tool, param_name)
        if inp is not None:
            try:
                style[param_name] = inp[time]
            except Exception as e:
                style[param_name] = None
        else:
            style[param_name] = None
    
    return style


# ============================================
# Write style to Text+ node
# ============================================

def write_text_style(tool, comp, style):
    """Style dict ko Text+ node pe apply karo.
    
    Returns: (applied_count, failed_list)
    """
    time = comp.CurrentTime
    applied = 0
    failed = []
    
    for param_name, value in style.items():
        if value is None:
            continue
        
        inp = find_input_by_name(tool, param_name)
        if inp is None:
            failed.append(f"{param_name} (not found)")
            continue
        
        try:
            inp[time] = value
            applied += 1
        except Exception as e:
            failed.append(f"{param_name} ({e})")
    
    return applied, failed
# ============================================
# Backup style (before write)
# ============================================

def ensure_backup_dir():
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    return BACKUPS_DIR


def backup_text_style(tool, comp, name_prefix="backup"):
    """Text+ node ka current style backup karo JSON mein.
    
    Returns: backup file path
    """
    import datetime
    
    ensure_backup_dir()
    
    style = read_text_style(tool, comp)
    
    # Convert non-serializable values to strings
    safe_style = {}
    for k, v in style.items():
        try:
            json.dumps(v)
            safe_style[k] = v
        except:
            safe_style[k] = str(v)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    tool_name = tool.GetAttrs().get("TOOLS_Name", "unknown")
    safe_name = tool_name.replace("/", "_").replace(" ", "_")
    
    backup_path = BACKUPS_DIR / f"{name_prefix}_{safe_name}_{timestamp}.json"
    
    with open(backup_path, "w", encoding="utf-8") as f:
        json.dump(safe_style, f, indent=2, ensure_ascii=False)
    
    return backup_path
# ============================================
# Color helper (hex to RGB)
# ============================================

def hex_to_rgb(hex_color):
    """Hex color (#RRGGBB) ko RGB tuple mein convert kar.
    
    Returns: (r, g, b) values 0.0 to 1.0
    """
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        return (1.0, 1.0, 1.0)
    
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    return (r, g, b)


# ============================================
# Shading element helpers
# ============================================

# Appearance modes
APPEARANCE_TEXT_FILL = 0.0
APPEARANCE_TEXT_OUTLINE = 1.0
APPEARANCE_BG_FILL = 2.0      # solid background (pill!)
APPEARANCE_BG_OUTLINE = 3.0


def make_text_fill_style(color_hex="#FFFFFF", element=1):
    """Element N ke liye text fill style banao.
    
    Returns: dict {param_name: value}
    """
    r, g, b = hex_to_rgb(color_hex)
    return {
        f"Enabled {element}": 1.0,
        f"Appearance {element}": APPEARANCE_TEXT_FILL,
        f"Red {element}": r,
        f"Green {element}": g,
        f"Blue {element}": b,
        f"Alpha {element}": 1.0,
    }


def make_pill_background_style(
    color_hex="#E8622A",
    element=5,
    round_corners=1.0,
    padding_x=0.1,
    padding_y=0.05,
    behind_text=True,
):
    """Element N pe pill-shape background banao."""
    r, g, b = hex_to_rgb(color_hex)
    return {
        f"Enabled {element}": 1.0,
        f"Appearance {element}": APPEARANCE_BG_FILL,
        f"Level {element}": 1.0,  # ⭐ NEW: 1=Text (whole text), 2=Line, 3=Word, 4=Char
        f"Red {element}": r,
        f"Green {element}": g,
        f"Blue {element}": b,
        f"Alpha {element}": 1.0,
        f"Round {element}": round_corners,
        f"Extend Horizontal {element}": padding_x,
        f"Extend Vertical {element}": padding_y,
        f"Priority {element}": -1.0 if behind_text else 5.0,
    }


def make_hinglish_badge_style(text, font="Poppins"):
    """Complete Hinglish pill badge template.
    
    Returns: dict ready to apply via write_text_style()
    """
    style = {
        # Content
        "Styled Text": text,
        "Font": font,
        "Style": "ExtraBold",
        "Size": 0.05,
    }
    
    # Element 1: white text
    style.update(make_text_fill_style(color_hex="#FFFFFF", element=1))
    
    # Element 5: orange pill background
    style.update(make_pill_background_style(
        color_hex="#E8622A",
        element=5,
        round_corners=1.0,
        padding_x=0.1,
        padding_y=0.05,
    ))
    
    return style
# ============================================
# Template loader system
# ============================================

LEVEL_MAP = {
    "Text": 1.0,
    "Line": 2.0,
    "Word": 3.0,
    "Character": 4.0,
}


def load_template(template_name):
    """Templates folder se JSON load kar.
    
    Args: 'hinglish_badge', 'corporate_clean', 'reel_pop' (without .json)
    Returns: dict with template data
    """
    template_path = TEMPLATES_DIR / f"{template_name}.json"
    
    if not template_path.exists():
        raise FileNotFoundError(f"Template nahi mila: {template_name}")
    
    with open(template_path, "r", encoding="utf-8") as f:
        return json.load(f)


def template_to_style(template_data, text=""):
    """Template JSON ko Text+ style dict mein convert kar.
    
    Args:
        template_data: load_template() ka output
        text: actual subtitle text (Hindi/English)
    
    Returns: style dict ready for write_text_style()
    """
    style_def = template_data["style"]
    style = {}
    
    # Text content
    if text:
        style["Styled Text"] = text
    
    # Core text params
    for key in ["Font", "Style", "Size"]:
        if key in style_def:
            style[key] = style_def[key]
    
    # Element 1 (text fill)
    if "element_1" in style_def:
        el1 = style_def["element_1"]
        if el1.get("type") == "text_fill":
            style.update(make_text_fill_style(
                color_hex=el1.get("color", "#FFFFFF"),
                element=1,
            ))
    
    # Element 5 (pill background or other)
    if "element_5" in style_def:
        el5 = style_def["element_5"]
        if el5.get("type") == "pill_background":
            pill_style = make_pill_background_style(
                color_hex=el5.get("color", "#E8622A"),
                element=5,
                round_corners=el5.get("round", 1.0),
                padding_x=el5.get("padding_x", 0.1),
                padding_y=el5.get("padding_y", 0.05),
                behind_text=el5.get("behind_text", True),
            )
            
            # Level override (Text/Line/Word/Character)
            level_name = el5.get("level", "Text")
            pill_style["Level 5"] = LEVEL_MAP.get(level_name, 1.0)
            
            style.update(pill_style)
    
    return style


def list_templates():
    """Saare available templates list karo."""
    if not TEMPLATES_DIR.exists():
        return []
    return sorted([p.stem for p in TEMPLATES_DIR.glob("*.json")])
# ============================================
# Template application with clean slate
# ============================================

def disable_all_shading_elements(tool, comp):
    """Saare 8 shading elements ko disable kar.
    Naya template apply karne se pehle use karo — clean slate.
    """
    time = comp.CurrentTime
    disabled = 0
    
    for element_num in range(1, 9):
        inp = find_input_by_name(tool, f"Enabled {element_num}")
        if inp is not None:
            try:
                inp[time] = 0.0
                disabled += 1
            except:
                pass
    
    return disabled
# ============================================
# Timeline subtitle access
# ============================================

def get_timeline_subtitles(resolve):
    """Resolve timeline ke subtitle clips read karo.
    
    Returns: list of dicts with text, start_frame, end_frame, duration
    """
    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    if not project:
        return []
    
    timeline = project.GetCurrentTimeline()
    if not timeline:
        return []
    
    subtitle_count = timeline.GetTrackCount("subtitle")
    if subtitle_count == 0:
        return []
    
    subtitles = []
    
    for track_idx in range(1, subtitle_count + 1):
        items = timeline.GetItemListInTrack("subtitle", track_idx)
        if not items:
            continue
        
        for item in items:
            try:
                text = item.GetName() if hasattr(item, "GetName") else ""
                start = item.GetStart() if hasattr(item, "GetStart") else 0
                end = item.GetEnd() if hasattr(item, "GetEnd") else 0
                duration = item.GetDuration() if hasattr(item, "GetDuration") else 0
                
                subtitles.append({
                    "text": text,
                    "start_frame": start,
                    "end_frame": end,
                    "duration": duration,
                    "track": track_idx,
                })
            except Exception as e:
                print(f"Error reading subtitle: {e}")
    
    return subtitles


def format_subtitles_text(subtitles):
    """Subtitle list ko display-friendly text mein convert karo.
    
    Returns: multi-line string
    """
    if not subtitles:
        return "(No subtitles found in timeline)"
    
    lines = []
    for i, sub in enumerate(subtitles, 1):
        lines.append(f"[{i}] {sub['text']}")
    
    return "\n".join(lines)
# ============================================
# Auto-transcribe trigger
# ============================================

def trigger_auto_transcribe(resolve):
    """Resolve ka CreateSubtitlesFromAudio trigger karo.
    
    Note: No arguments accepted — Resolve apne default settings use karta.
    User pehle Resolve UI mein language/granularity set kar sakta.
    
    Returns: (success: bool, message: str)
    """
    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    if not project:
        return False, "Project nahi mila"
    
    timeline = project.GetCurrentTimeline()
    if not timeline:
        return False, "Timeline nahi mila"
    
    # Count before (for comparison)
    before_count = timeline.GetTrackCount("subtitle")
    before_clips = 0
    if before_count > 0:
        items = timeline.GetItemListInTrack("subtitle", 1)
        before_clips = len(items) if items else 0
    
    # Trigger transcription
    try:
        result = timeline.CreateSubtitlesFromAudio()
        
        if not result:
            return False, "Transcription failed — audio track check karo"
        
        # Count after
        after_count = timeline.GetTrackCount("subtitle")
        after_clips = 0
        if after_count > 0:
            items = timeline.GetItemListInTrack("subtitle", 1)
            after_clips = len(items) if items else 0
        
        return True, f"✅ Transcribed: {after_clips} subtitle clips created"
    
    except Exception as e:
        return False, f"Error: {e}"