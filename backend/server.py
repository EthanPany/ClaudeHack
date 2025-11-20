from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path
from imagegenerator import ImageGenerator
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Dining Hall API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Internal data structure to store food items
food_database: Dict[str, Dict] = {}
image_generator = ImageGenerator("images")

# Mount images folder for static file serving
app.mount("/images", StaticFiles(directory="images"), name="images")


def load_and_process_data():
    """Load CSV data and generate missing images"""
    csv_path = Path("dataset/nov19.csv")

    if not csv_path.exists():
        print("Warning: CSV file not found")
        return

    try:
        # Read CSV file
        df = pd.read_csv(csv_path)

        # Check if CSV is empty
        if df.empty:
            print("Warning: CSV file is empty")
            return

        print(f"Loaded {len(df)} items from CSV")

        # Process each food item
        for idx, row in df.iterrows():
            food_name = str(row.get('name', f'Item {idx}'))
            dining_hall = str(row.get('diningHall', 'Unknown Hall'))
            calories = row.get('calories', 0)
            image_path = row.get('image_path', '')

            # Check if image_path is provided and file exists (skip "na" values)
            filename = None
            if image_path and pd.notna(image_path) and str(image_path).strip() and str(image_path).lower() != 'na':
                # Use provided image path
                provided_path = Path(image_path)
                if provided_path.exists():
                    filename = provided_path.name
                    print(f"✓ Using existing image: {filename}")
                else:
                    print(f"⚠ Image path not found, will generate: {image_path}")
                    filename = image_generator.generate_image(food_name, dining_hall)
            else:
                # Generate image if it doesn't exist
                filename = image_generator.generate_image(food_name, dining_hall)

            # Create unique key
            key = f"{food_name}_{dining_hall}"

            # Store in database
            food_database[key] = {
                "id": key,
                "name": food_name,
                "diningHall": dining_hall,
                "calories": int(calories) if pd.notna(calories) else 0,
                "image_url": f"/images/{filename}" if filename else None,
                "filename": filename
            }

        print(f" Processed {len(food_database)} food items")

    except Exception as e:
        print(f"Error loading CSV: {str(e)}")


@app.on_event("startup")
async def startup_event():
    """Run on server startup"""
    print("Starting server...")
    load_and_process_data()
    print("Server ready!")


@app.get("/")
async def root():
    return {"message": "Dining Hall API", "total_items": len(food_database)}


@app.get("/api/foods", response_model=List[Dict])
async def get_all_foods():
    """Get all food items with image URLs and dining hall information"""
    return list(food_database.values())


@app.get("/api/reload")
async def reload_data():
    """Reload CSV and regenerate missing images"""
    food_database.clear()
    load_and_process_data()
    return {"message": "Data reloaded", "total_items": len(food_database)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
