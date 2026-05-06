import base64
import json
from openai import OpenAI

# ==========================================
# CONFIG
# ==========================================

client = OpenAI()

# ==========================================
# IMAGE ENCODER
# ==========================================

def encode_image(image_path):

    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# ==========================================
# UNIVERSAL TEMPLATE GENERATOR
# ==========================================

def generate_template_json(image_path, optional_question_text=""):

    image_base64 = encode_image(image_path)

    prompt = f"""
You are an expert educational multimodal reasoning engine.

Your task is to analyze ANY educational question image
(JEE, NEET, mechanics, optics, circuits, geometry, algebra, graph theory etc.)

You must generate a FULLY PARAMETERIZED JSON TEMPLATE.

STRICTLY RETURN JSON ONLY.

==================================================
GOALS
==================================================

1. Detect:
   - subject
   - chapter
   - concept

2. Extract:
   - variables
   - equations
   - constraints
   - diagram structure

3. Replace actual values using placeholders:
   @s0, @s1, @s2 ...

4. Generate:
   - sampled variables
   - computed equations
   - options
   - detailed solution explanation

5. Make template reusable for dynamic generation.

==================================================
IMPORTANT RULES
==================================================

- STRICT JSON ONLY
- NO markdown
- NO explanation outside JSON
- Every numeric value must become parameterized
- Include symbolic + sampled values
- Infer formulas automatically
- Infer physics laws automatically
- Infer geometry/circuit/optics constraints automatically

==================================================
OUTPUT FORMAT
==================================================

{{
  "template_id": "",

  "subject": "",

  "chapter": "",

  "concept": "",

  "question_template": {{
    "text": ""
  }},

  "generated_values": {{}},

  "sampled_variables": {{}},

  "variables": [
    {{
      "name": "",
      "type": "",
      "role": "",
      "range": [],
      "sampled_value": ""
    }}
  ],

  "constraints": [
    {{
      "type": "",
      "expression": ""
    }}
  ],

  "computed_equations": [
    {{
      "step": 1,
      "equation": ""
    }}
  ],

  "image_template": {{
    "type": "",
    "objects": []
  }},

  "options": [
    {{
      "id": "A",
      "value": "",
      "is_correct": false
    }}
  ],

  "answer_template": {{
    "formula": "",
    "expanded_formula": "",
    "correct_answer": ""
  }},

  "solution_explanation": []
}}

==================================================
SPECIAL INSTRUCTIONS
==================================================

IF PHYSICS:
- infer laws automatically
- include derived equations
- include stepwise solving

IF OPTICS:
- include Snell's law
- prism relation
- critical angle equations
- TIR conditions

IF MECHANICS:
- include Newton laws
- force balance equations
- friction equations

IF CIRCUITS:
- include KVL/KCL
- equivalent resistance rules

IF GEOMETRY:
- include angle constraints
- similarity relations

==================================================
VARIABLE RULES
==================================================

- Add BOTH symbolic and sampled values
- Ensure sampled values satisfy constraints
- Generate realistic ranges
- Include intermediate variables

==================================================
OPTIONS RULES
==================================================

- Generate 4 MCQ options
- Exactly one correct answer

==================================================
SOLUTION RULES
==================================================

- Add stepwise equations
- Add human-readable explanation
- Add expanded formula using sampled values

==================================================
Optional Question Text:
{optional_question_text}
"""

    response = client.chat.completions.create(

        model="gpt-4.1",

        temperature=0,

        response_format={"type": "json_object"},

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


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    image_path = "question.png"

    result = generate_template_json(
        image_path=image_path,
        optional_question_text=""
    )

    print("\n=========== GENERATED TEMPLATE JSON ===========\n")

    print(json.dumps(result, indent=2))