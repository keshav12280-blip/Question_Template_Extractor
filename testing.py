import json
import re
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# ---------------- LOAD ENV (ROBUST) ----------------
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENAI_API_KEY")
print(api_key);
if not api_key:
    raise ValueError(
        f"❌ OPENAI_API_KEY not set.\n"
        f"👉 Make sure .env file exists at: {env_path}\n"
        f"👉 And contains: OPENAI_API_KEY=your_key"
    )

print("✅ API Key Loaded Successfully")

client = OpenAI()

# ---------------- LLM CALL ----------------
def call_llm(question):
    prompt = f"""
You are a physics/math engine.

Given a question, return STRICT JSON with:
- concept (one word: motion, rotation, optics, thermodynamics, electrostatics, algebra, geometry)
- variables: list of {{name, value}}
- template: string with @s0 format
- steps: list of equations
- answer: variable name
- false_equations: 3 incorrect equations

Return ONLY JSON.

Question: {question}
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        temperature=0
    )

    text = response.output[0].content[0].text
    text = re.sub(r"```json|```", "", text).strip()

    return text

# ---------------- PARSER ----------------
def parse_output(output):
    try:
        return json.loads(output)
    except Exception:
        raise ValueError(f"❌ Invalid JSON from model:\n{output}")

# ---------------- SOLVER ----------------
def solve(parsed):
    env = {}

    for v in parsed.get("variables", []):
        env[v["name"]] = float(v["value"])

    for step in parsed.get("steps", []):
        if "=" in step:
            left, right = step.split("=")
            try:
                env[left.strip()] = eval(right.strip(), {}, env)
            except Exception as e:
                raise ValueError(f"❌ Error in step '{step}': {e}")

    return env

# ---------------- BUILDER ----------------
def build(question):
    raw = call_llm(question)
    parsed = parse_output(raw)
    env = solve(parsed)

    return {
        "question": question,
        "concept": parsed.get("concept"),
        "template": parsed.get("template"),
        "variables": parsed.get("variables"),
        "steps": parsed.get("steps"),
        "answer": env.get(parsed.get("answer")),
        "false_equations": parsed.get("false_equations", [])
    }

# ---------------- MAIN ----------------
if __name__ == "__main__":
    print("🚀 Question Engine Running (type 'exit' to quit)\n")

    while True:
        q = input("Enter question: ")

        if q.lower() == "exit":
            break

        try:
            result = build(q)
            print("\n✅ OUTPUT:\n")
            print(json.dumps(result, indent=2))
        except Exception as e:
            print("\n❌ ERROR:", e)