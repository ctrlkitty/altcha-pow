import base64
import hashlib
import json
import time


class AltchaSolver:
    def solve_challenge(self, challenge, salt, maxnumber=1000000):
        t0 = time.time()

        for n in range(maxnumber + 1):
            guess = hashlib.sha256((salt + str(n)).encode()).hexdigest()
            if guess == challenge:
                return {
                    "number": n,
                    "took": int((time.time() - t0) * 1000),
                }

        print(f"No solution found")
        return None

    def build_payload(self, challenge_data, solution):
        if solution is None:
            print("No solution available, payload not built")
            return ""

        raw = json.dumps(
            {
                "algorithm": challenge_data["algorithm"],
                "challenge": challenge_data["challenge"],
                "number": solution["number"],
                "salt": challenge_data["salt"],
                "signature": challenge_data["signature"],
                "took": solution["took"],
            },
            separators=(",", ":"),
        ).encode()

        return base64.b64encode(raw).decode("utf-8")


# Example usage
if __name__ == "__main__":
    import requests

    base_url = "http://217.154.51.201"
    challenge_url = f"{base_url}/altcha"
    submit_url = f"{base_url}/submit"

    try:
        challenge_data = requests.get(challenge_url, timeout=15).json()
    except Exception as e:
        print(f"Failed to fetch challenge: {e}")
        exit(1)

    solver = AltchaSolver()
    result = solver.solve_challenge(challenge_data["challenge"], challenge_data["salt"])
    payload = solver.build_payload(challenge_data, result)

    if not payload:
        print("Nothing to submit")
        exit(1)

    submit_resp = requests.post(
        submit_url,
        data={"altcha": payload, "note": "solved successfully"},
        timeout=15,
    )

    print(f"resp: {submit_resp.text}")
