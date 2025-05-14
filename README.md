# Aura Radio - Audio Downloader Server

**Aura Radio** is a lightweight Flask-based backend server for downloading audio (MP3) from various platforms using `yt-dlp`. It supports metadata embedding, thumbnails, and cookies for premium/private content.

## Features

- Download high-quality MP3 from video URLs
- Embed thumbnails and metadata using FFmpeg
- Use YouTube or other platform cookies for private or age-restricted content
- Clean, API-based design for integration with frontend apps (like a music player)

## Requirements

- Python 3.7+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- ffmpeg (must be installed and in system PATH)

Install dependencies:

```bash
pip install flask yt-dlp
```

Make sure `ffmpeg` is installed:

```bash
# Debian/Ubuntu
sudo apt install ffmpeg

# Windows
# Download and add to PATH: https://ffmpeg.org/download.html
```

## Getting Started

Run the server:

```bash
python server.py
```

The API will be available at: `http://localhost:5000`

## Usage

Send a GET request to:

```
/download?url=<video_url>
```

Example:

```
http://localhost:5000/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

It will:

- Extract audio in MP3 format
- Embed thumbnail and metadata
- Return the file as a download

## Cookie Support

To download from platforms that require login (like private YouTube videos):

1. Export cookies from your browser using the [Cookie Editor extension](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm?utm_campaign=cgagnier.ca).
2. Open the extension and navigate to the "Export" tab.
3. Copy the cookies from the `youtube.com` domain (ensure the cookies are in **Netscape** format).
4. Save the cookies as `cookies.txt` in the root of your project.
5. The server will automatically use `cookies.txt` during downloads.

**Note:** Make sure to replace any expired cookies to ensure successful downloads from restricted content.

## Output Files

All downloaded MP3s and thumbnails are saved in the `downloads/` directory.

## Notes

- File names are sanitized to remove illegal characters.
- If the video title contains special characters, it will be cleaned.
- Error messages are returned in JSON format.

## Example Response (on error)

```json
{
  "error": "Missing URL"
}
```

## Deployment

Use a production server like Gunicorn or deploy on services like:

- Render: https://render.com
- Heroku: https://heroku.com
- Railway: https://railway.app
