from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "BDIX IPTV Smart Server is Running!"

@app.route('/stream')
def get_stream():
    # প্লেলিস্ট থেকে টোকেন এবং সার্ভার নম্বর রিড করা হবে
    token = request.args.get('token')
    server = request.args.get('server', '1')

    if not token:
        return "Error: Please provide the active live 'token' parameter in the URL.", 400

    # ১. প্রথম স্ক্রিনশট থেকে পাওয়া ফিক্সড প্লেয়ার আইডি ও ডাইনামিক টোকেন স্ট্রাকচার
    secure_hash = "QAUWckhqUnlkNqygcdGCcGOPskuUcSju"
    match_url = f"https://lb8.strmd.st/secure/{secure_hash}/rtmp/stream/{token}/{server}/playlist.m3u8"

    # ২. ৪MD 403 Forbidden বাইপাস করার জন্য অরিজিনাল হেডার্স
    stream_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Referer": "https://footstreams.me/",
        "Origin": "https://footstreams.me"
    }

    try:
        session = requests.Session()
        stream_response = session.get(match_url, headers=stream_headers, timeout=10)
        
        if stream_response.status_code == 200:
            # সঠিক হেডার পাস করে প্লেয়ারে লাইভ ডাটা পুশ করা
            return Response(stream_response.text, mimetype='application/x-mpegURL')
        else:
            return f"Media Server responded with status: {stream_response.status_code}. Token might be expired or IP blocked.", stream_response.status_code

    except Exception as e:
        return f"Server Error: {str(e)}", 500
