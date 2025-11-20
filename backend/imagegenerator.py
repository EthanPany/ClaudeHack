import os
import requests
from openai import OpenAI
from pathlib import Path

class ImageGenerator:
    def __init__(self, images_dir="images"):
        self.images_dir = Path(images_dir)
        self.images_dir.mkdir(exist_ok=True)
        self.api_key = os.getenv("OPENAI_API_KEY")
        self._client = None

    @property
    def client(self):
        """Lazy-load OpenAI client"""
        if self._client is None and self.api_key:
            self._client = OpenAI(api_key=self.api_key)
        return self._client

    def generate_filename(self, food_name, dining_hall):
        """Generate a safe filename from food name and dining hall"""
        # Clean the strings and combine them
        clean_food = "".join(c if c.isalnum() else "_" for c in food_name.lower())
        clean_hall = "".join(c if c.isalnum() else "_" for c in dining_hall.lower())
        return f"{clean_food}_{clean_hall}.png"

    def image_exists(self, filename):
        """Check if an image already exists"""
        return (self.images_dir / filename).exists()

    def generate_image(self, food_name, dining_hall):
        """Generate an image for a food item if it doesn't exist"""
        filename = self.generate_filename(food_name, dining_hall)
        filepath = self.images_dir / filename

        # Skip if image already exists
        if filepath.exists():
            print(f"✓ Image already exists: {filename}")
            return filename

        # Check if API key is available
        if not self.api_key:
            print(f"⊘ Skipping image generation (no API key): {food_name}")
            return None

        # Generate image using DALL-E 2 (faster and cheaper)
        try:
            print(f"Generating image for: {food_name} from {dining_hall}...")
            response = self.client.images.generate(
                model="dall-e-2",
                prompt=f"A delicious, appetizing photo of {food_name} with a small wiscosin madison badge",
                size="256x256",
                n=1,
            )

            # Download and save the image
            image_url = response.data[0].url
            image_data = requests.get(image_url).content

            with open(filepath, 'wb') as f:
                f.write(image_data)

            print(f"✓ Generated: {filename}")
            return filename

        except Exception as e:
            print(f"✗ Error generating image for {food_name}: {str(e)}")
            return None
