# =========================================================
# FULLY AI-BASED UNIVERSAL EDUCATIONAL GENERATOR
# SINGLE INPUT VERSION
#
# INPUT:
#   question.png
#   question.json
#
# OUTPUT:
#   2 GENERATED SYNTHETIC QUESTION IMAGES
#
# NO HARDCODED DRAWING
# NO MANUAL DIAGRAM FUNCTIONS
# FULLY AI-BASED USING HUGGINGFACE MODELS
#
# =========================================================

import os
import json
import torch

from PIL import Image

# =========================================================
# OCR
# =========================================================

from paddleocr import PaddleOCR

# =========================================================
# TRANSFORMERS
# =========================================================

from transformers import (

    AutoProcessor,

    Qwen2VLForConditionalGeneration,

    Pix2StructProcessor,
    Pix2StructForConditionalGeneration,

    LlavaNextProcessor,
    LlavaNextForConditionalGeneration
)

# =========================================================
# DIFFUSION
# =========================================================

from diffusers import (

    StableDiffusionXLPipeline
)

# =========================================================
# CONFIG
# =========================================================

INPUT_IMAGE = "question.png"

INPUT_JSON = "question.json"

OUTPUT_DIR = "outputs"

TOTAL_VARIANTS = 2

DEVICE = "cuda"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# =========================================================
# LOAD OCR
# =========================================================

print("\nLoading OCR...\n")

ocr = PaddleOCR(
    use_angle_cls=True
)

# =========================================================
# LOAD QWEN2-VL
# =========================================================

print("\nLoading Qwen2-VL...\n")

qwen_processor = AutoProcessor.from_pretrained(
    "Qwen/Qwen2-VL-7B-Instruct"
)

qwen_model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2-VL-7B-Instruct",
    torch_dtype=torch.float16,
    device_map="auto"
)

# =========================================================
# LOAD PIX2STRUCT
# =========================================================

print("\nLoading Pix2Struct...\n")

pix_processor = Pix2StructProcessor.from_pretrained(
    "google/pix2struct-docvqa-large"
)

pix_model = Pix2StructForConditionalGeneration.from_pretrained(
    "google/pix2struct-docvqa-large"
).to(DEVICE)

# =========================================================
# LOAD LLAVA
# =========================================================

print("\nLoading LLaVA...\n")

llava_processor = LlavaNextProcessor.from_pretrained(
    "llava-hf/llava-v1.6-mistral-7b-hf"
)

llava_model = LlavaNextForConditionalGeneration.from_pretrained(
    "llava-hf/llava-v1.6-mistral-7b-hf",
    torch_dtype=torch.float16,
    device_map="auto"
)

# =========================================================
# LOAD SDXL
# =========================================================

print("\nLoading SDXL...\n")

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16
).to(DEVICE)

# =========================================================
# OCR EXTRACTION
# =========================================================

def extract_ocr(image_path):

    print("\nRunning OCR...\n")

    result = ocr.ocr(image_path)

    extracted = []

    for block in result:

        for line in block:

            extracted.append(
                line[1][0]
            )

    return extracted

# =========================================================
# IMAGE UNDERSTANDING
# =========================================================

def understand_image(image_path):

    print("\nUnderstanding Image...\n")

    image = Image.open(image_path)

    prompt = """
Analyze this educational question image.

Return STRICT JSON ONLY.

Extract:

1. subject
2. topic
3. chapter
4. equations
5. diagram_structure
6. labels
7. objects
8. question_type
9. answer_type
10. layout_structure

FORMAT:

{
  "subject":"",
  "chapter":"",
  "topic":"",
  "objects":[],
  "equations":[],
  "labels":[],
  "question_type":"",
  "layout_structure":{}
}
"""

    messages = [
        {
            "role":"user",
            "content":[
                {
                    "type":"image",
                    "image":image
                },
                {
                    "type":"text",
                    "text":prompt
                }
            ]
        }
    ]

    text = qwen_processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = qwen_processor(
        text=[text],
        images=[image],
        return_tensors="pt"
    ).to(qwen_model.device)

    outputs = qwen_model.generate(
        **inputs,
        max_new_tokens=2048
    )

    response = qwen_processor.batch_decode(
        outputs,
        skip_special_tokens=True
    )[0]

    start = response.find("{")
    end = response.rfind("}") + 1

    parsed = json.loads(
        response[start:end]
    )

    return parsed

# =========================================================
# LOAD TEMPLATE JSON
# =========================================================

