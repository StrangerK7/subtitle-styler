"""
test_subtitle_edit.py — Day 8 Block 1
Subtitle text edit karne ka test.

CRITICAL: Yeh test timeline pe ACTUALLY changes karega.
Backup recommended pehle.
"""

import sys
sys.path.insert(0, "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules")

import DaVinciResolveScript as dvr_script


def main():
    resolve = dvr_script.scriptapp("Resolve")
    project = resolve.GetProjectManager().GetCurrentProject()
    timeline = project.GetCurrentTimeline()
    
    print("=" * 50)
    print("SUBTITLE EDIT TEST")
    print("=" * 50)
    
    # Get first subtitle item
    items = timeline.GetItemListInTrack("subtitle", 1)
    if not items:
        print("❌ Koi subtitle nahi mila")
        sys.exit(1)
    
    first_item = items[0]
    original_text = first_item.GetName()
    print(f"\n📝 Original text: '{original_text}'")
    
    # Test 1: SetName() with new text
    test_text = "TEST EDIT — Day 8"
    print(f"\n🧪 Test 1: SetName('{test_text}')")
    
    try:
        result = first_item.SetName(test_text)
        print(f"   Return value: {result}")
        
        # Verify
        new_name = first_item.GetName()
        print(f"   New text after SetName: '{new_name}'")
        
        if new_name == test_text:
            print("   ✅ SetName WORKING — text successfully changed!")
        elif new_name == original_text:
            print("   ❌ SetName failed — text NOT changed")
        else:
            print(f"   ⚠️ Unexpected: text changed but not to expected value")
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Restore original (cleanup)
    print(f"\n🔄 Restoring original text...")
    try:
        first_item.SetName(original_text)
        restored = first_item.GetName()
        if restored == original_text:
            print(f"   ✅ Restored: '{restored}'")
        else:
            print(f"   ⚠️ Restore mismatch: '{restored}'")
    except Exception as e:
        print(f"   ❌ Restore error: {e}")


if __name__ == "__main__":
    main()