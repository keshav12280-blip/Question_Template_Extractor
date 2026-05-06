import os
import base64
import json
from openai import OpenAI
from sympy import sympify

# ==============================
# CONFIG
# ==============================

client = OpenAI()

IMAGE_FOLDER = "questions"

# ==============================
# IMAGE ENCODER
# ==============================

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ==============================
# STEP 1: EXTRACT SCENE
# ==============================

def extract_scene(image_path, question_text):

    image_base64 = encode_image(image_path)

    prompt = f"""
You are an expert JEE question diagram extractor.

Read image carefully and return STRICT JSON only.

Format:

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
- detect all numbers
- detect symbols
- detect physical objects
- detect relations
- return JSON only
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
# STEP 2: SOLVE
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
- solve carefully
- return JSON only
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
# STEP 3: VALIDATE
# ==============================

def validate_equation(equation):

    try:
        expr = sympify(equation)
        return str(expr.evalf())
    except:
        return "Validation failed"

# ==============================
# STEP 4: PROCESS ONE IMAGE
# ==============================

def process_question(image_path, question_text):

    print(f"\nProcessing: {image_path}")

    scene = extract_scene(image_path, question_text)

    solution = solve_question(scene, question_text)

    validated = validate_equation(solution["equation"])

    final_output = {
        "image": image_path,
        "scene": scene,
        "solution": solution,
        "validated_result": validated
    }

    print(json.dumps(final_output, indent=2))

# ==============================
# STEP 5: BATCH PROCESS ALL IMAGES
# ==============================

def process_folder():

    for filename in os.listdir(IMAGE_FOLDER):

        if filename.lower().endswith((".png", ".jpg", ".jpeg")):

            image_path = os.path.join(IMAGE_FOLDER, filename)

            # optional manual question text
            question_text = input(f"\nEnter question text for {filename}: ")

            process_question(image_path, question_text)

# ==============================
# RUN
# ==============================

if __name__ == "__main__":

    process_folder()