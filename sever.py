from flask import Flask, request, send_file, jsonify
import os
import re
import yt_dlp

app = Flask(__name__)

output_dir = "downloads"
cookies_path = "cookies.txt"
os.makedirs(output_dir, exist_ok=True)

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', '', name)

@app.route('/download', methods=['GET'])
def download_mp3():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get("title", "unknown")
            safe_title = sanitize_filename(title)

        output_path = os.path.join(output_dir, f"{safe_title}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'writethumbnail': True,
            'cookiefile': cookies_path,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                },
                {
                    'key': 'EmbedThumbnail',
                },
                {
                    'key': 'FFmpegMetadata',
                },
            ],
            'prefer_ffmpeg': True,
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        final_filename = os.path.join(output_dir, f"{safe_title}.mp3")
        if not os.path.exists(final_filename):
            return jsonify({'error': f'File not found: {final_filename}'}), 500

        return send_file(final_filename, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
