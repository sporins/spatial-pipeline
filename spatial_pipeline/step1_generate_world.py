import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MARBLE_API_KEY")
BASE_URL = "https://api.worldlabs.ai/marble/v1"
HEADERS = {"WLT-Api-Key": API_KEY, "Content-Type": "application/json"}

def generate_world(prompt):
    print(f"Generating world: {prompt}")
    response = requests.post(
        f"{BASE_URL}/worlds:generate",
        headers=HEADERS,
        json={
            "display_name": "Test World",
            "world_prompt": {
                "type": "text",
                "text_prompt": prompt
            }
        }
    )
    response.raise_for_status()
    return response.json()

def poll_operation(operation_id):
    print(f"Polling operation: {operation_id}")
    while True:
        response = requests.get(
            f"{BASE_URL}/operations/{operation_id}",
            headers=HEADERS
        )
        response.raise_for_status()
        data = response.json()
        status = data.get("metadata", {}).get("progress", {}).get("status")
        print(f"Status: {status}")
        if data.get("done"):
            return data
        time.sleep(15)

def download_mesh(url, save_path):
    print(f"Downloading collider mesh...")
    response = requests.get(url)
    response.raise_for_status()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(response.content)
    print(f"Saved mesh to: {save_path}")

if __name__ == "__main__":
    operation = generate_world("A simple indoor shopping mall with clear walkways and stores")
    operation_id = operation["operation_id"]
    result = poll_operation(operation_id)
    world = result["response"]
    world_id = world["world_id"]
    mesh_url = world["assets"]["mesh"]["collider_mesh_url"]
    print(f"World ID: {world_id}")
    print(f"Mesh URL: {mesh_url}")
    download_mesh(mesh_url, f"spatial_pipeline/meshes/{world_id}.glb")
    print("Done! World generated and mesh downloaded successfully.")
