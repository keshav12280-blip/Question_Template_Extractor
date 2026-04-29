import json
import re
import os
from datetime import datetime
from openai import OpenAI

client = OpenAI()

# ---------------- LLM CALL ----------------
def call_llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content

# ---------------- PARSER ----------------
def parse_question(question):
    prompt = f"""
You are a physics/math parser.

Extract structured JSON:
- variables (s0, s1...)
- template (@s0 format)
- steps (formula steps)
- answer variable

Return ONLY JSON.

Question: {question}
"""

    output = call_llm(prompt)
    output = re.sub(r"```json|```", "", output).strip()

    return json.loads(output)

# ---------------- CONCEPT DETECTION ----------------
def detect_concept(question):
    prompt = f"""
Classify into one:
motion, rotation, optics, thermodynamics, electrostatics, algebra, geometry

Return one word.

Question: {question}
"""
    return call_llm(prompt).strip().lower()

# ---------------- SOLVER ----------------
def solve(parsed):
    env = {}

    for v in parsed["variables"]:
        env[v["name"]] = float(v["value"])

    for step in parsed["steps"]:
        if "=" in step:
            left, right = step.split("=")
            env[left.strip()] = eval(right.strip(), {}, env)

    return env

# ---------------- FALSE EQUATIONS ----------------
def generate_false(parsed):
    prompt = f"""
Given correct steps:
{parsed['steps']}

Generate 3 incorrect equations.
Return JSON list.
"""
    output = call_llm(prompt)
    output = re.sub(r"```json|```", "", output).strip()

    try:
        return json.loads(output)
    except:
        return []

# ---------------- BUILDER ----------------
def build(question):
    parsed = parse_question(question)
    concept = detect_concept(question)
    env = solve(parsed)
    false_eq = generate_false(parsed)

    return {
        "question": question,
        "concept": concept,
        "template": parsed["template"],
        "variables": parsed["variables"],
        "steps": parsed["steps"],
        "answer": env.get(parsed["answer"]),
        "false_equations": false_eq
    }

# ---------------- RUN ----------------
if __name__ == "__main__":
    while True:
        q = input("\nEnter question: ")
        try:
            res = build(q)
            print("\nOUTPUT:\n")
            print(json.dumps(res, indent=2))
        except Exception as e:
            print("Error:", e)