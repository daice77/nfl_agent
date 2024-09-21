import logging
import os
import uuid
from typing import Annotated, Optional

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import AnyMessage, add_messages
from tools.stats_retriever import StatsRetriever
from tools.team_manager import TeamManager
from tools.trade_evaluator import TradeEvaluator
from tools.waiver_wire import WaiverWire
from tools.web_search import WebSearch
from typing_extensions import TypedDict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# def update_dialog_stack(left: list[str], right: Optional[str]) -> list[str]:
#     if right is None:
#         return left
#     if right == "pop":
#         return left[:-1]
#     return left + [right]


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    user_info: str
    # dialog_state: Annotated[
    #     list[Literal["main_assistant", "stats", "news", "trade", "waiver", "team"]],
    #     update_dialog_stack,
    # ]


# Initialize tools
stats_retriever = StatsRetriever()
web_search = WebSearch(api_key=os.getenv("AI_SEARCH_API_KEY"))
trade_evaluator = TradeEvaluator()
waiver_wire = WaiverWire()
team_manager = TeamManager(
    api_key=os.getenv("CBS_API_KEY"),
    username=os.getenv("CBS_USERNAME"),
    password=os.getenv("CBS_PASSWORD"),
)

# Define tools using Tool class
tools = [
    Tool(
        name="GetStats",
        func=stats_retriever.get_stats,
        description="Retrieve various statistics for players, teams, drafts, officials, schedules, injuries, and snap counts.",
    ),
    Tool(
        name="SearchNews",
        func=web_search.search,
        description="Search for latest player news",
    ),
    Tool(
        name="EvaluateTrade",
        func=trade_evaluator.evaluate_trade,
        description="Evaluate potential trades",
    ),
    Tool(
        name="CheckWaiverWire",
        func=waiver_wire.check_waiver_wire,
        description="Check the waiver wire for hot players",
    ),
    Tool(
        name="ManageTeam",
        func=team_manager.manage_team,
        description="Manage your fantasy team roster",
    ),
]

# LLM setup
llm = ChatOpenAI(
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-3.5-turbo",
)

# Prompt templates
main_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """\
You are an advanced NFL fantasy football AI assistant.
Your role is to understand user queries and route them to the appropriate specialized assistant or use the relevant tool.
Do not attempt to answer queries directly unless they are general greetings or clarifications.

Available specialized assistants and tools:
- Stats Assistant (GetStats tool): For player and team statistics
- News Assistant (SearchNews tool): For latest news and updates
- Trade Assistant (EvaluateTrade tool): For trade analysis
- Waiver Assistant (CheckWaiverWire tool): For waiver wire recommendations
- Team Management Assistant (ManageTeam tool): For roster and lineup management

When a user query comes in, identify the most appropriate assistant or tool and specify it in your response. For example:
- For statistics queries: "Routing to Stats Assistant for detailed statistics."
- For news queries: "Routing to News Assistant for the latest updates."
- For trade analysis: "Routing to Trade Assistant for trade evaluation."
- For waiver wire help: "Routing to Waiver Assistant for waiver wire recommendations."
- For team management: "Routing to Team Management Assistant for roster advice."

If the query is unclear or doesn't match any specific assistant, ask for clarification.""",
        ),
        ("human", "{input}"),
    ]
)

stats_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """\
You are a statistics expert for NFL fantasy football. Your role is to provide detailed, accurate player and team statistics and analyze performance trends.
Focus on relevant fantasy metrics such as targets, red zone usage, snap counts, and efficiency stats.

When providing stats:
1. Use the GetStats tool to retrieve the most current data available. You can query for player stats, team stats, draft information, schedules, injuries, and more.
2. Clarify the time period (e.g., last game, last 3 games, season to date).
3. Compare to league averages or positional rankings when relevant.
4. Highlight any significant trends or changes in usage/performance.
5. Consider the impact of factors like injuries to teammates, changes in coaching, or upcoming matchups.

Example queries for the GetStats tool:
- GetStats: player [player name]
- GetStats: team [team abbreviation]
- GetStats: draft picks season [year]
- GetStats: officials game [game id]
- GetStats: schedules season [year]
- GetStats: injuries team [team abbreviation]
- GetStats: snap counts season [year]

Remember to interpret and analyze the statistics, don't just list them. Provide insights that would be valuable for fantasy football managers.""",
        ),
        ("human", "{input}"),
    ]
)

