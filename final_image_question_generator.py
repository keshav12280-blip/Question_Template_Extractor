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
You are an expert educational multimodal reasoning system.

Your task is to analyze ANY educational question image
(JEE, NEET, geometry, graph theory, circuits, optics, mechanics etc.)

You must generate a UNIVERSAL PARAMETERIZED JSON TEMPLATE.

IMPORTANT GOALS:
1. Detect the subject automatically
2. Detect the concept automatically
3. Extract all variables from image/text
4. Replace actual values with symbolic placeholders like:
   @s0, @s1, @s2
5. Generate mathematical/physics constraints
6. Generate image structure template
7. Generate formula template
8. Ensure generated variables can later be changed dynamically
9. Return STRICT JSON ONLY

The JSON format MUST follow this structure:

{{
  "template_id": "",
  "subject": "",
  "chapter": "",
  "concept": "",

  "question_template": {{
    "text": ""
  }},

  "generated_values": {{}},

  "variables": [
    {{
      "name": "",
      "type": "",
      "role": "",
      "range": []
    }}
  ],

  "constraints": [
    {{
      "type": "",
      "expression": ""
    }}
  ],

  "image_template": {{
    "type": "svg",
    "objects": []
  }},

  "answer_template": {{
    "formula": "",
    "correct_answer": ""
  }}
}}

IMPORTANT RULES:
- Replace all numeric values using @s0, @s1 etc
- Infer constraints automatically
- If geometry:
    infer angle constraints
- If circuits:
    infer equivalent circuit constraints
- If optics:
    infer Snell law / prism constraints
- If graph:
    infer node-edge constraints
- If mechanics:
    infer Newton law constraints
- Generate reusable dynamic template
- STRICT JSON ONLY
- NO explanation outside JSON

Optional question text:
{optional_question_text}
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