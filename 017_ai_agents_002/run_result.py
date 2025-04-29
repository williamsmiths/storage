# --- Phần Thiết lập ---
from agents import Agent, Runner
import agents.items # Cần import để dùng isinstance
import asyncio
import pprint # Để in danh sách/dictionary đẹp hơn
from agent import translator_agent
from agents.items import MessageOutputItem
input_text = "Hello, world!"

# --- Chạy Agent (dùng run_sync cho đơn giản) ---
print("Đang chạy agent...")
result = Runner.run_sync(translator_agent, input_text)
print("Agent đã chạy xong!\n")

# --- Minh họa các thuộc tính của RunResult ---

# 1. final_output: Lấy kết quả cuối cùng
print("--- 1. final_output ---")
final_answer = result.final_output
print(f"Kết quả dịch cuối cùng: {final_answer}") #
print(f"Kiểu dữ liệu của final_output: {type(final_answer).__name__}\n") #

# 2. last_agent: Xem agent nào đã tạo ra kết quả
print("--- 2. last_agent ---")
last_agent_executed = result.last_agent
print(f"Agent cuối cùng thực thi: {last_agent_executed.name}") #
# Bạn cũng có thể truy cập các thuộc tính khác của agent này
print(f"Chỉ dẫn của agent cuối: {last_agent_executed.instructions}\n") #
print("")

# 3. new_items: Xem các bước trung gian
print("--- 3. new_items ---")
intermediate_steps = result.new_items
print(f"Số bước trung gian: {len(intermediate_steps)}") #
print("Chi tiết các bước:")
for i, item in enumerate(intermediate_steps):
    print(f"  Bước {i+1}: Loại = {type(item).__name__}") #
    # Ví dụ: In nội dung nếu là tin nhắn từ LLM
    if isinstance(item, MessageOutputItem):
        print(f"     -> Nội dung: {item.raw_item}") #
    # Lưu ý: Với agent dịch thuật đơn giản này, thường chỉ có MessageOutputItem.
    # Nếu agent có tools hoặc handoff, bạn sẽ thấy các loại item khác ở đây.
print("")

# 4. to_input_list(): Lấy lịch sử hội thoại cho lượt tiếp theo
print("--- 4. to_input_list() ---")
conversation_history = result.to_input_list()
print("Lịch sử hội thoại (dạng list để dùng làm input tiếp theo):") #
pprint.pprint(conversation_history) #
print("")

# --- Minh họa cách dùng lịch sử cho lượt chạy tiếp theo ---
print("--- Thêm lượt hội thoại mới ---")
next_user_message = {"role": "user", "content": "Translate 'Tạm biệt'"}
next_input = conversation_history + [next_user_message]

print("Input cho lượt chạy tiếp theo (bao gồm lịch sử):")
pprint.pprint(next_input)

# # Bạn có thể chạy lại agent với next_input
print("\nĐang chạy lượt tiếp theo...")
result_next = Runner.run_sync(translator_agent, next_input)
print(f"Kết quả lượt tiếp theo: {result_next.final_output}")
