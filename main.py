import subprocess
import time
import re

AGENT_ID = 16662  # agent kamu

SLEEP_SECONDS = 300  # 5 menit per loop

def get_current_problem():
    """Ambil problem terbaru via mine.py"""
    result = subprocess.run(["python", "mine.py", "status"], capture_output=True, text=True)
    output = result.stdout
    # parsing problem_id terakhir dari output status CLI
    m = re.search(r"problem_id[:=]\s*(\d+)", output)
    if m:
        return m.group(1)
    return None

def solve_problem(problem_id):
    """
    Contoh solve logic untuk problem tipe 427/428 dari SKILL.md
    Ini bisa dikembangkan jika ada tipe problem lain.
    """
    N = AGENT_ID
    total = sum(k for k in range(1, N+1) if (k%3==0 or k%5==0) and k%15!=0)
    mod = (N % 100) + 1
    return total % mod

def submit_answer(problem_id, answer):
    """Submit jawaban via CLI resmi mine.py"""
    cmd = ["python", "mine.py", "submit", "--problem-id", str(problem_id), "--answer", str(answer)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("Submit output:", result.stdout)

def claim_rewards():
    """Claim reward via CLI"""
    result = subprocess.run(["python", "mine.py", "claim"], capture_output=True, text=True)
    print("Claim output:", result.stdout)

def main():
    print(f"Auto Mining started for Agent ID {AGENT_ID}")
    loops = 0

    while True:
        problem_id = get_current_problem()
        if problem_id:
            print(f"Found problem: {problem_id}")
            answer = solve_problem(problem_id)
            print(f"Calculated answer: {answer}")
            submit_answer(problem_id, answer)
        else:
            print("No active problem found. Waiting...")

        loops += 1
        if loops % 12 == 0:  # kira-kira 1 jam
            claim_rewards()

        time.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    main()
