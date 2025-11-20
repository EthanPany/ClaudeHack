# Dining Hall Backend API

FastAPI backend for dining hall food recommendations with AI-generated food images using DALL-E 3.

## Quick Start

### Prerequisites
- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- OpenAI API key

### Installation & Setup

1. **Install dependencies using uv:**
   ```bash
   cd backend
   uv sync
   ```

2. **Set up your OpenAI API key:**

   Create a `.env` file:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

### Running the Server

Start the development server with auto-reload:
```bash
uv run uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

The server will be available at **http://localhost:8000**

On startup, the server will:
- Load food items from `dataset/nov19.csv`
- Generate AI images for items that don't have images yet (using DALL-E 3)
- Store images in the `images/` folder
- Index all items in an in-memory database

## API Documentation

### Interactive API Docs

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

#### `GET /`
Get API status and total items count

**Response:**
```json
{
  "message": "Dining Hall API",
  "total_items": 105
}
```

#### `GET /api/foods`
Get all food items with images and dining hall information

**Response:**
```json
[
  {
    "id": "Sunrise Special Smoothie_Four Lakes Market",
    "name": "Sunrise Special Smoothie",
    "diningHall": "Four Lakes Market",
    "calories": 219,
    "image_url": "/images/sunrise_special_smoothie_four_lakes_market.png",
    "filename": "sunrise_special_smoothie_four_lakes_market.png"
  }
]
```

#### `GET /api/reload`
Reload CSV data and regenerate missing images

**Response:**
```json
{
  "message": "Data reloaded",
  "total_items": 105
}
```

#### `GET /images/{filename}`
Serve AI-generated food images

**Example:**
```
http://localhost:8000/images/sunrise_special_smoothie_four_lakes_market.png
```

## Data Format

The CSV file (`dataset/nov19.csv`) should have these columns:

| Column | Type | Description |
|--------|------|-------------|
| `name` | string | Name of the food item |
| `diningHall` | string | Name of the dining hall |
| `calories` | integer | Calorie count |
| `image_path` | string | Path to existing image or "na" to generate |

**Example:**
```csv
name,diningHall,calories,image_path
Pizza,North Campus Dining,450,na
Burger,South Campus Dining,650,na
Grilled Salmon,West Campus Dining,320,images/custom_salmon.png
```

## Features

- **AI Image Generation**: Automatically generates food images using DALL-E 3 with professional food photography prompts
- **Smart Caching**: Only generates images if they don't already exist
- **Fast Indexing**: In-memory hashmap for O(1) lookups
- **CORS Enabled**: Ready for frontend integration
- **Auto-reload**: Development server watches for code changes

## Project Structure

```
backend/
├── server.py              # FastAPI application
├── imagegenerator.py      # DALL-E 3 image generation
├── pyproject.toml         # uv dependencies
├── .env                   # Environment variables (not committed)
├── .gitignore            # Git ignore rules
├── dataset/
│   └── nov19.csv         # Food items data
└── images/               # Generated images (not committed)
    └── .gitkeep
```

## Testing

Use the included Postman collection:
```bash
# Import postman_collection.json into Postman
```

Or use curl:
```bash
# Get all foods
curl http://localhost:8000/api/foods

# Check server status
curl http://localhost:8000/

# Reload data
curl http://localhost:8000/api/reload
```

## Troubleshooting

**Images not generating?**
- Check that `OPENAI_API_KEY` is set in `.env`
- Verify the API key has access to DALL-E 3
- Check server logs for error messages

**CSV not loading?**
- Ensure `dataset/nov19.csv` exists
- Check CSV format matches the schema above

**Port already in use?**
- Change the port: `uv run uvicorn server:app --port 8001`
- Or kill existing process: `lsof -ti:8000 | xargs kill -9`
