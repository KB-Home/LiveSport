import re
import json
import requests

def get_live_token():
    web_url = "https://atmflix.live/football/638081" 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
        'Referer': 'https://atmflix.live/'
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
    return "nimblesessionid=20664801&wmsAuthSign=c2VydmVyX3RpbWU9OC8yOS8yMDI2IDM6MzI6MDkgUE0maGFzaF92YWx1ZT1GS0s3M2EybFpmc1c4NWlWT09SQkZRPT0mdmFsaWRtaW51dGVzPTIw"

def generate_w3u():
    token_query = get_live_token()
    w3u_data = {
        "name": "ATMFLIX Sports",
        "author": "Auto Token Bot",
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
        "referer": "https://atmflix.live/",
        "station": [
            {
                "name": "MonoMax 3",
                "image": "https://drive.google.com/uc?export=download&id=1XWfSp-4LeKJAGbII5uVYAnDB3oZHyRST",
                "url": f"https://cdn2.stream.atmflix.live/atmflixlive/monomax-sports3/chunks.m3u8?{token_query}",
                "info": "atmflix.live"
            },
            {
                "name": "MonoMax 4",
                "image": "https://drive.google.com/uc?export=download&id=1XWfSp-4LeKJAGbII5uVYAnDB3oZHyRST",
                "url": f"https://cdn2.stream.atmflix.live/atmflixlive/monomax-sports4/chunks.m3u8?{token_query}",
                "info": "atmflix.live"
            }
        ]
    }
    with open("ATMFlix.w3u", "w", encoding="utf-8") as f:
        json.dump(w3u_data, f, ensure_ascii=False, indent=2)
    print("Playlist updated successfully!")

if __name__ == "__main__":
    generate_w3u()
