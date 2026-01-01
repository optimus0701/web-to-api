# Postman Examples - WebAI-to-API

Hướng dẫn chi tiết sử dụng tất cả API endpoints với Postman.

---

## 📋 Mục Lục

- [Cấu Hình Chung](#cấu-hình-chung)
- [1. /v1/chat/completions (OpenAI-compatible)](#1-v1chatcompletions)
- [2. /gemini (New Session)](#2-gemini)
- [3. /gemini-chat (Persistent Session)](#3-gemini-chat)
- [4. /translate](#4-translate)
- [5. /v1beta/models/{model} (Google API)](#5-v1betamodelsmodel)
- [Postman Collection](#postman-collection)

---

## Cấu Hình Chung

### Base URL
```
http://localhost:6969
```

### Headers (Tất cả requests)
```
Content-Type: application/json
```

### Models Gemini Có Sẵn
- `gemini-3.0-pro` - Mạnh nhất, mới nhất
- `gemini-2.5-pro` - Cân bằng tốt
- `gemini-2.5-flash` - Nhanh nhất (mặc định)

---

## 1. /v1/chat/completions

**OpenAI-compatible endpoint** - Khuyến nghị sử dụng cho hầu hết use cases.

### 1.1. Request Đơn Giản

**Method:** `POST`  
**URL:** `http://localhost:6969/v1/chat/completions`

**Body:**
```json
{
  "model": "gemini-2.5-flash",
  "messages": [
    {
      "role": "user",
      "content": "Xin chào! Bạn là ai?"
    }
  ]
}
```

**Response:**
```json
{
  "id": "chatcmpl-1735707600",
  "object": "chat.completion",
  "created": 1735707600,
  "model": "gemini-2.5-flash",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Xin chào! Tôi là Gemini, một mô hình ngôn ngữ lớn..."
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

### 1.2. Với System Prompt

**Body:**
```json
{
  "model": "gemini-2.5-pro",
  "messages": [
    {
      "role": "system",
      "content": "Bạn là một chuyên gia lập trình Python với 10 năm kinh nghiệm."
    },
    {
      "role": "user",
      "content": "Giải thích về list comprehension"
    }
  ]
}
```

---

### 1.3. Với Conversation History

**Body:**
```json
{
  "model": "gemini-2.5-flash",
  "messages": [
    {
      "role": "system",
      "content": "Bạn là trợ lý AI thông minh và hữu ích."
    },
    {
      "role": "user",
      "content": "Python là gì?"
    },
    {
      "role": "assistant",
      "content": "Python là ngôn ngữ lập trình bậc cao, dễ học và mạnh mẽ, được tạo bởi Guido van Rossum."
    },
    {
      "role": "user",
      "content": "Nó có ứng dụng gì?"
    }
  ]
}
```

---

### 1.4. Yêu Cầu Code Generation

**Body:**
```json
{
  "model": "gemini-3.0-pro",
  "messages": [
    {
      "role": "system",
      "content": "Bạn là một chuyên gia lập trình. Hãy viết code sạch, có comment và follow best practices."
    },
    {
      "role": "user",
      "content": "Viết function Python để kiểm tra số nguyên tố"
    }
  ]
}
```

---

### 1.5. Phân Tích Dữ Liệu

**Body:**
```json
{
  "model": "gemini-2.5-pro",
  "messages": [
    {
      "role": "system",
      "content": "Bạn là data analyst chuyên nghiệp. Phân tích dữ liệu và đưa ra insights."
    },
    {
      "role": "user",
      "content": "Phân tích xu hướng AI trong năm 2024"
    }
  ]
}
```

---

### 1.6. Multi-turn Conversation (Chat Bot)

**Request 1:**
```json
{
  "model": "gemini-2.5-flash",
  "messages": [
    {
      "role": "user",
      "content": "Tôi muốn học lập trình web"
    }
  ]
}
```

**Request 2 (tiếp theo):**
```json
{
  "model": "gemini-2.5-flash",
  "messages": [
    {
      "role": "user",
      "content": "Tôi muốn học lập trình web"
    },
    {
      "role": "assistant",
      "content": "Tuyệt vời! Tôi khuyên bạn nên bắt đầu với HTML, CSS và JavaScript..."
    },
    {
      "role": "user",
      "content": "Học mất bao lâu?"
    }
  ]
}
```

---

### 1.7. Sử Dụng Model Mạnh Nhất

**Body:**
```json
{
  "model": "gemini-3.0-pro",
  "messages": [
    {
      "role": "system",
      "content": "Bạn là chuyên gia về AI và machine learning."
    },
    {
      "role": "user",
      "content": "Giải thích chi tiết về transformer architecture"
    }
  ]
}
```

---

## 2. /gemini

Tạo **session mới** cho mỗi request. Thích hợp cho các câu hỏi độc lập.

### 2.1. Request Cơ Bản

**Method:** `POST`  
**URL:** `http://localhost:6969/gemini`

**Body:**
```json
{
  "message": "Xin chào! Hôm nay thế nào?",
  "model": "gemini-2.5-flash"
}
```

**Response:**
```json
{
  "response": "Xin chào! Tôi là một mô hình AI nên không có trải nghiệm về ngày tháng như con người..."
}
```

---

### 2.2. Câu Hỏi Kiến Thức

**Body:**
```json
{
  "message": "Giải thích về blockchain",
  "model": "gemini-2.5-pro"
}
```

---

### 2.3. Yêu Cầu Sáng Tạo

**Body:**
```json
{
  "message": "Viết một câu chuyện ngắn về robot",
  "model": "gemini-3.0-pro"
}
```

---

### 2.4. Tóm Tắt Văn Bản

**Body:**
```json
{
  "message": "Tóm tắt nội dung sau: [Văn bản dài của bạn ở đây...]",
  "model": "gemini-2.5-flash"
}
```

---

### 2.5. Giải Toán

**Body:**
```json
{
  "message": "Giải phương trình: 2x + 5 = 15",
  "model": "gemini-2.5-pro"
}
```

---

## 3. /gemini-chat

Duy trì **session liên tục**. Thích hợp cho cuộc hội thoại nhiều lượt.

### 3.1. Request Đầu Tiên

**Method:** `POST`  
**URL:** `http://localhost:6969/gemini-chat`

**Body:**
```json
{
  "message": "Tôi muốn học Python",
  "model": "gemini-2.5-flash"
}
```

**Response:**
```json
{
  "response": "Tuyệt vời! Python là một lựa chọn tuyệt vời để bắt đầu lập trình..."
}
```

---

### 3.2. Request Tiếp Theo (Cùng Session)

**Body:**
```json
{
  "message": "Tôi nên bắt đầu từ đâu?",
  "model": "gemini-2.5-flash"
}
```

**Response sẽ dựa trên ngữ cảnh câu hỏi trước.**

---

### 3.3. Tiếp Tục Cuộc Hội Thoại

**Body:**
```json
{
  "message": "Còn về thư viện thì sao?",
  "model": "gemini-2.5-flash"
}
```

---

### 3.4. Chat Bot Support

**Request 1:**
```json
{
  "message": "Tôi gặp lỗi khi cài đặt package",
  "model": "gemini-2.5-pro"
}
```

**Request 2:**
```json
{
  "message": "Lỗi là 'ModuleNotFoundError'",
  "model": "gemini-2.5-pro"
}
```

**Request 3:**
```json
{
  "message": "Tôi đã thử pip install nhưng không được",
  "model": "gemini-2.5-pro"
}
```

---

### 3.5. Học Tập Tương Tác

**Session học Python:**

```json
// Request 1
{
  "message": "Dạy tôi về biến trong Python",
  "model": "gemini-2.5-flash"
}

// Request 2
{
  "message": "Cho tôi ví dụ",
  "model": "gemini-2.5-flash"
}

// Request 3
{
  "message": "Còn về kiểu dữ liệu thì sao?",
  "model": "gemini-2.5-flash"
}
```

---

## 4. /translate

Endpoint để dịch thuật. Duy trì session như `/gemini-chat`.

### 4.1. Dịch Anh → Việt

**Method:** `POST`  
**URL:** `http://localhost:6969/translate`

**Body:**
```json
{
  "message": "Translate to Vietnamese: Hello, how are you today?",
  "model": "gemini-2.5-flash"
}
```

**Response:**
```json
{
  "response": "Xin chào, hôm nay bạn thế nào?"
}
```

---

### 4.2. Dịch Việt → Anh

**Body:**
```json
{
  "message": "Translate to English: Tôi đang học lập trình",
  "model": "gemini-2.5-flash"
}
```

---

### 4.3. Dịch Văn Bản Dài

**Body:**
```json
{
  "message": "Translate to Vietnamese: Artificial Intelligence is revolutionizing the way we live and work. Machine learning algorithms can now process vast amounts of data...",
  "model": "gemini-2.5-pro"
}
```

---

### 4.4. Dịch Code Comments

**Body:**
```json
{
  "message": "Translate Python comments to Vietnamese:\n\n# Initialize the variable\nx = 10\n\n# Loop through the list\nfor item in items:\n    print(item)",
  "model": "gemini-2.5-flash"
}
```

---

### 4.5. Dịch Chuyên Ngành

**Body:**
```json
{
  "message": "Translate to Vietnamese (technical terms): The RESTful API uses HTTP methods to perform CRUD operations on resources.",
  "model": "gemini-2.5-pro"
}
```

---

## 5. /v1beta/models/{model}

**Google Generative AI v1beta API** compatible endpoint.

### 5.1. Gemini 2.5 Flash

**Method:** `POST`  
**URL:** `http://localhost:6969/v1beta/models/gemini-2.5-flash`

**Body:**
```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "Giải thích về Docker"
        }
      ]
    }
  ]
}
```

---

### 5.2. Gemini 2.5 Pro

**URL:** `http://localhost:6969/v1beta/models/gemini-2.5-pro`

**Body:**
```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "Phân tích kiến trúc microservices"
        }
      ]
    }
  ]
}
```

---

### 5.3. Gemini 3.0 Pro

**URL:** `http://localhost:6969/v1beta/models/gemini-3.0-pro`

**Body:**
```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "Explain quantum computing in detail"
        }
      ]
    }
  ]
}
```

---

### 5.4. Multi-part Content

**Body:**
```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "Phần 1: Giới thiệu về AI"
        },
        {
          "text": "Phần 2: Ứng dụng của AI"
        }
      ]
    }
  ]
}
```

---

### 5.5. Complex Query

**Body:**
```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "Phân tích và so sánh: \n1. React vs Vue.js\n2. Performance\n3. Ecosystem\n4. Learning curve\n5. Use cases"
        }
      ]
    }
  ]
}
```

---

## Postman Collection

### Cấu Hình Environment

**Environment Name:** `WebAI-Local`

**Variables:**
```
base_url: http://localhost:6969
default_model: gemini-2.5-flash
pro_model: gemini-2.5-pro
best_model: gemini-3.0-pro
```

### Sử Dụng Variables

**URL:**
```
{{base_url}}/v1/chat/completions
```

**Body:**
```json
{
  "model": "{{default_model}}",
  "messages": [...]
}
```

---

## Tests Scripts cho Postman

### Script 1: Kiểm Tra Status Code

Thêm vào tab **Tests**:

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
```

---

### Script 2: Kiểm Tra Response Structure

```javascript
pm.test("Response has choices array", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.choices).to.be.an('array');
});

pm.test("Response has content", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.choices[0].message.content).to.exist;
    pm.expect(jsonData.choices[0].message.content.length).to.be.above(0);
});
```

---

### Script 3: Log Response Time

```javascript
pm.test("Response time is less than 10s", function () {
    pm.expect(pm.response.responseTime).to.be.below(10000);
});

console.log("Response time: " + pm.response.responseTime + "ms");
```

---

### Script 4: Extract và Log Content

```javascript
// Extract response
var jsonData = pm.response.json();
var content = jsonData.choices[0].message.content;

// Log to console
console.log("=== AI Response ===");
console.log(content);
console.log("=== End Response ===");

// Save to environment (để sử dụng trong request tiếp theo)
pm.environment.set("last_response", content);
```

---

### Script 5: Validate Model

```javascript
pm.test("Correct model used", function () {
    var jsonData = pm.response.json();
    var requestedModel = pm.request.body.raw ? 
        JSON.parse(pm.request.body.raw).model : 
        pm.environment.get("default_model");
    
    pm.expect(jsonData.model).to.eql(requestedModel);
});
```

---

## Pre-request Scripts

### Script 1: Add Timestamp

```javascript
pm.environment.set("timestamp", new Date().toISOString());
console.log("Request sent at: " + pm.environment.get("timestamp"));
```

---

### Script 2: Random Model Selection

```javascript
const models = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-3.0-pro"];
const randomModel = models[Math.floor(Math.random() * models.length)];
pm.environment.set("random_model", randomModel);
console.log("Using model: " + randomModel);
```

---

## Import Collection vào Postman

### Tạo Collection JSON

Tạo file `WebAI-API-Collection.json`:

```json
{
  "info": {
    "name": "WebAI-to-API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Chat Completions",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"model\": \"{{default_model}}\",\n  \"messages\": [\n    {\n      \"role\": \"user\",\n      \"content\": \"Xin chào!\"\n    }\n  ]\n}"
        },
        "url": {
          "raw": "{{base_url}}/v1/chat/completions",
          "host": ["{{base_url}}"],
          "path": ["v1", "chat", "completions"]
        }
      }
    },
    {
      "name": "Gemini - New Session",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"message\": \"Xin chào!\",\n  \"model\": \"{{default_model}}\"\n}"
        },
        "url": {
          "raw": "{{base_url}}/gemini",
          "host": ["{{base_url}}"],
          "path": ["gemini"]
        }
      }
    },
    {
      "name": "Gemini Chat - Persistent",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"message\": \"Tiếp tục cuộc trò chuyện\",\n  \"model\": \"{{default_model}}\"\n}"
        },
        "url": {
          "raw": "{{base_url}}/gemini-chat",
          "host": ["{{base_url}}"],
          "path": ["gemini-chat"]
        }
      }
    },
    {
      "name": "Translate",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"message\": \"Translate to Vietnamese: Hello world\",\n  \"model\": \"{{default_model}}\"\n}"
        },
        "url": {
          "raw": "{{base_url}}/translate",
          "host": ["{{base_url}}"],
          "path": ["translate"]
        }
      }
    }
  ]
}
```

### Import vào Postman

1. Mở Postman
2. Click **Import**
3. Chọn file `WebAI-API-Collection.json`
4. Click **Import**

---

## Tips & Best Practices

### 1. Chọn Model Phù Hợp

- **Câu hỏi đơn giản, chat**: `gemini-2.5-flash`
- **Phân tích, lý luận**: `gemini-2.5-pro`
- **Tasks phức tạp, quan trọng**: `gemini-3.0-pro`

### 2. Tối Ưu Response Time

- Sử dụng model nhanh hơn cho simple tasks
- Giữ messages ngắn gọn
- Tránh gửi quá nhiều conversation history

### 3. Error Handling

Kiểm tra status codes:
- `200` - Success
- `400` - Bad request (kiểm tra body)
- `503` - Service unavailable (server chưa ready)
- `500` - Internal error

### 4. Organizing Collections

Tạo folders trong Collection:
- `Basic Queries`
- `Conversation`
- `Code Generation`
- `Translation`
- `Advanced`

---

**Chúc bạn test API thành công! 🚀**
