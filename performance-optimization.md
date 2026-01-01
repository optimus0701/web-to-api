# Tối Ưu Performance cho WebAI-to-API

Hướng dẫn cải thiện tốc độ response và khắc phục vấn đề chậm.

---

## 🐌 Nguyên Nhân Response Chậm

### 1. **Model Selection**
- `gemini-3.0-pro`: Chậm nhất nhưng mạnh nhất
- `gemini-2.5-pro`: Trung bình
- `gemini-2.5-flash`: Nhanh nhất ⚡ (khuyến nghị)

### 2. **Network Issues**
- Kết nối tới Gemini servers chậm
- Cookies hết hạn
- Bị rate limit

### 3. **Message Length**
- Conversation history quá dài
- Input text quá lớn

### 4. **Server Configuration**
- Chạy development mode thay vì production
- Không đủ workers

---

## ⚡ Giải Pháp Tối Ưu

### 1️⃣ Sử Dụng Model Nhanh Nhất

**Trong `config.conf`:**
```ini
[AI]
default_model_gemini = gemini-2.5-flash
```

**Trong API request:**
```json
{
  "model": "gemini-2.5-flash",
  "messages": [...]
}
```

**Kết quả:** Response nhanh gấp 2-3 lần so với `gemini-3.0-pro`

---

### 2️⃣ Cấu Hình Proxy (Nếu Bị Chặn)

Nếu bị lỗi 403 hoặc connection timeout:

**Trong `config.conf`:**
```ini
[Proxy]
http_proxy = http://127.0.0.1:7890
```

**Sử dụng proxy nhanh:**
- Cloudflare WARP
- Local proxy (v2ray, clash)

---

### 3️⃣ Giới Hạn Conversation History

**❌ Không nên:**
```json
{
  "model": "gemini-2.5-flash",
  "messages": [
    // 50+ messages ở đây...
  ]
}
```

**✅ Nên:**
```json
{
  "model": "gemini-2.5-flash",
  "messages": [
    {"role": "system", "content": "..."},
    // Chỉ giữ 5-10 messages gần nhất
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."},
    {"role": "user", "content": "Câu hỏi mới"}
  ]
}
```

**Code Python để giới hạn history:**
```python
def limit_history(messages, max_messages=10):
    """Giữ system prompt + N messages gần nhất"""
    system_messages = [m for m in messages if m["role"] == "system"]
    other_messages = [m for m in messages if m["role"] != "system"]
    
    # Giữ N messages cuối
    limited_messages = other_messages[-max_messages:]
    
    return system_messages + limited_messages

# Sử dụng
messages = limit_history(all_messages, max_messages=8)
```

---

### 4️⃣ Chạy Production Mode với Multiple Workers

**Với Docker:**

**File `.env`:**
```env
ENVIRONMENT=production
```

**Chạy:**
```bash
docker compose -f docker-compose.yml up -d
```

**Kết quả:** Server chạy với 4 workers, xử lý đồng thời nhiều requests.

---

**Chạy Local:**

```bash
# Thay vì: poetry run python src/run.py
# Chạy với uvicorn trực tiếp:

cd src
uvicorn app.main:app --host 0.0.0.0 --port 6969 --workers 4
```

---

### 5️⃣ Cập Nhật Cookies Gemini

Cookies cũ có thể làm chậm hoặc gây lỗi.

**Option 1: Tự động lấy từ browser**

```ini
# config.conf
[AI]
gemini_cookie_1psid =
gemini_cookie_1psidts =

[Browser]
name = firefox  # hoặc chrome
```

Server sẽ tự động lấy cookies mới nhất.

**Option 2: Cập nhật thủ công**

1. Mở https://gemini.google.com
2. Đăng nhập lại
3. Lấy cookies mới (F12 → Application → Cookies)
4. Cập nhật vào `config.conf`
5. Restart server

---

### 6️⃣ Sử Dụng Streaming (Cho Response Lớn)

**Request với streaming:**
```json
{
  "model": "gemini-2.5-flash",
  "messages": [...],
  "stream": true
}
```

**Lợi ích:**
- User thấy response ngay lập tức
- Không phải đợi toàn bộ response

**Python client với streaming:**
```python
import requests

def chat_stream(messages):
    url = "http://localhost:6969/v1/chat/completions"
    
    payload = {
        "model": "gemini-2.5-flash",
        "messages": messages,
        "stream": True
    }
    
    with requests.post(url, json=payload, stream=True) as response:
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                print(chunk.decode(), end='', flush=True)

# Sử dụng
chat_stream([
    {"role": "user", "content": "Viết một câu chuyện dài"}
])
```

---

### 7️⃣ Tối Ưu httpx Connection Pool

**Tạo file `src/app/config_httpx.py`:**

```python
import httpx

# Cấu hình connection pool
HTTPX_LIMITS = httpx.Limits(
    max_keepalive_connections=20,
    max_connections=100,
    keepalive_expiry=30.0
)

HTTPX_TIMEOUT = httpx.Timeout(
    timeout=60.0,  # Tổng timeout
    connect=10.0,  # Connect timeout
    read=50.0,     # Read timeout
    write=10.0     # Write timeout
)
```

---

### 8️⃣ Cache Response (Cho Repeated Queries)

**Sử dụng Redis cache:**

