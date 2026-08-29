import re
import json
import requests

def get_live_token():
    web_url = "https://atmflix.live" 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
        'Referer': 'https://atmflix.live'
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
    return "nimblesessionid=20661044&wmsAuthSign=c2VydmVyX3RpbWU9OC8yOS8yMDI2IDE6Mjk6MjggUE0maGFzaF92YWx1ZT1icWNrR0d4TUtVSTJUblVCemtSV2NBPT0mdmFsaWRtaW51dGVzPTIw"

def generate_w3u():
    token_query = get_live_token()
    w3u_data = {
        "name": "ATMFLIX Live Sports",
        "author": "Auto Token Bot",
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
        "referer": "https://atmflix.live",
        "station": [
            {
                "name": "MonoMax 1",
                "image": "https://google.com",
                "url": f"https://atmflix.live?{token_query}",
                "info": "atmflix.live"
            }
        ]
    }
    with open("playlist.w3u", "w", encoding="utf-8") as f:
        json.dump(w3u_data, f, ensure_ascii=False, indent=2)
    print("Playlist updated successfully!")

if __name__ == "__main__":
    generate_w3u()
