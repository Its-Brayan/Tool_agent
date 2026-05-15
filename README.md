# Tool Agent

A simple AI agent built with LangGraph that uses Groq's Llama model and Tavily web search to answer questions.

## Features

- Integrates with Groq's Llama-3.1-8B model for reasoning
- Uses Tavily search tool for web-based information retrieval
- Built using LangGraph for state management and flow control

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Tool_Agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with:
   ```
   GROQ_API_KEY=your_groq_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

## Usage

Run the agent:
```bash
python app.py
```

The agent will process a sample query about "What is the price of fuel as of today?" and print the response.

## Requirements

- Python 3.8+
- API keys for Groq and Tavily services

## Dependencies

See `requirements.txt` for a full list of dependencies.