news_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """\
You are a news and updates specialist for NFL fantasy football.
Your role is to provide the latest, most relevant news that could impact a player's fantasy value.
This includes injury updates, depth chart changes, trade rumors, and coaching decisions.

When delivering news:
1. Use the SearchNews tool to find the most recent and reliable information.
2. Prioritize information that has a direct fantasy impact.
3. Provide context on how the news might affect the player's performance or opportunity.
4. Suggest potential actions the fantasy manager might consider (e.g., bench, trade, pick up a handcuff).
5. Always include the source and timing of the news.""",
        ),
        ("human", "{input}"),
    ]
)

trade_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """\
You are a trade analysis expert for NFL fantasy football.
Your role is to evaluate trade offers and provide insights on their fairness and strategic value.
Consider both short-term and long-term implications of trades.

When evaluating trades:
1. Use the EvaluateTrade tool to get data-driven insights on trade values.
2. Assess the value of each player involved, considering their performance, upcoming schedule, and injury risk.
3. Consider the specific needs of the user's team (e.g., positional strengths/weaknesses).
4. Analyze how the trade might impact the team's weekly scoring potential and consistency.
5. Suggest counter-offers if the initial trade seems unfair or suboptimal.
6. Remind users to consider trade deadlines and playoff implications when relevant.""",
        ),
        ("human", "{input}"),
    ]
)

waiver_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """\
You are a waiver wire and free agent specialist for NFL fantasy football.
Your role is to identify valuable pickups and provide advice on FAAB (Free Agent Acquisition Budget) bidding or waiver priority.

When recommending waiver wire moves:
1. Use the CheckWaiverWire tool to get up-to-date information on available players and their potential value.
2. Identify players with increasing opportunity (due to injuries, depth chart changes, etc.).
3. Consider upcoming matchups and strength of schedule.
4. Analyze trends in player usage and efficiency.
5. Suggest drop candidates from the user's team if they need to make room.
6. Provide context on how much FAAB to bid or how to prioritize waiver claims.""",
        ),
        ("human", "{input}"),
    ]
)

team_management_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a team management expert for NFL fantasy football. Your role is to help users optimize their roster, set lineups, and make strategic team decisions.

