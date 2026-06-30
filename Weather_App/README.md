<div align="center">

# 🌤️ Weather Agent

**A conversational AI agent that turns natural-language weather questions into real-time, human-readable answers.**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Groq](https://img.shields.io/badge/LLM-Groq%20%7C%20LLaMA%203-orange?style=flat)](https://groq.com)
[![Open-Meteo](https://img.shields.io/badge/Data-Open--Meteo%20API-blue?style=flat)](https://open-meteo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## Overview

Weather Agent is an LLM-powered assistant that lets users ask weather questions in plain English — *"Will it rain in Chennai tomorrow?"* or *"What's it like in Tokyo this weekend?"* — and get a clear, conversational answer grounded in live data.

The project was built to explore practical, end-to-end agent design: combining a low-latency LLM with a real-time external API, handling ambiguous user input, and producing reliable, grounded responses rather than hallucinated ones.

## Why This Project

This agent demonstrates core skills relevant to applied AI engineering:

- **Tool-augmented LLM design** — the model doesn't guess weather data, it retrieves and reasons over real API responses.
- **Prompt engineering** — structured prompts translate free-form user input into precise API parameters (location, date range, intent).
- **API integration** — geocoding and live weather retrieval via Open-Meteo, with no paid dependencies.
- **Fast inference** — built on Groq's LLaMA 3 for low-latency conversational responses.
- **Clean, modular architecture** — separation between query understanding, data retrieval, and response generation.

## Demo

```
You: What's the weather in Chennai right now?
Agent: It's currently 31°C and partly cloudy in Chennai, with humidity at 68%.

You: Should I carry an umbrella tomorrow?
Agent: Yes — there's a high chance of rain in Chennai tomorrow afternoon,
        with temperatures around 27°C. Better safe than sorry!
```

## Architecture

```
User Query
    │
    ▼
┌─────────────────────┐
│  Query Understanding │  → LLM (Groq/LLaMA 3) extracts location, intent, date
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│   Geocoding Layer    │  → Resolves place name → lat/lon
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Weather Retrieval   │  → Open-Meteo API call
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ Response Generation  │  → LLM formats data into natural language
└─────────────────────┘
    │
    ▼
Conversational Reply
```

## Tech Stack

| Layer | Technology |
|---|---|
| LLM Inference | Groq API (LLaMA 3) |
| Weather Data | Open-Meteo API (free, no key required) |
| Language | Python |
| Environment Config | python-dotenv |

## Getting Started

### Prerequisites

- Python 3.9+
- A free [Groq API key](https://console.groq.com)

### Installation

```bash
git clone https://github.com/Thenmozhi-codes/weather-ai-agent.git
cd weather_App
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

### Run

```bash
python app.py
```

## Project Structure

```
weather_App/
├── app.py              # Entry point / chat loop
├── tool.py             # Core agent logic and LLM orchestration
├── weather_api.py        # Open-Meteo integration
├── requirements.txt
├── .gitignore
└── README.md
```

## Roadmap

- [ ] Multi-day forecast support
- [ ] Unit preference toggle (°C / °F)
- [ ] Voice input/output
- [ ] Severe weather alerts
- [ ] Deploy as a web app (Streamlit/Gradio)

## About

Built as a hands-on project to deepen practical understanding of LLM agent design — from prompt construction to API orchestration — as part of ongoing work toward a career in AI development.

**Author:** Thenmozhi Sivanesan 

## License

MIT License — free to use, modify, and build on.

## Acknowledgments

- [Groq](https://groq.com) for fast LLM inference
- [Open-Meteo](https://open-meteo.com) for free, reliable weather data
---
⭐ If you like this project, consider giving it a Star
