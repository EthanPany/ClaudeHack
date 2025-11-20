# Quick Start Guide

Get the Dining Hall API running in 3 minutes.

## Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) installed
- OpenAI API key

## Setup

### 1. Install Dependencies

```bash
cd backend
uv sync
```

### 2. Configure API Key

```bash
# Create .env file
cp .env.example .env

# Add your OpenAI API key to .env
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

### 3. Run the Server

```bash
uv run uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

**Server running at:** http://localhost:8000

## Test It

### Browser
Open http://localhost:8000/docs for interactive API docs

### Terminal
```bash
# Check status
curl http://localhost:8000/

# Get all foods
curl http://localhost:8000/api/foods | python -m json.tool | head -50
```

## What Happens on Startup

1. Server loads `dataset/nov19.csv` (105 food items)
2. Checks which items need images
3. Generates missing images using DALL-E 3
4. API becomes available at `/api/foods`

**Note:** Initial startup may take time as images are generated (16/105 generated currently).

## Next Steps

- **View Docs:** http://localhost:8000/docs
- **Import Postman:** `postman_collection.json`
- **Read Full Docs:** See [API_DOCS.md](API_DOCS.md)
- **README:** See [README.md](README.md)

## Common Commands

```bash
# Start server
uv run uvicorn server:app --host 0.0.0.0 --port 8000 --reload

# Run in background
uv run uvicorn server:app --host 0.0.0.0 --port 8000 &

# Check running servers
lsof -ti:8000

# Stop server
lsof -ti:8000 | xargs kill -9
```

## Troubleshooting

**Port 8000 in use?**
```bash
lsof -ti:8000 | xargs kill -9
```

**Images not generating?**
- Check `.env` has valid `OPENAI_API_KEY`
- Check server logs for errors

**CSV changes not reflected?**
```bash
curl http://localhost:8000/api/reload
```

---

**Need help?** Check [README.md](README.md) or [API_DOCS.md](API_DOCS.md)
