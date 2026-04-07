# 🤖 Build Your First Working AI Agent

> VinUni Workshop — ~50 dòng Python. Không framework. Không magic.

## Cấu trúc Agent

```
Agent = LLM + Tools + Loop
```

| Thành phần | Vai trò |
|------------|---------|
| **LLM** | Bộ não — quyết định gọi tool nào |
| **Tools** | Tay chân — function Python thật |
| **Loop** | Trái tim — lặp cho đến khi xong |

## Quick Start

```bash
# 1. Clone repo
git clone https://github.com/mrgoonie/vinuni-first-working-agent.git
cd vinuni-first-working-agent

# 2. Tạo file .env
cp .env.example .env
# Sửa OPENROUTER_API_KEY trong .env

# 3. Cài dependencies
pip install -r requirements.txt

# 4. Chạy!
python agent.py
```

## Lấy API Key

1. Vào [openrouter.ai](https://openrouter.ai/)
2. Đăng ký tài khoản (free)
3. Tạo API key tại [openrouter.ai/keys](https://openrouter.ai/keys)
4. Paste vào file `.env`

## Code Walkthrough

### Bước 1: Define Tools
```python
def get_weather(city: str) -> str:
    """Mỗi tool = 1 function Python bình thường"""
    ...

tools_map = {"get_weather": get_weather, "calculate": calculate}
```

### Bước 2: Tool Schema — "Menu" cho LLM
```python
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Lấy thời tiết hiện tại",
            "parameters": { ... }
        }
    }
]
```

### Bước 3: The Loop ♻️ — Trái tim của Agent
```python
while True:                          # ← Lặp liên tục
    response = client.chat(...)      # Hỏi LLM
    if response == "tool_calls":     # LLM muốn gọi tool?
        result = tools_map[name]()   #   → Gọi function
        messages.append(result)      #   → Đưa kết quả lại
    else:
        return response.content      # → Xong, trả lời user
```

## Slides

📺 [Xem slides workshop](https://api.agentwiki.cc/s/nLGnEgJFcztu73USoUE8I/)

## License

MIT
