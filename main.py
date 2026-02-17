import time
import os
import requests

# -----------------------------
# CONFIG
# -----------------------------
AGENT_ID = int(os.environ.get("AGENT_ID", "16662"))  # pastikan variable ini ada di Railway
API_URL = "https://agentcoin.site/api/problem/cu"    # endpoint problem (cek sesuai docs)
SUBMIT_URL = "https://agentcoin.site/api/submit"    # endpoint submit (cek sesuai docs)
SLEEP_SECONDS = 10
# -----------------------------

def solve(N):
    """Sum of integers <= N divisible by 3 or 5 but not 15"""
    def sum_divisible_by(d):
        m = N // d
        return d * m * (m + 1) // 2

    s3 = sum_divisible_by(3)
    s5 = sum_divisible_by(5)
    s15 = sum_divisible_by(15)
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
            print("Fetching problem...")
            r = requests.get(API_URL, timeout=15)
            print("Status code:", r.status_code)

            if r.status_code != 200:
                time.sleep(SLEEP_SECONDS)
                continue

            data = r.json()
            if "problem_id" not in data:
                print("No problem_id, sleeping...")
                time.sleep(SLEEP_SECONDS)
                continue

            problem_id = data["problem_id"]
            question = data.get("question", "")
            is_active = data.get("is_active", False)
            print("Problem id:", problem_id)
            print("Active:", is_active)
            print("Question:", question)

            if not is_active:
                print("Not active, waiting...")
                time.sleep(SLEEP_SECONDS)
                continue

            if "divisible by 3 or 5" not in question:
                print("Cannot solve this problem type")
                time.sleep(SLEEP_SECONDS)
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

            print("Submitting answer:", payload)
            res = requests.post(SUBMIT_URL, json=payload, timeout=15)
            print("Submit response:", res.text)

        except Exception as e:
            print("Error:", e)

        time.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    main()
