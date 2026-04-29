import base64
import json
from openai import OpenAI
from sympy import sympify

# ==============================
# CONFIG
# ==============================

client = OpenAI()

# ==============================
# IMAGE ENCODER
# ==============================

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ==============================
# STEP 1: EXTRACT SCENE FROM IMAGE
# ==============================

def extract_scene(image_path, question_text):

    image_base64 = encode_image(image_path)

    prompt = f"""
You are an expert JEE question diagram extractor.

Read image carefully and extract structured JSON only.

Return STRICT JSON:

{{
  "subject": "",
  "chapter": "",
  "values": [],
  "symbols": [],
  "objects": [],
  "relations": []
}}

Question:
{question_text}

Rules:
- detect all visible numbers
- detect symbols
- detect physical objects
- detect relations
- no explanation outside JSON
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
                        }
                    }
                ]
            }
        ]
    )

    return json.loads(response.choices[0].message.content)

# ==============================
# STEP 2: SOLVE QUESTION
# ==============================

def solve_question(scene, question_text):

    prompt = f"""
You are a JEE solver.

Scene JSON:
{json.dumps(scene)}

Question:
{question_text}

Return STRICT JSON:

{{
  "formula_used": "",
  "steps": [],
  "equation": "",
  "final_answer": ""
}}

Rules:
- choose formula automatically
- solve step by step
- return only JSON
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return json.loads(response.choices[0].message.content)

# ==============================
# STEP 3: VALIDATE EQUATION USING PYTHON
# ==============================

def validate_equation(equation):

    try:
        expr = sympify(equation)
        return str(expr.evalf())
    except:
        return "Validation failed"

# ==============================
# STEP 4: COMPLETE PIPELINE
# ==============================

def process_question(image_path, question_text):

    print("\n--- Extracting Scene ---")
    scene = extract_scene(image_path, question_text)

    print(json.dumps(scene, indent=2))

    print("\n--- Solving ---")
    solution = solve_question(scene, question_text)

    print(json.dumps(solution, indent=2))

    validated = validate_equation(solution["equation"])

    final_output = {
        "scene": scene,
        "solution": solution,
        "validated_result": validated
    }

    print("\n--- FINAL OUTPUT ---")
    print(json.dumps(final_output, indent=2))

    return final_output

# ==============================
# RUN
# ==============================

if __name__ == "__main__":

    process_question(
        image_path="question.png",
        question_text="Find equivalent capacitance between A and B"
    )