"""
Build Your First Working AI Agent — VinUni Workshop
~50 lines of Python. No framework. No magic.
"""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# ── Setup: OpenRouter as LLM provider ──

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODEL = "anthropic/claude-haiku-4.5"


# ── BƯỚC 1: Define tools (tay chân của agent) ──

def get_weather(city: str) -> str:
    """Lấy thời tiết hiện tại"""
    data = {
        "Ho Chi Minh": "34°C, nắng, độ ẩm 65%",
        "Ha Noi": "28°C, mưa nhẹ, độ ẩm 80%",
        "Da Nang": "30°C, nắng nhẹ, độ ẩm 70%",
    }
    return data.get(city, f"Không có data cho {city}")


def calculate(expression: str) -> str:
    """Tính toán biểu thức toán học"""
    return str(eval(expression))


# Map tên tool → function thật
tools_map = {
    "get_weather": get_weather,
    "calculate": calculate,
}


# ── BƯỚC 2: Tool schema — "Menu" cho LLM ──

tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Lấy thời tiết hiện tại của thành phố",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Tên thành phố (VD: Ho Chi Minh, Ha Noi)",
                    }
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Tính toán biểu thức toán học",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Biểu thức toán (VD: 2+2, 100*1.1)",
                    }
                },
                "required": ["expression"],
            },
        },
    },
]


# ── BƯỚC 3: THE AGENT LOOP — trái tim của agent ──

def run_agent(task: str) -> str:
    messages = [{"role": "user", "content": task}]

    while True:  # ← THE LOOP
        response = client.chat.completions.create(
            model=MODEL,
            max_tokens=1024,
            tools=tools_schema,
            messages=messages,
        )

        choice = response.choices[0]

        # Kiểm tra: LLM muốn gọi tool không?
        if choice.finish_reason == "tool_calls":
            # CÓ → parse & gọi function
            messages.append(choice.message)

            for tool_call in choice.message.tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments)
                result = tools_map[fn_name](**fn_args)
                print(f"  🔧 {fn_name}({fn_args}) → {result}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })
        else:
            # KHÔNG → xong rồi, trả lời user
            return choice.message.content  # ← BREAK khỏi loop


# ── BƯỚC 4-5: Chạy thử! ──

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 VinUni Agent — Demo")
    print("=" * 50)

    # Test 1: Task đơn giản (1 tool)
    print("\n📝 Task 1: Thời tiết Hà Nội")
    print("-" * 30)
    answer = run_agent("Thời tiết Hà Nội hôm nay thế nào?")
    print(f"\n💬 {answer}")

    # Test 2: Task phức tạp (multi-tool)
    print("\n📝 Task 2: So sánh thời tiết + tính toán")
    print("-" * 30)
    answer = run_agent(
        "So sánh thời tiết Hà Nội và HCM. "
        "Chênh lệch nhiệt độ bao nhiêu độ?"
    )
    print(f"\n💬 {answer}")