When assisting with team management:
1. Use the ManageTeam tool to view and update the user's roster.
2. Provide advice on optimal lineup settings based on matchups, injuries, and recent performance.
3. Suggest add/drop moves to improve the overall team strength.
4. Consider bye weeks and playoff schedules when making recommendations.
5. Advise on when to stash players with future potential.
6. Help users understand and navigate league-specific rules and settings.""",
        ),
        ("human", "{input}"),
    ]
)


class Assistant:
    def __init__(
        self,
        prompt_template: ChatPromptTemplate,
        tool: Optional[Tool] = None,
        name: str = "Unnamed",
    ):
        self.prompt_template = prompt_template
        self.tool = tool
        self.name = name

    def __call__(self, state: State) -> State:
        try:
            messages = state["messages"]
            system_message = self.prompt_template.messages[0]
            task_description = system_message.prompt.template
            user_input = (
                messages[-1].content if isinstance(messages[-1], HumanMessage) else ""
            )
            prompt = f"{task_description}\n{user_input}"

            logger.info(f"{self.name} received input: {user_input}")

            response = llm.invoke([{"role": "user", "content": prompt}])
            if isinstance(response, AIMessage):
                ai_content = response.content
            else:
                ai_content = str(response)

            logger.info(f"{self.name} response: {ai_content}")

            messages.append(AIMessage(content=ai_content))

            if self.tool and self.should_use_tool(ai_content):
                tool_response = self.use_tool(user_input)
                if tool_response:
                    logger.info(
                        f"{self.name} used tool {self.tool.name}. Response: {tool_response}"
                    )
                    messages.append(
                        AIMessage(content=f"Tool response: {tool_response}")
                    )
                    interpretation_prompt = f"{task_description}\nTool response: {tool_response}\nPlease interpret this data and provide insights for the user."
                    interpretation = llm.invoke(
                        [{"role": "user", "content": interpretation_prompt}]
                    )
                    if isinstance(interpretation, AIMessage):
                        interpretation_content = interpretation.content
                    else:
                        interpretation_content = str(interpretation)

                    logger.info(
                        f"{self.name} interpretation of tool response: {interpretation_content}"
                    )
                    messages.append(AIMessage(content=interpretation_content))

            state["messages"] = messages
            return state
        except Exception as e:
            logger.error(f"Error in {self.name}: {str(e)}", exc_info=True)
            return state

    def use_tool(self, user_input: str) -> Optional[str]:
        if self.tool:
            try:
                return self.tool.func(user_input)
            except Exception as e:
                logger.error(
                    f"Error using tool {self.tool.name} in {self.name}: {str(e)}"
                )
        return None

    def should_use_tool(self, response: str) -> bool:
        return self.tool is not None and self.tool.name.lower() in response.lower()


# Specialized assistant definitions
main_assistant = Assistant(prompt_template=main_assistant_prompt, name="Main Assistant")
stats_assistant = Assistant(
    prompt_template=stats_assistant_prompt, tool=tools[0], name="Stats Assistant"
)
news_assistant = Assistant(
    prompt_template=news_assistant_prompt, tool=tools[1], name="News Assistant"
)
trade_assistant = Assistant(
    prompt_template=trade_assistant_prompt, tool=tools[2], name="Trade Assistant"
)
waiver_assistant = Assistant(
    prompt_template=waiver_assistant_prompt, tool=tools[3], name="Waiver Assistant"
)
team_management_assistant = Assistant(
    prompt_template=team_management_prompt,
    tool=tools[4],
    name="Team Management Assistant",
)
# Graph definition
graph = StateGraph(State)

# Add nodes
graph.add_node("main_assistant", main_assistant)
graph.add_node("stats_assistant", stats_assistant)
graph.add_node("news_assistant", news_assistant)
graph.add_node("trade_assistant", trade_assistant)
graph.add_node("waiver_assistant", waiver_assistant)
graph.add_node("team_management_assistant", team_management_assistant)

# Add edges
graph.add_edge(START, "main_assistant")


def route_intent(state: State):
    last_message = state["messages"][-1]
    if isinstance(last_message, HumanMessage):
        content = last_message.content.lower()
        if any(
            keyword in content
            for keyword in ["statistics", "stats", "numbers", "performance"]
        ):
            state["dialog_state"].append("stats")
            return "stats_assistant"
        elif any(
            keyword in content for keyword in ["news", "update", "latest", "injury"]
        ):
            state["dialog_state"].append("news")
            return "news_assistant"
        elif any(keyword in content for keyword in ["trade", "exchange", "deal"]):
            state["dialog_state"].append("trade")
            return "trade_assistant"
        elif any(keyword in content for keyword in ["waiver", "free agent", "pickup"]):
            state["dialog_state"].append("waiver")
            return "waiver_assistant"
        elif any(
            keyword in content for keyword in ["manage", "roster", "lineup", "team"]
        ):
            state["dialog_state"].append("team")
            return "team_management_assistant"
    return END


graph.add_conditional_edges(
    "main_assistant",
    route_intent,
    {
        "stats_assistant": "stats_assistant",
        "news_assistant": "news_assistant",
        "trade_assistant": "trade_assistant",
        "waiver_assistant": "waiver_assistant",
        "team_management_assistant": "team_management_assistant",
        END: END,
    },
)

# Add edges from specialized assistants back to main assistant
for assistant in [
    "stats_assistant",
    "news_assistant",
    "trade_assistant",
    "waiver_assistant",
    "team_management_assistant",
]:
    graph.add_edge(assistant, "main_assistant")

# Compile the graph
app = graph.compile()


class FantasyFootballAgent:
    def __init__(self):
        self.app = app

    def run(
        self, user_input: str, thread_id: Optional[str] = None, user_info: str = "User"
    ) -> str:
        try:
            if thread_id is None:
                thread_id = str(uuid.uuid4())
            state_input = {
                "messages": [HumanMessage(content=user_input)],
                "user_info": user_info,
                "dialog_state": ["main_assistant"],
            }
            logger.info(f"Processing input: {user_input}")

            final_state = self.app.invoke(state_input)
            messages = final_state["messages"]

            # Extract all AI responses
            ai_responses = [
                msg.content for msg in messages if isinstance(msg, AIMessage)
            ]

            if ai_responses:
                response = "\n".join(ai_responses)
                logger.info(f"Assistant response: {response}")
                logger.info(f"Dialog state: {final_state['dialog_state']}")
                return response
            else:
                logger.warning("Couldn't generate a proper response")
                return "I apologize, but I couldn't generate a proper response."
        except Exception as e:
            logger.error(f"Error in FantasyFootballAgent: {str(e)}", exc_info=True)
            raise  # Re-raise the exception to be caught in the main loop


if __name__ == "__main__":
    agent = FantasyFootballAgent()
    user_question = "Who should I start this week, Player A or Player B?"
    response = agent.run(user_question)
    print(response)
