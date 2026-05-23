"""
test_insert_title.py — Day 9 Block 2
Test: timeline.InsertFusionTitleIntoTimeline()

Goal: Subtitle clip ke time pe Fusion Title insert kare.
"""

import sys
sys.path.insert(0, "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules")

import DaVinciResolveScript as dvr_script


def main():
    resolve = dvr_script.scriptapp("Resolve")
    project = resolve.GetProjectManager().GetCurrentProject()
    timeline = project.GetCurrentTimeline()
    
    print("=" * 60)
    print("INSERT FUSION TITLE — exploration")
    print("=" * 60)
    
    # Try inspecting the method
    method = timeline.InsertFusionTitleIntoTimeline
    print(f"\n✅ Method exists: {method}")
    
    # Check docstring
    if hasattr(method, "__doc__") and method.__doc__:
        print(f"\n📖 Docstring:\n{method.__doc__}")
    
    # Get video track count BEFORE
    before_video = timeline.GetTrackCount("video")
    print(f"\n📊 BEFORE:")
    print(f"   Video tracks: {before_video}")
    
    # Try call with no args
    print(f"\n🧪 Test 1: InsertFusionTitleIntoTimeline() — no args")
    try:
        result = timeline.InsertFusionTitleIntoTimeline()
        print(f"   Return: {result}")
        print(f"   Type: {type(result).__name__}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Get video track count AFTER
    after_video = timeline.GetTrackCount("video")
    print(f"\n📊 AFTER:")
    print(f"   Video tracks: {after_video}")
    
    # Check what's on V1, V2 now
    print(f"\n📋 Items on each video track:")
    for v_idx in range(1, after_video + 1):
        items = timeline.GetItemListInTrack("video", v_idx)
        if items:
            print(f"   V{v_idx}: {len(items)} item(s)")
            for item in items:
                name = item.GetName() if hasattr(item, "GetName") else "?"
                start = item.GetStart() if hasattr(item, "GetStart") else "?"
                duration = item.GetDuration() if hasattr(item, "GetDuration") else "?"
                print(f"     - {name} (start: {start}, dur: {duration})")


if __name__ == "__main__":
    main()