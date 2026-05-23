"""
explore_subtitle_methods.py — Day 8 deep exploration
Subtitle clip pe konse methods available hain — read/write/modify.

Usage: python3 explore_subtitle_methods.py
"""

import sys
sys.path.insert(0, "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules")

import DaVinciResolveScript as dvr_script


def main():
    resolve = dvr_script.scriptapp("Resolve")
    if not resolve:
        print("❌ Resolve nahi mila")
        sys.exit(1)
    
    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    if not project:
        print("❌ Project nahi mila")
        sys.exit(1)
    
    timeline = project.GetCurrentTimeline()
    if not timeline:
        print("❌ Timeline nahi mila")
        sys.exit(1)
    
    print("=" * 60)
    print("SUBTITLE CLIP METHODS EXPLORATION")
    print("=" * 60)
    
    # Get first subtitle item
    items = timeline.GetItemListInTrack("subtitle", 1)
    if not items:
        print("⚠️ Koi subtitle clip nahi mila")
        sys.exit(0)
    
    first_item = items[0]
    print(f"\n📝 First subtitle: '{first_item.GetName()}'")
    print(f"   Type: {type(first_item).__name__}")
    
    # ALL methods (not just callable)
    print("\n" + "=" * 60)
    print("ALL ATTRIBUTES + METHODS:")
    print("=" * 60)
    
    all_attrs = dir(first_item)
    
    # Categorize
    getters = []
    setters = []
    others = []
    
    for attr in all_attrs:
        if attr.startswith("_"):
            continue
        if attr.startswith("Get"):
            getters.append(attr)
        elif attr.startswith("Set"):
            setters.append(attr)
        else:
            others.append(attr)
    
    print(f"\n🔍 GETTERS ({len(getters)}):")
    for g in getters:
        print(f"   {g}")
    
    print(f"\n✏️ SETTERS ({len(setters)}):")
    for s in setters:
        print(f"   {s}")
    
    print(f"\n🔧 OTHER METHODS ({len(others)}):")
    for o in others:
        print(f"   {o}")
    
    # Try calling each Setter with safe args
    print("\n" + "=" * 60)
    print("SETTER METHODS — signatures (if accessible):")
    print("=" * 60)
    
    for setter_name in setters:
        try:
            method = getattr(first_item, setter_name)
            # Check if callable
            if callable(method):
                doc = method.__doc__ if hasattr(method, '__doc__') else ""
                print(f"\n  {setter_name}()")
                if doc:
                    print(f"    Doc: {doc[:200]}")
        except Exception as e:
            print(f"  {setter_name}: Error - {e}")
    
    # Timeline methods exploration
    print("\n" + "=" * 60)
    print("TIMELINE OBJECT METHODS:")
    print("=" * 60)
    
    timeline_attrs = [a for a in dir(timeline) if not a.startswith("_")]
    relevant = [a for a in timeline_attrs if any(kw in a.lower() for kw in [
        "subtitle", "caption", "transcrib", "audio", "import", "export"
    ])]
    
    print(f"\nRelevant timeline methods (subtitle/audio related):")
    for m in relevant:
        print(f"  timeline.{m}")
    
    # Project methods
    print("\n" + "=" * 60)
    print("PROJECT OBJECT METHODS (transcription related):")
    print("=" * 60)
    
    project_attrs = [a for a in dir(project) if not a.startswith("_")]
    relevant_proj = [a for a in project_attrs if any(kw in a.lower() for kw in [
        "subtitle", "caption", "transcrib", "audio"
    ])]
    
    for m in relevant_proj:
        print(f"  project.{m}")


if __name__ == "__main__":
    main()