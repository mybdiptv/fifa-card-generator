from flask import Flask, redirect, request

app = Flask(__name__)

@app.route('/stream')
def get_stream():
    # সরাসরি ব্রাউজার থেকে টোকেন এবং সার্ভার নম্বর নিচ্ছি
    token = request.args.get('token')
    server = request.args.get('server', '1')
    
    if not token:
        return "Token missing! please provide ?token=...&server=1", 400

    # মিডিয়া সার্ভারের সরাসরি লিংক
    # এখানে আমরা কোনো হেডার বা পাইথন প্রক্সি ব্যবহার করছি না, সরাসরি রিডাইরেক্ট করছি
    target_url = f"https://lb8.strmd.st/secure/QAUWckhqUnlkNqygcdGCcGOPskuUcSju/rtmp/stream/{token}/{server}/playlist.m3u8"
    
    # এটি ব্রাউজারকে সরাসরি ওই লিংকে পাঠিয়ে দেবে
    return redirect(target_url, code=302)
