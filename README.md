# AltchaSolver

Simple ALTCHA proof-of-work solver + payload builder.

## What It Does

- Solves a SHA-256 ALTCHA challenge by brute force.
- Builds a base64 ALTCHA payload for form submission.
- Includes a small runnable example in the same file.

## Class API

### AltchaSolver.solve_challenge(challenge, salt, maxnumber=1000000)

Returns:

- dict like `{"number": 12345, "took": 42}` on success
- `None` if no solution is found in the range

### AltchaSolver.build_payload(challenge_data, solution)

Returns:

- base64 payload string on success
- empty string if `solution` is missing

Expected keys in `challenge_data`:

- `algorithm`
- `challenge`
- `salt`
- `signature`

## Quick Example

```python
from AltchaSolver import AltchaSolver

challenge_data = {
    "algorithm": "SHA-256",
    "challenge": "...",
    "salt": "...",
    "signature": "...",
}

solver = AltchaSolver()
solution = solver.solve_challenge(
    challenge=challenge_data["challenge"],
    salt=challenge_data["salt"],
    maxnumber=50000,
)

payload = solver.build_payload(challenge_data, solution)
print(payload)
```

## Run The Built-In Demo

The bottom block in [AltchaSolver.py](AltchaSolver.py) does:

1. GET `/altcha`
2. solve challenge
3. POST payload to `/submit`

Run:

```bash
python AltchaSolver.py
```

## Requirements

- Python 3.10+
- `requests`

Install:

```bash
pip install requests
```
