# =========================================================
# UNIVERSAL JSON + IMAGE QUESTION GENERATOR
# USING:
#   - JSON TEMPLATE
#   - INPUT IMAGE
#   - HUGGINGFACE QWEN2-VL
#
# INPUT:
#   template.json
#   question.png
#
# OUTPUT:
#   2 regenerated clean question images
#
# =========================================================

import os
import json
import random
import math
import torch

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from transformers import (
    AutoProcessor,
    Qwen2VLForConditionalGeneration
)

# =========================================================
# CONFIG
# =========================================================

MODEL_NAME = "Qwen/Qwen2-VL-7B-Instruct"

INPUT_IMAGE = "question.png"

INPUT_JSON = "pulley.json"

OUTPUT_DIR = "outputs"

TOTAL_IMAGES = 2

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# =========================================================
# LOAD MODEL
# =========================================================

print("\nLoading Qwen2-VL...\n")

processor = AutoProcessor.from_pretrained(
    MODEL_NAME
)

model = Qwen2VLForConditionalGeneration.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"
)

print("\nModel Loaded.\n")

# =========================================================
# LOAD JSON TEMPLATE
# =========================================================

with open(INPUT_JSON, "r") as f:

    template = json.load(f)

# =========================================================
# FONT
# =========================================================

FONT_PATH = (
    "/System/Library/Fonts/"
    "Supplemental/Arial.ttf"
)

font_question = ImageFont.truetype(
    FONT_PATH,
    34
)

font_option = ImageFont.truetype(
    FONT_PATH,
    30
)

font_answer = ImageFont.truetype(
    FONT_PATH,
    28
)

# =========================================================
# STEP 1:
# UNDERSTAND IMAGE USING QWEN
# =========================================================

def understand_image(image_path):

    image = Image.open(image_path)

    prompt = """
Analyze this educational diagram carefully.

Explain:
- what objects exist
- diagram structure
- labels
- educational concept

Return STRICT JSON ONLY.

FORMAT:

{
  "diagram_type":"",
  "objects":[],
  "labels":[],
  "layout":""
}
"""

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": image
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ]

    text = processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = processor(
        text=[text],
        images=[image],
        return_tensors="pt"
    ).to(model.device)

    output_ids = model.generate(
        **inputs,
        max_new_tokens=1024
    )

    response = processor.batch_decode(
        output_ids,
        skip_special_tokens=True
    )[0]

    # =====================================================
    # SAFE JSON EXTRACTION
    # =====================================================

    start = response.find("{")
    end = response.rfind("}") + 1

    json_text = response[start:end]

    return json.loads(json_text)

# =========================================================
# STEP 2:
# SAMPLE VARIABLES FROM JSON
# =========================================================

def sample_variables(template):

    sampled = {}

    for variable in template["variables"]:

        name = variable["name"]

        low = variable["range"][0]
        high = variable["range"][1]

        # =================================================
        # INTEGER
        # =================================================

        if isinstance(low, int):

            sampled[name] = random.randint(
                int(low),
                int(high)
            )

        # =================================================
        # FLOAT
        # =================================================

        else:

            sampled[name] = round(
                random.uniform(
                    float(low),
                    float(high)
                ),
                2
            )

    return sampled

# =========================================================
# STEP 3:
# COMPUTE PHYSICS VALUES
# =========================================================

def compute_values(values):

    # =====================================================
    # PRISM LOGIC
    # =====================================================

    mu = values["mu"]

    A = values["A"]

    # critical angle

    c = math.degrees(
        math.asin(1/mu)
    )

    # TIR condition

    r2 = c

    r1 = A - r2

    sin_i = mu * math.sin(
        math.radians(r1)
    )

    sin_i = min(1, sin_i)

    i = math.degrees(
        math.asin(sin_i)
    )

    values["c"] = round(c,2)

    values["r1"] = round(r1,2)

    values["r2"] = round(r2,2)

    values["i"] = round(i,2)

    return values

# =========================================================
# STEP 4:
# GENERATE OPTIONS
# =========================================================

def generate_options(correct):

    options = [

        round(correct,2),

        round(correct + 10,2),

        round(max(5, correct - 15),2),

        round(correct + 20,2)
    ]

    random.shuffle(options)

    return options

