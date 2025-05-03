import re
import json
import httpx
import xml.etree.ElementTree as ET
from agents import FunctionTool, RunContextWrapper # Import các thành phần cần thiết
from pydantic import BaseModel, Field, ValidationError             # Import Pydantic
from typing import Optional, Any                   # Import Any

async def _fetch_and_parse_transcript(video_id: str, language: str) -> str:
    """(Internal logic) Gets the transcript text for a given YouTube video ID and language."""
    # ... (Toàn bộ code của hàm get_youtube_transcript gốc ở đây) ...
    print(f"--- Tool (Manual): Attempting to fetch transcript for video ID: {video_id}, language: {language} ---")
    watch_url = f"https://www.youtube.com/watch?v={video_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,vi;q=0.8"
    }
    try:
        async with httpx.AsyncClient(headers=headers, follow_redirects=True, timeout=15.0) as client:
            print(f"--- Tool (Manual): Fetching watch page: {watch_url} ---")
            response = await client.get(watch_url)
            response.raise_for_status()
            html = response.text
            caption_tracks_regex = r'"captionTracks":(\[.*?\])'
            match = re.search(caption_tracks_regex, html)
            if not match: return f"Error: Could not find transcript data for video {video_id}."
            try:
                caption_tracks = json.loads(match.group(1))
                if not caption_tracks: return f"Error: No caption tracks found for video {video_id}."
            except json.JSONDecodeError: return f"Error: Failed to parse transcript data for video {video_id}."
            transcript_url: Optional[str] = None
            target_track = None
            for track in caption_tracks:
                if track.get("languageCode") == language: target_track = track; break
            if not target_track and language != "en":
                for track in caption_tracks:
                     if track.get("languageCode") == "en": target_track = track; break
            if not target_track: target_track = caption_tracks[0]
            if not target_track or "baseUrl" not in target_track: return f"Error: Could not find a suitable transcript URL for video {video_id} (language: {language})."
            transcript_url = target_track.get("baseUrl")
            found_lang = target_track.get("languageCode", "unknown")
            print(f"--- Tool (Manual): Found transcript URL for language '{found_lang}': {transcript_url} ---")
            transcript_response = await client.get(transcript_url)
            transcript_response.raise_for_status()
            transcript_content = transcript_response.text
            try:
                root = ET.fromstring(transcript_content)
                lines = [elem.text for elem in root.findall('.//{*}text') or root.findall('.//{*}p') if elem.text]
                full_transcript = "\n".join(lines).strip()
                if not full_transcript: return f"Transcript for {video_id} ({found_lang}) (raw content):\n{transcript_content[:1000]}..."
                print(f"--- Tool (Manual): Successfully extracted transcript text for {video_id} ({found_lang}). ---")
                return f"Transcript for {video_id} ({found_lang}):\n{full_transcript}"
            except ET.ParseError: return f"Transcript for {video_id} ({found_lang}) (raw content):\n{transcript_content[:1000]}..."
    except httpx.TimeoutException: return f"Error: Request timed out for video {video_id}."
    except httpx.HTTPStatusError as e: return f"Error: HTTP error {e.response.status_code} for video {video_id}."
    except httpx.RequestError as e: return f"Error: Network error for video {video_id}."
    except Exception as e: return f"Error: Unexpected error for video {video_id}: {e}"
# --- Kết thúc logic gốc ---

# 1. Định nghĩa Pydantic model cho các tham số
class GetTranscriptArgs(BaseModel):
    video_id: str = Field(..., description="The unique ID of the YouTube video (e.g., 'dQw4w9WgXcQ').")
    language: str = Field(..., description="The desired language code for the transcript (e.g., 'en', 'vi', 'fr').")

# 2. Định nghĩa hàm on_invoke_tool (hàm xử lý chính)
async def invoke_get_transcript(ctx: RunContextWrapper[Any], args_json: str) -> str:
    """
    Parses arguments from JSON, calls the core transcript fetching logic,
    handles potential errors during the process, and returns the result
    or a user-friendly error message.
    """
    try:
        # Phân tích JSON string thành Pydantic model
        # Thêm try...except quanh đây để bắt lỗi validation từ Pydantic
        try:
             parsed_args = GetTranscriptArgs.model_validate_json(args_json)
        except ValidationError as val_err:
             print(f"--- Tool (Manual) Invocation Error: Invalid arguments JSON: {val_err} ---")
             # Trả về thông báo lỗi rõ ràng về tham số không hợp lệ
             return f"Error: Invalid parameters provided for transcript tool. Details: {val_err}"

        # Gọi hàm logic gốc với các tham số đã được phân tích
        # Thêm try...except quanh đây để bắt lỗi từ hàm logic gốc
        result = await _fetch_and_parse_transcript(
            video_id=parsed_args.video_id,
            language=parsed_args.language
        )
        return result

    # Bắt các lỗi cụ thể từ httpx hoặc lỗi chung
    except httpx.HTTPStatusError as http_err:
         print(f"--- Tool (Manual) Invocation Error: HTTP error {http_err.response.status_code} ---")
         return f"Lỗi HTTP {http_err.response.status_code} khi cố gắng lấy transcript. Vui lòng kiểm tra lại ID video hoặc thử lại sau."
    except httpx.TimeoutException:
         print(f"--- Tool (Manual) Invocation Error: Timeout ---")
         return "Yêu cầu lấy transcript bị quá thời gian chờ. Vui lòng thử lại."
    except httpx.RequestError as req_err:
         print(f"--- Tool (Manual) Invocation Error: Request error {req_err} ---")
         return f"Lỗi mạng khi cố gắng lấy transcript: {req_err}. Vui lòng kiểm tra kết nối và thử lại."
    except ValueError as val_err: # Bắt lỗi ValueError từ việc parse JSON hoặc XML
         print(f"--- Tool (Manual) Invocation Error: Value error {val_err} ---")
         return f"Lỗi xử lý dữ liệu transcript: {val_err}"
    except Exception as e:
        # Xử lý lỗi chung không mong muốn
        print(f"--- Tool (Manual) Invocation Error: Unexpected error: {type(e).__name__}: {e} ---")
        # import traceback
        # print(traceback.format_exc()) # Gỡ comment để debug
        return f"Đã xảy ra lỗi không mong muốn trong quá trình xử lý transcript: {type(e).__name__}."


# 3. Tạo instance FunctionTool
# Get the base schema from Pydantic
schema = GetTranscriptArgs.model_json_schema()
# Add 'additionalProperties: false' as required by some APIs (like OpenAI)
schema["additionalProperties"] = False

get_youtube_transcript_manual_tool = FunctionTool(
    name="get_youtube_transcript_manual", # Tên tool (có thể khác tên hàm)
    description="Gets the transcript text for a given YouTube video ID and language (Manually created tool).", # Mô tả tool
    params_json_schema=schema, # Use the modified schema
    on_invoke_tool=invoke_get_transcript, # Chỉ định hàm xử lý
    strict_json_schema=True # Nên để True
)