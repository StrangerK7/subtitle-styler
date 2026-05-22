"""
explore_textplus.py — Day 1 exploration v2
Text+ tool ka full API discover karna.

Usage: python3 explore_textplus.py (Fusion page khulli ho with Text+ node)
"""

import sys
import json

RESOLVE_SCRIPT_API = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
sys.path.insert(0, f"{RESOLVE_SCRIPT_API}/Modules")

import DaVinciResolveScript as dvr_script

resolve = dvr_script.scriptapp("Resolve")
if not resolve:
    print("❌ Resolve nahi mila")
    sys.exit(1)

fu = resolve.Fusion()
comp = fu.GetCurrentComp()
if not comp:
    print("❌ Fusion page khol — koi comp active nahi")
    sys.exit(1)

# Find Text+ nodes
tools = comp.GetToolList()
print("=" * 60)
print("TEXT+ EXPLORATION v2")
print("=" * 60)

text_tools = []
for idx, tool in tools.items():
    reg_id = tool.GetAttrs().get("TOOLS_RegID", "")
    if reg_id == "TextPlus":
        name = tool.GetAttrs().get("TOOLS_Name", "")
        text_tools.append((idx, name, tool))

print(f"\nText+ nodes found: {len(text_tools)}")

if not text_tools:
    print("⚠️  Text+ node banao Fusion mein, fir script dobara chala")
    sys.exit(0)

idx, name, tool = text_tools[0]
print(f"\nExploring: {name} (index {idx})")
print("=" * 60)

# Read all inputs into a name → value dict
inputs = tool.GetInputList()
print(f"Total parameters: {len(inputs)}")

all_params = {}
for in_idx, inp in inputs.items():
    pname = inp.GetAttrs().get("INPS_Name", f"Unknown_{in_idx}")
    try:
        value = inp[comp.CurrentTime]
        all_params[pname] = value
    except:
        all_params[pname] = "(unreadable)"

# Key parameters to highlight
print()
print("=" * 60)
print("KEY PARAMETERS (most useful for styling):")
print("=" * 60)

key_params = [
    "StyledText",
    "Font",
    "Style",
    "Size",
    "VerticalTopCenterBottom",
    "HorizontalLeftCenterRight",
    "Center",
    "Red1", "Green1", "Blue1", "Alpha1",
    "LineSpacing",
    "CharacterSpacing",
]

for param_name in key_params:
    value = all_params.get(param_name, "(NOT FOUND)")
    print(f"  {param_name:30s} = {value}")

# Save full dump
print()
print("=" * 60)
print("ALL PARAMETERS (saving to file):")
print("=" * 60)

# Group by category (rough heuristic by name prefix)
categories = {
    "Content": [],
    "Color": [],
    "Layout": [],
    "Shading": [],
    "Animation": [],
    "Other": [],
}

for pname, pvalue in sorted(all_params.items()):
    if pname in ["StyledText", "Font", "Style", "Size"]:
        categories["Content"].append((pname, pvalue))
    elif pname.startswith(("Red", "Green", "Blue", "Alpha")):
        categories["Color"].append((pname, pvalue))
    elif pname in ["Center", "Width", "Height", "VerticalTopCenterBottom", "HorizontalLeftCenterRight"]:
        categories["Layout"].append((pname, pvalue))
    elif "Shading" in pname or "Outline" in pname or "Shadow" in pname or "Border" in pname:
        categories["Shading"].append((pname, pvalue))
    elif "Anim" in pname or "Modifier" in pname:
        categories["Animation"].append((pname, pvalue))
    else:
        categories["Other"].append((pname, pvalue))

for cat, items in categories.items():
    print(f"\n--- {cat} ({len(items)} params) ---")
    for pname, pvalue in items[:10]:  # first 10 of each
        val_str = str(pvalue)
        if len(val_str) > 60:
            val_str = val_str[:57] + "..."
        print(f"  {pname:30s} = {val_str}")
    if len(items) > 10:
        print(f"  ... and {len(items) - 10} more")

# Save complete dump to JSON
safe_dump = {}
for k, v in all_params.items():
    try:
        json.dumps(v)
        safe_dump[k] = v
    except:
        safe_dump[k] = str(v)

output_file = "textplus_dump.json"
with open(output_file, "w") as f:
    json.dump(safe_dump, f, indent=2)

print()
print(f"💾 Full dump saved to: {output_file}")
print(f"   Total params: {len(all_params)}")