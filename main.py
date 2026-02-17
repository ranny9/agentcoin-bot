import time
import os
import requests

API_URL = "https://agentcoin.site/api/problem"
SUBMIT_URL = "https://agentcoin.site/api/submit"

AGENT_ID = int(os.environ.get("AGENT_ID", "16662"))

def solve(N):
    def sum_divisible_by(d):
        m = N // d
        return d * m * (m + 1) // 2

    s3 = sum_divisible_by(3)
    s5 = sum_divisible_by(5)
    s15 = sum_divisible_by(15)

    # divisible by 3 or 5 but NOT 15
    result = s3 + s5 - 2 * s15

    return result

def solve_with_mod(N):
    total = solve(N)
    mod = (N % 100) + 1
    return total % mod

def main():
    print("Agent started, id =", AGENT_ID)

    while True:
        try:
            r = requests.get(API_URL)
            if r.status_code != 200:
                time.sleep(5)
                continue

            data = r.json()

            if "problem_id" not in data:
                time.sleep(5)
                continue

            problem_id = data["problem_id"]
            question = data["question"]

            if "divisible by 3 or 5" not in question:
                print("cannot solve this problem type")
                time.sleep(5)
                continue

            if "modulo" in question:
                answer = solve_with_mod(AGENT_ID)
            else:
                answer = solve(AGENT_ID)

            payload = {
                "agent_id": AGENT_ID,
                "problem_id": problem_id,
                "answer": str(answer)
            }

            res = requests.post(SUBMIT_URL, json=payload)
            print("submit:", res.text)

        except Exception as e:
            print("error:", e)

        time.sleep(10)

if __name__ == "__main__":
    main()
