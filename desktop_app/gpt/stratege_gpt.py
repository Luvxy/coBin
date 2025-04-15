from openai import OpenAI
from dotenv import load_dotenv
import json
import re
import os

# .env 파일 로드
load_dotenv()

def chat_gpt(text):

    client = OpenAI()

    # Vision 모델에 이미지 전송
    response = client.responses.create(
        model="gpt-4o",  # 또는 "gpt-4-vision-preview"
        input=[
            {
                "role": "system",
                "content": [
                    {
                    "type": "input_text",
                    "text": "너는 PyQt 기반 블록 시스템에서 사용되는 조건 및 액션 클래스를 분석하고, 이를 조합하여 자동매매 전략을 생성하는 전문가야.\n\n## 📌 목적\n- PySide6 기반 GUI 자동매매 시스템에서 사용되는 조건(Condition)과 액션(Action) 클래스를 확인한 후,\n- 이들을 적절히 조합하여 전략을 구성하고,\n- 해당 전략을 JSON 형식으로 출력해.\n\n## 📥 입력 파일 구성\n- `ui_block.py`: PyQt5 GUI 블록 시스템의 메인 코드. 여기서 `ui.conditions`, `ui.actions`에서 조건/액션을 불러오고, 전략 구성을 위한 Block 클래스를 정의함.\n- `ui/conditions.py`: 조건 클래스들이 정의되어 있으며, 각각은 `name`, `config_fields`, `backtest`, `check_condition` 등의 메서드를 가짐.\n- `ui/actions.py`: 액션 클래스들이 정의되어 있으며, 각각은 `name`, `config_fields`, `run_action`, `backtest` 등의 메서드를 가짐.\n- 기존 전략 예시는 `default.json` 파일 형태로 제공됨.\n\n## 🎯 너의 작업\n1. `ConditionRegistry.get_condition_names()` 와 `ActionRegistry.get_action_names()` 를 통해 조건/액션 목록을 확인하고,\n2. 해당 조건/액션의 `config_fields`를 기반으로 설정값을 임의로 구성하여,\n3. 전략을 구성하고,\n4. 최종적으로 `default.json`과 동일한 형식의 JSON 리스트로 출력해.\n\n## 🧠 생성 전략 예시\n전략은 다음 중 하나 이상의 목적을 가질 수 있음:\n- 볼린저밴드 돌파 후 매수\n- 연속 양봉 발생 시 매수\n- 고점 갱신 확인 후 진입\n- 조건 없는 스탑로스/익절 전략\n\n## 💡 주의사항\n- 각 조건/액션의 `설정값`은 그 클래스의 `config_fields` 정보를 기반으로 타입과 옵션을 맞춰야 함\n- 전략 내 조건은 0~5개까지 자유롭게 조합할 수 있으며, 액션은 반드시 1개 존재해야 함\n- `주기` 필드는 생략 가능하며, 있으면 초 단위 문자열로 `\"30\"` 등으로 입력\n\n## 📤 출력 형식\nPython 리스트 형식으로 다음과 같이 출력해:\n\n```json\n[\n    {\n        \"조건\": [ { \"이름\": \"조건 이름\", \"설정값\": { ... } }, ... ],\n        \"액션\": { \"이름\": \"액션 이름\", \"설정값\": { ... } },\n        \"주기\": \"60\"\n    },\n    ...\n]\n"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                    "type": "input_text",
                    "text": f"{text}"
                    }
                ]
            },
        ],
        temperature=1,
        max_output_tokens=2048,
        top_p=1,
        store=True,
    )
    
    return response.output[0].content[0].text

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


response = chat_gpt("볼린저밴드 돌파 후 매수")
print(response)
append_gpt_strategy_to_json_file(response, "output.json")
