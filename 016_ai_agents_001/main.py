import asyncio
from agents import Agent, Runner
from dotenv import load_dotenv
load_dotenv(override=True)

# Initialize the agent
agent = Agent(
    name="Translator Anh-Việt",
    instructions="Bạn là một trợ lý dịch thuật chuyên nghiệp.",
)

async def main():
    user_input = input("Bạn cần dịch gì? \n")
    # Initialize the runner
    result = await Runner.run(agent, input=user_input)

    # Print the result
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
