from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/stream')
def get_stream():
    # ব্রাউজার বা প্লেয়ার থেকে শুধু লাইভ টোকেন এবং সার্ভার নম্বর নেওয়া হবে
    token = request.args.get('token')
    server = request.args.get('server', '1')

    if not token:
        return "Error: URL-এ অবশ্যই সচল 'token' দিতে হবে।", 400

    # মিডিয়া সার্ভারের মূল ইউআরএল
    match_url = f"https://lb8.strmd.st/secure/QAUWckhqUnlkNqygcdGCcGOPskuUcSju/rtmp/stream/{token}/{server}/playlist.m3u8"

    # ৪MD Forbidden বাইপাস করার হেডার
    stream_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://footstreams.me/",
        "Origin": "https://footstreams.me"
    }

    try:
        session = requests.Session()
        stream_response = session.get(match_url, headers=stream_headers, timeout=10)
        
        if stream_response.status_code == 200:
            return Response(stream_response.text, mimetype='application/x-mpegURL')
        return f"Media Server error code: {stream_response.status_code}", stream_response.status_code
    except Exception as e:
        return f"Error: {str(e)}", 500
