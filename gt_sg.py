from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": False})

import numpy as np
from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.prims import RigidPrimView
from omni.physx import get_physx_interface
import carb
from pxr import Usd, UsdGeom, Semantics, Gf

# Initialize the world
my_world = World(stage_units_in_meters=1.0)
asset_path = "/home/zhang/.local/share/ov/pkg/isaac-sim-4.0.0/gt/s.usd"
add_reference_to_stage(usd_path=asset_path, prim_path="/World/env")

# Enable physics and initialize
my_world._physics_context.enable_gpu_dynamics(True)
my_world.initialize_physics()

# List of prim paths to inspect
prim_paths = [
    "/World/env/Cube",
    # Add more prim paths as needed
]

# Create RigidPrimView list
prim_views = []
for path in prim_paths:
    view = RigidPrimView(prim_paths_expr=path, name=f"{path.split('/')[-1]}_view")
    my_world.scene.add(view)
    prim_views.append(view)

# Add ground plane
my_world.reset()
my_world.scene.add_default_ground_plane()

def get_prim_info(prim_path):
    """Retrieve prim's position, orientation, bounding box and semantic information"""
    stage = my_world.stage
    prim = stage.GetPrimAtPath(prim_path)
    
    if not prim.IsValid():
        print(f"Prim at path {prim_path} is not valid")
        return None
    
    # Get transform information
    xform = UsdGeom.Xformable(prim)
    time = Usd.TimeCode.Default()
    world_transform = xform.ComputeLocalToWorldTransform(time)
    translation = world_transform.ExtractTranslation()
    rotation = world_transform.ExtractRotationQuat()
    
    # Get bounding box
    bbox = UsdGeom.Boundable(prim).ComputeWorldBound(time, UsdGeom.Tokens.default_)
    bbox_range = bbox.GetRange()
    bbox_size = bbox_range.GetSize()
    
    # Get semantic information
    semantic = Semantics.SemanticsAPI.Get(prim, "Semantics")
    semantic_data = {
        "type": semantic.GetSemanticTypeAttr().Get(),
        "data": semantic.GetSemanticDataAttr().Get()
    } if semantic else None
    
    return {
        "path": prim_path,
        "position": translation,
        "orientation": rotation,
        "bbox_size": bbox_size,
        "semantic": semantic_data
    }

def print_prim_info(prim_info):
    """Print formatted prim information"""
    print(f"\nPrim Path: {prim_info['path']}")
    print(f"Position: {prim_info['position']}")
    print(f"Orientation (quaternion): {prim_info['orientation']}")
    print(f"Bounding Box Size: {prim_info['bbox_size']}")
    if prim_info['semantic']:
        print(f"Semantic Type: {prim_info['semantic']['type']}")
        print(f"Semantic Data: {prim_info['semantic']['data']}")
    else:
        print("No semantic information available")

# Main simulation loop
frame_count = 0
while simulation_app.is_running():
    my_world.step(render=True)
    
    # Print information every 60 frames
    frame_count += 1
    if frame_count % 60 == 0:
        print("\n" + "="*50)
        print(f"Frame {frame_count} - Object Information")
        print("="*50)
        
        for path in prim_paths:
            prim_info = get_prim_info(path)
            if prim_info:
                print_prim_info(prim_info)

simulation_app.close()