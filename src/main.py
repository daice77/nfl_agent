import os
from langgraph import Agent, Tool
from tools.stats_retriever import StatsRetriever
from tools.web_search import WebSearch
from tools.team_manager import TeamManager
from tools.trade_evaluator import TradeEvaluator
from tools.waiver_wire import WaiverWire

def main():
    # Initialize tools
    stats_retriever = StatsRetriever()
    web_search = WebSearch(api_key=os.getenv('AI_SEARCH_API_KEY'))
    team_manager = TeamManager(
        api_key=os.getenv('CBS_API_KEY'),
        username=os.getenv('CBS_USERNAME'),
        password=os.getenv('CBS_PASSWORD')
    )
    trade_evaluator = TradeEvaluator()
    waiver_wire = WaiverWire()

    # Create LangGraph agent
    agent = Agent(
        tools=[
            Tool(name='StatsRetriever', func=stats_retriever.get_player_stats, description='Retrieve player stats'),
            Tool(name='WebSearch', func=web_search.search, description='Fetch latest news on players'),
            Tool(name='TeamManager', func=team_manager.manage_team, description='Manage team roster'),
            Tool(name='TradeEvaluator', func=trade_evaluator.evaluate_trade, description='Evaluate potential trades'),
            Tool(name='WaiverWire', func=waiver_wire.check_waiver_wire, description='Monitor waiver wire'),
        ]
    )

    # Start interaction
    print("Welcome to the Fantasy Football AI Agent!")
    while True:
        user_input = input("\nHow can I assist you? (Type 'exit' to quit)\n")
        if user_input.lower() == 'exit':
            break
        response = agent.run(user_input)
        print(f"\n{response}")

if __name__ == '__main__':
    main()