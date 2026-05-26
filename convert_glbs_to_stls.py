import bpy
import os
import sys
import traceback

# ---- USER DEFAULT CONFIG (used only if GUI does not pass folders) ----
INPUT_FOLDER = r"C:/comfy/output"
OUTPUT_FOLDER = r"C:/comfy/output/raw stls"
TARGET_SIZE = 1.0  # largest dimension -> 1 meter
# --------------------------------------------------------------------

# If launched from GUI, override folders
if len(sys.argv) >= 2:
    try:
        INPUT_FOLDER = sys.argv[-2]
        OUTPUT_FOLDER = sys.argv[-1]
        print(f"\n📁 Using GUI folders:\n  Input:  {INPUT_FOLDER}\n  Output: {OUTPUT_FOLDER}\n")
    except:
        print("⚠ Failed to read GUI folder args, falling back to defaults.")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def center_and_scale():
    objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    if not objs:
        return None

    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]

    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

    for o in objs:
        o.location = (0, 0, 0)

    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # bounding box measurement
    xs, ys, zs = [], [], []
    for o in objs:
        for v in o.bound_box:
            xs.append(v[0])
            ys.append(v[1])
            zs.append(v[2])

    size = max(max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
    if size == 0:
        return objs[0]

    scale_factor = TARGET_SIZE / size

    for o in objs:
        o.scale = (scale_factor, scale_factor, scale_factor)

    bpy.ops.object.transform_apply(scale=True)
    bpy.context.view_layer.update()

    return objs[0]


def process_glb_to_stl(glb_path, out_path):
    print(f"Converting: {glb_path}")

    bpy.ops.wm.read_factory_settings(use_empty=True)

    try:
        bpy.ops.import_scene.gltf(filepath=glb_path)
        bpy.context.view_layer.update()
    except Exception:
        print("❌ Failed to import GLB")
        traceback.print_exc()
        return False

    obj = center_and_scale()
    if not obj:
        print("⚠ No mesh found after import")
        return False

    try:
        bpy.ops.wm.stl_export(filepath=out_path)
        print("Saved:", out_path)
        return True
    except Exception:
        print("❌ Failed to export STL")
        traceback.print_exc()
        return False


# ---- MAIN LOOP ----
for file in os.listdir(INPUT_FOLDER):
    if file.lower().endswith(".glb"):

        glb_path = os.path.join(INPUT_FOLDER, file)
        name_no_ext = os.path.splitext(file)[0]
        out_path = os.path.join(OUTPUT_FOLDER, name_no_ext + ".stl")

        try:
            success = process_glb_to_stl(glb_path, out_path)
            if not success:
                print("⚠ Skipping due to error:", file)
        except Exception:
            print("🔥 Unexpected failure:", file)
            traceback.print_exc()

print("\nDONE — all GLBs processed.\n")

