import os
import cv2
import json
import random
import easyocr
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# =====================================================
# CONFIG
# =====================================================

INPUT_IMAGE = "question.png"
TEMPLATE_JSON = "template.json"

OUTPUT_DIR = "high_quality_outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

reader = easyocr.Reader(['en'])

# =====================================================
# LOAD TEMPLATE
# =====================================================

with open(TEMPLATE_JSON, "r") as f:
    template = json.load(f)

# =====================================================
# GENERATE VALUES
# =====================================================

def generate_variable(variable):

    constraints = variable["constraints"]

    min_val = constraints["min"]
    max_val = constraints["max"]

    return random.randint(min_val, max_val)

# =====================================================
# GENERATE VARIABLE SET
# =====================================================

def generate_values():

    values = {}

    for var in template["variables"]:

        values[var["name"]] = generate_variable(var)

    return values

# =====================================================
# HIGH QUALITY TEXT REPLACEMENT
# =====================================================

def replace_text_high_quality(
    image,
    region,
    value
):

    x = region["x"]
    y = region["y"]

    width = region["width"]
    height = region["height"]

    # =================================================
    # MASK
    # =================================================

    mask = np.zeros(
        image.shape[:2],
        dtype=np.uint8
    )

    cv2.rectangle(
        mask,
        (x, y),
        (x+width, y+height),
        255,
        -1
    )

    # =================================================
    # INPAINT
    # =================================================

    image = cv2.inpaint(
        image,
        mask,
        7,
        cv2.INPAINT_TELEA
    )

    # =================================================
    # PIL CONVERSION
    # =================================================

    pil_img = Image.fromarray(image)

    draw = ImageDraw.Draw(pil_img)

    # =================================================
    # AUTO FONT SIZE
    # =================================================

    font_size = height - 8

    while font_size > 10:

        try:

            font = ImageFont.truetype(
                "arial.ttf",
                font_size
            )

        except:

            font = ImageFont.load_default()
            break

        bbox = draw.textbbox(
            (0,0),
            value,
            font=font
        )

        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        if (
            text_width <= width
            and
            text_height <= height
        ):
            break

        font_size -= 1

    # =================================================
    # CENTER TEXT
    # =================================================

    tx = x + (width - text_width)//2
    ty = y + (height - text_height)//2

    draw.text(
        (tx, ty),
        value,
        fill="black",
        font=font
    )

    return np.array(pil_img)

# =====================================================
# GENERATE IMAGE
# =====================================================

def generate_image(values, output_path):

    image = cv2.imread(INPUT_IMAGE)

    editable_regions = template[
        "image_template"
    ][
        "editable_regions"
    ]

    for region in editable_regions:

        variable_name = region["variable"]

        value = str(values[variable_name])

        if region.get("suffix"):
            value += region["suffix"]

        image = replace_text_high_quality(
            image,
            region,
            value
        )

    cv2.imwrite(
        output_path,
        image
    )

# =====================================================
# MAIN
# =====================================================

def generate_questions(num_questions=5):

    for i in range(num_questions):

        values = generate_values()

        print("\nGenerated Values:")
        print(values)

        output_path = os.path.join(
            OUTPUT_DIR,
            f"question_{i+1}.png"
        )

        generate_image(
            values,
            output_path
        )

        print(
            f"Saved: {output_path}"
        )

# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":

    generate_questions(5)