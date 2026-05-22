"""
explore_shading.py — Day 2 Shading Elements exploration
Text+ node ke shading layer params dhoondhna.

Usage: python3 explore_shading.py
"""

import sys
import json
sys.path.insert(0, "/Users/kamil/Code/davinci-tools/subtitle-styler")

from core import (
    get_resolve_terminal,
    get_fusion_and_comp,
    find_text_tools,
)


def main():
    resolve = get_resolve_terminal()
    fu, comp = get_fusion_and_comp(resolve)
    
    if not comp:
        print("❌ Fusion page khol")
        sys.exit(1)
    
    text_tools = find_text_tools(comp)
    if not text_tools:
        print("⚠️  Text+ node nahi mila")
        sys.exit(0)
    
    idx, name, tool = text_tools[0]
    print(f"📝 Exploring shading: {name}")
    print("=" * 60)
    
    inputs = tool.GetInputList()
    
    # Saare params jo "shading" se related hain
    shading_params = {}
    for in_idx, inp in inputs.items():
        pname = inp.GetAttrs().get("INPS_Name", "")
        if any(keyword in pname.lower() for keyword in [
            "shading", "outline", "shadow", "border", 
            "background", "fill", "element"
        ]):
            try:
                value = inp[comp.CurrentTime]
                shading_params[pname] = value
            except:
                shading_params[pname] = "(unreadable)"
    
    print(f"\nFound {len(shading_params)} shading-related params:\n")
    
    # Sort by name for clarity
    for pname in sorted(shading_params.keys()):
        value = shading_params[pname]
        val_str = str(value)
        if len(val_str) > 60:
            val_str = val_str[:57] + "..."
        print(f"  {pname:40s} = {val_str}")
    
    # Save to JSON
    safe_dump = {}
    for k, v in shading_params.items():
        try:
            json.dumps(v)
            safe_dump[k] = v
        except:
            safe_dump[k] = str(v)
    
    with open("shading_dump.json", "w") as f:
        json.dump(safe_dump, f, indent=2)
    
    print(f"\n💾 Saved to: shading_dump.json")
    print(f"   Total params: {len(shading_params)}")


if __name__ == "__main__":
    main()