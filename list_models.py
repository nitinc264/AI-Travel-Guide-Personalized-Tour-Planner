# list_models.py
import os, requests, json
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise SystemExit("Set GOOGLE_API_KEY in .env")

url = f"https://generativelanguage.googleapis.com/v1/models?key={GOOGLE_API_KEY}"
r = requests.get(url)
r.raise_for_status()
j = r.json()

# print a compact summary so you can choose a model name
models = j.get("models") or j.get("model", [])
print("=== Models returned ===")
for m in models:
    # print the name and any useful metadata keys we commonly see
    print("NAME:", m.get("name"))
    # best effort: show fields that often indicate supported methods/actions
    for key in ("supportedActions","supportedMethods","capabilities","displayName"):
        if key in m:
            print(f"  {key}: {m.get(key)}")
    # show a trimmed full object if you want to inspect
    print("  raw preview:", json.dumps(m, indent=2)[:500])
    print("---")
