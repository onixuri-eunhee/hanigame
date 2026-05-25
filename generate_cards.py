import requests, base64, os, time, json

API_KEY = "YOUR_GOOGLE_API_KEY_HERE"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-fast-generate-001:predict?key={API_KEY}"
OUT = "/Users/eunhuismacbook/Desktop/hanigame/images"

STYLE = (
    "cute chibi kawaii flat illustration for children's educational game, "
    "bold outlines, bright saturated colors, simple clean background with soft gradient, "
    "adorable expressive face, rounded shapes, sticker-book style, "
    "no text, no words, square composition"
)

CARDS = [
    ("01_hello",             "cute chibi cartoon child waving hello with both hands, big happy smile, school uniform, colorful confetti falling, joyful"),
    ("02_my_name",           "cute chibi cartoon boy pointing proudly to himself with a shiny star name badge on chest, sparkling eyes, warm background"),
    ("03_six_years",         "cute chibi cartoon child holding up 6 fingers, smiling widely next to a colorful birthday cake with 6 lit candles"),
    ("04_want_firefighter",  "cute chibi cartoon child wearing oversized red firefighter helmet, eyes closed dreaming, sparkly thought bubble with fire helmet above head"),
    ("05_brave_firefighter", "brave cute chibi firefighter standing heroically in front of bright orange flames, red uniform with yellow stripe, both fists raised, confident smile"),
    ("06_help_people",       "cute chibi firefighter in red uniform gently carrying a small grateful person to safety, warm caring expression, glowing heart"),
    ("07_save_lives",        "cute chibi firefighter carefully cradling a fluffy puppy rescued from danger, bright red heart glowing around them, blue sky"),
    ("08_woo_woo",           "adorable bright red cartoon fire truck zooming fast on road, big flashing siren lights red and blue, speed lines, happy face on truck"),
    ("09_police",            "cute chibi cartoon child proudly wearing police officer cap with gold badge, thumbs up pose, navy blue uniform, shiny badge on chest"),
    ("10_strong",            "cute chibi police officer flexing both arms showing big muscles, shiny gold badge, determined proud smile, yellow sparkle effects"),
    ("11_catch",             "cute chibi police officer running fast chasing a funny round green cartoon villain, handcuffs flying in air, action pose"),
    ("12_keep_safe",         "cute chibi police officer standing with arms spread wide protectively in front of a small happy family, warm golden shield glow"),
    ("13_doctor_child",      "cute chibi cartoon child wearing oversized white doctor coat, holding stethoscope with excited expression, red cross on coat pocket"),
    ("14_doctors_kind",      "warm gentle chibi doctor smiling softly, large glowing red heart floating above, soft pastel hospital background, white coat"),
    ("15_help_sick",         "caring chibi doctor handing colorful medicine bottle to a small sick patient with rosy cheeks, gentle warm smile, clinic background"),
    ("16_feel_better",       "happy chibi cartoon character jumping with joy arms raised after full recovery, golden stars and sparkles exploding all around, big grin"),
    ("17_help_wide",         "cute chibi cartoon child standing with both arms spread wide open ready to help everyone, warm golden glow, red and pink hearts floating"),
    ("18_dream",             "chibi cartoon child peacefully sleeping on a fluffy cloud, dream thought bubble showing tiny firefighter police officer and doctor together, starry night sky"),
    ("19_thank_you",         "cute chibi cartoon child bowing deeply with both hands pressed together, colorful flowers and confetti surrounding them, grateful expression"),
]

headers = {"Content-Type": "application/json"}

for i, (fname, prompt) in enumerate(CARDS):
    out_path = f"{OUT}/{fname}.png"
    if os.path.exists(out_path):
        print(f"[SKIP] {fname}.png already exists")
        continue

    full_prompt = f"{prompt}. {STYLE}"
    body = {
        "instances": [{"prompt": full_prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "1:1",
            "safetyFilterLevel": "BLOCK_SOME",
            "personGeneration": "ALLOW_ALL"
        }
    }

    print(f"[{i+1:02d}/{len(CARDS)}] Generating {fname} ...")
    try:
        r = requests.post(URL, headers=headers, json=body, timeout=60)
        if r.status_code == 200:
            data = r.json()
            b64 = data["predictions"][0]["bytesBase64Encoded"]
            with open(out_path, "wb") as f:
                f.write(base64.b64decode(b64))
            print(f"       ✅ saved {fname}.png")
        else:
            print(f"       ❌ HTTP {r.status_code}: {r.text[:200]}")
    except Exception as e:
        print(f"       ❌ Error: {e}")

    # 1초 대기 (rate limit 방지)
    if i < len(CARDS) - 1:
        time.sleep(1.2)

print("\n완료! 생성된 파일:")
for f in sorted(os.listdir(OUT)):
    print(f"  {f}")
