# Hướng Dẫn Sử Dụng Cloudflare WARP Proxy

Cấu hình Cloudflare WARP để tăng tốc độ và bypass restrictions cho WebAI-to-API.

---

## 📋 Mục Lục

- [Tại Sao Cần Proxy?](#tại-sao-cần-proxy)
- [Cài Đặt Cloudflare WARP](#cài-đặt-cloudflare-warp)
- [Cấu Hình WARP Proxy](#cấu-hình-warp-proxy)
- [Tích Hợp với WebAI-to-API](#tích-hợp-với-webai-to-api)
- [Troubleshooting](#troubleshooting)
- [Các Proxy Alternatives](#các-proxy-alternatives)

---

## Tại Sao Cần Proxy?

### Vấn Đề Khi Không Dùng Proxy:

- ❌ **Lỗi 403 Forbidden** khi kết nối Gemini
- ❌ **Response chậm** do routing không tối ưu
- ❌ **Bị rate limit** hoặc block do IP
- ❌ **Connection timeout** thường xuyên

### Lợi Ích Khi Dùng Cloudflare WARP:

- ✅ **Tăng tốc độ** - Routing tối ưu qua Cloudflare network
- ✅ **Bypass restrictions** - Thay đổi IP, tránh bị block
- ✅ **Bảo mật cao hơn** - Traffic được encrypt
- ✅ **Miễn phí** - WARP hoàn toàn free
- ✅ **Ổn định** - Cloudflare infrastructure

---

## Cài Đặt Cloudflare WARP

### Windows

#### Cách 1: Tải Official App

1. **Tải Cloudflare WARP:**
   - Truy cập: https://one.one.one.one/
   - Click **Download for Windows**
   - Hoặc link trực tiếp: https://1111-releases.cloudflareclient.com/windows/Cloudflare_WARP_Release-x64.msi

2. **Cài đặt:**
   - Chạy file `.msi` đã tải
   - Follow wizard → Next → Install
   - Chờ cài đặt hoàn tất

3. **Khởi động WARP:**
   - Mở app Cloudflare WARP từ Start Menu
   - Click **Connect/ON**
   - Đợi status thành **Connected**

4. **Kiểm tra:**
   ```powershell
   # Kiểm tra IP hiện tại
   curl ifconfig.me
   
   # Nếu WARP hoạt động, IP sẽ là Cloudflare IP
   ```

---

### Linux/Ubuntu

#### Cài đặt WARP trên Ubuntu

```bash
# 1. Thêm Cloudflare GPG key
curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg | sudo gpg --yes --dearmor --output /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg

# 2. Thêm repository
echo "deb [signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] https://pkg.cloudflareclient.com/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/cloudflare-client.list

# 3. Update và cài đặt
sudo apt-get update
sudo apt-get install cloudflare-warp

# 4. Đăng ký và kết nối
warp-cli register
warp-cli connect

# 5. Kiểm tra status
warp-cli status
```

---

### macOS

1. **Tải app:**
   - Truy cập: https://1.1.1.1/
   - Download for macOS

2. **Cài đặt:**
   - Mở file `.dmg`
   - Kéo app vào Applications
   - Mở app và click **Connect**

---

## Cấu Hình WARP Proxy

### Mode 1: WARP as System Proxy (Khuyến Nghị)

Đây là cách đơn giản nhất - WARP sẽ tự động route toàn bộ traffic.

**Windows:**
1. Mở Cloudflare WARP app
2. Click vào Settings (⚙️)
3. Preferences → Network → Enable **Gateway with WARP**
4. Click **Connect**

**Kết quả:** Toàn bộ traffic trên máy đi qua WARP, không cần config thêm.

---

### Mode 2: WARP SOCKS5 Proxy (Advanced)

Chỉ route traffic của WebAI-to-API qua WARP.

#### Bước 1: Enable WARP Proxy Mode

**Windows:**
```powershell
# Bật proxy mode (SOCKS5)
# Mặc định WARP chạy ở port 40000
```

**Linux:**
```bash
# Set WARP to proxy mode
warp-cli set-mode proxy

# Kiểm tra settings
warp-cli settings
```

#### Bước 2: WARP Proxy Address

WARP SOCKS5 proxy mặc định:
```
socks5://127.0.0.1:40000
```

---

### Mode 3: WARP via HTTP Proxy (Port Forwarding)

Nếu cần HTTP proxy thay vì SOCKS5:

#### Sử dụng Privoxy để convert SOCKS5 → HTTP

**Windows:**

1. **Tải Privoxy:**
   - https://www.privoxy.org/sf-download-mirror/Win32/
   - Tải bản mới nhất

2. **Cài đặt Privoxy**

3. **Cấu hình Privoxy:**
   
   Mở file `C:\Program Files\Privoxy\config.txt`, thêm:
   ```
   forward-socks5 / 127.0.0.1:40000 .
   listen-address 127.0.0.1:8118
   ```

4. **Restart Privoxy service**

5. **Test:**
   ```powershell
   curl -x http://127.0.0.1:8118 ifconfig.me
   ```

**Linux:**

```bash
# Cài Privoxy
sudo apt-get install privoxy

# Cấu hình
sudo nano /etc/privoxy/config

# Thêm vào cuối file:
forward-socks5 / 127.0.0.1:40000 .
listen-address 127.0.0.1:8118

# Restart
sudo systemctl restart privoxy

# Test
curl -x http://127.0.0.1:8118 ifconfig.me
```

---

## Tích Hợp với WebAI-to-API

### Option 1: System-wide WARP (Đơn Giản Nhất)

Chỉ cần bật WARP app, không cần config gì thêm.

**File `config.conf`:**
```ini
[Proxy]
# Để trống - WARP tự động handle
http_proxy =
```

**Chạy server:**
```bash
poetry run python src/run.py
```

**Kết quả:** Server tự động đi qua WARP.

---

### Option 2: SOCKS5 Proxy (Advanced)

**File `config.conf`:**
```ini
[Proxy]
# WARP SOCKS5 proxy
http_proxy = socks5://127.0.0.1:40000
```

**Restart server:**
```bash
poetry run python src/run.py
```

---

### Option 3: HTTP Proxy via Privoxy

**File `config.conf`:**
```ini
[Proxy]
# Privoxy HTTP proxy (forward to WARP)
http_proxy = http://127.0.0.1:8118
```

**Restart server:**
```bash
poetry run python src/run.py
```

---

## Kiểm Tra Proxy Hoạt Động

### Test 1: Kiểm Tra IP

**Không dùng proxy:**
```bash
curl ifconfig.me
```

**Qua WARP:**
```bash
# Windows với Privoxy
curl -x http://127.0.0.1:8118 ifconfig.me

# Linux với WARP
curl ifconfig.me  # (Nếu WARP bật system-wide)
```

IP sẽ khác và là IP của Cloudflare.

---

### Test 2: Test Gemini Connection

**Chạy server và xem logs:**

```bash
poetry run python src/run.py
```

**Check logs:**
- ✅ `INFO: ✅ WebAI-to-API mode is available`
- ✅ Không có lỗi 403

**Test API:**
```bash
curl -X POST http://localhost:6969/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.5-flash",
    "messages": [{"role": "user", "content": "Hi!"}]
  }'
```

---

### Test 3: Speed Test

**Python script:**
```python
import requests
import time

def test_speed(use_proxy=False):
    proxies = None
    if use_proxy:
        proxies = {
            'http': 'http://127.0.0.1:8118',
            'https': 'http://127.0.0.1:8118'
        }
    
    start = time.time()
    response = requests.post(
        "http://localhost:6969/v1/chat/completions",
        json={
            "model": "gemini-2.5-flash",
            "messages": [{"role": "user", "content": "Hello"}]
        },
        proxies=proxies
    )
    elapsed = time.time() - start
    
    return elapsed

# Test
print(f"Without WARP: {test_speed(False):.2f}s")
print(f"With WARP: {test_speed(True):.2f}s")
```

---

## Troubleshooting

### 1. WARP Không Kết Nối

**Triệu chứng:** Status stuck ở "Connecting..."

**Giải pháp:**

```bash
# Windows: Reset WARP
# Mở WARP app → Settings → Advanced → Reset

# Linux: Reset
warp-cli disconnect
warp-cli delete
warp-cli register
warp-cli connect
```

---

### 2. Lỗi "Proxy Connection Failed"

**Kiểm tra WARP đang chạy:**

**Windows:**
```powershell
# Check WARP service
Get-Service -Name "Cloudflare WARP"

# Nếu stopped, start:
Start-Service -Name "Cloudflare WARP"
```

**Linux:**
```bash
# Check status
warp-cli status

# Start if needed
warp-cli connect
```

---

### 3. Server Vẫn Bị 403

**Option 1: Kiểm tra proxy config**

```ini
# config.conf
[Proxy]
http_proxy = http://127.0.0.1:8118  # Đảm bảo đúng port
```

**Option 2: Test proxy thủ công**

```bash
# Test proxy hoạt động
curl -x http://127.0.0.1:8118 https://www.google.com

# Nếu không hoạt động, kiểm tra Privoxy
```

**Option 3: Restart toàn bộ**

```bash
# Stop server
# Restart WARP
# Restart Privoxy (nếu dùng)
# Start server lại
```

---

### 4. Response Vẫn Chậm

**Nguyên nhân:** WARP có thể routing qua các node xa.

**Giải pháp:**

```bash
# Linux: Thử endpoint gần hơn
warp-cli set-primary-ipv4 1.1.1.1

# Hoặc switch sang WARP+ (nếu có)
```

---

## Các Proxy Alternatives

### 1. v2ray/v2rayN (Advanced)

**Ưu điểm:**
- Cực kỳ linh hoạt
- Nhiều protocols (VMess, VLESS, Trojan)
- Speed tốt

**Nhược điểm:**
- Phức tạp hơn
- Cần mua/thuê server

**Download:**
- Windows: https://github.com/2dust/v2rayN
- Linux: https://github.com/v2fly/v2ray-core

**Config cho WebAI-to-API:**
```ini
[Proxy]
http_proxy = http://127.0.0.1:10809  # v2ray SOCKS port
```

---

### 2. Clash (GUI-friendly)

**Ưu điểm:**
- Giao diện đẹp
- Rule-based routing
- Speed test built-in

**Nhược điểm:**
- Cần subscription

**Download:**
- Windows: Clash for Windows
- Linux: Clash for Linux

**Config:**
```ini
[Proxy]
http_proxy = http://127.0.0.1:7890  # Clash default port
```

---

### 3. Shadowsocks

**Ưu điểm:**
- Nhẹ, đơn giản
- Speed tốt

**Config:**
```ini
[Proxy]
http_proxy = socks5://127.0.0.1:1080
```

---

## So Sánh Proxy Options

| Proxy | Speed | Free | Ease of Use | Stability |
|-------|-------|------|-------------|-----------|
| **Cloudflare WARP** | ⚡⚡⚡ | ✅ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| v2ray | ⚡⚡⚡⚡ | ❌ | ⭐⭐ | ⭐⭐⭐⭐ |
| Clash | ⚡⚡⚡⚡ | ❌ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Shadowsocks | ⚡⚡⚡ | ❌ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

**Khuyến nghị:** Dùng **Cloudflare WARP** cho phần lớn use cases (free, stable, easy).

---

## Configuration Examples

### Production Setup với WARP

**File `config.conf`:**
```ini
[AI]
default_ai = gemini
default_model_gemini = gemini-2.5-flash
gemini_cookie_1psid = 
gemini_cookie_1psidts = 

[EnabledAI]
gemini = true

[Browser]
name = chrome

[Proxy]
# Cloudflare WARP qua Privoxy
http_proxy = http://127.0.0.1:8118
```

**Chạy production:**
```bash
# Docker
docker compose -f docker-compose.yml up -d

# Local
cd src
uvicorn app.main:app --host 0.0.0.0 --port 6969 --workers 4
```

---

## Docker với WARP

### Option 1: Host Network Mode

```yaml
# docker-compose.yml
services:
  web_ai:
    build: .
    network_mode: "host"  # Dùng host network, access WARP
    environment:
      - PYTHONPATH=/app/src
```

**Config:**
```ini
[Proxy]
http_proxy = http://127.0.0.1:8118
```

---

### Option 2: Container Link

```yaml
services:
  web_ai:
    build: .
    environment:
      - PYTHONPATH=/app/src
      - http_proxy=http://host.docker.internal:8118
      - https_proxy=http://host.docker.internal:8118
```

---

## Monitoring

**Script để monitor proxy health:**

```python
import requests
import time

def check_proxy_health():
    """Kiểm tra proxy có hoạt động không"""
    
    proxies = {
        'http': 'http://127.0.0.1:8118',
        'https': 'http://127.0.0.1:8118'
    }
    
    try:
        # Test get IP
        response = requests.get(
            'https://ifconfig.me', 
            proxies=proxies, 
            timeout=10
        )
        
        ip = response.text.strip()
        print(f"✅ Proxy working - IP: {ip}")
        return True
        
    except Exception as e:
        print(f"❌ Proxy error: {e}")
        return False

# Check mỗi 60s
while True:
    check_proxy_health()
    time.sleep(60)
```

---

## Best Practices

### 1. Always Monitor Proxy Status

```bash
# Linux cron job
*/5 * * * * warp-cli status | grep -q "Connected" || warp-cli connect
```

### 2. Fallback Configuration

Có backup plan nếu WARP down:

```python
# Auto-detect proxy
def get_proxy():
    # Try WARP first
    try:
        requests.get('http://127.0.0.1:8118', timeout=2)
        return {'http': 'http://127.0.0.1:8118'}
    except:
        # Fallback to no proxy
        return None
```

### 3. Log Proxy Usage

```python
import logging

logging.info(f"Using proxy: {os.getenv('http_proxy', 'None')}")
```

---

## Tổng Kết

### Quick Start với WARP:

```bash
# 1. Cài WARP
# Download từ: https://1.1.1.1/

# 2. Cài Privoxy (nếu cần HTTP proxy)
# Windows: Download từ privoxy.org
# Linux: sudo apt install privoxy

# 3. Config Privoxy
# Thêm vào config: forward-socks5 / 127.0.0.1:40000 .

# 4. Config WebAI-to-API
# config.conf: http_proxy = http://127.0.0.1:8118

# 5. Chạy server
poetry run python src/run.py
```

### Kết Quả:

- ✅ Không còn lỗi 403
- ✅ Response nhanh hơn 30-50%
- ✅ Ổn định hơn
- ✅ IP reputation tốt hơn

**Chúc bạn setup thành công! 🚀**
