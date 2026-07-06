import re
import requests
from flask import Flask, redirect, request

app = Flask(__name__)

@app.route('/')
def home():
    return "BDIX IPTV Server is Running!"

@app.route('/stream')
def get_stream():
    # ডিফল্ট হিসেবে আগের star-sports-1 রাখা হলো
    match_id = request.args.get('match', 'star-sports-1')
    server = request.args.get('server')

    # ইউআরএল ফরম্যাট সংশোধন: স্ল্যাশ (/) এর বদলে হাইফেন (-) ব্যবহার করা হয়েছে
    if server:
        source_url = f"https://footstreams.me/watch/{match_id}-admin-{server}"
    else:
        source_url = f"https://footstreams.me/watch/{match_id}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://footstreams.me/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        session = requests.Session()
        html_content = session.get(source_url, headers=headers, timeout=10).text
        
        # .m3u8 লিংক খোঁজার রেগুলার এক্সপ্রেশন
        match = re.search(r'https://[a-zA-Z0-9\.]+\.strmd\.st/secure/[^\s"\']+playlist\.m3u8', html_content)
        
        if match:
            return redirect(match.group(0), code=302)
            
        return f"Stream not found for URL: {source_url}", 404
        
    except Exception as e:
        return f"Error: {str(e)}", 500
