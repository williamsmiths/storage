# Ví dụ chạy bất đồng bộ (asynchronous)
import time
import asyncio
from agents import Runner
from agent import translator_agent

async def run_agent_async():
    print("   (Async) Bắt đầu chạy agent...")
    start_time = time.time()
    input_text = "Hello, how are you today?"
    # ---- Dòng này sẽ chờ, nhưng không block event loop ----
    result_async = await Runner.run(translator_agent, input_text) # [cite: 25, 29, 67]
    # -----------------------------------------------------

    end_time = time.time()
    print(f"   (Async) Kết quả: {result_async.final_output}") # [cite: 35]
    print(f"   (Async) Thời gian chạy agent: {end_time - start_time:.2f} giây")
    print("   (Async) Đã chạy xong agent.")
    return result_async

async def other_async_task():
    print("   (Other Task) Bắt đầu chạy tác vụ khác...")
    await asyncio.sleep(1) # Giả lập một công việc khác đang chạy (ví dụ: chờ I/O)
    print("   (Other Task) Tác vụ khác: Đếm 1 giây...")
    await asyncio.sleep(1)
    print("   (Other Task) Tác vụ khác: Đếm 2 giây...")
    await asyncio.sleep(1)
    print("   (Other Task) Đã chạy xong tác vụ khác.")

async def main():
    print("Bắt đầu chạy bất đồng bộ...")
    start_main = time.time()

    # Chạy cả hai tác vụ "gần như" đồng thời
    task_agent = asyncio.create_task(run_agent_async())
    task_other = asyncio.create_task(other_async_task())

    # Đợi cả hai tác vụ hoàn thành
    await task_agent
    await task_other

    end_main = time.time()
    print(f"Tổng thời gian chạy (bất đồng bộ): {end_main - start_main:.2f} giây")
    print("Đã chạy xong bất đồng bộ.")

# Chạy hàm main bất đồng bộ
if __name__ == "__main__":
    asyncio.run(main())

