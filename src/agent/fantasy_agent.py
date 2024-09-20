import os
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI
from langchain.tools import Tool

from tools.stats_retriever import StatsRetriever
from tools.web_search import WebSearch
from tools.team_manager import TeamManager
from tools.trade_evaluator import TradeEvaluator
from tools.waiver_wire import WaiverWire

class FantasyFootballAgent:
    def __init__(self):
        # Initialize tools
        self.stats_retriever = StatsRetriever()
        self.web_search = WebSearch(api_key=os.getenv('AI_SEARCH_API_KEY'))
        self.team_manager = TeamManager(
            api_key=os.getenv('CBS_API_KEY'),
            username=os.getenv('CBS_USERNAME'),
            password=os.getenv('CBS_PASSWORD')
        )
        self.trade_evaluator = TradeEvaluator()
        self.waiver_wire = WaiverWire()

        # Define tools for the agent
        tools = [
            Tool(
                name='GetPlayerStats',
                func=self.stats_retriever.get_player_stats,
                description='Use this to get statistics for a player.'
            ),
            Tool(
                name='SearchNews',
                func=self.web_search.search,
                description='Use this to search for the latest news about players.'
            ),
            Tool(
                name='ManageTeam',
                func=self.team_manager.manage_team,
                description='Use this to manage your team roster.'
            ),
            Tool(
                name='EvaluateTrade',
                func=self.trade_evaluator.evaluate_trade,
                description='Use this to evaluate potential trades.'
            ),
            Tool(
                name='CheckWaiverWire',
                func=self.waiver_wire.check_waiver_wire,
                description='Use this to check the waiver wire for hot players.'
            ),
        ]

        # Initialize the language model (LLM)
        llm = OpenAI(
            temperature=0,
            openai_api_key=os.getenv('OPENAI_API_KEY')  # Ensure you have set this environment variable
        )

        # Initialize the agent with the tools
        self.agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

    def run(self, user_input):
        # Process the user input through the agent
        response = self.agent.run(user_input)
        return response
