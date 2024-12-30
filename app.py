from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

def fetch_info(url):
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'no_warnings': True,
        'format': 'best'  # 必要に応じて変更可能
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
    return info_dict

@app.route('/', methods=['GET'])
def fetch_info_route():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        info = fetch_info(url)
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
