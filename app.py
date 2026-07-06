import requests
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/')
def home():
    return "BDIX IPTV Permanent Proxy Server is Running!"

@app.route('/stream')
def get_stream():
    # প্লেলিস্ট বা ইউআরএল থেকে ম্যাচ আইডি এবং সার্ভার নম্বর নেওয়া
    match_id = request.args.get('match', 'portugal-vs-spain-2511721')
    server = request.args.get('server', '1')

    # ১. স্ক্রিনশটের ডাটা এবং strmd.st সার্ভারের মূল সিকিউর টোকেন পাথ প্যাটার্ন
    # এটি সরাসরি মিডিয়া প্রোভাইডারের মেইন আর্কিটেকচার হিট করবে, ফলে পেজ স্ক্র্যাপ করার প্রয়োজন নেই
    secure_hash = "QAUWckhqUnlkNqygcdGCcGOPskuUcSju"
    stream_token = "Kdmp7byfeWY4hCRPQUJzS779TXojAc1upP_kMojK31W6fH4M05LUfVQJr8jvUU_RsAAzMbq4Q"
    
    # ডাইনামিকালি প্রতিটি সার্ভারের জন্য পারফেক্ট m3u8 ইউআরএল তৈরি
    match_url = f"https://lb8.strmd.st/secure/{secure_hash}/rtmp/stream/{stream_token}/{server}/playlist.m3u8"

    # ২. ৪MD Forbidden বাইপাস করার জন্য সাইটের হুবহু অরিজিনাল হেডার্স পাস করা
    stream_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Referer": "https://footstreams.me/",
        "Origin": "https://footstreams.me",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        # Vercel ব্যাকএন্ড থেকে নিজেই ভিডিও প্লেলিস্ট ডাটা রিড করবে
        session = requests.Session()
        stream_response = session.get(match_url, headers=stream_headers, timeout=10)
        
        if stream_response.status_code == 200:
            # সঠিক মাইম-টাইপ (mimetype) সহ আপনার প্লেয়ারে লাইভ স্ট্রিম ডাটা পুশ করা
            return Response(stream_response.text, mimetype='application/x-mpegURL')
        else:
            return f"Media Server responded with status: {stream_response.status_code}. Token might be expired.", stream_response.status_code

    except Exception as e:
        return f"Server Error: {str(e)}", 500
