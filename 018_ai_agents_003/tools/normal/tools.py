from agents import function_tool, RunContextWrapper
from typing import Optional, Any
import json
import httpx
import re
import xml.etree.ElementTree as ET



async def custom_youtube_error_handler(ctx: RunContextWrapper[Any], error: Exception) -> str:
    """Hàm xử lý lỗi tùy chỉnh cho tool lấy transcript YouTube."""
    print(f"--- Custom Error Handler: Caught error: {type(error).__name__}: {error} ---")
    if isinstance(error, httpx.HTTPStatusError):
         return f"Lỗi HTTP {error.response.status_code} khi cố gắng lấy transcript. Vui lòng kiểm tra lại ID video hoặc thử lại sau."
    elif isinstance(error, httpx.TimeoutException):
         return "Yêu cầu lấy transcript bị quá thời gian chờ. Vui lòng thử lại."
    elif isinstance(error, httpx.RequestError):
         return "Lỗi mạng khi cố gắng lấy transcript. Vui lòng kiểm tra kết nối và thử lại."
    else:
         # Lỗi chung khác
         return f"Đã xảy ra lỗi không mong muốn khi lấy transcript: {type(error).__name__}. Vui lòng thử lại."

@function_tool(failure_error_function=custom_youtube_error_handler)
async def get_youtube_transcript(video_id: str, language: str) -> str:
    """Gets the transcript text for a given YouTube video ID and language.

    Fetches the YouTube watch page, finds the caption tracks data,
    selects the track for the specified language (defaulting to English),
    fetches the transcript content (usually XML), parses it, and returns
    the concatenated text content.

    Args:
        video_id: The unique ID of the YouTube video (e.g., 'dQw4w9WgXcQ').
        language: The desired language code for the transcript (e.g., 'en', 'vi', 'fr').
                  Defaults to 'en' (English).
    """
    print(f"--- Tool: Attempting to fetch transcript for video ID: {video_id}, language: {language} ---")
    watch_url = f"https://www.youtube.com/watch?v={video_id}"
    headers = {
        # Giả lập trình duyệt thông thường để tránh bị chặn đơn giản
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,vi;q=0.8" # Yêu cầu ngôn ngữ ưu tiên
    }

    try:
        async with httpx.AsyncClient(headers=headers, follow_redirects=True, timeout=15.0) as client:
            # 1. Lấy HTML trang xem video
            print(f"--- Tool: Fetching watch page: {watch_url} ---")
            response = await client.get(watch_url)
            response.raise_for_status() # Kiểm tra lỗi HTTP
            html = response.text

            # 2. Tìm dữ liệu captionTracks bằng Regex
            # Regex này tìm đoạn JSON chứa thông tin về caption tracks
            # Lưu ý: Regex này rất có thể sẽ cần cập nhật nếu YouTube thay đổi cấu trúc
            caption_tracks_regex = r'"captionTracks":(\[.*?\])'
            match = re.search(caption_tracks_regex, html)

            if not match:
                print("--- Tool Error: Could not find captionTracks JSON in HTML. ---")
                # RAISE exception instead of returning string
                raise ValueError("Could not find captionTracks JSON in HTML. The video might not have captions, or the page structure might have changed.")
            # 3. Phân tích JSON captionTracks
            try:
                caption_tracks_json = match.group(1)
                caption_tracks = json.loads(caption_tracks_json)
                if not caption_tracks:
                     print("--- Tool Warning: captionTracks JSON is empty. ---")
                     # RAISE exception
                     raise ValueError(f"No caption tracks found for video {video_id}.")
            except json.JSONDecodeError as e:
                print("--- Tool Error: Failed to parse captionTracks JSON. ---")
                # RAISE exception
                raise ValueError(f"Failed to parse transcript data for video {video_id}.") from e

            # 4. Tìm URL của transcript theo ngôn ngữ yêu cầu
            transcript_url: Optional[str] = None
            target_track = None

            # Ưu tiên tìm chính xác ngôn ngữ được yêu cầu
            for track in caption_tracks:
                if track.get("languageCode") == language:
                    target_track = track
                    break

            # Nếu không tìm thấy, thử tìm ngôn ngữ mặc định 'en' (nếu khác ngôn ngữ yêu cầu)
            if not target_track and language != "en":
                 print(f"--- Tool Info: Language '{language}' not found, trying 'en'... ---")
                 for track in caption_tracks:
                      if track.get("languageCode") == "en":
                           target_track = track
                           break

            # Nếu vẫn không tìm thấy, lấy track đầu tiên làm phương án cuối cùng
            if not target_track:
                 print(f"--- Tool Info: Default language 'en' not found, using first available track... ---")
                 target_track = caption_tracks[0]


            if not target_track or "baseUrl" not in target_track:
                 print("--- Tool Error: Could not determine a valid transcript URL. ---")
                 # RAISE exception
                 raise ValueError(f"Could not find a suitable transcript URL for video {video_id} (language: {language}).")

            transcript_url = target_track.get("baseUrl")
            found_lang = target_track.get("languageCode", "unknown")
            print(f"--- Tool: Found transcript URL for language '{found_lang}': {transcript_url} ---")


            # 5. Lấy nội dung transcript (thường là XML)
            transcript_response = await client.get(transcript_url)
            transcript_response.raise_for_status()
            transcript_content = transcript_response.text

            # 6. Phân tích XML và trích xuất văn bản
            try:
                root = ET.fromstring(transcript_content)
                # Tìm tất cả các thẻ 'text' hoặc 'p' (tùy định dạng) và nối nội dung lại
                lines = [elem.text for elem in root.findall('.//{*}text') or root.findall('.//{*}p') if elem.text]
                full_transcript = "\n".join(lines).strip()

                if not full_transcript:
                     print("--- Tool Warning: Parsed transcript text is empty. ---")
                     # Trả về nội dung gốc nếu không phân tích được
                     return f"Transcript for {video_id} ({found_lang}) (raw content):\n{transcript_content[:1000]}..." # Giới hạn độ dài

                print(f"--- Tool: Successfully extracted transcript text for {video_id} ({found_lang}). Length: {len(full_transcript)} chars ---")
                return full_transcript

            except ET.ParseError:
                print("--- Tool Warning: Failed to parse transcript XML. Returning raw content. ---")
                # Nếu không phải XML hợp lệ, trả về nội dung gốc (có thể là định dạng khác)
                return f"Transcript for {video_id} ({found_lang}) (raw content):\n{transcript_content[:1000]}..." # Giới hạn độ dài

    except httpx.TimeoutException as e:
        print(f"--- Tool Error: Request timed out for {video_id}. ---")
        # RAISE exception
        raise e
    except httpx.HTTPStatusError as e:
        print(f"--- Tool Error: HTTP error occurred: {e.response.status_code} for {e.request.url} ---")
        # RAISE exception
        raise e
    except httpx.RequestError as e:
         print(f"--- Tool Error: Network request error occurred: {e} ---")
         # RAISE exception
         raise e
    except ValueError as e: # Catch specific ValueErrors raised above
         print(f"--- Tool Error: Data processing error: {e} ---")
         # RAISE exception
         raise e
    except Exception as e:
        print(f"--- Tool Error: An unexpected error occurred: {e} ---")
        # Ghi log lỗi chi tiết hơn ở đây nếu cần
        # import traceback
        # print(traceback.format_exc())
        # RAISE exception
        raise e

# if __name__ == "__main__":
#     asyncio.run(get_youtube_transcript("nCzFL4qKfnI", "vi"))