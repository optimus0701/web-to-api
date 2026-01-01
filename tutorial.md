# Hướng Dẫn Sử Dụng WebAI-to-API Trong Dự Án Khác

## 📋 Mục Lục
- [Giới Thiệu](#giới-thiệu)
- [Cài Đặt và Cấu Hình](#cài-đặt-và-cấu-hình)
- [Tích Hợp API](#tích-hợp-api)
- [API Endpoints](#api-endpoints)
- [Ví Dụ Tích Hợp](#ví-dụ-tích-hợp)
- [Troubleshooting](#troubleshooting)

---

## Giới Thiệu

**WebAI-to-API** là một web server được xây dựng bằng FastAPI cho phép bạn biến các LLM dựa trên trình duyệt (như Gemini) thành các API endpoint cục bộ. Dự án hỗ trợ hai chế độ hoạt động:

1. **WebAI Server** (Chính): Kết nối với giao diện web Gemini thông qua cookies của trình duyệt
2. **gpt4free Server** (Dự phòng): Hỗ trợ nhiều LLM khác nhau (ChatGPT, Claude, DeepSeek, v.v.)

### Các Tính Năng Chính

- 🚀 **OpenAI-compatible API**: Tương thích với định dạng API của OpenAI
- 🔄 **Hỗ trợ conversation history**: Duy trì ngữ cảnh hội thoại
- 🌐 **Nhiều endpoints linh hoạt**: `/gemini`, `/gemini-chat`, `/translate`, `/v1/chat/completions`
- 🎯 **Hỗ trợ nhiều models**: gemini-3.0-pro, gemini-2.5-pro, gemini-2.5-flash

---

## Cài Đặt và Cấu Hình

### Bước 1: Clone và Cài Đặt Dependencies

```bash
# Clone repository
git clone https://github.com/Amm1rr/WebAI-to-API.git
cd WebAI-to-API

# Cài đặt dependencies bằng Poetry
poetry install

# Hoặc sử dụng pip
pip install -r requirements.txt
```

### Bước 2: Tạo File Cấu Hình

```bash
# Tạo file config.conf từ template
cp config.conf.example config.conf
```

### Bước 3: Chỉnh Sửa File `config.conf`

```ini
[AI]
# AI service mặc định
default_ai = gemini

# Model mặc định cho Gemini
# Tùy chọn: gemini-3.0-pro, gemini-2.5-pro, gemini-2.5-flash
default_model_gemini = gemini-2.5-flash

# Gemini cookies (để trống nếu muốn tự động lấy từ trình duyệt)
gemini_cookie_1psid =
gemini_cookie_1psidts =

[EnabledAI]
# Bật/tắt AI services
gemini = true

[Browser]
# Trình duyệt mặc định để lấy cookies
# Tùy chọn: firefox, brave, chrome, edge, safari
name = firefox

[Proxy]
# Proxy tùy chọn cho kết nối Gemini (để khắc phục lỗi 403)
http_proxy =
```

### Bước 4: Chạy Server

```bash
# Chạy server (mặc định tại localhost:6969)
poetry run python src/run.py

# Chạy với các tùy chọn tùy chỉnh
poetry run python src/run.py --host 0.0.0.0 --port 8080
```

**🎉 Server sẽ khởi động tại:** `http://localhost:6969`

**📚 Xem API docs tại:** `http://localhost:6969/docs`

---

## Tích Hợp API

### Thông Tin Kết Nối

Sau khi chạy server thành công, bạn có thể tích hợp API vào dự án của mình:

```
Base URL: http://localhost:6969
```

### Các Models Được Hỗ Trợ

| Model | Mô Tả |
|-------|-------|
| `gemini-3.0-pro` | Model mạnh nhất và mới nhất |
| `gemini-2.5-pro` | Model lý luận nâng cao |
| `gemini-2.5-flash` | Model nhanh và hiệu quả (mặc định) |

---

## API Endpoints

### 1. `/v1/chat/completions` (Khuyến Nghị)

**OpenAI-compatible endpoint** - Tốt nhất cho tích hợp vào các ứng dụng hiện có.

**Đặc điểm:**
- ✅ Hỗ trợ system prompts
- ✅ Duy trì conversation history
- ✅ Tương thích với OpenAI API format
- ✅ Hỗ trợ streaming (tùy chọn)

**Request:**

```http
POST /v1/chat/completions
Content-Type: application/json

{
  "model": "gemini-2.5-flash",
  "messages": [
    {
      "role": "system",
      "content": "Bạn là một trợ lý AI hữu ích."
    },
    {
      "role": "user",
      "content": "Python là gì?"
    }
  ],
  "stream": false
}
```

**Response:**

```json
{
  "id": "chatcmpl-1704088800",
  "object": "chat.completion",
  "created": 1704088800,
  "model": "gemini-2.5-flash",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Python là một ngôn ngữ lập trình..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0
  }
}
```

---

### 2. `/gemini`

Tạo một cuộc hội thoại mới với LLM. Mỗi request tạo một **session mới**.

**Request:**

```http
POST /gemini
Content-Type: application/json

{
  "message": "Xin chào!",
  "model": "gemini-2.5-flash",
  "files": []
}
```

**Response:**

```json
{
  "response": "Xin chào! Tôi có thể giúp gì cho bạn?"
}
```

---

### 3. `/gemini-chat`

Tiếp tục cuộc hội thoại với LLM **không tạo session mới**. Duy trì ngữ cảnh giữa các messages.

**Request:**

```http
POST /gemini-chat
Content-Type: application/json

{
  "message": "Tiếp tục câu chuyện trước đó",
  "model": "gemini-2.5-flash",
  "files": []
}
```

**Response:**

```json
{
  "response": "Được, tôi sẽ tiếp tục..."
}
```

---

### 4. `/translate`

Được thiết kế để tích hợp với extension [Translate It!](https://github.com/iSegaro/Translate-It). **Duy trì session** giống như `/gemini-chat`.

**Request:**

```http
POST /translate
Content-Type: application/json

{
  "message": "Translate this to Vietnamese: Hello world",
  "model": "gemini-2.5-flash"
}
```

---

### 5. `/v1beta/models/{model}` 

**Google Generative AI v1beta API** compatible endpoint.

**Request:**

```http
POST /v1beta/models/gemini-2.5-flash
Content-Type: application/json

{
  "contents": [
    {
      "parts": [
        {
          "text": "Giải thích về AI"
        }
      ]
    }
  ]
}
```

---

## Ví Dụ Tích Hợp

### Python (với `requests`)

```python
import requests

# Base URL của WebAI-to-API server
BASE_URL = "http://localhost:6969"

def chat_with_gemini(message, model="gemini-2.5-flash"):
    """
    Gửi message tới Gemini API
    
    Args:
        message: Nội dung tin nhắn
        model: Model sử dụng (mặc định: gemini-2.5-flash)
    
    Returns:
        Response text từ Gemini
    """
    url = f"{BASE_URL}/v1/chat/completions"
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ]
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    result = response.json()
    return result["choices"][0]["message"]["content"]

# Sử dụng
try:
    answer = chat_with_gemini("Cho tôi biết về Python?")
    print(f"Gemini: {answer}")
except Exception as e:
    print(f"Lỗi: {e}")
```

### Python với Conversation History

```python
import requests

BASE_URL = "http://localhost:6969"

class GeminiConversation:
    """Quản lý cuộc hội thoại với Gemini"""
    
    def __init__(self, system_prompt=None, model="gemini-2.5-flash"):
        self.model = model
        self.messages = []
        
        if system_prompt:
            self.messages.append({
                "role": "system",
                "content": system_prompt
            })
    
    def send_message(self, user_message):
        """Gửi message và nhận response"""
        # Thêm user message vào lịch sử
        self.messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Gửi request
        response = requests.post(
            f"{BASE_URL}/v1/chat/completions",
            json={
                "model": self.model,
                "messages": self.messages
            }
        )
        response.raise_for_status()
        
        # Lấy response
        result = response.json()
        assistant_message = result["choices"][0]["message"]["content"]
        
        # Thêm assistant response vào lịch sử
        self.messages.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    def clear_history(self):
        """Xóa lịch sử hội thoại (giữ system prompt)"""
        system_messages = [m for m in self.messages if m["role"] == "system"]
        self.messages = system_messages

# Sử dụng
conversation = GeminiConversation(
    system_prompt="Bạn là một giáo viên lập trình Python chuyên nghiệp."
)

# Hội thoại liên tục
print(conversation.send_message("Python là gì?"))
print(conversation.send_message("Nó có dễ học không?"))
print(conversation.send_message("Cho tôi một ví dụ code Python đơn giản"))
```

---

### JavaScript/Node.js (với `axios`)

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:6969';

/**
 * Gửi message tới Gemini API
 * @param {string} message - Nội dung tin nhắn
 * @param {string} model - Model sử dụng
 * @returns {Promise<string>} Response từ Gemini
 */
async function chatWithGemini(message, model = 'gemini-2.5-flash') {
  try {
    const response = await axios.post(`${BASE_URL}/v1/chat/completions`, {
      model: model,
      messages: [
        {
          role: 'user',
          content: message
        }
      ]
    });
    
    return response.data.choices[0].message.content;
  } catch (error) {
    console.error('Lỗi:', error.message);
    throw error;
  }
}

// Sử dụng
(async () => {
  try {
    const answer = await chatWithGemini('Giải thích về JavaScript?');
    console.log(`Gemini: ${answer}`);
  } catch (error) {
    console.error('Có lỗi xảy ra:', error);
  }
})();
```

### JavaScript với Conversation History

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:6969';

class GeminiConversation {
  constructor(systemPrompt = null, model = 'gemini-2.5-flash') {
    this.model = model;
    this.messages = [];
    
    if (systemPrompt) {
      this.messages.push({
        role: 'system',
        content: systemPrompt
      });
    }
  }
  
  async sendMessage(userMessage) {
    // Thêm user message
    this.messages.push({
      role: 'user',
      content: userMessage
    });
    
    // Gửi request
    const response = await axios.post(`${BASE_URL}/v1/chat/completions`, {
      model: this.model,
      messages: this.messages
    });
    
    const assistantMessage = response.data.choices[0].message.content;
    
    // Thêm assistant response vào lịch sử
    this.messages.push({
      role: 'assistant',
      content: assistantMessage
    });
    
    return assistantMessage;
  }
  
  clearHistory() {
    const systemMessages = this.messages.filter(m => m.role === 'system');
    this.messages = systemMessages;
  }
}

// Sử dụng
(async () => {
  const conversation = new GeminiConversation(
    'Bạn là một trợ lý AI thông minh.'
  );
  
  console.log(await conversation.sendMessage('Xin chào!'));
  console.log(await conversation.sendMessage('Bạn có thể giúp gì cho tôi?'));
})();
```

---

### TypeScript (Discord Bot Example)

```typescript
import axios from 'axios';

interface ChatMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

interface ChatCompletionRequest {
  model: string;
  messages: ChatMessage[];
  stream?: boolean;
}

interface ChatCompletionResponse {
  id: string;
  object: string;
  created: number;
  model: string;
  choices: Array<{
    index: number;
    message: {
      role: string;
      content: string;
    };
    finish_reason: string;
  }>;
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

class GeminiClient {
  private baseUrl: string;
  private defaultModel: string;

  constructor(baseUrl: string = 'http://localhost:6969', defaultModel: string = 'gemini-2.5-flash') {
    this.baseUrl = baseUrl;
    this.defaultModel = defaultModel;
  }

  async chat(messages: ChatMessage[], model?: string): Promise<string> {
    const requestData: ChatCompletionRequest = {
      model: model || this.defaultModel,
      messages: messages,
      stream: false
    };

    try {
      const response = await axios.post<ChatCompletionResponse>(
        `${this.baseUrl}/v1/chat/completions`,
        requestData,
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );

      return response.data.choices[0].message.content;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(`API Error: ${error.response?.data || error.message}`);
      }
      throw error;
    }
  }

  async simpleChat(message: string, systemPrompt?: string): Promise<string> {
    const messages: ChatMessage[] = [];
    
    if (systemPrompt) {
      messages.push({ role: 'system', content: systemPrompt });
    }
    
    messages.push({ role: 'user', content: message });
    
    return this.chat(messages);
  }
}

// Sử dụng trong Discord Bot
import { Client, GatewayIntentBits, Message } from 'discord.js';

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ]
});

const gemini = new GeminiClient();

client.on('messageCreate', async (message: Message) => {
  // Bỏ qua tin nhắn từ bot
  if (message.author.bot) return;
  
  // Chỉ phản hồi khi được mention
  if (message.mentions.has(client.user!)) {
    try {
      const userMessage = message.content.replace(`<@${client.user!.id}>`, '').trim();
      
      const response = await gemini.simpleChat(
        userMessage,
        'Bạn là một bot Discord thông minh và hữu ích.'
      );
      
      await message.reply(response);
    } catch (error) {
      console.error('Error:', error);
      await message.reply('Xin lỗi, đã có lỗi xảy ra khi xử lý yêu cầu của bạn.');
    }
  }
});

client.login('YOUR_DISCORD_BOT_TOKEN');
```

---

### cURL Examples

#### Request đơn giản

```bash
curl -X POST http://localhost:6969/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.5-flash",
    "messages": [
      {
        "role": "user",
        "content": "Xin chào!"
      }
    ]
  }'
```

#### Request với system prompt và conversation history

```bash
curl -X POST http://localhost:6969/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.5-pro",
    "messages": [
      {
        "role": "system",
        "content": "Bạn là một chuyên gia về AI."
      },
      {
        "role": "user",
        "content": "AI là gì?"
      },
      {
        "role": "assistant",
        "content": "AI (Artificial Intelligence) là trí tuệ nhân tạo..."
      },
      {
        "role": "user",
        "content": "Nó có ứng dụng gì?"
      }
    ]
  }'
```

---

### PHP Example

```php
<?php

class GeminiClient {
    private $baseUrl;
    private $defaultModel;
    
    public function __construct($baseUrl = 'http://localhost:6969', $defaultModel = 'gemini-2.5-flash') {
        $this->baseUrl = $baseUrl;
        $this->defaultModel = $defaultModel;
    }
    
    public function chat($messages, $model = null) {
        $url = $this->baseUrl . '/v1/chat/completions';
        
        $data = [
            'model' => $model ?? $this->defaultModel,
            'messages' => $messages
        ];
        
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json'
        ]);
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        if ($httpCode !== 200) {
            throw new Exception("API Error: HTTP $httpCode");
        }
        
        $result = json_decode($response, true);
        return $result['choices'][0]['message']['content'];
    }
    
    public function simpleChat($message, $systemPrompt = null) {
        $messages = [];
        
        if ($systemPrompt) {
            $messages[] = [
                'role' => 'system',
                'content' => $systemPrompt
            ];
        }
        
        $messages[] = [
            'role' => 'user',
            'content' => $message
        ];
        
        return $this->chat($messages);
    }
}

// Sử dụng
try {
    $gemini = new GeminiClient();
    $response = $gemini->simpleChat(
        'Giải thích về PHP?',
        'Bạn là một chuyên gia lập trình PHP.'
    );
    
    echo "Gemini: " . $response . "\n";
} catch (Exception $e) {
    echo "Lỗi: " . $e->getMessage() . "\n";
}
?>
```

---

## Troubleshooting

### 1. Lỗi "Gemini client is not initialized"

**Nguyên nhân:** Server không thể khởi tạo Gemini client (thường do thiếu cookies hoặc cookies không hợp lệ).

**Giải pháp:**

```bash
# Option 1: Để server tự động lấy cookies từ trình duyệt
# Đảm bảo bạn đã đăng nhập Gemini trên trình duyệt (Firefox, Chrome, v.v.)
# Trong config.conf:
[Browser]
name = firefox  # hoặc chrome, brave, edge, safari

# Option 2: Cung cấp cookies thủ công
# Lấy cookies __Secure-1PSID và __Secure-1PSIDTS từ trình duyệt
# Trong config.conf:
[AI]
gemini_cookie_1psid = YOUR_1PSID_COOKIE
gemini_cookie_1psidts = YOUR_1PSIDTS_COOKIE
```

### 2. Lỗi 403 khi kết nối Gemini

**Nguyên nhân:** IP bị chặn hoặc vị trí địa lý không được hỗ trợ.

**Giải pháp:** Sử dụng proxy

```ini
# Trong config.conf:
[Proxy]
http_proxy = http://127.0.0.1:2334
```

### 3. Lỗi "Connection refused"

**Nguyên nhân:** Server chưa chạy hoặc đang chạy ở port khác.

**Giải pháp:**

```bash
# Kiểm tra server có đang chạy không
# Đảm bảo base URL chính xác, ví dụ:
http://localhost:6969  # port mặc định
```

### 4. Response chậm hoặc timeout

**Nguyên nhân:** Model phức tạp hoặc message quá dài.

**Giải pháp:**

```python
# Sử dụng model nhanh hơn
payload = {
    "model": "gemini-2.5-flash",  # Thay vì gemini-3.0-pro
    "messages": [...]
}

# Hoặc tăng timeout trong client
response = requests.post(url, json=payload, timeout=60)  # 60 giây
```

### 5. Chuyển đổi giữa WebAI và gpt4free

Khi server đang chạy, bạn có thể chuyển đổi giữa các chế độ:

```
Nhấn '1' + Enter: Chuyển sang WebAI mode (nhanh hơn, dùng Gemini)
Nhấn '2' + Enter: Chuyển sang gpt4free mode (nhiều model hơn)
Ctrl+C: Thoát server
```

### 6. Lỗi khi sử dụng gpt4free mode

**Lỗi:** `ProviderNotFoundError`

**Giải pháp:** Khi sử dụng gpt4free, bạn cần chỉ định provider hợp lệ, không phải model name.

```bash
# Kiểm tra danh sách providers có sẵn:
curl http://localhost:6969/v1/providers

# Sử dụng đúng provider trong request
```

---

## Best Practices

### 1. Quản lý Session hiệu quả

- Sử dụng `/v1/chat/completions` cho hầu hết các use cases
- Sử dụng `/gemini` khi cần session mới cho mỗi request
- Sử dụng `/gemini-chat` khi cần duy trì context giữa các request

### 2. Chọn Model phù hợp

| Use Case | Recommended Model |
|----------|------------------|
| Phản hồi nhanh, chat đơn giản | `gemini-2.5-flash` |
| Phân tích phức tạp, reasoning | `gemini-2.5-pro` |
| Tasks quan trọng, latest features | `gemini-3.0-pro` |

### 3. Error Handling

Luôn implement error handling trong code:

```python
try:
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    result = response.json()
except requests.exceptions.Timeout:
    print("Request timeout - thử lại sau")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
```

### 4. Rate Limiting

Tránh spam requests:

```python
import time

def chat_with_rate_limit(message, min_delay=1.0):
    """Thêm delay giữa các requests"""
    response = chat_with_gemini(message)
    time.sleep(min_delay)
    return response
```

---

## Tài Liệu Tham Khảo

- **Repository chính:** https://github.com/Amm1rr/WebAI-to-API
- **API Documentation:** http://localhost:6969/docs (khi server đang chạy)
- **gpt4free Documentation:** https://github.com/xtekky/gpt4free

---

## Kết Luận

WebAI-to-API cung cấp một cách đơn giản và hiệu quả để tích hợp Gemini AI vào ứng dụng của bạn thông qua API RESTful. Với hướng dẫn này, bạn có thể:

- ✅ Cài đặt và cấu hình server
- ✅ Tích hợp API vào bất kỳ ngôn ngữ lập trình nào
- ✅ Sử dụng conversation history và system prompts
- ✅ Xử lý lỗi và troubleshooting hiệu quả

**Chúc bạn coding vui vẻ! 🚀**
