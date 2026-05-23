"""
test_auto_transcribe.py — Day 8 Block 2
Resolve ka CreateSubtitlesFromAudio() trigger karne ka test.

Yeh API auto-transcription chalata — agar Python se chala 
to Desi Captions ka core feature unlock ho jayega.
"""

import sys
sys.path.insert(0, "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules")

import DaVinciResolveScript as dvr_script


def main():
    resolve = dvr_script.scriptapp("Resolve")
    project = resolve.GetProjectManager().GetCurrentProject()
    timeline = project.GetCurrentTimeline()
    
    print("=" * 60)
    print("AUTO-TRANSCRIBE TEST — CreateSubtitlesFromAudio")
    print("=" * 60)
    
    # Check method exists
    if not hasattr(timeline, "CreateSubtitlesFromAudio"):
        print("❌ CreateSubtitlesFromAudio method nahi mila")
        sys.exit(1)
    
    method = timeline.CreateSubtitlesFromAudio
    print(f"\n✅ Method exists: {method}")
    
    # Try to get docstring
    if hasattr(method, "__doc__"):
        doc = method.__doc__
        if doc:
            print(f"\n📖 Documentation:\n{doc}")
    
    # Check current subtitle count BEFORE
    before_count = timeline.GetTrackCount("subtitle")
    before_items = timeline.GetItemListInTrack("subtitle", 1) if before_count > 0 else []
    print(f"\n📊 BEFORE:")
    print(f"   Subtitle tracks: {before_count}")
    print(f"   Subtitle clips: {len(before_items)}")
    
    # Test 1: Call with no arguments
    print(f"\n🧪 Test 1: CreateSubtitlesFromAudio() — no args")
    try:
        result = timeline.CreateSubtitlesFromAudio()
        print(f"   Return: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Check AFTER
    after_count = timeline.GetTrackCount("subtitle")
    after_items = timeline.GetItemListInTrack("subtitle", 1) if after_count > 0 else []
    print(f"\n📊 AFTER (no-args call):")
    print(f"   Subtitle tracks: {after_count}")
    print(f"   Subtitle clips: {len(after_items)}")
    
    # Test 2: Try with language parameter (common Resolve pattern)
    print(f"\n🧪 Test 2: CreateSubtitlesFromAudio with language dict")
    try:
        # Common Resolve API pattern — dict of options
        options = {"language": "en"}
        result = timeline.CreateSubtitlesFromAudio(options)
        print(f"   Return: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Try with language string directly
    print(f"\n🧪 Test 3: CreateSubtitlesFromAudio('en') — string arg")
    try:
        result = timeline.CreateSubtitlesFromAudio("en")
        print(f"   Return: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")


if __name__ == "__main__":
    main()