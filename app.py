from flask import Flask, request, render_template_string, redirect, url_for, send_file
import io

app = Flask(__name__)

channels = []

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
input, button { padding:10px; width:100%; margin:5px 0; }
button { background:#00ffcc;
