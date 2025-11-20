# Dining Hall Backend

Simple FastAPI backend for dining hall recommendation app.

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Set up your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

Or export it:
```bash
export OPENAI_API_KEY=your_key_here
```

## Running the Server

```bash
uv run uvicorn server:app --reload
```

The server will:
- Read food items from `dataset/nov19.csv`
- Generate images for items that don't have images yet
- Store images in the `images/` folder
- Serve API at http://localhost:8000

## API Endpoints

- `GET /` - Server info
- `GET /api/foods` - Get all food items with images and dining hall info
- `GET /api/reload` - Reload CSV and regenerate missing images
- `GET /images/{filename}` - Serve generated images

## CSV Format

The CSV file should have at least these columns:
- `food_name` - Name of the food item
- `dining_hall` - Name of the dining hall

Example:
```csv
food_name,dining_hall
Pizza,North Campus Dining
Burger,South Campus Dining
```
