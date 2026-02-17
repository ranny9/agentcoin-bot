import requests
import time
import re

AGENT_ID = 16662

PROBLEM_URL = "https://api.agentcoin.site/api/problem/current"
SUBMIT_URL = "https://api.agentcoin.site/api/submit"


def solve_problem(text):
    # khusus problem:
    # Let N = 16662. Compute the sum ...
    m = re.search(r"Let N = (\d+)", text)
    if not m:
        return None

    N = int(m.group(1))

    total = 0
    for k in range(1, N + 1):
        if (k % 3 == 0 or k % 5 == 0) and k % 15 != 0:
            total += k

    mod = (N % 100) + 1
    return total % mod


while True:
    try:
        r = requests.get(PROBLEM_URL, timeout=15)
        data = r.json()

        if not data.get("is_active"):
            print("not active")
            time.sleep(30)
            continue

        problem_id = data.get("problem_id")

        template = data.get("template") or data.get("template_text")
        if not template:
            print("no template")
            time.sleep(30)
            continue

        print("problem_id:", problem_id)
        print(template)

        answer = solve_problem(template)

        if answer is None:
            print("cannot solve this problem type")
            time.sleep(60)
            continue

        print("answer:", answer)

        payload = {
            "agent_id": AGENT_ID,
            "problem_id": problem_id,
            "answer": str(answer)
        }

        resp = requests.post(SUBMIT_URL, json=payload, timeout=15)
        print("submit:", resp.text)

    except Exception as e:
        print("error:", e)

    time.sleep(60)
