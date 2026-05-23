"""
explore_timeline_methods.py — Day 9 Block 1
Timeline pe Fusion Composition / gap clip kaise add karte — explore.
"""

import sys
sys.path.insert(0, "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules")

import DaVinciResolveScript as dvr_script


def main():
    resolve = dvr_script.scriptapp("Resolve")
    project = resolve.GetProjectManager().GetCurrentProject()
    timeline = project.GetCurrentTimeline()
    media_pool = project.GetMediaPool()
    
    print("=" * 60)
    print("TIMELINE + MEDIA POOL — adding items exploration")
    print("=" * 60)
    
    # Timeline methods
    print("\n🎬 TIMELINE METHODS (add/insert related):")
    timeline_methods = [m for m in dir(timeline) if not m.startswith("_")]
    relevant = [m for m in timeline_methods if any(kw in m.lower() for kw in [
        "add", "insert", "create", "import", "fusion"
    ])]
    for m in relevant:
        print(f"  timeline.{m}")
    
    # Media pool methods
    print("\n📦 MEDIA POOL METHODS (add/insert related):")
    pool_methods = [m for m in dir(media_pool) if not m.startswith("_")]
    relevant_pool = [m for m in pool_methods if any(kw in m.lower() for kw in [
        "add", "insert", "create", "import", "fusion"
    ])]
    for m in relevant_pool:
        print(f"  media_pool.{m}")
    
    # Check track count
    print(f"\n📊 TIMELINE STATE:")
    for track_type in ["video", "audio", "subtitle"]:
        count = timeline.GetTrackCount(track_type)
        print(f"  {track_type}: {count} track(s)")
    
    # Try: Can we add an empty Fusion Composition clip?
    print("\n🧪 TEST: Add Fusion Composition to timeline")
    
    if hasattr(media_pool, "AddSubTitleToTimeline"):
        print("  ✅ AddSubTitleToTimeline method exists")
    
    # Common method for Fusion comp creation
    if hasattr(media_pool, "CreateEmptyTimeline"):
        print("  ✅ CreateEmptyTimeline exists")
    
    # Check available methods to spot Fusion composition creation
    print("\n  Looking for 'fusion' / 'composition' methods on media_pool:")
    for m in pool_methods:
        if "fusion" in m.lower() or "composition" in m.lower() or "title" in m.lower():
            print(f"    {m}")
    
    # Same on project
    print("\n  On project:")
    proj_methods = [m for m in dir(project) if not m.startswith("_")]
    for m in proj_methods:
        if "fusion" in m.lower() or "composition" in m.lower():
            print(f"    project.{m}")


if __name__ == "__main__":
    main()