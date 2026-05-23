"""
explore_subtitle_fusion.py — Day 9 Block 1
Subtitle clip ka Fusion composition explore karna.

Goal: Pata lagana subtitle clip ke saath kaise Text+ node add hota.
"""

import sys
sys.path.insert(0, "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules")

import DaVinciResolveScript as dvr_script


def main():
    resolve = dvr_script.scriptapp("Resolve")
    project = resolve.GetProjectManager().GetCurrentProject()
    timeline = project.GetCurrentTimeline()
    
    print("=" * 60)
    print("SUBTITLE → FUSION EXPLORATION")
    print("=" * 60)
    
    items = timeline.GetItemListInTrack("subtitle", 1)
    if not items:
        print("❌ Koi subtitle nahi mila")
        sys.exit(1)
    
    print(f"\n📝 {len(items)} subtitle clips found\n")
    
    # First subtitle item — full investigation
    first = items[0]
    print(f"Investigating: '{first.GetName()}'")
    print("=" * 60)
    
    # Check Fusion-related methods (from Day 8 exploration we saw):
    # - GetFusionCompByIndex
    # - GetFusionCompByName
    # - GetFusionCompCount
    # - GetFusionCompNameList
    # - AddFusionComp
    
    fusion_count = first.GetFusionCompCount()
    print(f"\n🎬 Fusion comp count: {fusion_count}")
    
    if fusion_count > 0:
        names = first.GetFusionCompNameList()
        print(f"   Names: {names}")
        
        # Try get first comp
        comp = first.GetFusionCompByIndex(1)
        if comp:
            print(f"\n✅ Got Fusion comp via index 1")
            print(f"   Type: {type(comp).__name__}")
            
            # Get tools in comp
            tools = comp.GetToolList()
            print(f"\n🔧 Tools in comp: {len(tools) if tools else 0}")
            
            if tools:
                for idx, tool in tools.items():
                    name = tool.GetAttrs().get("TOOLS_Name", "?")
                    reg_id = tool.GetAttrs().get("TOOLS_RegID", "?")
                    print(f"   [{idx}] {name} ({reg_id})")
    else:
        print("\n⚠️ No Fusion comp on subtitle clip")
        print("   Trying AddFusionComp...")
        
        try:
            new_comp = first.AddFusionComp()
            if new_comp:
                print(f"   ✅ AddFusionComp returned: {type(new_comp).__name__}")
                
                # Check tools in new comp
                tools = new_comp.GetToolList()
                print(f"   Tools after add: {len(tools) if tools else 0}")
                
                if tools:
                    for idx, tool in tools.items():
                        name = tool.GetAttrs().get("TOOLS_Name", "?")
                        reg_id = tool.GetAttrs().get("TOOLS_RegID", "?")
                        print(f"     [{idx}] {name} ({reg_id})")
            else:
                print("   ❌ AddFusionComp returned None")
        except Exception as e:
            print(f"   ❌ AddFusionComp error: {e}")
    
    # Check methods on comp object (if we got one)
    print("\n" + "=" * 60)
    print("COMP OBJECT — tool creation methods:")
    print("=" * 60)
    
    if fusion_count > 0:
        comp = first.GetFusionCompByIndex(1)
        if comp:
            methods = [m for m in dir(comp) if not m.startswith("_")]
            
            # Filter for tool creation related
            relevant = [m for m in methods if any(kw in m.lower() for kw in [
                "add", "create", "insert", "tool", "text"
            ])]
            
            print(f"\nRelevant methods ({len(relevant)}):")
            for m in relevant:
                print(f"  comp.{m}")


if __name__ == "__main__":
    main()