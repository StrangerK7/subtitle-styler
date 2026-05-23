"""
test_textplus_overlay.py — Day 9 Block 3
Text+ overlay insert + Fusion comp access + style application proof.

Goal: ONE subtitle ko styled Text+ overlay mein convert karna.
"""

import sys
sys.path.insert(0, "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules")

import DaVinciResolveScript as dvr_script


def main():
    resolve = dvr_script.scriptapp("Resolve")
    project = resolve.GetProjectManager().GetCurrentProject()
    timeline = project.GetCurrentTimeline()
    
    print("=" * 60)
    print("TEXT+ OVERLAY DEEP TEST")
    print("=" * 60)
    
    # Step 1: Get first subtitle's text
    subs = timeline.GetItemListInTrack("subtitle", 1)
    if not subs:
        print("❌ No subtitles")
        sys.exit(1)
    
    first_sub = subs[0]
    sub_text = first_sub.GetName()
    sub_start = first_sub.GetStart()
    sub_duration = first_sub.GetDuration()
    print(f"\n📝 First subtitle:")
    print(f"   Text: '{sub_text}'")
    print(f"   Start: {sub_start}")
    print(f"   Duration: {sub_duration}")
    
    # Step 2: Insert Text+ on timeline (playhead position)
    print(f"\n🧪 Inserting Text+ at playhead...")
    text_item = timeline.InsertFusionTitleIntoTimeline("Text+")
    
    if not text_item:
        print("   ❌ Insert failed")
        sys.exit(1)
    
    print(f"   ✅ Inserted: {text_item.GetName()}")
    print(f"   Start: {text_item.GetStart()}")
    print(f"   Duration: {text_item.GetDuration()}")
    
    # Step 3: Access Fusion comp inside the Text+ item
    print(f"\n🎬 Accessing Fusion comp...")
    comp_count = text_item.GetFusionCompCount()
    print(f"   Fusion comp count: {comp_count}")
    
    if comp_count == 0:
        print("   ❌ No comp inside")
        sys.exit(1)
    
    comp = text_item.GetFusionCompByIndex(1)
    if not comp:
        print("   ❌ Couldn't get comp")
        sys.exit(1)
    
    print(f"   ✅ Got comp: {type(comp).__name__}")
    
    # Step 4: List tools in the comp
    print(f"\n🔧 Tools in comp:")
    tools = comp.GetToolList()
    if tools:
        for idx, tool in tools.items():
            name = tool.GetAttrs().get("TOOLS_Name", "?")
            reg_id = tool.GetAttrs().get("TOOLS_RegID", "?")
            print(f"   [{idx}] {name} ({reg_id})")
    
    # Step 5: Find the Text+ tool
    text_tool = None
    if tools:
        for idx, tool in tools.items():
            reg_id = tool.GetAttrs().get("TOOLS_RegID", "")
            if reg_id == "TextPlus":
                text_tool = tool
                break
    
    if text_tool:
        print(f"\n✅ Found Text+ tool!")
        
        # Read current text
        current_text = text_tool.GetInput("StyledText")
        print(f"   Current StyledText: '{current_text}'")
        
        # Set to subtitle text
        print(f"\n   Setting StyledText to: '{sub_text}'")
        result = text_tool.SetInput("StyledText", sub_text)
        print(f"   SetInput result: {result}")
        
        # Verify
        new_text = text_tool.GetInput("StyledText")
        print(f"   New StyledText: '{new_text}'")
        
        if new_text == sub_text:
            print("   ⭐⭐⭐ TEXT SUCCESSFULLY APPLIED!")
    else:
        print("   ❌ Text+ tool not found")


if __name__ == "__main__":
    main()