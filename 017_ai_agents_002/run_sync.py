import time
from agents import Runner
from agent import translator_agent

print("Bắt đầu chạy đồng bộ...")
start_time = time.time()
input_text = "Hello, how are you today?"
# ---- Dòng này sẽ BLOCCK chương trình ----
result_sync = Runner.run_sync(translator_agent, input_text)
# ----------------------------------------

end_time = time.time()
print(f"Kết quả (đồng bộ): {result_sync.final_output}")
print(f"Thời gian chạy (đồng bộ): {end_time - start_time:.2f} giây")
print("Đã chạy xong đồng bộ.")
