# Question Template Extractor

> A multimodal AI system for extracting structured JSON templates from educational question images and generating dynamic question variants automatically.

---

# Overview

Question Template Extractor converts educational images into reusable machine-readable structured templates using GPT-4.1 Vision.

The system understands:
- textual questions
- diagrams
- equations
- physics reasoning
- geometry constraints
- circuit structures
- optics diagrams
- mathematical expressions

and converts them into fully parameterized JSON templates that can later be reused for:
- automatic question generation
- synthetic dataset creation
- AI tutoring systems
- adaptive learning platforms
- multimodal educational reasoning benchmarks

---

# Motivation

Traditional OCR systems only extract plain text.

Educational questions contain:
- diagrams
- symbolic reasoning
- constraints
- equations
- relationships between objects
- hidden semantic structure

This repository aims to bridge that gap by transforming educational images into:
- semantic representations
- symbolic templates
- reusable structured educational objects

---

# Key Features

## 1. Image → JSON Template Extraction

The system extracts:

- Subject
- Chapter
- Concept
- Variables
- Constraints
- Equations
- Diagram structure
- MCQ options
- Answer formulas
- Stepwise solutions

---

## 2. Parameterized Templates

Actual values are replaced with placeholders:

```json
{
  "@s0": "mass",
  "@s1": "theta"
}
```

This enables:
- dynamic sampling
- infinite variants
- reusable question templates

---

## 3. Dynamic Question Generation

Once a template is extracted:
- variables can be resampled
- equations recomputed
- options regenerated
- answers recalculated
- diagrams recreated dynamically

---

## 4. Multimodal Educational Reasoning

Supports:
- text understanding
- diagram reasoning
- symbolic reasoning
- equation generation
- constraint inference

---

# Supported Domains

| Domain | Supported |
|---|---|
| Mechanics | ✅ |
| Optics | ✅ |
| Electrostatics | ✅ |
| Circuits | ✅ |
| Geometry | ✅ |
| Algebra | ✅ |
| Graph Theory | ✅ |
| Coordinate Geometry | ✅ |
| Calculus | ✅ |

---

# Example Input Types

## Mechanics

- Inclined planes
- Friction
- Newton laws
- Force systems

---

## Optics

- Prism
- Refraction
- Total internal reflection
- Lens diagrams

---

## Circuits

- Equivalent resistance
- Capacitance
- Series/parallel combinations
- Kirchhoff laws

---

## Geometry

- Triangle problems
- Angle constraints
- Coordinate geometry
- Circle theorems

---

# Repository Structure

```bash
Question_Template_Extractor/
│
├── main.py
├── README.md
├── requirements.txt
├── .env
│
├── examples/
│   ├── prism_question.png
│   ├── mechanics_question.png
│   ├── circuit_question.png
│
├── outputs/
│   ├── optics_template.json
│   ├── mechanics_template.json
│   ├── circuits_template.json
│
└── generated_questions/
    ├── generated_1.json
    ├── generated_2.json
```

---

# System Architecture

```text
Educational Question Image
            ↓
      GPT-4.1 Vision
            ↓
 Multimodal Understanding
            ↓
 Variable Extraction
            ↓
 Constraint Detection
            ↓
 Equation Generation
            ↓
 JSON Template Creation
            ↓
 Dynamic Question Generator
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/keshav12280-blip/Question_Template_Extractor.git

cd Question_Template_Extractor
```

---

## Create Virtual Environment

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Requirements

```txt
openai
python-dotenv
pillow
```

---

# OpenAI API Setup

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

---

# Running the Project

## Basic Execution

```bash
python main.py
```

---

# Example Usage

```python
result = generate_template_json(
    image_path="question.png",
    optional_question_text=""
)

print(json.dumps(result, indent=2))
```

---

# Example Educational Images

The system supports educational diagrams such as:

- capacitor networks
- prism optics
- inclined planes
- geometry figures
- graph structures
- symbolic equations

---

# Example Output JSON

## Mechanics Example

```json
{
  "template_id": "mechanics_inclined_plane",

  "subject": "Physics",

  "concept": "Static Friction",

  "variables": [
    {
      "name": "m",
      "type": "mass"
    }
  ],

  "constraints": [
    {
      "type": "force_balance",
      "expression": "F + f = mgsin(theta)"
    }
  ],

  "answer_template": {
    "formula": "F = mgsin(theta) - mu*mgcos(theta)"
  }
}
```

