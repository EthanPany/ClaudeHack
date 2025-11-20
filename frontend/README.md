# Dining Hall Guide - Frontend

A beautiful React application for discovering dining hall foods and getting AI-powered recommendations using Claude.

## Features

- **Food Browser**: Browse all available foods with beautiful cards showing images, calories, and dining hall locations
- **Selection System**: Click on food cards to select items you're interested in
- **AI Chat Assistant**: Get personalized dining hall recommendations based on your selections
- **Smart Recommendations**: AI automatically suggests the best dining hall based on your food choices

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Backend server running on `http://localhost:8000`
- Anthropic API key for Claude AI

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Anthropic API key:
   ```
   VITE_ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

The app will be available at **http://localhost:3000**

## Usage

1. **Browse Foods**: On the home page, you'll see cards for all available foods from various dining halls
2. **Select Items**: Click on any food cards to select items you like (selected cards will show a checkmark)
3. **Get Recommendations**: Once you've selected foods, click "Get AI Recommendations" to go to the chat
4. **Chat with AI**: The AI will analyze your selections and recommend the best dining hall, plus answer any questions

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── FoodCards.jsx          # Food browsing and selection
│   │   ├── FoodCards.css
│   │   ├── ChatInterface.jsx      # AI chat interface
│   │   └── ChatInterface.css
│   ├── App.jsx                    # Main app with routing
│   ├── App.css
│   ├── main.jsx                   # Entry point
│   └── index.css
├── index.html
├── vite.config.js
├── package.json
└── .env.example
```

## API Integration

The frontend connects to the backend API at `http://localhost:8000`:

- `GET /api/foods` - Fetch all food items
- `GET /images/{filename}` - Load food images

API calls are proxied through Vite dev server (configured in `vite.config.js`).

## Environment Variables

- `VITE_ANTHROPIC_API_KEY` - Your Anthropic API key for Claude AI chat

## Technologies Used

- **React 19** - UI framework
- **React Router** - Navigation
- **Vite** - Build tool and dev server
- **Anthropic SDK** - Claude AI integration
- **CSS3** - Styling with gradients and animations

## Development

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Notes

- Make sure the backend server is running before starting the frontend
- The app uses `dangerouslyAllowBrowser: true` for the Anthropic SDK - this is fine for local development but should use a backend proxy in production
- Food selection state is maintained in the App component and shared between pages
