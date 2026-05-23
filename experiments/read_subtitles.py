"""
read_subtitles.py — Day 7 exploration
Resolve timeline ka subtitle track Python se read karna.

Usage: python3 read_subtitles.py
"""

import sys
sys.path.insert(0, "/Users/kamil/Code/davinci-tools/subtitle-styler")

RESOLVE_SCRIPT_API = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
sys.path.insert(0, f"{RESOLVE_SCRIPT_API}/Modules")

import DaVinciResolveScript as dvr_script


def main():
    resolve = dvr_script.scriptapp("Resolve")
    if not resolve:
        print("❌ Resolve nahi mila")
        sys.exit(1)
    
    print("=" * 60)
    print("SUBTITLE TRACK EXPLORATION")
    print("=" * 60)
    
    # Get project + timeline
    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    if not project:
        print("❌ Koi project khula nahi hai")
        sys.exit(1)
    
    print(f"📁 Project: {project.GetName()}")
    
    timeline = project.GetCurrentTimeline()
    if not timeline:
        print("❌ Koi timeline active nahi")
        sys.exit(1)
    
    print(f"🎬 Timeline: {timeline.GetName()}")
    
    # Track type counts
    print("\nTrack counts:")
    for track_type in ["video", "audio", "subtitle"]:
        count = timeline.GetTrackCount(track_type)
        print(f"  {track_type}: {count} track(s)")
    
    # Subtitle track explore
    subtitle_count = timeline.GetTrackCount("subtitle")
    
    if subtitle_count == 0:
        print("\n⚠️ Koi subtitle track nahi mila timeline mein")
        print("Resolve mein 'Create Subtitles from Audio' chala pehle")
        sys.exit(0)
    
    print(f"\n📝 Found {subtitle_count} subtitle track(s)")
    
    # Iterate through subtitle tracks
    for track_idx in range(1, subtitle_count + 1):
        print(f"\n{'='*60}")
        print(f"SUBTITLE TRACK #{track_idx}")
        print(f"{'='*60}")
        
        # Get items in this track
        items = timeline.GetItemListInTrack("subtitle", track_idx)
        
        if not items:
            print("  (empty track)")
            continue
        
        print(f"\n  Total subtitle clips: {len(items)}")
        
        # Iterate items
        for i, item in enumerate(items, 1):
            try:
                name = item.GetName() if hasattr(item, "GetName") else "?"
                start = item.GetStart() if hasattr(item, "GetStart") else "?"
                end = item.GetEnd() if hasattr(item, "GetEnd") else "?"
                duration = item.GetDuration() if hasattr(item, "GetDuration") else "?"
                
                print(f"\n  [{i}] Name: {name}")
                print(f"      Start: {start} frames")
                print(f"      End: {end} frames")
                print(f"      Duration: {duration} frames")
                
                # Try to get subtitle text
                # Resolve API: GetClipProperty() ya getter methods
                if hasattr(item, "GetClipProperty"):
                    props = item.GetClipProperty()
                    if props:
                        for k, v in props.items():
                            if "text" in str(k).lower() or "subtitle" in str(k).lower():
                                print(f"      {k}: {v}")
                
                # Check all available methods
                if i == 1:  # First item ke liye full method list
                    methods = [m for m in dir(item) if not m.startswith("_") and callable(getattr(item, m, None))]
                    print(f"\n      [Available methods (first 20)]: {methods[:20]}")
                
            except Exception as e:
                print(f"  Error reading item {i}: {e}")


if __name__ == "__main__":
    main()