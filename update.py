import re
import json
import requests

def get_live_token():
    web_url = "https://doolive4k.tv/ดูทีวีออนไลน์" 
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
        'Referer': 'https://doolive4k.tv/',
        'Origin': 'https://doolive4k.tv',
        'Host': 'kt5kce43ak.ja-me-kai-kai-rak-kon-na-ta-yang-chan.sbs',
        'Accept-Language': 'th,en-US;q=0.9,en;q=0.8'
    }
    try:
        response = requests.get(web_url, headers=headers, timeout=15)
        html_text = response.text
        
        match = re.search(r'(nimblesessionid=[^&"\'\s]+&wmsAuthSign=[^"\'\s]+)', html_text)
        if match:
            return match.group(1)
            
        session_match = re.search(r'nimblesessionid=["\']?([^"\'&\s]+)["\']?', html_text)
        auth_match = re.search(r'wmsAuthSign=["\']?([^"\'&\s]+)["\']?', html_text)
        if session_match and auth_match:
            return f"nimblesessionid={session_match.group(1)}&wmsAuthSign={auth_match.group(1)}"
    except Exception as e:
        print(f"Error fetching token: {e}")
        
    return "nimblesessionid=7843036&wmsAuthSign=c2VydmVyX3RpbWU9OC8zMC8yMDI2IDc6MjM6MzEgQU0maGFzaF92YWx1ZT01alhlcmExZlJQWTY4aHYvd29MckZ3PT0mdmFsaWRtaW51dGVzPTM2MCZpZD0x"

def generate_w3u():
    token_query = get_live_token()
    w3u_data = {
        "name": "doolive4k",
        "author": "Auto Token Bot",
        "station": [
            {
                "name": "Bein 1",
                "image": "https://drive.google.com/uc?export=download&id=1st_OJB-u_X125waLX27KQ3WBt744wB-V",
                "url": f"https://kt5kce43ak.ja-me-kai-kai-rak-kon-na-ta-yang-chan.sbs/doolive4k-tv/bein-1-th/chunks.m3u8?{token_query}",
                "info": "doolive4k.tv"
            }
        ]
    }
    with open("doolive4k.w3u", "w", encoding="utf-8") as f:
        json.dump(w3u_data, f, ensure_ascii=False, indent=2)
    print("Playlist updated successfully!")

if __name__ == "__main__":
    generate_w3u()