def load_template(json_path):

    print("\nLoading JSON Template...\n")

    with open(json_path, "r") as f:

        template = json.load(f)

    return template

# =========================================================
# GENERATE QUESTION VARIANT
# =========================================================

def generate_variant(scene, template):

    print("\nGenerating New Variant...\n")

    prompt = f"""
You are generating a NEW educational question.

SCENE:

{json.dumps(scene, indent=2)}

TEMPLATE:

{json.dumps(template, indent=2)}

Generate:

1. modified_question
2. modified_values
3. modified_options
4. modified_answer
5. modified_diagram_description
6. modified_equations

Return STRICT JSON ONLY.

FORMAT:

{{
  "modified_question":"",
  "modified_options":[],
  "modified_answer":"",
  "modified_diagram_description":"",
  "modified_equations":[]
}}
"""

    messages = [
        {
            "role":"user",
            "content":[
                {
                    "type":"text",
                    "text":prompt
                }
            ]
        }
    ]

    text = qwen_processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = qwen_processor(
        text=[text],
        return_tensors="pt"
    ).to(qwen_model.device)

    outputs = qwen_model.generate(
        **inputs,
        max_new_tokens=2048
    )

    response = qwen_processor.batch_decode(
        outputs,
        skip_special_tokens=True
    )[0]

    start = response.find("{")
    end = response.rfind("}") + 1

    generated = json.loads(
        response[start:end]
    )

    return generated

# =========================================================
# GENERATE DIAGRAM
# =========================================================

def generate_diagram(generated):

    print("\nGenerating Diagram...\n")

    prompt = f"""
Clean educational textbook diagram.

Topic:
{generated['modified_diagram_description']}

Style:
- JEE Advanced
- black and white
- clean scientific rendering
- textbook style
- white background
- precise labels
- educational illustration
"""

    image = pipe(
        prompt=prompt,
        num_inference_steps=35,
        guidance_scale=8.0
    ).images[0]

    return image

# =========================================================
# GENERATE FINAL PAGE
# =========================================================

def generate_page(generated):

    print("\nGenerating Final Educational Page...\n")

    prompt = f"""
Generate a clean educational exam page.

Question:
{generated['modified_question']}

Options:
{generated['modified_options']}

Answer:
{generated['modified_answer']}

Equations:
{generated['modified_equations']}

Style:
- JEE Advanced paper
- black text
- white page
- clean typography
- scientific layout
- educational worksheet
- textbook rendering
- professional formatting
"""

    image = pipe(
        prompt=prompt,
        num_inference_steps=40,
        guidance_scale=8.5
    ).images[0]

    return image

# =========================================================
# MAIN
# =========================================================

def main():

    # =====================================================
    # OCR
    # =====================================================

    ocr_text = extract_ocr(
        INPUT_IMAGE
    )

    print("\nOCR TEXT:\n")

    for t in ocr_text:

        print(t)

    # =====================================================
    # UNDERSTAND IMAGE
    # =====================================================

    scene = understand_image(
        INPUT_IMAGE
    )

    print("\nSCENE UNDERSTANDING:\n")

    print(
        json.dumps(
            scene,
            indent=2
        )
    )

    # =====================================================
    # LOAD JSON
    # =====================================================

    template = load_template(
        INPUT_JSON
    )

    # =====================================================
    # GENERATE 2 VARIANTS
    # =====================================================

    for idx in range(1, TOTAL_VARIANTS + 1):

        print("\n================================")
        print(f"GENERATING VARIANT {idx}")
        print("================================")

        # ---------------------------------------------
        # GENERATE QUESTION
        # ---------------------------------------------

        generated = generate_variant(
            scene,
            template
        )

        print("\nGENERATED QUESTION:\n")

        print(
            json.dumps(
                generated,
                indent=2
            )
        )

        # ---------------------------------------------
        # GENERATE DIAGRAM
        # ---------------------------------------------

        diagram = generate_diagram(
            generated
        )

        diagram.save(
            os.path.join(
                OUTPUT_DIR,
                f"diagram_{idx}.png"
            )
        )

        # ---------------------------------------------
        # GENERATE FINAL PAGE
        # ---------------------------------------------

        final_page = generate_page(
            generated
        )

        output_path = os.path.join(
            OUTPUT_DIR,
            f"question_variant_{idx}.png"
        )

        final_page.save(output_path)

        print(
            f"\nSaved: {output_path}"
        )

# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    main()