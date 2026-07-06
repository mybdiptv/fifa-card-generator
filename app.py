import re
import requests
from flask import Flask, redirect, request

app = Flask(__name__)

@app.route('/')
def home():
    return "BDIX IPTV Server is Running!"

@app.route('/stream')
def get_stream():
    # ইউজার যদি লিংকে match এবং server উল্লেখ না করে, তবে ডিফল্ট হিসেবে আগের star-sports-1 লোড হবে
    match_id = request.args.get('match', 'star-sports-1')
    server = request.args.get('server')

    # যদি server প্যারামিটার থাকে (যেমন: 1, 2, 3), তবে লিংকের শেষে /admin/{server} যোগ হবে
    if server:
        source_url = f"https://footstreams.me/watch/{match_id}/admin/{server}"
    else:
        source_url = f"https://footstreams.me/watch/{match_id}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://footstreams.me/"
    }
    
    try:
        html_content = requests.get(source_url, headers=headers, timeout=10).text
        
        # আপনার রেগুলার এক্সপ্রেশনটি আগের মতোই রাখা হয়েছে যা .m3u8 লিংকটি খুঁজে বের করবে
        match = re.search(r'https://[a-zA-Z0-9\.]+\.strmd\.st/secure/[^\s"\']+playlist\.m3u8', html_content)
        
        if match:
            return redirect(match.group(0), code=302)
        return f"Stream not found for URL: {source_url}", 404
        
    except Exception as e:
        return f"Error: {str(e)}", 500
