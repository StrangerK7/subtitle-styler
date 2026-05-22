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
    
    with open(backup_path, "w") as f:
        json.dump(safe_style, f, indent=2, ensure_ascii=False)
    
    return backup_path