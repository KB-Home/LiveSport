import re
import json
import requests

def get_live_token():
    # อิงตามหน้าดูบอลที่คุณส่งมาจริงก่อนหน้านี้
    web_url = "https://atmflix.live" 
    
    # อ้างอิงค่าจาก Request Headers จริงที่คุณส่งมาเป๊ะๆ เพื่อความเสถียร
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
        'Referer': 'https://atmflix.live/',
        'Origin': 'https://atmflix.live',
        'Accept-Language': 'th,en-US;q=0.9,en;q=0.8'
    }
    try:
        response = requests.get(web_url, headers=headers, timeout=15)
        html_text = response.text
        
        # ดึงคู่ Token ออกมา
        match = re.search(r'(nimblesessionid=[^&"\'\s]+&wmsAuthSign=[^"\'\s]+)', html_text)
        if match:
            return match.group(1)
            
        session_match = re.search(r'nimblesessionid=["\']?([^"\'&\s]+)["\']?', html_text)
        auth_match = re.search(r'wmsAuthSign=["\']?([^"\'&\s]+)["\']?', html_text)
        if session_match and auth_match:
            return f"nimblesessionid={session_match.group(1)}&wmsAuthSign={auth_match.group(1)}"
    except Exception as e:
        print(f"Error fetching token: {e}")
        
    # ค่าสำรองล่าสุดที่คุณส่งมา (กรณีกดรันแล้วดึงหน้าเว็บไม่สำเร็จในรอบนั้น)
    return "nimblesessionid=20666499&wmsAuthSign=c2VydmVyX3RpbWU9OC8yOS8yMDI2IDU6NTA6MzcgUE0maGFzaF92YWx1ZT16elhKUEU3K08wM0pIODJlakFobkVBPT0mdmFsaWRtaW51dGVzPTIw"

def generate_w3u():
    token_query = get_live_token()
    w3u_data = {
        "name": "ATMFLIX Sports",
        "author": "Auto Token Bot",
        "station": [
            {
                "name": "MonoMax 3",
                "image": "https://google.com",
                "url": f"https://cdn2.stream.atmflix.live/atmflixlive/monomax-sports3/chunks.m3u8?{token_query}",
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
                "referer": "https://atmflix.live/",
                "info": "atmflix.live"
            }
        ]
    }
    # บันทึกไฟล์ในชื่อ ATMFlix.w3u ตามที่คุณใช้งาน
    with open("ATMFlix.w3u", "w", encoding="utf-8") as f:
        json.dump(w3u_data, f, ensure_ascii=False, indent=2)
    print("Playlist updated successfully!")

if __name__ == "__main__":
    generate_w3u()
