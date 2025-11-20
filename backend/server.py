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

app = FastAPI(
    title="Dining Hall API",
    description="Backend API for dining hall food recommendations with AI-generated images",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

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
    """Load CSV data - check for existing images, use Unsplash placeholder if not available"""
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

            # Check if AI-generated image already exists
            generated_filename = image_generator.generate_filename(food_name, dining_hall)
            generated_path = image_generator.images_dir / generated_filename

            filename = None
            image_url = None

            # Priority 1: Check if AI-generated image exists
            if generated_path.exists():
                filename = generated_filename
                image_url = f"/images/{filename}"
                print(f"✓ Using generated image: {filename}")
            # Priority 2: Check if custom image path is provided
            elif image_path and pd.notna(image_path) and str(image_path).strip() and str(image_path).lower() != 'na':
                provided_path = Path(image_path)
                if provided_path.exists():
                    filename = provided_path.name
                    image_url = f"/images/{filename}"
                    print(f"✓ Using custom image: {filename}")
                else:
                    # Use Unsplash placeholder
                    image_url = f"https://source.unsplash.com/400x400/?{food_name.replace(' ', '+')},food"
                    print(f"⊙ Using placeholder for: {food_name}")
            else:
                # Use Unsplash placeholder
                image_url = f"https://source.unsplash.com/400x400/?{food_name.replace(' ', '+')},food"
                print(f"⊙ Using placeholder for: {food_name}")

            # Create unique key
            key = f"{food_name}_{dining_hall}"

            # Store in database
            food_database[key] = {
                "id": key,
                "name": food_name,
                "diningHall": dining_hall,
                "calories": int(calories) if pd.notna(calories) else 0,
                "image_url": image_url,
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


@app.get("/", tags=["Status"])
async def root():
    """
    Get API status and total items count

    Returns:
        - message: API name
        - total_items: Number of food items loaded
    """
    return {"message": "Dining Hall API", "total_items": len(food_database)}


@app.get("/api/foods", response_model=List[Dict], tags=["Foods"])
async def get_all_foods():
    """
    Get all food items with images and dining hall information

    Returns a list of food items, each containing:
        - id: Unique identifier (food_name_diningHall)
        - name: Name of the food item
        - diningHall: Which dining hall serves this item
        - calories: Calorie count
        - image_url: URL to the AI-generated image
        - filename: Image filename
    """
    return list(food_database.values())


@app.get("/api/reload", tags=["Admin"])
async def reload_data():
    """
    Reload CSV data and regenerate missing images

    This endpoint will:
        - Clear the current database
        - Reload data from dataset/nov19.csv
        - Generate images for items without existing images

    Returns:
        - message: Status message
        - total_items: Number of items processed
    """
    food_database.clear()
    load_and_process_data()
    return {"message": "Data reloaded", "total_items": len(food_database)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
