from agents import Agent
from pydantic import BaseModel
# Ví dụ Agent Dịch thuật đơn giản
instructions_dich_thuat = """
Bạn là một trợ lý dịch thuật chuyên nghiệp.
Nhiệm vụ chính của bạn là dịch văn bản giữa tiếng Anh và tiếng Việt một cách chính xác và tự nhiên.
- Nếu người dùng cung cấp văn bản bằng tiếng Anh, hãy dịch sang tiếng Việt.
- Nếu người dùng cung cấp văn bản bằng tiếng Việt, hãy dịch sang tiếng Anh.
- Chỉ trả về nội dung bản dịch, không thêm bất kỳ lời giải thích nào khác.
"""

class TranslatorAgentOutput(BaseModel):
    output: str
    original_text: str

translator_agent = Agent(
    name="Translator Anh-Việt",
    instructions=instructions_dich_thuat,
    model="gpt-4.1-nano",
    tools=[],
    handoffs=[],
    mcp_servers=[],
    mcp_config={},
    output_type=TranslatorAgentOutput
)
