# Fantasy Football AI Agent

This project is an AI agent designed to help you manage your fantasy football team. It utilizes LangChain to integrate various tools, including statistics retrieval, web search for the latest news, team management, trade evaluation, and waiver wire monitoring.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Tools](#tools)
- [Data](#data)
- [License](#license)

## Features

- **Statistics Retrieval**: Access and analyze player stats from provided data frames.
- **Web Search**: Get the latest news and updates on players using an AI-powered search service.
- **Team Management**: Interact with your CBS dynasty PPR league to get and update your team roster.
- **Trade Evaluation**: Analyze potential trades to maximize your team's performance.
- **Waiver Wire Monitoring**: Check available players and place waiver claims when a player becomes valuable.

## Requirements

- Python 3.8 or higher
- [LangChain](https://github.com/hwchase17/langchain)
- Required Python packages (listed in `requirements.txt`)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/fantasy_football_ai.git
   cd fantasy_football_ai
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **API Keys**

   - **OpenAI API Key**: Sign up for an OpenAI account and obtain an API key.
   - **Web Search Tool**: Sign up for the AI-powered search service (e.g., [Perplexity AI](https://www.perplexity.ai/)) and obtain an API key.
   - **Team Management Tool**: Ensure you have access to the CBS Sports API and obtain necessary credentials.

2. **Environment Variables**

   Create a `.env` file in the root directory with the following:

   ```dotenv
   OPENAI_API_KEY=your_openai_api_key
   AI_SEARCH_API_KEY=your_ai_search_api_key
   CBS_API_KEY=your_cbs_api_key
   CBS_USERNAME=your_cbs_username
   CBS_PASSWORD=your_cbs_password
   ```

## Usage

Run the main script to start the AI agent:

```bash
python main.py
```

## Tools

- **Fantasy Agent (`agent/fantasy_agent.py`)**

  Implements the AI agent using LangChain, integrating all tools and providing a natural language interface.

- **Stats Retriever (`tools/stats_retriever.py`)**

  Retrieves and processes player statistics from the provided data frames.

- **Web Search (`tools/web_search.py`)**

  Uses an AI-powered search service to fetch the latest news on players.

- **Team Manager (`tools/team_manager.py`)**

  Interacts with the CBS Sports API to manage your team roster.

- **Trade Evaluator (`tools/trade_evaluator.py`)**

  Analyzes potential trades based on player performance and projections.

- **Waiver Wire Monitor (`tools/waiver_wire.py`)**

  Checks for available players and places waiver claims when necessary.

## Data

- **Stats DataFrames (`data/stats_dataframes.py`)**

  Contains the data frames with player statistics and other relevant data.

## License

This project is licensed under the MIT License.