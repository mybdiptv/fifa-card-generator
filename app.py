import re
import requests
from flask import Flask, redirect, request
from urllib.parse import quote

app = Flask(__name__)

@app.route('/')
def home():
    return "BDIX IPTV Permanent Server is Running!"

@app.route('/stream')
def get_stream():
    match_id = request.args.get('match', 'star-sports-1')
    server = request.args.get('server')

    # ১. ডাইনামিক ইউআরএল বিল্ডার (ভবিষ্যতে ম্যাচ বা সার্ভার যাই বদলাক, এটি অটো তৈরি হবে)
    if server:
        target_url = f"https://footstreams.me/watch/{match_id}-admin-{server}"
    else:
        target_url = f"https://footstreams.me/watch/{match_id}"

    # ২. বোট প্রোটেকশন বাইপাস করার জন্য ফ্রি স্ক্র্যাপিং প্রক্সি মেথড (যেমন: Crawlbase বা ScraperAPI)
    # আপনি চাইলে সরাসরি ScraperAPI এর ফ্রি টোকেনও এখানে ব্যবহার করতে পারেন
    # আপাততো আমরা হেডার্স আরও স্ট্রং করে সরাসরি ট্রাই করছি, যদি ব্লক করে তবে এপিআই প্রক্সি লিংক জেনারেট হবে
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Referer": "https://footstreams.me/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive"
    }
    
    try:
        session = requests.Session()
        # মূল সাইটের সোর্স পেজ রিকোয়েস্ট
        response = session.get(target_url, headers=headers, timeout=12)
        html_content = response.text
        
        # ৩. স্মার্ট রেগুলার এক্সপ্রেশন: এটি ডোমেইন (lb8 বা অন্য কিছু) এবং টোকেন যাই হোক না কেন, 
        # শুধুমাত্র .strmd.st এবং playlist.m3u8 মিলিয়ে লাইভ লিংকটি তুলে আনবে।
        match = re.search(r'https://[a-zA-Z0-9\.]+\.strmd\.st/secure/[^\s"\']+playlist\.m3u8', html_content)
        
        if match:
            # লাইভ টোকেন সহ একদম তাজা লিংক রিডাইরেক্ট হবে
            return redirect(match.group(0), code=302)
            
        # ৪. ব্যাকআপ মেথড: যদি প্রথম স্ক্রিনশটের মতো ডিরেক্ট পাথ লুকানো থাকে
        path_match = re.search(r'/rtmp/stream/[^\s"\']+/playlist\.m3u8', html_content)
        if path_match:
            # ডোমেইন পরিবর্তন হলেও যেন কোড না ভাঙে, তাই ডাইনামিক ডোমেইন খোঁজা
            dom_match = re.search(r'https://[a-zA-Z0-9\.]+\.strmd\.st', html_content)
            base_domain = dom_match.group(0) if dom_match else "https://lb8.strmd.st"
            return redirect(f"{base_domain}/secure/QAUWckhqUnlkNqygcdGCcGOPskuUcSju{path_match.group(0)}", code=302)
            
        return f"Stream temporarily unavailable on site. Check URL: {target_url}", 404
        
    except Exception as e:
        return f"Server Error: {str(e)}", 500
