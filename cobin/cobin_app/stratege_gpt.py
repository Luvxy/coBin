from openai import OpenAI
from dotenv import load_dotenv
import json
import re
import os

# .env 파일 로드
load_dotenv()

def load_prompt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
    
system_prompt = load_prompt("gpt_prompt.txt")

class chat_gpt:
    @staticmethod
    def chat_gpt(text):

        client = OpenAI()

        # Vision 모델에 이미지 전송
        response = client.chat.completions.create(
            model="gpt-4o",  # 또는 "gpt-4-vision-preview"
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"{text}"
                },
            ],
            temperature=1,
            max_tokens=2048,
            top_p=1,
        )
        
        return response.choices[0].message.content
    
    @staticmethod
    def append_gpt_strategy_to_json_file(gpt_output_text: str, json_path: str):
        """
        GPT 응답 텍스트에서 JSON 전략을 추출하고, 기존 JSON 파일에 append
        (없으면 새로 만듦)

        :param gpt_output_text: GPT의 전체 응답 텍스트
        :param json_path: 저장할 json 경로 (예: 'output.json')
        """
        try:
            # 1. ```json ... ``` 블록 추출
            match = re.search(r"```json\s*(.*?)```", gpt_output_text, re.DOTALL)
            if not match:
                raise ValueError("```json ... ``` 블록을 찾을 수 없습니다.")
            
            extracted_json_str = match.group(1).strip()
            new_data = json.loads(extracted_json_str)

            # 2. 기존 파일 로드 (없으면 빈 리스트로 시작)
            if os.path.exists(json_path):
                with open(json_path, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            else:
                existing_data = []

            # 3. 데이터 append
            if isinstance(new_data, list):
                existing_data.extend(new_data)
            else:
                existing_data.append(new_data)

            # 4. 저장
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=4)

            print(f"✅ 전략이 '{json_path}'에 저장되었습니다.")
            return existing_data

        except json.JSONDecodeError as je:
            print(f"❌ JSON 파싱 오류: {je.msg} at line {je.lineno} column {je.colno}")
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
