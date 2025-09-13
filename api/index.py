from flask import Flask, render_template_string, request, redirect, url_for, session
import uuid

app = Flask(__name__)
app.secret_key = "supersecret"

# Admin credentials
ADMIN_USER = "The-Hassan"
ADMIN_PASS = "Hassan-786"

# Approved & Pending storage
approved_ids = set()
pending_ids = set()

# Background image
bg_image = "https://i.ibb.co/wrC4P96k/23740f20818450daec3818412c7fa1e9.jpg"

# ----------------- Approval Page -----------------
approval_page = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Approval System</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta2/css/all.min.css"/>
<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: url("{{ bg_image }}") no-repeat center center fixed;
  background-size: cover;
  color: #FFFF99;
  text-align: center;
  padding: 20px;
}
.card {
  max-width: 420px;
  margin: 60px auto;
  padding: 20px;
  border-radius: 15px;
  background: rgba(0,0,0,0.7);
  box-shadow: 0 0 25px rgba(255,255,255,0.2);
}
h1 { font-size: 28px; animation: neon 1.5s infinite alternate; color:#FFFF99; }
@keyframes neon { from { text-shadow:0 0 5px #ff00cc;} to{ text-shadow:0 0 20px #00ffff,0 0 30px #ff00cc;} }
.device-box { background:#222; padding:10px; border-radius:8px; margin:15px 0; font-size:14px; word-wrap: break-word; color:#fff; }
.status { margin:15px 0; padding:8px; border-radius:8px; font-weight:bold; color:#fff; }
.approved { background: green; }
.rejected { background: red; }
.btn { margin:10px; padding:12px 22px; font-size:16px; border-radius:25px; border:none; cursor:pointer; font-weight:bold; }
.start { background: white; color: black; }
.admin { background: none; color: #FFFF99; border: 2px solid #ff0077; box-shadow:0 0 10px #ff0077; }
.icons { margin-top:20px; }
.icons a { font-size:22px; margin:0 10px; transition:0.3s; }
.icons a.whatsapp { color:#25D366; }
.icons a.facebook { color:#1877F2; }
.icons a.github { color:#FFFFFF; }
.icons a.youtube { color:#FF0000; }
.icons a:hover.whatsapp { color:#00ff00; text-shadow:0 0 10px #25D366; }
.icons a:hover.facebook { color:#33a2ff; text-shadow:0 0 10px #1877F2; }
.icons a:hover.github { color:#ffffff; text-shadow:0 0 10px #ffffff; }
.icons a:hover.youtube { color:#ff3333; text-shadow:0 0 10px #FF0000; }
.footer { margin-top:25px; font-size:18px; font-weight:bold; text-align:center; color:#fff; }
.footer span { background: linear-gradient(90deg,#ff00cc,#00ffff); -webkit-background-clip:text; -webkit-text-fill-color:transparent; animation: glow 2s infinite alternate; }
@keyframes glow { from{ text-shadow:0 0 5px #ff00cc;} to{ text-shadow:0 0 20px #00ffff,0 0 30px #ff00cc;} }
.copyright { font-size:12px; margin-top:10px; color:#fff; }
</style>
</head>
<body>
<div class="card">
<h1>🔥 HASSAN APK.0.1 🔥</h1>
<p>Your Device ID:</p>
<div class="device-box">{{ device_id }}</div>

{% if approved %}
  <div class="status approved">✅ Approved</div>
  <button class="btn start" onclick="window.location.href='/main'">🚀 START</button>
{% else %}
  <div class="status rejected">❌ Not Approved</div>
  <button class="btn start" onclick="alert('⏳ Wait for admin approval!')">🚀 START</button>
{% endif %}

<a href="{{ url_for('admin') }}"><button class="btn admin">👤 Admin Panel</button></a>

<div class="icons">
  <a href="https://www.facebook.com/Hassandastagir091" title="Facebook"><i class="fab fa-facebook"></i></a>
  <a href="https://wa.me/+923472864331" title="WhatsApp"><i class="fab fa-whatsapp"></i></a>
  <a href="https://github.com/devixayyat/" title="GitHub"><i class="fab fa-github"></i></a>
  <a href="https://youtube.com/@hassanshah-g5y5j?si=EIqvlXB9jEbOuCbf"><i class="fab fa-youtube"></i></a>
</div>

<div class="footer">
<marquee behavior="scroll" direction="left" scrollamount="6">✨ Made by <span>Mr Hassan Dastagir</span> ✨</marquee>
<p class="copyright">© 2025 MR HASSAN All RIGHTS RESERVED.</p>
</div>
</div>
</body>
</html>
'''

# ----------------- Routes -----------------
@app.route('/')
def approval():
    if "device_id" not in session:
        session["device_id"] = str(uuid.uuid4())
    device_id = session["device_id"]
    if device_id not in approved_ids and device_id not in pending_ids:
        pending_ids.add(device_id)
    approved = device_id in approved_ids
    return render_template_string(approval_page, device_id=device_id, approved=approved, bg_image=bg_image)

@app.route('/main')
def main():
    device_id = session.get('device_id')
    if device_id in approved_ids:
        return f"<h1>Welcome {device_id} ✅</h1>"
    return redirect(url_for('approval'))

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == "POST":
        user = request.form.get("username")
        pw = request.form.get("password")
        if user == ADMIN_USER and pw == ADMIN_PASS:
            session['admin'] = True
            return redirect(url_for('dashboard'))
    return '''
<form method="post">
<input name="username" placeholder="Username">
<input name="password" placeholder="Password" type="password">
<button type="submit">Login</button>
</form>
'''

@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    return f"<h2>Approved: {list(approved_ids)}</h2><h2>Pending: {list(pending_ids)}</h2>"

@app.route('/approve/<device_id>')
def approve(device_id):
    approved_ids.add(device_id)
    pending_ids.discard(device_id)
    return redirect(url_for('dashboard'))

@app.route('/reject/<device_id>')
def reject(device_id):
    approved_ids.discard(device_id)
    pending_ids.discard(device_id)
    return redirect(url_for('dashboard'))

# ----------------- Serverless handler -----------------
from mangum import Mangum
handler = Mangum(app)
