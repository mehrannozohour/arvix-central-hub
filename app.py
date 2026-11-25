import os
import requests
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# آدرس ۳ ورکر هوش مصنوعی (در صورت تغییر آدرس تونل، این مقادیر را تغییر دهید)
WORKERS = {
    "W1": os.getenv("WORKER_1", "https://arvix-ai-studio.loca.lt"),
    "W2": os.getenv("WORKER_2", "https://arvix-post-worker.loca.lt"),
    "W3": os.getenv("WORKER_3", "https://arvix-camera-tracker.loca.lt")
}

PROXY_HEADERS = {
    "Bypass-Tunnel-Reminder": "true",
    "User-Agent": "Mozilla/5.0"
}

app = FastAPI(title="Arvix Central AI Hub")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/generate-image")
async def proxy_t2i(req: Request):
    data = await req.json()
    res = requests.post(f"{WORKERS['W1']}/generate-image", json=data, headers=PROXY_HEADERS, timeout=90)
    return res.json()

@app.post("/api/text-to-video")
async def proxy_t2v(req: Request):
    data = await req.json()
    res = requests.post(f"{WORKERS['W1']}/text-to-video", json=data, headers=PROXY_HEADERS, timeout=300)
    return res.json()

@app.post("/api/composite-tracked-video")
async def proxy_tracker(req: Request):
    data = await req.json()
    res = requests.post(f"{WORKERS['W3']}/composite-tracked-video", json=data, headers=PROXY_HEADERS, timeout=360)
    return res.json()

@app.post("/api/text-to-speech")
async def proxy_tts(req: Request):
    data = await req.json()
    res = requests.post(f"{WORKERS['W2']}/text-to-speech", json=data, headers=PROXY_HEADERS, timeout=60)
    return res.json()

@app.post("/api/transcribe-subtitle")
async def proxy_whisper(req: Request):
    data = await req.json()
    res = requests.post(f"{WORKERS['W2']}/transcribe-subtitle", json=data, headers=PROXY_HEADERS, timeout=120)
    return res.json()

@app.post("/api/upscale-image")
async def proxy_upscale(req: Request):
    data = await req.json()
    res = requests.post(f"{WORKERS['W2']}/upscale-image", json=data, headers=PROXY_HEADERS, timeout=120)
    return res.json()