# =========================================================
# STEP 5:
# GENERATE QUESTION TEXT
# =========================================================

def generate_question(template, values):

    question = template[
        "question_template"
    ][
        "text"
    ]

    # =====================================================
    # REPLACE SYMBOLIC VARIABLES
    # =====================================================

    replacements = {

        "@s0": "AB",
        "@s1": "ABC",
        "@s2": str(values["mu"]),
        "@s3": "AC",
        "@s4": "i"
    }

    for k,v in replacements.items():

        question = question.replace(
            k,
            str(v)
        )

    return question

# =========================================================
# STEP 6:
# DRAW PRISM DIAGRAM
# =========================================================

def draw_diagram(draw, values):

    # prism

    A = (1200,120)
    B = (1000,500)
    C = (1400,500)

    draw.line([A,B], fill="black", width=4)
    draw.line([A,C], fill="black", width=4)
    draw.line([B,C], fill="black", width=4)

    # labels

    draw.text((1180,80), "A", fill="black")
    draw.text((960,510), "B", fill="black")
    draw.text((1410,510), "C", fill="black")

    # incident ray

    draw.line(
        [(850,350), (1060,280)],
        fill="black",
        width=4
    )

    draw.text(
        (760,320),
        "incident ray",
        fill="black",
        font=font_answer
    )

    # angle

    draw.text(
        (1040,220),
        f"i = {values['i']}°",
        fill="black",
        font=font_answer
    )

    # mu

    draw.text(
        (1170,300),
        f"μ = {values['mu']}",
        fill="blue",
        font=font_answer
    )

# =========================================================
# STEP 7:
# RENDER CLEAN PAGE
# =========================================================

def render_page(
    idx,
    question,
    options,
    correct,
    values
):

    img = Image.new(
        "RGB",
        (1700,900),
        "white"
    )

    draw = ImageDraw.Draw(img)

    # =====================================================
    # QUESTION NUMBER
    # =====================================================

    draw.rectangle(
        (20,20,70,90),
        fill="black"
    )

    draw.text(
        (38,35),
        str(idx),
        fill="white",
        font=font_answer
    )

    # =====================================================
    # QUESTION
    # =====================================================

    draw.text(
        (100,40),
        question,
        fill="black",
        font=font_question
    )

    # =====================================================
    # OPTIONS
    # =====================================================

    labels = ["A","B","C","D"]

    positions = [

        (100,220),
        (450,220),
        (100,340),
        (450,340)
    ]

    for k,opt in enumerate(options):

        draw.text(
            positions[k],
            f"({labels[k]}) {opt}°",
            fill="black",
            font=font_option
        )

    # =====================================================
    # DIAGRAM
    # =====================================================

    draw_diagram(
        draw,
        values
    )

    # =====================================================
    # ANSWER
    # =====================================================

    draw.text(
        (100,700),
        f"Correct Answer = {correct}°",
        fill="blue",
        font=font_answer
    )

    # =====================================================
    # SAVE
    # =====================================================

    output_path = os.path.join(
        OUTPUT_DIR,
        f"question_{idx}.png"
    )

    img.save(output_path)

    print(
        f"Saved: {output_path}"
    )

# =========================================================
# MAIN
# =========================================================

def main():

    # =====================================================
    # UNDERSTAND IMAGE
    # =====================================================

    diagram_understanding = understand_image(
        INPUT_IMAGE
    )

    print("\n================================")
    print("DIAGRAM UNDERSTANDING")
    print("================================")

    print(
        json.dumps(
            diagram_understanding,
            indent=2
        )
    )

    # =====================================================
    # GENERATE QUESTIONS
    # =====================================================

    for idx in range(1, TOTAL_IMAGES + 1):

        print("\n================================")
        print(f"QUESTION {idx}")
        print("================================")

        # sample variables

        values = sample_variables(
            template
        )

        # compute physics

        values = compute_values(
            values
        )

        print("\nValues:")
        print(values)

        # generate question

        question = generate_question(
            template,
            values
        )

        print("\nQuestion:")
        print(question)

        # generate options

        options = generate_options(
            values["i"]
        )

        print("\nOptions:")
        print(options)

        # render

        render_page(
            idx,
            question,
            options,
            values["i"],
            values
        )

# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    main()