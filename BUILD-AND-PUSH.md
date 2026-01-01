# Build và Push Docker Image lên Docker Hub

## 🎯 Hướng Dẫn Build và Push Image mới

### Bước 1: Đăng Nhập Docker Hub

```bash
# Đăng nhập Docker Hub
docker login

# Nhập username: optimus0701
# Nhập password/token của bạn
```

---

### Bước 2: Build Docker Image

**Trên Ubuntu Server:**

```bash
cd ~/WebAI-to-API

# Build image với tag mới
sudo docker build -t optimus0701/web_ai_server:latest .

# Hoặc dùng Makefile
sudo make build
```

**Kết quả:** Image được build với tên `optimus0701/web_ai_server:latest`

---

### Bước 3: Test Image Local

```bash
# Test image trước khi push
sudo docker compose -f docker-compose.yml up

# Hoặc run trực tiếp
sudo docker run -d \
  --name web_ai_test \
  -p 6969:6969 \
  -e PYTHONPATH=/app/src \
  optimus0701/web_ai_server:latest

# Test API
curl http://localhost:6969/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.0-flash-exp",
    "messages": [{"role": "user", "content": "Hi!"}]
  }'
```

---

### Bước 4: Push lên Docker Hub

```bash
# Push image
sudo docker push optimus0701/web_ai_server:latest

# Hoặc dùng Makefile
sudo make push
```

**Progress sẽ hiện:**
```
The push refers to repository [docker.io/optimus0701/web_ai_server]
...
latest: digest: sha256:... size: ...
```

---

### Bước 5: Verify trên Docker Hub

1. Mở browser: https://hub.docker.com/
2. Login với account `optimus0701`
3. Vào Repositories
4. Kiểm tra `web_ai_server` đã có image mới

---

## 📊 Thay Đổi Đã Áp Dụng

### 1. **Updated Model Names** ✅

**File: `src/schemas/request.py`**

```python
class GeminiModels(str, Enum):
    # Gemini 2.0 Series (Latest)
    FLASH_2_0_EXP = "gemini-2.0-flash-exp"          # Mặc định
    EXP_ADVANCED_2_0 = "gemini-2.0-exp-advanced"
    
    # Gemini 1.5 Series (Stable)
    PRO_1_5 = "gemini-1.5-pro"
    FLASH_1_5 = "gemini-1.5-flash"
    PRO_RESEARCH_1_5 = "gemini-1.5-pro-research"
```

### 2. **Updated Docker Image Name** ✅

**File: `docker-compose.yml`**
```yaml
image: optimus0701/web_ai_server:latest  # Changed
```

**File: `Makefile`**
```makefile
build:
    docker build -t optimus0701/web_ai_server:latest .

push:
    docker push optimus0701/web_ai_server:latest
```

---

## 🚀 Quick Commands

### Build Fresh (Xóa Cache)

```bash
sudo make build-fresh
```

### Build và Push Một Lệnh

```bash
# Build và test
sudo make build
sudo docker compose -f docker-compose.yml up -d
curl http://localhost:6969/docs

# Nếu OK, push
sudo make push
```

---

## 📝 Sử Dụng Image từ Docker Hub

Sau khi push, người khác có thể dùng:

```bash
# Pull image
docker pull optimus0701/web_ai_server:latest

# Run
docker run -d \
  --name web_ai_server \
  -p 6969:6969 \
  -e PYTHONPATH=/app/src \
  -e ENVIRONMENT=production \
  optimus0701/web_ai_server:latest
```

**Hoặc với docker-compose.yml:**

```yaml
services:
  web_ai:
    image: optimus0701/web_ai_server:latest  # Từ Docker Hub
    container_name: web_ai_server
    restart: always
    ports:
      - "6969:6969"
    environment:
      - PYTHONPATH=/app/src
      - ENVIRONMENT=production
```

---

## 🔧 Troubleshooting

### Lỗi "denied: requested access to the resource is denied"

```bash
# Đăng nhập lại
docker logout
docker login
# Nhập username: optimus0701
```

### Lỗi "unauthorized: authentication required"

```bash
# Kiểm tra đã login đúng account chưa
docker info | grep Username

# Phải hiện: Username: optimus0701
```

### Push chậm

```bash
# Kiểm tra kích thước image
docker images optimus0701/web_ai_server

# Nếu quá lớn (>1GB), xem xét tối ưu Dockerfile
```

---

## 📖 Test API với Models Mới

### Available Models:

| Model Name | Type | Speed | Description |
|------------|------|-------|-------------|
| `gemini-2.0-flash-exp` | Latest | ⚡⚡⚡ | Fastest, experimental |
| `gemini-2.0-exp-advanced` | Latest | ⚡⚡ | Advanced experimental |
| `gemini-1.5-pro` | Stable | ⚡⚡ | Production ready |
| `gemini-1.5-flash` | Stable | ⚡⚡⚡ | Fast & stable |
| `gemini-1.5-pro-research` | Stable | ⚡ | Research tasks |

### Test Request:

```bash
curl -X POST http://localhost:6969/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.0-flash-exp",
    "messages": [
      {"role": "user", "content": "Xin chào!"}
    ]
  }'
```

**Response:**
```json
{
  "id": "chatcmpl-...",
  "model": "gemini-2.0-flash-exp",
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "Xin chào! ..."
    }
  }]
}
```

---

## ✅ Checklist Hoàn Thành

- [x] Cập nhật model names trong `src/schemas/request.py`
- [x] Cập nhật default model trong `src/app/config.py`
- [x] Cập nhật image name trong `docker-compose.yml`
- [x] Cập nhật image name trong `Makefile`
- [ ] Build image: `sudo make build`
- [ ] Test local: `sudo docker compose -f docker-compose.yml up`
- [ ] Login Docker Hub: `docker login`
- [ ] Push image: `sudo make push`
- [ ] Verify trên Docker Hub

---

**Chúc bạn build và push thành công! 🐳🚀**