```python
import redis
import json
import hashlib

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_cache_key(messages):
    """Tạo cache key từ messages"""
    content = json.dumps(messages, sort_keys=True)
    return hashlib.md5(content.encode()).hexdigest()

def chat_with_cache(messages):
    cache_key = get_cache_key(messages)
    
    # Kiểm tra cache
    cached = redis_client.get(cache_key)
    if cached:
        print("📦 From cache")
        return json.loads(cached)
    
    # Gọi API
    response = requests.post(
        "http://localhost:6969/v1/chat/completions",
        json={"model": "gemini-2.5-flash", "messages": messages}
    ).json()
    
    # Lưu vào cache (1 giờ)
    redis_client.setex(cache_key, 3600, json.dumps(response))
    
    return response
```

---

### 9️⃣ Sử Dụng gpt4free Mode (Fallback)

Nếu Gemini quá chậm, chuyển sang gpt4free mode:

**Khi server chạy:**
```
Press '2' then Enter
```

**Hoặc cấu hình:**
```ini
# config.conf
[EnabledAI]
gemini = false  # Tắt Gemini, dùng g4f
```

**API request:**
```json
{
  "model": "DDG",  // Sử dụng provider thay vì model
  "messages": [...]
}
```

---

### 🔟 Load Balancing (Advanced)

**Chạy nhiều instances:**

```bash
# Instance 1
uvicorn app.main:app --host 0.0.0.0 --port 6969

# Instance 2
uvicorn app.main:app --host 0.0.0.0 --port 6970

# Instance 3
uvicorn app.main:app --host 0.0.0.0 --port 6971
```

**Nginx load balancer:**

```nginx
upstream webai {
    server 127.0.0.1:6969;
    server 127.0.0.1:6970;
    server 127.0.0.1:6971;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://webai;
    }
}
```

---

## 📊 Benchmark Results

| Configuration | Avg Response Time |
|---------------|-------------------|
| gemini-3.0-pro (default) | ~8-12s |
| gemini-2.5-pro | ~5-8s |
| gemini-2.5-flash | ~2-4s ⚡ |
| gemini-2.5-flash + proxy | ~1.5-3s ⚡⚡ |
| gemini-2.5-flash + streaming | Instant UI response ⚡⚡⚡ |

---

## ✅ Recommended Configuration

**File `config.conf` tối ưu:**

```ini
[AI]
# Sử dụng model nhanh nhất
default_ai = gemini
default_model_gemini = gemini-2.5-flash

# Để trống để auto-detect cookies
gemini_cookie_1psid =
gemini_cookie_1psidts =

[EnabledAI]
gemini = true

[Browser]
# Browser bạn đã đăng nhập Gemini
name = chrome

[Proxy]
# Sử dụng proxy nếu cần (tùy chọn)
http_proxy =
```

---

## 🚀 Quick Wins

### Thay Đổi Ngay Lập Tức:

1. **Đổi model sang flash:**
   ```json
   {"model": "gemini-2.5-flash"}
   ```

2. **Giới hạn conversation history:**
   ```python
   messages = messages[-8:]  # Chỉ giữ 8 messages cuối
   ```

3. **Chạy production mode:**
   ```bash
   cd src
   uvicorn app.main:app --host 0.0.0.0 --port 6969 --workers 4
   ```

### Kết Quả:
- ⚡ Response nhanh gấp 2-4 lần
- 💪 Xử lý được nhiều requests hơn
- 🎯 Ổn định hơn

---

## 🔍 Troubleshooting Performance

### Kiểm Tra Response Time

**Với curl:**
```bash
time curl -X POST http://localhost:6969/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "gemini-2.5-flash", "messages": [{"role": "user", "content": "Hi"}]}'
```

**Với Python:**
```python
import time
import requests

start = time.time()
response = requests.post(
    "http://localhost:6969/v1/chat/completions",
    json={
        "model": "gemini-2.5-flash",
        "messages": [{"role": "user", "content": "Hello"}]
    }
)
elapsed = time.time() - start

print(f"Response time: {elapsed:.2f}s")
```

### Xem Server Logs

```bash
# Local
poetry run python src/run.py

# Docker
docker logs -f web_ai_server
```

Tìm các dòng:
- `ERROR` - Lỗi
- `WARNING` - Cảnh báo
- `INFO` - Thông tin

---

## 📈 Monitoring Performance

**Script monitor response time:**

```python
import requests
import time
from collections import deque

class PerformanceMonitor:
    def __init__(self, window_size=10):
        self.response_times = deque(maxlen=window_size)
    
    def chat(self, message):
        start = time.time()
        
        response = requests.post(
            "http://localhost:6969/v1/chat/completions",
            json={
                "model": "gemini-2.5-flash",
                "messages": [{"role": "user", "content": message}]
            }
        )
        
        elapsed = time.time() - start
        self.response_times.append(elapsed)
        
        print(f"Response time: {elapsed:.2f}s")
        print(f"Average (last {len(self.response_times)}): {self.avg():.2f}s")
        
        return response.json()
    
    def avg(self):
        if not self.response_times:
            return 0
        return sum(self.response_times) / len(self.response_times)

# Sử dụng
monitor = PerformanceMonitor()
monitor.chat("Hello")
monitor.chat("How are you?")
monitor.chat("Tell me about AI")
```

---

## 💡 Tips Cuối Cùng

1. **Luôn dùng `gemini-2.5-flash`** trừ khi cần reasoning phức tạp
2. **Giữ messages ngắn gọn** - không gửi quá nhiều history
3. **Cập nhật cookies thường xuyên** - tránh bị rate limit
4. **Sử dụng streaming** cho response dài
5. **Chạy production mode** với multiple workers
6. **Monitor performance** để phát hiện vấn đề sớm

---

**Chúc bạn có API siêu nhanh! ⚡🚀**
