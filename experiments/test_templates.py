"""
test_templates.py — Apply templates from JSON files
Production pattern: choose template, apply with custom text.

Usage: python3 test_templates.py
"""

import sys
sys.path.insert(0, "/Users/kamil/Code/davinci-tools/subtitle-styler")

from core import (
    get_resolve_terminal,
    get_fusion_and_comp,
    find_text_tools,
    write_text_style,
    backup_text_style,
    load_template,
    template_to_style,
    list_templates,
    disable_all_shading_elements,
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
    
    # List available templates
    templates = list_templates()
    if not templates:
        print("⚠️  Koi template nahi mila templates/ folder mein")
        sys.exit(0)
    
    print("=" * 60)
    print("🎨 TEMPLATE APPLIER")
    print("=" * 60)
    print("\nAvailable templates:")
    for i, t in enumerate(templates, 1):
        td = load_template(t)
        print(f"  {i}. {t}: {td.get('name', '?')}")
    
    # User chooses
    while True:
        choice = input(f"\nChoose template (1-{len(templates)}): ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(templates):
                chosen = templates[idx]
                break
        except ValueError:
            pass
        print("⚠️  Valid number daal.")
    
    # Custom text input
    print()
    text = input("Subtitle text (Hindi/English): ").strip()
    if not text:
        text = "नमूना सबटाइटल"  # Default Hindi sample
    
    # Apply
    template_data = load_template(chosen)
    style = template_to_style(template_data, text=text)
    
    idx, name, tool = text_tools[0]
    
    print()
    print(f"📝 Target: {name}")
    print(f"📋 Template: {template_data.get('name', chosen)}")
    print(f"🎯 Text: {text}")
    print(f"🎨 Applying {len(style)} parameters...")
    
    # Backup
    backup_path = backup_text_style(tool, comp, name_prefix=f"pre_{chosen}")
    
    # Clean slate — disable all elements first
    print("🧹 Disabling all shading elements (clean slate)...")
    disabled = disable_all_shading_elements(tool, comp)
    print(f"   Disabled: {disabled}")
    
    # Apply new template
    applied, failed = write_text_style(tool, comp, style)
    
    print(f"\n✅ Applied: {applied}")
    if failed:
        print(f"⚠️  Failed: {len(failed)}")
    
    print(f"💾 Backup: {backup_path.name}")


if __name__ == "__main__":
    main()