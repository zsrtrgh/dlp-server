from flask import Flask, request, Response
import yt_dlp
import urllib.parse

app = Flask(__name__)

def is_youtube(url):
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.netloc.endswith(('youtube.com', 'youtu.be')):
        return True
    return False

def generate_stream(url, media_type, quality):
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'outtmpl': '-',
        'no_warnings': True,
    }
    
    if is_youtube(url):
        if quality == 'best':
            ydl_opts['format'] = 'best'
        else:
            if media_type == 'audio':
                ydl_opts['format'] = 'bestaudio'
            else:
                ydl_opts['format'] = '18'  # YouTube format code for 360p MP4
        
    if media_type == 'audio':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '0',  # '0' is for lossless
        }]
        content_type = 'audio/wav'
    else:
        content_type = 'video/mp4'
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        best_format = info_dict['url']
        
        with ydl.urlopen(best_format) as stream:
            while True:
                chunk = stream.read(1024)
                if not chunk:
                    break
                yield chunk



@app.route('/download')
def download():
    url = request.args.get('url')
    media_type = request.args.get('type', 'video')
    quality = request.args.get('quality', 'standard')
    
    if not url:
        return "Error: No URL provided", 400
    
    if media_type not in ['audio', 'video']:
        return "Error: Invalid type. Must be 'audio' or 'video'", 400
    
    if quality not in ['standard', 'best']:
        return "Error: Invalid quality. Must be 'standard' or 'best'", 400
    
    return Response(generate_stream(url, media_type, quality), content_type='audio/wav' if media_type == 'audio' else 'video/mp4')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
