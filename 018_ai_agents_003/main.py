from agents import Runner
from agent import youtube_agent, web_search_agent, file_search_agent, orchestrator_agent
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents.items import TResponseInputItem
async def main():

    # input_video_id = input("Enter the YouTube video ID: ")
    # result = await Runner.run(youtube_agent, input_video_id)
    # print(result)

    # input_search_query = input("Enter the search query: ")
    # result = await Runner.run(web_search_agent, input_search_query)
    # print(result)

    # result = await Runner.run(file_search_agent, "Tho con ten la gi?")
    # print(result)

    input_items: list[TResponseInputItem] = []
    while True:
        input_query = input("Enter the query: ")
        input_items.append({"content": input_query, "role": "user"})
        result = Runner.run_streamed(orchestrator_agent, input_items)
        async for item in result.stream_events():
            if item.type == "raw_response_event" and isinstance(item.data, ResponseTextDeltaEvent):
                print(item.data.delta, end="", flush=True)

        input_items = result.to_input_list()
        print("\n")

                

if __name__ == "__main__":
    asyncio.run(main())