from flask import Flask, request, render_template_string, redirect, url_for, send_file
import os
import io

app = Flask(__name__)

channels = []

# بسيط جدًا لتصنيف القنوات
def detect_category(name):
    name = name.lower()
    if "sport" in name:
        return "Sports"
    if "cartoon" in name:
        return "Kids"
    if "movie" in name or "mbc" in name:
        return "Movies"
    if "news" in name:
        return "News"
    return "General"


HTML = """
<!DOCTYPE html>
<html>
<head>
<title>stream app</title>
<style>
body { font-family: Arial; background:#111; color:white; padding:20px; }
input, button { padding:10px; margin:5px 0; width:100%; }
button { background:#00ffcc; border:none; font-weight:bold; cursor:pointer; }
.box { background:#1c1c1c; padding:15px; border-radius:10px; margin-bottom:20px; }
.channel { padding:8px; background:#333; margin:5px 0; display:flex; justify-content:space-between; }
.cat { color:yellow; font-size:12px; }
</style>
</head>
<body>

<h1>🔥 stream app</h1>

<div class="box">
<h3>Upload Channels File</h3>
<form method="POST" action="/upload" enctype="multipart/form-data">
<input type="file" name="file">
<button type="submit">Upload</button>
</form>
</div>

<div class="box">
<h3>Search</h3>
<form method="GET" action="/">
<input type="text" name="q" placeholder="Search channel">
<button type="submit">Search</button>
</form>
</div>

<div class="box">
<h3>Actions</h3>
<a href="/sort"><button>Sort by Category</button></a>
<a href="/export"><button>Export TXT</button></a>
</div>

<div class="box">
<h3>Channels ({{channels|length}})</h3>

{% for c in channels %}
<div class="channel">
<span>{{c['name']}}</span>
<span class="cat">{{c['category']}}</span>
</div>
{% endfor %}

</div>

</body>
</html>
"""


@app.route("/")
def index():
    q = request.args.get("q", "")
    if q:
        filtered = [c for c in channels if q.lower() in c["name"].lower()]
    else:
        filtered = channels

    return render_template_string(HTML, channels=filtered)


@app.route("/upload", methods=["POST"])
def upload():
    global channels

    file = request.files["file"]
    content = file.read().decode("utf-8")

    lines = content.split("\n")

    channels = []
    for i, line in enumerate(lines):
        line = line.strip()
        if line:
            channels.append({
                "id": i,
                "name": line,
                "category": detect_category(line)
            })

    return redirect(url_for("index"))


@app.route("/sort")
def sort():
    global channels
    channels = sorted(channels, key=lambda x: x["category"])
    return redirect(url_for("index"))


@app.route("/export")
def export():
    output = io.StringIO()

    for i, c in enumerate(channels):
        num = str(i+1).zfill(3)
        output.write(f"{num} - {c['name']}\n")

    mem = io.BytesIO()
    mem.write(output.getvalue().encode())
    mem.seek(0)

    return send_file(mem,
                     download_name="channels.txt",
                     as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
