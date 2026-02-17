import requests
import time

AGENT_ID = "16662"
URL = "https://api.agentcoin.site/api/problem/current"

while True:
    try:
        r = requests.get(URL, timeout=10)
        data = r.json()

        print("is_active:", data.get("is_active"))
        print("problem_id:", data.get("problem_id"))

        template = data.get("template") or data.get("template_text")

        if template:
            q = template.replace("{AGENT_ID}", AGENT_ID)
            print("question:")
            print(q)

        else:
            print("no template field found")

    except Exception as e:
        print("error:", e)

    print("sleep 60s...\n")
    time.sleep(60)
