import os
from PIL import Image, ImageDraw

# CONFIG
INPUT_IMAGE_PATH = "370_1631703165.100000011.png"
OUTPUT_ROOT = "data/datasets/hazard_crops"
CROP_SIZE = 256
HAZARD_SIZE = (80, 150) # (width, height) of the person/hazard

def prepare_test_data():
    # 1. Load Original
    if not os.path.exists(INPUT_IMAGE_PATH):
        print(f"Error: Could not find {INPUT_IMAGE_PATH}")
        return
        
    img = Image.open(INPUT_IMAGE_PATH).convert("RGB")
    w, h = img.size

    # 2. Define where to crop (e.g., Center-ish bottom)
    # Adjust these coords to point to the TRACKS in your image
    center_x = w // 2
    center_y = h // 2 + 100 
    
    left = center_x - (CROP_SIZE // 2)
    top = center_y - (CROP_SIZE // 2)
    right = left + CROP_SIZE
    bottom = top + CROP_SIZE
    
    # 3. Crop the 256x256 patch
    crop = img.crop((left, top, right, bottom))
    
    # 4. Create the Mask
    # WHITE (255) = KEEP (Background)
    # BLACK (0)   = GENERATE (The Hole)
    mask = Image.new("L", (CROP_SIZE, CROP_SIZE), 255)
    draw = ImageDraw.Draw(mask)
    
    # Draw a black rectangle in the center where the person should go
    # We put it slightly lower so feet touch the ground, not floating
    box_w, box_h = HAZARD_SIZE
    box_x = (CROP_SIZE - box_w) // 2
    box_y = (CROP_SIZE - box_h) // 2 + 20 
    
    draw.rectangle(
        [box_x, box_y, box_x + box_w, box_y + box_h], 
        fill=0 # Black
    )

    # 5. Save
    img_out = os.path.join(OUTPUT_ROOT, "images", "test_01.png")
    mask_out = os.path.join(OUTPUT_ROOT, "masks", "test_01.png")
    
    crop.save(img_out)
    mask.save(mask_out)
    
    print(f"Saved Crop: {img_out}")
    print(f"Saved Mask: {mask_out}")
    print("Ready to run test.py")

if __name__ == "__main__":
    prepare_test_data()