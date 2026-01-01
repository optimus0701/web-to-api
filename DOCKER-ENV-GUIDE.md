# Docker Configuration với Environment Variables

## 🎯 Những Gì Đã Thay Đổi

Giờ đây cookies và cấu hình được đọc từ **environment variables** thay vì `config.conf`, không cần rebuild Docker image khi thay đổi cookies!

---

## ✅ Priority Đọc Config

1. **Environment variables** (.env file) ⭐ Ưu tiên cao nhất
2. **config.conf** - Fallback
3. **Browser cookies** - Auto-detect nếu không có

---

## 📝 Cấu Hình File `.env`

### Tạo file `.env`:

```bash
cd ~/WebAI-to-API

# Copy từ template
cp .env.example .env

# Edit .env
nano .env
```

### Nội dung `.env`:

```env
# Docker Mode
ENVIRONMENT=production

# Gemini Cookies (QUAN TRỌNG!)
# Lấy từ: https://gemini.google.com
# F12 → Application → Cookies → gemini.google.com
GEMINI_COOKIE_1PSID=your_1psid_value_here
GEMINI_COOKIE_1PSIDTS=your_1psidts_value_here

# Browser for auto-cookie retrieval
BROWSER_NAME=chrome

# Proxy (optional)
HTTP_PROXY=
HTTPS_PROXY=
```

---

## 🚀 Sử Dụng

### 1. No Rebuild Required!

```bash
# Sửa cookies trong .env
nano .env

# Restart container (không cần build lại!)
sudo docker compose -f docker-compose.yml restart

# Hoặc stop và up lại
sudo docker compose -f docker-compose.yml down
sudo docker compose -f docker-compose.yml up -d
```

**Lợi ích:** Thay đổi cookies trong vài giây, không cần rebuild image (tiết kiệm 1-2 phút)!

---

### 2. Verify Environment Variables

```bash
# Xem env variables trong container
sudo docker exec web_ai_server env | grep GEMINI

# Nên hiện:
# GEMINI_COOKIE_1PSID=g.a000...
# GEMINI_COOKIE_1PSIDTS=sidts-...
```

---

## 📋 Workflow Mới

### Lần Đầu Setup:

```bash
# 1. Clone repo
git clone https://github.com/Amm1rr/WebAI-to-API.git
cd WebAI-to-API

# 2. Tạo .env
cp .env.example .env

# 3. Thêm cookies vào .env
nano .env
# Paste GEMINI_COOKIE_1PSID và GEMINI_COOKIE_1PSIDTS

# 4. Pull image từ Docker Hub (hoặc build local)
sudo docker pull optimus0701/web_ai_server:latest

# 5. Run
sudo docker compose -f docker-compose.yml up -d

# 6. Check logs
sudo docker logs -f web_ai_server
```

---

### Khi Cookies Hết Hạn:

```bash
# 1. Lấy cookies mới từ browser
# F12 → Application → Cookies

# 2. Update .env
nano .env
# Sửa GEMINI_COOKIE_1PSID và GEMINI_COOKIE_1PSIDTS

# 3. Restart (KHÔNG CẦN BUILD!)
sudo docker compose -f docker-compose.yml restart

# 4. Verify
curl http://localhost:6969/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gemini-2.0-flash-exp","messages":[{"role":"user","content":"Hi"}]}'
```

---

## 🔒 Security Best Practices

### 1. Protect `.env` File

```bash
# Đảm bảo .env không bị commit
echo ".env" >> .gitignore

# Set permissions (chỉ owner đọc được)
chmod 600 .env
```

### 2. Use `.env.example` Template

```bash
# Tạo template không có cookies thật
cp .env .env.example

# Xóa cookies trong .env.example
sed -i 's/GEMINI_COOKIE_1PSID=.*/GEMINI_COOKIE_1PSID=/' .env.example
sed -i 's/GEMINI_COOKIE_1PSIDTS=.*/GEMINI_COOKIE_1PSIDTS=/' .env.example

# Commit .env.example vào git
git add .env.example
git commit -m "Add .env.example template"
```

---

## 📊 So Sánh: Trước vs Sau

| Feature | Trước (config.conf) | Sau (.env) |
|---------|---------------------|------------|
| **Thay đổi cookies** | Rebuild image (1-2 min) | Restart container (5s) ⚡ |
| **Security** | Trong image | Chỉ trong .env file 🔒 |
| **Deployment** | Phức tạp | Dễ dàng ✅ |
| **Flexibility** | Thấp | Cao 🎯 |

---

## 🐳 Docker Compose Changes

**File:** `docker-compose.yml`

```yaml
environment:
  - PYTHONPATH=/app/src
  - ENVIRONMENT=${ENVIRONMENT:-production}
  # Gemini cookies - override via .env file
  - GEMINI_COOKIE_1PSID=${GEMINI_COOKIE_1PSID:-}
  - GEMINI_COOKIE_1PSIDTS=${GEMINI_COOKIE_1PSIDTS:-}
  # Browser name for auto-cookie retrieval
  - BROWSER_NAME=${BROWSER_NAME:-chrome}
  # Proxy settings
  - HTTP_PROXY=${HTTP_PROXY:-}
  - HTTPS_PROXY=${HTTPS_PROXY:-}
```

---

## 🧪 Testing

```bash
# Test with environment variables
sudo docker run -it --rm \
  -e GEMINI_COOKIE_1PSID="your_cookie" \
  -e GEMINI_COOKIE_1PSIDTS="your_cookie_ts" \
  -p 6969:6969 \
  optimus0701/web_ai_server:latest

# Test API
curl http://localhost:6969/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.0-flash-exp",
    "messages": [{"role": "user", "content": "Test"}]
  }'
```

---

## 💡 Tips

### 1. Multiple Environments

```bash
# Production
cp .env .env.production

# Development
cp .env .env.development

# Use specific env file
sudo docker compose --env-file .env.production up -d
```

### 2. Override từ Command Line

```bash
# Override cookies từ CLI
sudo GEMINI_COOKIE_1PSID="new_cookie" \
     GEMINI_COOKIE_1PSIDTS="new_cookie_ts" \
     docker compose -f docker-compose.yml up -d
```

### 3. Auto-update Cookies Script

```bash
#!/bin/bash
# update-cookies.sh

# Lấy cookies từ browser
PSID=$(...)
PSIDTS=$(...)

# Update .env
sed -i "s/GEMINI_COOKIE_1PSID=.*/GEMINI_COOKIE_1PSID=$PSID/" .env
sed -i "s/GEMINI_COOKIE_1PSIDTS=.*/GEMINI_COOKIE_1PSIDTS=$PSIDTS/" .env

# Restart
docker compose -f docker-compose.yml restart
```

---

## ✅ Checklist

- [x] Tạo file `.env` từ `.env.example`
- [ ] Thêm Gemini cookies vào `.env`
- [ ] Run `docker compose -f docker-compose.yml up -d`
- [ ] Verify logs: `docker logs web_ai_server`
- [ ] Test API endpoint
- [ ] Add `.env` vào `.gitignore`

---

**Giờ đây thay đổi cookies chỉ mất 5 giây! 🚀**
