from tools.normal.tools import get_youtube_transcript
from tools.custom.tools import get_youtube_transcript_manual_tool
from agents import Agent, WebSearchTool, FileSearchTool

youtube_agent = Agent(
    name="YouTube Agent",
    instructions="""You are a YouTube Agent that summarizes the YouTube video. 
    You will be given a YouTube video ID and you will need to summarize the video by getting the transcript and then summarizing it.
    You will need to use the get_youtube_transcript_api tool to get the transcript of the video.
    Output the summary in Vietnamese.

    """,
    tools=[get_youtube_transcript_manual_tool],
    model="gpt-4.1-nano",
)   

web_search_agent = Agent(
    name="Web Search Agent",
    instructions="""You are a web search agent that searches the web for information.
    - First, you need to know what is the current time.
    - Then, you need to search the web for the information related to the current time.
    - Output the information in Vietnamese.
    """,
    tools=[WebSearchTool(
        user_location={"type": "approximate", "city": "Ha Noi", "country": "VN"},
        search_context_size="medium"
    )]
)

file_search_agent = Agent(
    name="File Search Agent",
    instructions="""You are a file search agent that searches the file for information.
    - If the user ask for personal information, you need to search the file for the information related to the user.
    - Output the information in Vietnamese.
    """,
    tools=[FileSearchTool(
        vector_store_ids=["vs_680f464976588191a2f6f405209a84ff"],
        max_num_results=3,
        include_search_results=True,
    )],
)

orchestrator_agent = Agent(
    name="Orchestrator Agent",
    instructions="""You are a orchestrator agent that orchestrates the other agents.
    You will be given a query and you will need to decide which agent to use to answer the query.
    - If the query is about a youtube video, you will use the youtube agent.
    - If the query is about a web search, you will use the web search agent.
    - If the query is about a file search, you will use the file search agent.
    """,
    tools=[
        youtube_agent.as_tool(
            tool_name="get_youtube_transcript",
            tool_description="Get the transcript of the youtube video and summarize it.",
        ),
        web_search_agent.as_tool(
            tool_name="web_search",
            tool_description="Search the web for information.",
        ),
        file_search_agent.as_tool(
            tool_name="file_search",
            tool_description="Search the file for information.",
        ),
    ],
    model="gpt-4.1-nano",
)