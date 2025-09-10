# worker.py
import time
import json
import os

# ملف بسيط لمعالجة "المهام" من commands.json
# (نسخة أولية: يستدعي دوال مبسطة ويمكن تطويرها لاحقًا مع OpenAI و scraping)

def fetch_data(command):
    # مثال: لوامرك تكون نصوص (مثل "بحث عن شركة X")
    return f"Mock data for: {command}"

def analyze_data(data):
    # ملخص بسيط تحليلي placeholder
    return f"Summary -> {data}"

def ensure_files():
    if not os.path.exists("commands.json"):
        with open("commands.json", "w", encoding="utf-8") as f:
            json.dump({"pending": [], "done": []}, f, ensure_ascii=False, indent=2)

def process_pending():
    with open("commands.json", "r", encoding="utf-8") as f:
        commands = json.load(f)
    pending = list(commands.get("pending", []))
    for cmd in pending:
        print("[WORKER] processing:", cmd)
        data = fetch_data(cmd)
        result = analyze_data(data)
        # انشئ ملف نتائج مؤقت للمراجعة أو التخزين
        out = {
            "task": cmd,
            "result": result,
            "raw": data,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        # اكتب ملف نتيجة في مجلد pending_artifacts
        os.makedirs("pending_artifacts", exist_ok=True)
        out_path = os.path.join("pending_artifacts", f"{int(time.time())}.json")
        with open(out_path, "w", encoding="utf-8") as of:
            json.dump(out, of, ensure_ascii=False, indent=2)
        # حرك المهمة من pending إلى done
        with open("commands.json", "r", encoding="utf-8") as f:
            c = json.load(f)
        if cmd in c.get("pending", []):
            c["pending"].remove(cmd)
            c.setdefault("done", []).append(cmd)
            with open("commands.json", "w", encoding="utf-8") as f:
                json.dump(c, f, ensure_ascii=False, indent=2)
        print("[WORKER] finished:", cmd)

def main():
    ensure_files()
    print("[WORKER] started")
    while True:
        try:
            process_pending()
        except Exception as e:
            print("[WORKER] error:", e)
        time.sleep(8)

if __name__ == "__main__":
    main()