---

# JSON Schema

Every extracted question follows:

```json
{
  "template_id": "",

  "subject": "",

  "chapter": "",

  "concept": "",

  "question_template": {},

  "generated_values": {},

  "sampled_variables": {},

  "variables": [],

  "constraints": [],

  "computed_equations": [],

  "image_template": {},

  "options": [],

  "answer_template": {},

  "solution_explanation": []
}
```

---

# Generated Components

## Variables

```json
{
  "name": "theta",
  "type": "angle",
  "sampled_value": 30
}
```

---

## Constraints

```json
{
  "type": "snells_law",
  "expression": "sin(i)=mu*sin(r)"
}
```

---

## Computed Equations

```json
{
  "step": 1,
  "equation": "r1+r2=A"
}
```

---

## Solution Explanation

```json
[
  "Find critical angle",
  "Apply prism relation",
  "Use Snell law"
]
```

---

# Dynamic Question Generation

The extracted templates can later be reused for infinite question generation.

Example:

```python
sampled_values = {
    "mu": 2,
    "A": 50,
    "theta": 30
}
```

The generator can automatically:
- regenerate equations
- compute answers
- generate distractors
- create new MCQs
- modify diagrams

---

# Research Applications

This project is useful for:

## 1. Educational Dataset Generation

Can generate:
- synthetic educational datasets
- multimodal reasoning datasets
- benchmark datasets

---

## 2. AI Tutoring Systems

Can power:
- personalized tutoring
- adaptive quizzes
- infinite practice systems

---

## 3. Educational LLM Training

Can generate:
- structured educational corpora
- symbolic reasoning datasets
- multimodal educational benchmarks

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend |
| GPT-4.1 Vision | Multimodal reasoning |
| OpenAI API | Image understanding |
| JSON | Structured templates |

---

# Example Concepts Parsed

## Mechanics
- Friction
- Inclined plane
- Force balance
- Newton laws

---

## Optics
- Prism
- Refraction
- Snell law
- Total internal reflection

---

## Circuits
- Capacitors
- Series combinations
- Parallel combinations
- Kirchhoff laws

---

## Geometry
- Triangle constraints
- Circle geometry
- Coordinate geometry

---

# Challenges Solved

| Problem | Solution |
|---|---|
| Diagram understanding | Vision-language reasoning |
| Symbol extraction | Structured parsing |
| Formula inference | Constraint generation |
| Question regeneration | Parameterized templates |

---

# Future Improvements

## Planned Features

- SVG diagram generation
- Symbolic algebra engine
- Difficulty-aware question generation
- Geometry reasoning engine
- OCR-free parsing
- Interactive educational generation
- Multi-step theorem proving
- Automated educational dataset pipelines

---

# Example Pipeline

```text
Question Image
    ↓
Vision Parsing
    ↓
Semantic Understanding
    ↓
Constraint Detection
    ↓
Template Generation
    ↓
Variable Sampling
    ↓
New Question Generation
```

---

# Performance Goals

The project is designed for:
- scalable educational dataset generation
- multimodal reasoning research
- educational AI systems
- adaptive testing systems

---

# Potential Future Research

Possible research directions:
- Multimodal educational knowledge graphs
- Symbolic educational reasoning
- Educational synthetic dataset generation
- Diagram-aware AI tutoring
- Educational multimodal agents

---

# Contributing

Contributions are welcome.

Possible areas:
- diagram parsers
- SVG generation
- symbolic solvers
- geometry engines
- OCR optimization
- educational dataset generation

---

# License

MIT License

---

# Author

Keshav Gupta

GitHub:
https://github.com/keshav12280-blip/Question_Template_Extractor

---

# Citation

If you use this repository in research:

```bibtex
@software{question_template_extractor,
  author = {Keshav Gupta},
  title = {Question Template Extractor},
  year = {2026},
  url = {https://github.com/keshav12280-blip/Question_Template_Extractor}
}
```

---

# Acknowledgements

- OpenAI GPT-4.1 Vision
- Multimodal reasoning research community
- Educational AI research community

---

# Star the Repository

If you found this useful, consider starring the repository.
