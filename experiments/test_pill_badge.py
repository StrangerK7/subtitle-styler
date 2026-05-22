"""
test_pill_badge.py — Apply Hinglish Pill Badge style
First real product capability of Subtitle Styler!

Usage: python3 test_pill_badge.py (Fusion page with Text+ node)
"""

import sys
sys.path.insert(0, "/Users/kamil/Code/davinci-tools/subtitle-styler")

from core import (
    get_resolve_terminal,
    get_fusion_and_comp,
    find_text_tools,
    write_text_style,
    backup_text_style,
    make_hinglish_badge_style,
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
    
    print("=" * 60)
    print("🎨 HINGLISH PILL BADGE TEST")
    print("=" * 60)
    print(f"\n📝 Target: {name}")
    
    # Backup
    print("\n💾 Backup save kar raha hoon...")
    backup_path = backup_text_style(tool, comp, name_prefix="pre_pill")
    print(f"   Saved: {backup_path.name}")
    
    # Define style
    badge_text = "ये भविष्यवाणी हैरान कर देगी"
    print(f"\n🎯 Text: {badge_text}")
    
    style = make_hinglish_badge_style(
        text=badge_text,
        font="Kohinoor Devanagari",  # Hindi font
    )
    
    print(f"\n🎨 Applying {len(style)} parameters...")
    
    # Apply
    applied, failed = write_text_style(tool, comp, style)
    
    print(f"\n✅ Applied: {applied}")
    if failed:
        print(f"⚠️  Failed: {len(failed)}")
        for f in failed:
            print(f"   - {f}")
    
    print()
    print("=" * 60)
    print(f"🔄 Restore: {backup_path.name}")
    print("=" * 60)


if __name__ == "__main__":
    main()