HTML_PAGE = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>استودیو ابری مدیا و کامپوزیت سینمایی</title>
    <style>
        :root { --bg: #020617; --card: rgba(30, 41, 59, 0.7); --border: rgba(255, 255, 255, 0.08); --primary: #6366f1; --txt: #f8fafc; --sub: #94a3b8; }
        * { box-sizing: border-box; font-family: system-ui, sans-serif; }
        body { background: radial-gradient(circle at 50% -20%, #1e1b4b, var(--bg) 75%); color: var(--txt); margin: 0; padding: 25px 15px; }
        .container { max-width: 1050px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 25px; }
        .badge { background: rgba(99, 102, 241, 0.2); color: #a5b4fc; padding: 4px 14px; border-radius: 9999px; font-size: 12px; font-weight: 600; border: 1px solid rgba(99, 102, 241, 0.3); }
        h1 { margin: 12px 0 6px; font-size: 26px; }
        .tabs { display: flex; gap: 8px; background: rgba(15, 23, 42, 0.6); padding: 6px; border-radius: 14px; border: 1px solid var(--border); margin: 20px 0; overflow-x: auto; }
        .tab-btn { flex: 1; padding: 10px 14px; background: transparent; color: var(--sub); border: none; border-radius: 10px; cursor: pointer; font-size: 13px; font-weight: 600; white-space: nowrap; transition: 0.2s; }
        .tab-btn.active { background: rgba(99, 102, 241, 0.25); color: #fff; border: 1px solid rgba(99, 102, 241, 0.4); }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .card { background: var(--card); backdrop-filter: blur(12px); border: 1px solid var(--border); border-radius: 20px; padding: 22px; }
        label { display: block; font-size: 13px; margin-bottom: 6px; color: #cbd5e1; }
        textarea, select, input[type="file"] { width: 100%; background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border); border-radius: 12px; padding: 12px; color: #fff; font-size: 14px; outline: none; margin-bottom: 15px; }
        .btn { padding: 12px 20px; border-radius: 12px; font-weight: 600; font-size: 14px; cursor: pointer; border: none; transition: 0.2s; }
        .btn-primary { background: linear-gradient(135deg, var(--primary), #4f46e5); color: #fff; }
        .btn-secondary { background: rgba(255, 255, 255, 0.08); color: #e2e8f0; border: 1px solid var(--border); }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        @media(max-width: 768px) { .grid-2 { grid-template-columns: 1fr; } }
        .output-box { margin-top: 20px; background: rgba(15, 23, 42, 0.8); border-radius: 16px; padding: 20px; border: 1px solid rgba(99, 102, 241, 0.2); text-align: center; }
        .output-box img, .output-box video { max-width: 100%; border-radius: 12px; }
        .modal { position: fixed; inset: 0; background: rgba(2, 6, 23, 0.85); backdrop-filter: blur(8px); display: flex; align-items: center; justify-content: center; z-index: 9999; }
        .spinner { width: 44px; height: 44px; border: 4px solid rgba(99, 102, 241, 0.2); border-top-color: var(--primary); border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 15px; }
        @keyframes spin { to { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <span class="badge">Koyeb Cloud Edition</span>
            <h1>استودیو ابری مدیا و کامپوزیت سینمایی</h1>
            <p style="color:var(--sub); font-size:14px;">ارتباط سرور-به-سرور امن بدون نیاز به تونل در فرانت‌اند</p>
        </div>

        <div class="tabs">
            <button class="tab-btn active" onclick="setTab(event, 'tab-video')">🎬 ساخت ویدیو و تصویر</button>
            <button class="tab-btn" onclick="setTab(event, 'tab-track')">🎯 ترکینگ و کامپوزیت سینمایی</button>
            <button class="tab-btn" onclick="setTab(event, 'tab-tts')">🎙️ نریشن گوینده</button>
            <button class="tab-btn" onclick="setTab(event, 'tab-whisper')">📝 زیرنویس Whisper</button>
            <button class="tab-btn" onclick="setTab(event, 'tab-up')">💎 ارتقای 4K لوکنتراست</button>
        </div>

        <!-- تب ۱: ویدیو و عکس -->
        <div id="tab-video" class="tab-content active">
            <div class="card">
                <h3>تولید تصویر رفرنس و رندر ویدیوی سینمایی</h3>
                <label>توصیف صحنه (Prompt):</label>
                <textarea id="p_in" rows="3" placeholder="توصیف کامل سوژه و نورپردازی..."></textarea>
                <div style="display:flex; gap:12px;">
                    <button class="btn btn-secondary" onclick="runT2I()">🖼️ عکس رفرنس (SDXL)</button>
                    <button class="btn btn-primary" onclick="runT2V()">🎥 ویدیوی متحرک (CogVideoX)</button>
                </div>
                <div id="out_video" class="output-box" style="display:none;"></div>
            </div>
        </div>

        <!-- تب ۲: ترکینگ -->
        <div id="tab-track" class="tab-content">
            <div class="card">
                <h3>ترکینگ پلان متحرک و کروماکی لوکنتراست</h3>
                <div class="grid-2">
                    <div>
                        <label>۱. ویدیوی پرده‌سبز (MP4):</label>
                        <input type="file" id="t_vid" accept="video/mp4">
                    </div>
                    <div>
                        <label>۲. عکس رفرنس بک‌گراند (JPG/PNG):</label>
                        <input type="file" id="t_bg" accept="image/*">
                    </div>
                </div>
                <div class="grid-2">
                    <div>
                        <label>بلور عمق میدان: <span id="lbl_b">13</span></label>
                        <input type="range" id="t_blur" min="0" max="30" value="13" oninput="document.getElementById('lbl_b').innerText=this.value">
                    </div>
                    <div>
                        <label>اووراسکن حرکت دوربین: <span id="lbl_o">1.40</span>x</label>
                        <input type="range" id="t_over" min="1.1" max="1.8" step="0.05" value="1.40" oninput="document.getElementById('lbl_o').innerText=this.value">
                    </div>
                </div>
                <button class="btn btn-primary" style="width:100%; margin-top:15px;" onclick="runTrack()">🚀 شروع ترکینگ و ادغام سینمایی</button>
                <div id="out_track" class="output-box" style="display:none;"></div>
            </div>
        </div>

        <!-- تب ۳: نریشن -->
        <div id="tab-tts" class="tab-content">
            <div class="card">
                <h3>نریشن و گوینده تبلیغاتی</h3>
                <label>متن گوینده:</label>
                <textarea id="tts_in" rows="3" placeholder="متن تبلیغاتی..."></textarea>
                <div class="grid-2">
                    <div>
                        <label>انتخاب صدا:</label>
                        <select id="tts_v">
                            <option value="fa-IR-FaridNeural">فرید (گوینده مرد فارسی)</option>
                            <option value="fa-IR-DilaraNeural">دلارا (گوینده زن فارسی)</option>
                            <option value="en-US-ChristopherNeural">کریستوفر (انگلیسی)</option>
                        </select>
                    </div>
                    <div style="display:flex; align-items:flex-end;">
                        <button class="btn btn-primary" style="width:100%; margin-bottom:15px;" onclick="runTTS()">🎙️ ساخت فایل صوتی MP3</button>
                    </div>
                </div>
                <div id="out_tts" class="output-box" style="display:none;"></div>
            </div>
        </div>

        <!-- تب ۴: زیرنویس -->
        <div id="tab-whisper" class="tab-content">
            <div class="card">
                <h3>استخراج زیرنویس SRT هماهنگ (Whisper)</h3>
                <label>فایل مدیا (صوتی/تصویری):</label>
                <input type="file" id="wh_file" accept="audio/*,video/*">
                <button class="btn btn-primary" onclick="runWhisper()">⚡ پردازش با Whisper</button>
                <div id="out_wh" class="output-box" style="display:none;"></div>
            </div>
        </div>

        <!-- تب ۵: ارتقای 4K -->
        <div id="tab-up" class="tab-content">
            <div class="card">
                <h3>ارتقای 4K و گریدینگ سینمایی فلت</h3>
                <label>تصویر ورودی:</label>
                <input type="file" id="up_file" accept="image/*">
                <div style="margin-bottom:15px;">
                    <label><input type="checkbox" id="up_cine" checked> اعمال لوکنتراست سینمایی و گرین</label>
                </div>
                <button class="btn btn-primary" onclick="runUpscale()">💎 ارتقای کیفیت تا 4K</button>
                <div id="out_up" class="output-box" style="display:none;"></div>
            </div>
        </div>
    </div>

    <div id="loading" class="modal" style="display:none;">
        <div style="background:#1e293b; padding:30px; border-radius:20px; text-align:center;">
            <div class="spinner"></div>
            <h4 id="load_t" style="margin:0 0 8px;">در حال پردازش...</h4>
            <p id="load_d" style="color:var(--sub); font-size:13px; margin:0;">درخواست در حال انتقال به ورکر مربوطه است.</p>
        </div>
    </div>

    <script>
        function setTab(e, id) {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            e.currentTarget.classList.add('active');
            document.getElementById(id).classList.add('active');
        }
        function showL(t, d) { document.getElementById('load_t').innerText = t; document.getElementById('load_d').innerText = d; document.getElementById('loading').style.display = 'flex'; }
        function hideL() { document.getElementById('loading').style.display = 'none'; }
        function toB64(f) { return new Promise((res, rej) => { const r = new FileReader(); r.readAsDataURL(f); r.onload = () => res(r.result.split(',')[1]); r.onerror = rej; }); }

        async function runT2I() {
            const p = document.getElementById('p_in').value.trim();
            if(!p) return alert('پرامپت را وارد کنید.');
            showL('تولید عکس...', 'پردازش با SDXL-Turbo...');
            try {
                const res = await fetch('/api/generate-image', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({prompt:p, width:1024, height:1024}) });
                const d = await res.json();
                hideL();
                if(d.status==='success') {
                    const b = document.getElementById('out_video'); b.style.display='block';
                    b.innerHTML = `<h4>تصویر خروجی:</h4><img src="data:image/png;base64,${d.image_base64}"><br><a class="btn btn-secondary" style="display:inline-block; margin-top:10px;" href="data:image/png;base64,${d.image_base64}" download="ref.png">⬇️ دانلود تصویر</a>`;
                }
            } catch(e) { hideL(); alert('خطا: '+e); }
        }

        async function runT2V() {
            const p = document.getElementById('p_in').value.trim();
            if(!p) return alert('پرامپت را وارد کنید.');
            showL('رندر ویدیوی CogVideoX...', 'محاسبه فریم‌ها (حدود ۱ تا ۲ دقیقه)...');
            try {
                const res = await fetch('/api/text-to-video', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({prompt:p, steps:25}) });
                const d = await res.json();
                hideL();
                if(d.status==='success') {
                    const b = document.getElementById('out_video'); b.style.display='block';
                    b.innerHTML = `<h4>ویدیوی سینمایی خروجی:</h4><video controls autoplay loop src="data:video/mp4;base64,${d.video_base64}"></video><br><a class="btn btn-secondary" style="display:inline-block; margin-top:10px;" href="data:video/mp4;base64,${d.video_base64}" download="video.mp4">⬇️ دانلود ویدیو</a>`;
                }
            } catch(e) { hideL(); alert('خطا: '+e); }
        }

        async function runTrack() {
            const v = document.getElementById('t_vid').files[0];
            const bg = document.getElementById('t_bg').files[0];
            if(!v || !bg) return alert('انتخاب هر دو فایل الزامی است.');
            showL('ترکینگ پلان و کامپوزیت...', 'ردیابی حرکت دوربین و پرداخت سینمایی لوکنتراست...');
            try {
                const video_base64 = await toB64(v);
                const background_image_base64 = await toB64(bg);
                const bg_blur = parseInt(document.getElementById('t_blur').value);
                const overscan = parseFloat(document.getElementById('t_over').value);
                const res = await fetch('/api/composite-tracked-video', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({video_base64, background_image_base64, bg_blur, overscan, max_frames:120}) });
                const d = await res.json();
                hideL();
                if(d.status==='success') {
                    const b = document.getElementById('out_track'); b.style.display='block';
                    b.innerHTML = `<h4>ویدیوی نهایی (${d.frames_tracked} فریم ترک‌شده):</h4><video controls autoplay loop src="data:video/mp4;base64,${d.video_base64}"></video><br><a class="btn btn-secondary" style="display:inline-block; margin-top:10px;" href="data:video/mp4;base64,${d.video_base64}" download="tracked.mp4">⬇️ دانلود ویدیو</a>`;
                }
            } catch(e) { hideL(); alert('خطا: '+e); }
        }

        async function runTTS() {
            const text = document.getElementById('tts_in').value.trim();
            const voice = document.getElementById('tts_v').value;
            if(!text) return alert('متن را وارد کنید.');
            showL('تولید صدای نریشن...', 'مدل Edge-TTS در حال سنتز صوت...');
            try {
                const res = await fetch('/api/text-to-speech', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({text, voice}) });
                const d = await res.json();
                hideL();
                if(d.status==='success') {
                    const b = document.getElementById('out_tts'); b.style.display='block';
                    b.innerHTML = `<h4>فایل صوتی نریشن:</h4><audio controls autoplay src="data:audio/mp3;base64,${d.audio_base64}"></audio><br><a class="btn btn-secondary" style="display:inline-block; margin-top:10px;" href="data:audio/mp3;base64,${d.audio_base64}" download="voice.mp3">⬇️ دانلود MP3</a>`;
                }
            } catch(e) { hideL(); alert('خطا: '+e); }
        }

        async function runWhisper() {
            const f = document.getElementById('wh_file').files[0];
            if(!f) return alert('فایل را انتخاب کنید.');
            showL('استخراج زیرنویس...', 'پردازش با Whisper...');
            try {
                const audio_base64 = await toB64(f);
                const res = await fetch('/api/transcribe-subtitle', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({audio_base64}) });
                const d = await res.json();
                hideL();
                if(d.status==='success') {
                    const b = document.getElementById('out_wh'); b.style.display='block';
                    const url = URL.createObjectURL(new Blob([d.srt], {type:'text/plain;charset=utf-8'}));
                    b.innerHTML = `<h4>متن استخراج‌شده:</h4><p style="background:#020617; padding:10px; border-radius:8px;">${d.full_text}</p><a class="btn btn-secondary" href="${url}" download="sub.srt">⬇️ دانلود فایل SRT</a>`;
                }
            } catch(e) { hideL(); alert('خطا: '+e); }
        }

        async function runUpscale() {
            const f = document.getElementById('up_file').files[0];
            if(!f) return alert('تصویر را انتخاب کنید.');
            showL('ارتقای کیفیت 4K...', 'پردازش با Real-ESRGAN...');
            try {
                const image_base64 = await toB64(f);
                const cinematic_mode = document.getElementById('up_cine').checked;
                const res = await fetch('/api/upscale-image', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({image_base64, cinematic_mode, lift_shadows:0.05, contrast:0.82}) });
                const d = await res.json();
                hideL();
                if(d.status==='success') {
                    const b = document.getElementById('out_up'); b.style.display='block';
                    b.innerHTML = `<h4>تصویر 4K لوکنتراست:</h4><img src="data:image/png;base64,${d.image_base64}"><br><a class="btn btn-secondary" style="display:inline-block; margin-top:10px;" href="data:image/png;base64,${d.image_base64}" download="4k.png">⬇️ دانلود تصویر</a>`;
                }
            } catch(e) { hideL(); alert('خطا: '+e); }
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def root():
    return HTML_PAGE

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
