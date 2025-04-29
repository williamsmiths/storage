# Ví dụ chạy bất đồng bộ với streaming
import time
import asyncio
from agents import Runner
from agent import translator_agent
from agents.items import MessageOutputItem
from openai.types.responses import ResponseTextDeltaEvent



async def run_agent_streamed():
    print("Bắt đầu chạy streaming...")
    start_time = time.time()
    input_text = """
RawResponsesStreamEvent are raw events passed directly from the LLM. They are in OpenAI Responses API format, 
which means each event has a type (like response.created, response.output_text.delta, etc) and data. 
These events are useful if you want to stream response messages to the user as soon as they are generated.
"""
    # ---- Sử dụng stream_events() để nhận các sự kiện ----
    async for item in Runner.run_streamed(translator_agent, input_text).stream_events():
         if item.type == "raw_response_event" and isinstance(item.data, ResponseTextDeltaEvent):
            print(item.data.delta, end="", flush=True)

    # --------------------------------------------

    end_time = time.time()
    print()
    print(f"Thời gian chạy (streaming): {end_time - start_time:.2f} giây")
    print("Đã chạy xong streaming.")

async def main_streamed():
    await run_agent_streamed()

# Chạy hàm main bất đồng bộ
if __name__ == "__main__":
    asyncio.run(main_streamed())