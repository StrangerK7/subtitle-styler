"""
write_hindi.py — Apply Hindi text + Devanagari font test
Usage: python3 write_hindi.py (Fusion page with Text+ node)
"""

import sys
sys.path.insert(0, "/Users/kamil/Code/davinci-tools/subtitle-styler")

from core import (
    get_resolve_terminal,
    get_fusion_and_comp,
    find_text_tools,
    read_text_style,
    write_text_style,
    backup_text_style,
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
    
    # Pehle Text+ node pe apply karenge
    idx, name, tool = text_tools[0]
    
    print("=" * 50)
    print("HINDI TEXT + DEVANAGARI FONT TEST")
    print("=" * 50)
    print(f"\n📝 Target: {name}")
    
    # Step 1: Backup current state
    print("\n💾 Backup save kar raha hoon...")
    backup_path = backup_text_style(tool, comp, name_prefix="pre_hindi")
    print(f"   Saved: {backup_path.name}")
    
    # Step 2: Define new style — Hindi text with Devanagari font
    print("\n🎨 Applying Hindi style...")
    
    new_style = {
        "Styled Text": "नमस्ते दुनिया",  # "Hello World" in Hindi
        "Font": "Kohinoor Devanagari",
        "Style": "Bold",
        "Size": 0.08,
        "Red 1": 1.0,
        "Green 1": 0.6,    # warm orange tint
        "Blue 1": 0.2,
        "Alpha 1": 1.0,
    }
    
    print("\nNew style:")
    for k, v in new_style.items():
        print(f"  {k:25s} = {v}")
    
    # Step 3: Apply
    print("\n🔧 Writing to Text+ node...")
    applied, failed = write_text_style(tool, comp, new_style)
    
    print(f"\n✅ Applied: {applied}")
    if failed:
        print(f"⚠️  Failed: {len(failed)}")
        for f in failed:
            print(f"   - {f}")
    
    print()
    print("=" * 50)
    print(f"🔄 Restore: backup file = {backup_path.name}")
    print("=" * 50)


if __name__ == "__main__":
    main()