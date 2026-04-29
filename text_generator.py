import json
import uuid
import re
from datetime import datetime
from openai import OpenAI

client = OpenAI()

# ---------------- LLM PROMPT ----------------
def build_prompt(question):
    return f"""
You are a scientific question compiler.

Extract ONLY JSON in this schema:

{{
  "concept": "topic name",
  "variables": [
    {{
      "name": "s0",
      "value": "number"
    }}
  ],
  "template": "question with @s0 replacing numbers",
  "answer_expression": "formula using s0",
  "false_equations": [
    "wrong formula 1",
    "wrong formula 2",
    "wrong formula 3"
  ]
}}

Rules:
1. Detect concept automatically.
2. Replace numeric values with @s0, @s1 etc.
3. answer_expression must use variables only.
4. false_equations must be mathematically plausible but incorrect.
5. Return ONLY valid JSON.

Question:
{question}
"""


# ---------------- LLM CALL ----------------
def call_llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Return only valid JSON."},
            {"role": "user", "content": prompt}
        ]
    )

    return json.loads(response.choices[0].message.content)


# ---------------- POSITION FINDER ----------------
def get_positions(question, value):
    start = question.find(value)
    end = start + len(value)
    return start, end


# ---------------- SAFE TIMESTAMP ----------------
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+05")


# ---------------- MAIN BUILDER ----------------
def build(question):
    llm_data = call_llm(build_prompt(question))

    value = llm_data["variables"][0]["value"]
    start, end = get_positions(question, value)

    now = get_timestamp()

    result = {
        "_id": uuid.uuid4().hex[:24],

        "question_template_id": 10777,

        "template_question_text": f"<div><span>{question}</span></div>",

        "created_date": now,
        "modified_date": now,

        "created_by": "a1b306dc-e71f-4e88-9af4-9596bf710cbc",
        "modified_by": "a1b306dc-e71f-4e88-9af4-9596bf710cbc",

        "question_data": question + "  &linebreak;  ",

        "language_id": 1,
        "language_name": "English",

        "total_marks": 1.0,

        "variable_details": [
            {
                "variable_name": "s0",
                "variable_value": value,
                "has_constraints": True,
                "possible_values": [value],
                "is_dependent": False,
                "number_of_auxiliary_variables": 0,
                "upper_limit": 5.0,
                "lower_limit": 1.0,
                "equations": [],
                "is_custom": False
            }
        ],

        "question_template": {
            "user": llm_data["template"] + "  &linebreak;  ",
            "ai": llm_data["template"] + "  &linebreak;  "
        },

        "ai_model_predicted_data": [
            {
                "question_data": [
                    question,
                    "&linebreak; "
                ],

                "user": {
                    "variables": [
                        {
                            "dynamic_variable": {
                                "s0": value
                            },
                            "position": {
                                "start": start,
                                "end": end
                            },
                            "type": "float"
                        }
                    ],
                    "number_of_variables": 1,
                    "template_string": llm_data["template"] + "  &linebreak;  "
                },

                "ai": {
                    "variables": [
                        {
                            "dynamic_variable": {
                                "s0": value
                            },
                            "position": {
                                "start": start,
                                "end": end
                            },
                            "type": "float"
                        }
                    ],
                    "number_of_variables": 1,
                    "template_string": llm_data["template"] + "  &linebreak;  "
                }
            }
        ],

        "answer_data": {
            "is_lhs": False,
            "type": "dynamic",

            "random_variable": [
                {
                    "has_constraints": True,
                    "is_dependent": False,
                    "number_of_auxiliary_variables": 0
                }
            ],

            "true_options": 1,
            "false_options": 3,

            "true_equation": [
                {
                    "equation": [
                        f"#n={llm_data['answer_expression']}",
                        "(::DECIMALUPTO 2:)#y=n#(::)"
                    ],
                    "marks": 1.0
                }
            ],

            "false_equation": [
                {
                    "equation": [
                        f"#n={eq}",
                        "(::DECIMALUPTO 2:)#y=n#(::)"
                    ],
                    "marks": 0.0
                }
                for eq in llm_data["false_equations"]
            ],

            "variable_values": {
                "dynamic_variable": {}
            },

            "answer_explanation": json.dumps([
                "!!DISPLAYCOMMENT: Use formula!!",
                f"(:Given:)#val=s0#(::)",
                f"(:So:)#y={llm_data['answer_expression']}#(::)"
            ])
        },

        "variable_edit": [
            {
                "varname": value,
                "checklatex": False,
                "type": "Integer",
                "constraints": {
                    "type": "integer",
                    "upperLimit": 5.0,
                    "lowerLimit": 1.0
                },
                "conditions": {
                    "type": "string",
                    "values": []
                },
                "dependantvariables": False,
                "auxvariable": [],
                "varindexpos": start,
                "variablesizefinal": len(value),
                "vartemplatestring": "s0",
                "vartype": False,
                "partiallyselectedfrom": str(start),
                "ispartiallyselected": value,
                "partialselectioncounter": 1
            }
        ],

        "_class": "com.extramarks.questionMSA.entity.QuestionTemplate"
    }

    return result


# ---------------- RUN ----------------
if __name__ == "__main__":
    while True:
        q = input("\nEnter question: ")

        try:
            output = build(q)

            print("\nOUTPUT JSON:\n")
            print(json.dumps(output, indent=2))

        except Exception as e:
            print("Error:", e)