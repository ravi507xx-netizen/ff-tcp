from flask import Flask, render_template_string, redirect
import subprocess, os, signal

app = Flask(__name__)
BOT_PROC = None  # global bot process

def start_bot():
    """Start bot_core.py in a child process if not already running."""
    global BOT_PROC
    if BOT_PROC is None or BOT_PROC.poll() is not None:
        # Use same python as Render runtime
        BOT_PROC = subprocess.Popen(["python", "bot_core.py"])

def stop_bot():
    """Stop bot process if running."""
    global BOT_PROC
    if BOT_PROC and BOT_PROC.poll() is None:
        try:
            BOT_PROC.terminate()
        except Exception:
            pass

def restart_bot():
    stop_bot()
    start_bot()

HTML = '''
<!doctype html>
<title>MK TCP BOT Control</title>
<div style="max-width:640px;margin:40px auto;font-family:system-ui">
  <h2>MK TCP BOT — Control Panel</h2>
  <p>Status: <b>{{ status }}</b></p>
  <form method="post" action="/start" style="display:inline-block;margin-right:8px">
    <button type="submit">Start</button>
  </form>
  <form method="post" action="/stop" style="display:inline-block;margin-right:8px">
    <button type="submit">Stop</button>
  </form>
  <form method="post" action="/restart" style="display:inline-block">
    <button type="submit">Restart</button>
  </form>
  <hr>
  <p>Tip: Render Web Service এই অ্যাপটাকে ইন্টারনেট পোর্টে bind করবে, তাই Health OK হবে।</p>
</div>
'''

@app.route("/")
def home():
    status = "Running ✅" if BOT_PROC and BOT_PROC.poll() is None else "Stopped ❌"
    return render_template_string(HTML, status=status)

@app.route("/start", methods=["POST"])
def s():
    start_bot()
    return redirect("/")

@app.route("/stop", methods=["POST"])
def t():
    stop_bot()
    return redirect("/")

@app.route("/restart", methods=["POST"])
def r():
    restart_bot()
    return redirect("/")

if __name__ == "__main__":
    # Render sets PORT env automatically. Bind to 0.0.0.0:<PORT>
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
