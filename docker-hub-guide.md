# Hướng Dẫn Build và Push Docker Image lên Docker Hub

## 📋 Mục Lục
- [Giới Thiệu](#giới-thiệu)
- [Yêu Cầu](#yêu-cầu)
- [Cấu Hình](#cấu-hình)
- [Build Docker Image](#build-docker-image)
- [Chạy với Docker Compose](#chạy-với-docker-compose)
- [Push lên Docker Hub](#push-lên-docker-hub)
- [Troubleshooting](#troubleshooting)

---

## Giới Thiệu

Project **WebAI-to-API** đã có sẵn cấu hình Docker với:
- ✅ `Dockerfile` - Định nghĩa image
- ✅ `docker-compose.yml` - Cấu hình production mode
- ✅ `docker-compose.override.yml` - Cấu hình development mode
- ✅ `Makefile` - Các lệnh build/run đơn giản

---

## Yêu Cầu

Đảm bảo bạn đã cài đặt:

- [Docker](https://docs.docker.com/get-docker/) (phiên bản mới nhất)
- [Docker Compose v2.24+](https://docs.docker.com/compose/)
- GNU Make (tùy chọn, để sử dụng Makefile)
- Tài khoản [Docker Hub](https://hub.docker.com/) (để push image)

### Kiểm Tra Cài Đặt

```bash
# Kiểm tra Docker
docker --version

# Kiểm tra Docker Compose
docker compose version

# Kiểm tra Make (tùy chọn)
make --version
```

---

## Cấu Hình

### Bước 1: Tạo File `.env`

Project sử dụng file `.env` để cấu hình môi trường:

```bash
# Tạo file .env
echo "ENVIRONMENT=development" > .env
```

**Nội dung file `.env`:**

```env
# Môi trường (development hoặc production)
ENVIRONMENT=development
```

**Lưu ý:**
- `ENVIRONMENT=development`: Chạy ở chế độ development với auto-reload
- `ENVIRONMENT=production`: Chạy ở chế độ production với 4 workers

### Bước 2: Tạo File `config.conf`

```bash
# Copy từ template
cp config.conf.example config.conf
```

**Chỉnh sửa `config.conf`:**

```ini
[AI]
default_ai = gemini
default_model_gemini = gemini-2.5-flash
gemini_cookie_1psid =
gemini_cookie_1psidts =

[EnabledAI]
gemini = true

[Browser]
name = firefox

[Proxy]
http_proxy =
```

---

## Build Docker Image

### Cách 1: Sử Dụng Makefile (Khuyến Nghị)

```bash
# Build image thông thường
make build

# Build image từ đầu (xóa cache)
make build-fresh
```

### Cách 2: Sử Dụng Docker CLI

```bash
# Build image với tag
docker build -t cornatul/webai.ai:latest .

# Build không dùng cache
docker build --no-cache -t cornatul/webai.ai:latest .
```

### Cách 3: Sử Dụng Docker Compose

```bash
# Build service
docker compose build

# Build không dùng cache
docker compose build --no-cache
```

---

## Chạy với Docker Compose

### Development Mode (Chế độ Phát Triển)

**Cấu hình `.env`:**
```env
ENVIRONMENT=development
```

**Chạy server:**

```bash
# Sử dụng Makefile
make up

# Hoặc sử dụng Docker Compose trực tiếp
docker compose up
```

**Đặc điểm Development Mode:**
- ✅ Auto-reload khi code thay đổi
- ✅ Chạy ở foreground (xem logs trực tiếp)
- ✅ File watching với Docker Compose v2.24+
- ✅ Debug logs

**Xem logs:**
```bash
# Logs đang chạy real-time
docker compose logs -f

# Logs của container
docker logs -f web_ai_server
```

---

### Production Mode (Chế độ Production)

**Cấu hình `.env`:**
```env
ENVIRONMENT=production
```

**Chạy server:**

```bash
# Sử dụng Makefile
make up

# Hoặc sử dụng Docker Compose trực tiếp
docker compose up -d
```

**Đặc điểm Production Mode:**
- ✅ Chạy với 4 workers (uvicorn)
- ✅ Chạy ở background (detached mode)
- ✅ Auto-restart khi crash
- ✅ Tối ưu performance

**Quản lý container:**

```bash
# Xem container đang chạy
docker ps

# Xem logs
docker compose logs -f

# Restart container
docker compose restart

# Stop container
make stop
# hoặc
docker compose down
```

---

## Kiểm Tra Server

Sau khi chạy thành công:

```bash
# Kiểm tra health check
curl http://localhost:6969

# Kiểm tra API docs
# Mở browser: http://localhost:6969/docs

# Test API
curl -X POST http://localhost:6969/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.5-flash",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

---

## Push lên Docker Hub

### Bước 1: Đăng Nhập Docker Hub

```bash
# Đăng nhập vào Docker Hub
docker login

# Nhập username và password khi được yêu cầu
```

### Bước 2: Tag Image với Tên của Bạn

**Lưu ý:** Image hiện tại được tag là `cornatul/webai.ai:latest`. Bạn cần thay đổi thành username Docker Hub của mình.

**Option 1: Sửa trong `docker-compose.yml`**

```yaml
services:
  web_ai:
    build: .
    image: YOUR_DOCKERHUB_USERNAME/webai-to-api:latest  # Thay đổi tên này
    # ... rest of config
```

**Option 2: Sửa trong `Makefile`**

```makefile
build:
	docker build -t YOUR_DOCKERHUB_USERNAME/webai-to-api:latest .

push:
	docker push YOUR_DOCKERHUB_USERNAME/webai-to-api:latest
```

**Option 3: Tag lại image hiện có**

```bash
# Tag lại image với username của bạn
docker tag cornatul/webai.ai:latest YOUR_DOCKERHUB_USERNAME/webai-to-api:latest

# Ví dụ:
docker tag cornatul/webai.ai:latest optimus0701/webai-to-api:latest
```

### Bước 3: Push Image lên Docker Hub

**Sử dụng Makefile (sau khi sửa Makefile):**

```bash
make push
```

**Sử dụng Docker CLI:**

```bash
# Push image
docker push YOUR_DOCKERHUB_USERNAME/webai-to-api:latest

# Ví dụ:
docker push optimus0701/webai-to-api:latest
```

### Bước 4: Xác Nhận Push Thành Công

```bash
# Kiểm tra trên Docker Hub
# Truy cập: https://hub.docker.com/r/YOUR_DOCKERHUB_USERNAME/webai-to-api

# Hoặc pull image để test
docker pull YOUR_DOCKERHUB_USERNAME/webai-to-api:latest
```

---

## Hướng Dẫn Đầy Đủ: Từ Build đến Push

### Quy Trình Hoàn Chỉnh

```bash
# 1. Tạo file .env
echo "ENVIRONMENT=production" > .env

# 2. Tạo file config.conf
cp config.conf.example config.conf
# Chỉnh sửa config.conf theo nhu cầu

# 3. Build image
docker build -t YOUR_DOCKERHUB_USERNAME/webai-to-api:latest .

# 4. Test local
docker compose up -d

# 5. Kiểm tra
curl http://localhost:6969/docs

# 6. Stop container
docker compose down

# 7. Đăng nhập Docker Hub
docker login

# 8. Push image
docker push YOUR_DOCKERHUB_USERNAME/webai-to-api:latest
```

---

## Sử Dụng Image từ Docker Hub

Sau khi push thành công, người khác có thể sử dụng image:

### Cách 1: Pull và Run trực tiếp

```bash
# Pull image
docker pull YOUR_DOCKERHUB_USERNAME/webai-to-api:latest

# Run container
docker run -d \
  --name webai-server \
  -p 6969:6969 \
  -e PYTHONPATH=/app/src \
  -e ENVIRONMENT=production \
  YOUR_DOCKERHUB_USERNAME/webai-to-api:latest
```

### Cách 2: Sử dụng Docker Compose

**Tạo file `docker-compose.yml`:**

```yaml
services:
  web_ai:
    image: YOUR_DOCKERHUB_USERNAME/webai-to-api:latest
    container_name: web_ai_server
    restart: always
    ports:
      - "6969:6969"
    environment:
      - PYTHONPATH=/app/src
      - ENVIRONMENT=production
```

**Chạy:**

```bash
docker compose up -d
```

---

## Troubleshooting

### 1. Lỗi "docker-compose: not found" trên Ubuntu

**Nguyên nhân:** Docker phiên bản mới (Docker Compose V2) sử dụng lệnh `docker compose` (không có dấu gạch ngang) thay vì `docker-compose` (có dấu gạch ngang).

**Giải pháp:**

**Option 1: Sử dụng lệnh mới (Khuyến nghị)**

Makefile đã được cập nhật để sử dụng `docker compose`. Nếu vẫn gặp lỗi, chạy trực tiếp:

```bash
# Thay vì: docker-compose up
docker compose up

# Thay vì: docker-compose down
docker compose down
```

**Option 2: Cài đặt docker-compose legacy**

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Hoặc cài standalone
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

**Option 3: Tạo alias**

```bash
# Thêm vào ~/.bashrc hoặc ~/.zshrc
echo 'alias docker-compose="docker compose"' >> ~/.bashrc
source ~/.bashrc
```

**Kiểm tra version:**

```bash
# Docker Compose V2 (mới)
docker compose version

# Docker Compose V1 (cũ)
docker-compose --version
```

### 2. Lỗi "Additional property develop is not allowed"

**Nguyên nhân:** File `docker-compose.override.yml` (chứa cấu hình development) vẫn được load khi chạy production mode. Thuộc tính `develop` chỉ hỗ trợ trong Docker Compose v2.24+.

**Giải pháp:**

**Option 1: Sử dụng Makefile đã cập nhật (Khuyến nghị)**

Makefile đã được sửa để chỉ load override file trong development mode:

```bash
# Production mode - chỉ dùng docker-compose.yml
docker compose -f docker-compose.yml up -d

# Development mode - dùng cả override file
docker compose -f docker-compose.yml -f docker-compose.override.yml up
```

**Option 2: Xóa/đổi tên override file khi chạy production**

```bash
# Tạm thời đổi tên
mv docker-compose.override.yml docker-compose.override.yml.bak

# Chạy production
docker compose up -d

# Khôi phục lại
mv docker-compose.override.yml.bak docker-compose.override.yml
```

**Option 3: Chạy trực tiếp với flag `-f`**

```bash
# Chỉ định file cụ thể (bỏ qua override)
docker compose -f docker-compose.yml up -d
```

### 3. Lỗi "permission denied" khi build

**Giải pháp:**

```bash
# Linux/Mac: Thêm quyền cho user
sudo usermod -aG docker $USER
# Logout và login lại

# Hoặc chạy với sudo
sudo docker build -t YOUR_DOCKERHUB_USERNAME/webai-to-api:latest .
```

### 2. Lỗi "denied: requested access to the resource is denied"

**Nguyên nhân:** Chưa đăng nhập Docker Hub hoặc không có quyền truy cập repository.

**Giải pháp:**

```bash
# Đăng nhập lại
docker logout
docker login

# Kiểm tra username
docker info | grep Username
```

### 3. Container không khởi động

**Kiểm tra logs:**

```bash
# Xem logs container
docker compose logs

# Hoặc
docker logs web_ai_server

# Kiểm tra trạng thái
docker ps -a
```

**Nguyên nhân thường gặp:**
- Thiếu file `config.conf`
- Port 6969 đã được sử dụng
- Gemini cookies không hợp lệ

### 4. Port 6969 đã được sử dụng

**Giải pháp 1: Dừng service đang dùng port**

```bash
# Windows
netstat -ano | findstr :6969
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :6969
kill -9 <PID>
```

**Giải pháp 2: Đổi port trong docker-compose.yml**

```yaml
ports:
  - "8080:6969"  # Sử dụng port 8080 thay vì 6969
```

### 5. Lỗi "no space left on device"

**Giải pháp:**

```bash
# Xóa images và containers không dùng
docker system prune -a

# Xóa volumes không dùng
docker volume prune
```

---

## Best Practices

### 1. Multi-stage Build (Tối ưu kích thước image)

**Cập nhật `Dockerfile`:**

```dockerfile
# Build stage
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app/src

EXPOSE 6969
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "6969"]
```

### 2. Tạo `.dockerignore`

**Tạo file `.dockerignore`:**

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
*.egg-info/

# Git
.git/
.gitignore

# IDE
.vscode/
.idea/
*.swp

# Docker
Dockerfile
docker-compose*.yml
.dockerignore

# Documentation
*.md
docs/

# Tests
tests/
*.test.py

# Cache
.cache/
.pytest_cache/

# Logs
*.log
logs/

# Environment
.env
.env.local
```

### 3. Versioning Images

```bash
# Tag với version cụ thể
docker build -t YOUR_DOCKERHUB_USERNAME/webai-to-api:v1.0.0 .
docker build -t YOUR_DOCKERHUB_USERNAME/webai-to-api:latest .

# Push cả hai tags
docker push YOUR_DOCKERHUB_USERNAME/webai-to-api:v1.0.0
docker push YOUR_DOCKERHUB_USERNAME/webai-to-api:latest
```

### 4. Health Checks

**Thêm vào `Dockerfile`:**

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:6969/ || exit 1
```

---

## Tổng Kết

### Quy Trình Đơn Giản với Makefile

```bash
# Setup
echo "ENVIRONMENT=production" > .env
cp config.conf.example config.conf

# Build
make build

# Test local
make up

# Stop
make stop

# Push to Docker Hub
docker login
make push
```

### Quy Trình Không Dùng Makefile

```bash
# Setup
echo "ENVIRONMENT=production" > .env
cp config.conf.example config.conf

# Build
docker build -t YOUR_DOCKERHUB_USERNAME/webai-to-api:latest .

# Test local
docker compose up -d

# Stop
docker compose down

# Push to Docker Hub
docker login
docker push YOUR_DOCKERHUB_USERNAME/webai-to-api:latest
```

---

## Tài Liệu Tham Khảo

- **Docker Documentation:** https://docs.docker.com/
- **Docker Compose:** https://docs.docker.com/compose/
- **Docker Hub:** https://hub.docker.com/
- **Project README:** [README.md](./README.md)
- **Docker Guide:** [Docker.md](./Docker.md)

**Chúc bạn deploy thành công! 🐳🚀**
