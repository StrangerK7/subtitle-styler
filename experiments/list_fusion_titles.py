"""
list_fusion_titles.py — Day 9
Available Fusion Titles ki list dhoondhna.
"""

import sys
sys.path.insert(0, "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules")

import DaVinciResolveScript as dvr_script


def main():
    resolve = dvr_script.scriptapp("Resolve")
    
    print("=" * 60)
    print("FUSION TITLES — exploration")
    print("=" * 60)
    
    # Try different ways to list available titles
    
    # Method 1: Resolve has GetMediaStorage
    print("\n🔍 Method 1: Direct resolve attributes")
    resolve_methods = [m for m in dir(resolve) if not m.startswith("_")]
    relevant = [m for m in resolve_methods if any(kw in m.lower() for kw in [
        "title", "fusion", "preset", "list"
    ])]
    for m in relevant:
        print(f"  resolve.{m}")
    
    # Method 2: Project might have it
    project = resolve.GetProjectManager().GetCurrentProject()
    print("\n🔍 Method 2: Project attributes")
    proj_methods = [m for m in dir(project) if not m.startswith("_")]
    relevant_p = [m for m in proj_methods if any(kw in m.lower() for kw in [
        "title", "fusion", "preset", "list"
    ])]
    for m in relevant_p:
        print(f"  project.{m}")
    
    # Method 3: Try common Fusion title names
    timeline = project.GetCurrentTimeline()
    
    common_titles = [
        "Text+",
        "Text",
        "Basic Title",
        "Title",
        "Subtitle",
    ]
    
    print("\n🧪 Test: Try common title names")
    for title_name in common_titles:
        try:
            result = timeline.InsertFusionTitleIntoTimeline(title_name)
            print(f"  '{title_name}' → {result}")
        except Exception as e:
            print(f"  '{title_name}' → Error: {e}")


if __name__ == "__main__":
    main()