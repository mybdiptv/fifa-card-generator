from flask import Flask, Response, request

app = Flask(__name__)

@app.route('/stream')
def stream():
    # ইউজার থেকে টোকেন এবং সার্ভার নম্বর নেওয়া
    token = request.args.get('token', 'Kdmp7byfeEwY4hCRPQUJzS779TXojAc1upP_kMojK31W6fh4M05LUfVQJr8jvUU_RsAAzMbq4Q')
    server = request.args.get('server', '1')
    
    # মিডিয়া সার্ভারের লিংক
    stream_url = f"https://lb8.strmd.st/secure/QAUWckhqUnIkNqygcdGCcGOPskuUcSju/rtmp/stream/{token}/{server}/playlist.m3u8"
    
    # একটি HTML ফাইল রিটার্ন করা হবে যা ব্রাউজারে রেফারার সেট করে প্লেয়ার ওপেন করবে
    html = f"""
    <html>
    <body style="margin:0; padding:0; background:#000;">
        <video id="video" width="100%" height="100%" controls autoplay></video>
        <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
        <script>
            var video = document.getElementById('video');
            var videoSrc = '{stream_url}';
            var hls = new Hls({{
                xhrSetup: function (xhr, url) {{
                    xhr.setRequestHeader('Referer', 'https://footstreams.me/');
                }}
            }});
            hls.loadSource(videoSrc);
            hls.attachMedia(video);
        </script>
    </body>
    </html>
    """
    return html
