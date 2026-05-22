"""
read_textstyle.py — Read current Text+ style
Usage: python3 read_textstyle.py (Fusion page with Text+ node)
"""

import sys
sys.path.insert(0, "/Users/kamil/Code/davinci-tools/subtitle-styler")

from core import (
    get_resolve_terminal,
    get_fusion_and_comp,
    find_text_tools,
    read_text_style,
)


def main():
    resolve = get_resolve_terminal()
    if not resolve:
        print("❌ Resolve nahi mila")
        sys.exit(1)
    
    fu, comp = get_fusion_and_comp(resolve)
    if not comp:
        print("❌ Fusion page khol pehle")
        sys.exit(1)
    
    text_tools = find_text_tools(comp)
    
    if not text_tools:
        print("⚠️  Koi Text+ node nahi mila comp mein")
        sys.exit(0)
    
    print("=" * 50)
    print("CURRENT TEXT+ STYLES")
    print("=" * 50)
    
    for idx, name, tool in text_tools:
        print(f"\n📝 {name}")
        print("-" * 40)
        
        style = read_text_style(tool, comp)
        
        for param, value in style.items():
            if value is None:
                print(f"  {param:25s} = (not set)")
            else:
                # Truncate long values
                val_str = str(value)
                if len(val_str) > 50:
                    val_str = val_str[:47] + "..."
                print(f"  {param:25s} = {val_str}")


if __name__ == "__main__":
    main()