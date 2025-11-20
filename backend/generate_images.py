"""
Background script to generate images for all food items in the CSV.
Run this separately from the server to generate images without blocking the API.

Usage:
    uv run python generate_images.py
"""

import pandas as pd
from pathlib import Path
from imagegenerator import ImageGenerator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Generate images for all food items that don't have them yet"""

    csv_path = Path("dataset/nov19.csv")
    image_generator = ImageGenerator("images")

    if not csv_path.exists():
        print("❌ Error: dataset/nov19.csv not found")
        return

    # Read CSV
    df = pd.read_csv(csv_path)
    print(f"📊 Loaded {len(df)} items from CSV")
    print(f"🎨 Starting image generation...\n")

    generated_count = 0
    skipped_count = 0
    error_count = 0

    for idx, row in df.iterrows():
        food_name = str(row.get('name', f'Item {idx}'))
        dining_hall = str(row.get('diningHall', 'Unknown Hall'))

        # Check if image already exists
        filename = image_generator.generate_filename(food_name, dining_hall)
        filepath = image_generator.images_dir / filename

        if filepath.exists():
            skipped_count += 1
            continue

        # Generate image
        print(f"[{idx + 1}/{len(df)}] Generating: {food_name}")
        result = image_generator.generate_image(food_name, dining_hall)

        if result:
            generated_count += 1
        else:
            error_count += 1

        # Show progress
        if (idx + 1) % 10 == 0:
            print(f"\n📈 Progress: {idx + 1}/{len(df)} items processed")
            print(f"   ✓ Generated: {generated_count}")
            print(f"   ⊙ Skipped: {skipped_count}")
            print(f"   ✗ Errors: {error_count}\n")

    # Final summary
    print("\n" + "="*50)
    print("🎉 Image Generation Complete!")
    print("="*50)
    print(f"Total items: {len(df)}")
    print(f"✓ Generated: {generated_count}")
    print(f"⊙ Skipped (already exist): {skipped_count}")
    print(f"✗ Errors: {error_count}")
    print("="*50)

if __name__ == "__main__":
    main()
