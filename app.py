import re
import requests
from flask import Flask, redirect, request

app = Flask(__name__)

# ক্রলবেস বা স্ক্র্যাপারএপিআই-এর মতো ফ্রি বোট বাইপাসার প্রক্সি টোকেন (ঐচ্ছিক)
# যদি নিচের কোড এমনিতেই কাজ না করে, তবে crawlbase.com থেকে একটি ফ্রি টোকেন নিয়ে এখানে বসাতে পারেন।
CRAWLBASE_TOKEN = "" 

@app.route('/')
def home():
    return "BDIX IPTV Permanent Server is Running!"

@app.route('/stream')
def get_stream():
    match_id = request.args.get('match', 'star-sports-1')
    server = request.args.get('server')

    # সঠিক ইউআরএল স্ট্রাকচার তৈরি
    if server:
        target_url = f"https://footstreams.me/watch/{match_id}-admin-{server}"
    else:
        target_url = f"https://footstreams.me/watch/{match_id}"

    # ব্রাউজারকে হুবহু নকল করার জন্য অ্যাডভান্সড হেডার্স
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Referer": "https://footstreams.me/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1"
    }

    try:
        session = requests.Session()
        
        # যদি আপনার কাছে ফ্রি ক্রলবেস বা স্ক্র্যাপারএপিআই টোকেন থাকে, তবে এটি অটোমেটিক বোট প্রোটেকশন বাইপাস করবে
        if CRAWLBASE_TOKEN:
            api_url = f"https://api.crawlbase.com/?token={CRAWLBASE_TOKEN}&url={target_url}"
            html_content = session.get(api_url, timeout=15).text
        else:
            # সরাসরি অ্যাডভান্সড হেডার্স দিয়ে ট্রাই করা
            html_content = session.get(target_url, headers=headers, timeout=12).text

        # স্ক্রিনশটের lb8.strmd.st বা যেকোনো সাবডোমেইনের সাথে .m3u8 লিংকটি খোঁজার রেগুলার এক্সপ্রেশন
        match = re.search(r'https://[a-zA-Z0-9\.]+\.strmd\.st/secure/[^\s"\']+playlist\.m3u8', html_content)
        
        if match:
            # লাইভ .m3u8 লিংকটি পাওয়া গেলে রিডাইরেক্ট হবে
            return redirect(match.group(0), code=302)
            
        # ব্যাকআপ চেক: যদি কোডের ভেতরে ডোমেইন ছাড়া শুধু পাথ থাকে
        path_match = re.search(r'/rtmp/stream/[^\s"\']+/playlist\.m3u8', html_content)
        if path_match:
            dom_match = re.search(r'https://[a-zA-Z0-9\.]+\.strmd\.st', html_content)
            base_domain = dom_match.group(0) if dom_match else "https://lb8.strmd.st"
            
            # আপনার স্ক্রিনশটের মূল স্ট্যাটিক সিকিউর পাথ পার্টটি টেম্পোরারি ব্যাকআপ হিসেবে রাখা
            full_url = f"{base_domain}/secure/QAUWckhqUnlkNqygcdGCcGOPskuUcSju{path_match.group(0)}"
            return redirect(full_url, code=302)
            
        # ডিবাগ করার জন্য পেজের আংশিক কোড আউটপুট দেওয়া
        return f"Stream not found. Cloudflare Blocked or Content Missing. Target URL: {target_url}", 404
        
    except Exception as e:
        return f"Server Error: {str(e)}", 500
