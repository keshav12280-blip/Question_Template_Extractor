from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image,
    KeepTogether,
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os

# =============================================================================
# OUTPUT FILE
# =============================================================================

OUTPUT_FILE = "AI_JEE_Question_Generation_Research_Architecture.pdf"

# =============================================================================
# IMAGE PATHS
# =============================================================================

IMG1 = "output images/output19.png"
IMG2 = "output images/output20.png"

print("IMG1 Exists:", os.path.exists(IMG1))
print("IMG2 Exists:", os.path.exists(IMG2))

# =============================================================================
# COLORS
# =============================================================================

NAVY = colors.HexColor("#0B132B")
ROYAL = colors.HexColor("#1C2541")
BLUE = colors.HexColor("#3A86FF")
GREEN = colors.HexColor("#2A9D8F")
PURPLE = colors.HexColor("#6A4C93")
ORANGE = colors.HexColor("#F77F00")

LIGHT = colors.HexColor("#F8FAFC")
BORDER = colors.HexColor("#D9E2EC")
TEXT = colors.HexColor("#4A5568")

WHITE = colors.white

# =============================================================================
# STYLES
# =============================================================================


def styles_build():

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="TitleX",
            fontSize=28,
            leading=34,
            alignment=TA_CENTER,
            textColor=WHITE,
            fontName="Helvetica-Bold",
        )
    )

    styles.add(
        ParagraphStyle(
            name="SubTitleX",
            fontSize=13,
            leading=18,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#D6E4FF"),
            fontName="Helvetica",
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionX",
            fontSize=16,
            leading=20,
            textColor=NAVY,
            fontName="Helvetica-Bold",
        )
    )

    styles.add(
        ParagraphStyle(
            name="BodyX",
            fontSize=9.5,
            leading=15,
            alignment=TA_JUSTIFY,
            textColor=TEXT,
            fontName="Helvetica",
        )
    )

    styles.add(
        ParagraphStyle(
            name="Mini",
            fontSize=8,
            leading=11,
            textColor=TEXT,
            alignment=TA_CENTER,
            fontName="Helvetica",
        )
    )

    styles.add(
        ParagraphStyle(
            name="CardTitle",
            fontSize=10,
            leading=13,
            textColor=WHITE,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
        )
    )

    return styles


# =============================================================================
# SECTION
# =============================================================================


def section(title, styles):

    t = Table(
        [[Paragraph(title, styles["SectionX"])]],
        colWidths=[180 * mm],
    )

    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("BOX", (0, 0), (-1, -1), 1, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    return t


# =============================================================================
# HIGHLIGHT
# =============================================================================


def highlight(text, styles):

    t = Table(
        [[Paragraph(text, styles["BodyX"])]],
        colWidths=[176 * mm],
    )

    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EEF7FF")),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#BEE3F8")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    return t


# =============================================================================
# IMAGE CARD
# =============================================================================


def image_card(path, title, styles):

    img = Image(path, width=175 * mm, height=88 * mm)

    title_box = Table(
        [[Paragraph(title, styles["SectionX"])]],
        colWidths=[176 * mm],
    )

    title_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("BOX", (0, 0), (-1, -1), 1, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )

    image_table = Table([[img]], colWidths=[176 * mm])

    image_table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )

    return KeepTogether([title_box, Spacer(1, 4), image_table])


# =============================================================================
# PIPELINE TABLE
# =============================================================================


def pipeline(styles):

    data = [
        [
            Paragraph("INPUT IMAGE", styles["CardTitle"]),
            Paragraph("GPT-4 VISION", styles["CardTitle"]),
            Paragraph("JSON ENGINE", styles["CardTitle"]),
            Paragraph("QWEN2-VL", styles["CardTitle"]),
            Paragraph("FINAL OUTPUT", styles["CardTitle"]),
        ],
        [
            Paragraph("JEE Question Upload", styles["Mini"]),
            Paragraph("Semantic Extraction", styles["Mini"]),
            Paragraph("Constraint Validation", styles["Mini"]),
            Paragraph("Layout-aware Editing", styles["Mini"]),
            Paragraph("Generated Variants", styles["Mini"]),
        ],
    ]

    t = Table(data, colWidths=[36 * mm] * 5)

    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), BLUE),
                ("BACKGROUND", (1, 0), (1, 0), GREEN),
                ("BACKGROUND", (2, 0), (2, 0), PURPLE),
                ("BACKGROUND", (3, 0), (3, 0), ORANGE),
                ("BACKGROUND", (4, 0), (4, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("INNERGRID", (0, 0), (-1, -1), 1, WHITE),
                ("BOX", (0, 0), (-1, -1), 1, BORDER),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    return t


# =============================================================================
# BUILD PDF
# =============================================================================


def build_pdf():

    styles = styles_build()

    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        leftMargin=10 * mm,
        rightMargin=10 * mm,
        topMargin=10 * mm,
        bottomMargin=10 * mm,
        title="AI JEE Question Generation Research Architecture",
        author="Keshav Gupta",
    )

    story = []

    # =========================================================================
    # COVER PAGE
    # =========================================================================

    cover = Table(
        [[Paragraph(
            "AI-Based Universal JEE Question Generation System",
            styles["TitleX"]
        )]],
        colWidths=[185 * mm],
    )

    cover.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("TOPPADDING", (0, 0), (-1, -1), 24),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 24),
            ]
        )
    )

    story.append(cover)
    story.append(Spacer(1, 6))

    subtitle = Table(
        [[Paragraph(
            "Multimodal AI Architecture for Automated JEE/NEET Variant Generation",
            styles["SubTitleX"]
        )]],
        colWidths=[185 * mm],
    )

    subtitle.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), ROYAL),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    story.append(subtitle)

    story.append(Spacer(1, 10))

    story.append(
        highlight(
            """
            <b>Objective:</b> Develop a scalable AI-native architecture capable
            of transforming a single expert-authored JEE/NEET question image
            into unlimited mathematically-valid and visually-consistent
            question variants using semantic reasoning,
            symbolic mathematics, and deterministic rendering.
            """,
            styles,
        )
    )

    story.append(Spacer(1, 10))
    story.append(pipeline(styles))

    story.append(PageBreak())

    # =========================================================================
    # PROBLEM STATEMENT
    # =========================================================================

    story.append(section("1. Problem Statement", styles))
    story.append(Spacer(1, 6))

    story.append(
        Paragraph(
            """
            Competitive examinations such as JEE Advanced,
            JEE Mains, and NEET require extensive exposure
            to conceptually diverse and numerically varied questions.
            Modern EdTech systems require scalable generation
            of large high-quality question banks while maintaining
            educational consistency and mathematical correctness.

            Traditional manual content authoring requires significant
            expert effort for question creation, validation,
            diagram preparation, and formatting.
            This creates substantial challenges for large-scale
            personalized learning systems.

            The proposed architecture addresses this challenge by
            combining multimodal AI reasoning,
            symbolic constraint validation,
            layout-aware image understanding,
            and deterministic rendering.
            """,
            styles["BodyX"],
        )
    )

    story.append(Spacer(1, 8))

    problem_table = [
        ["Challenge", "System Requirement"],
        ["Large-scale Content Demand", "Generate unlimited variants automatically"],
        ["Mathematical Consistency", "Constraint-aware parameter generation"],
        ["Diagram Preservation", "Maintain original visual structure"],
        ["Semantic Understanding", "Extract formulas and relationships accurately"],
        ["Readable Rendering", "Generate clean equations and diagrams"],
    ]

    pt = Table(problem_table, colWidths=[70 * mm, 110 * mm])

    pt.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]),
                ("BOX", (0, 0), (-1, -1), 1, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(pt)

    story.append(PageBreak())

    # =========================================================================
    # SYSTEM OVERVIEW
    # =========================================================================

    story.append(section("2. System Overview", styles))
    story.append(Spacer(1, 6))

    story.append(
        Paragraph(
            """
            The architecture operates as a multi-stage AI pipeline.
            The first stage performs semantic understanding of the
            original question image using GPT-4 Vision.
            This stage extracts variables, formulas,
            mathematical constraints, answer structures,
            and layout information into a structured JSON representation.

            The second stage performs symbolic validation using SymPy.
            Candidate parameters are sampled while ensuring all
            mathematical and physical constraints remain valid.

            The third stage uses Qwen2-VL for multimodal layout understanding.
            The model identifies editable regions and maps newly-generated
            parameters to the correct visual coordinates.

            Finally, deterministic rendering engines including Pillow,
            SVG, and LaTeX-based equation rendering
            generate high-quality visually-consistent question variants.
            """,
            styles["BodyX"],
        )
    )

    story.append(Spacer(1, 8))

    story.append(pipeline(styles))

    story.append(PageBreak())

    # =========================================================================
    # ARCHITECTURE
    # =========================================================================

    story.append(section("3. Unified AI Architecture", styles))
    story.append(Spacer(1, 6))

    architecture = [
        ["Layer", "Technology", "Purpose"],
        ["Input Layer", "Question Image", "Original JEE/NEET input"],
        ["Semantic Layer", "GPT-4 Vision", "Semantic JSON extraction"],
        ["Validation Layer", "SymPy", "Constraint verification"],
        ["Layout Layer", "Qwen2-VL", "Region-level edit planning"],
        ["Rendering Layer", "Pillow + SVG + LaTeX", "Readable diagram generation"],
        ["Output Layer", "PNG/PDF Export", "Final generated variants"],
    ]

    at = Table(architecture, colWidths=[45 * mm, 60 * mm, 75 * mm])

    at.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BLUE),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]),
                ("BOX", (0, 0), (-1, -1), 1, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(at)

    story.append(Spacer(1, 8))

    story.append(
        highlight(
            """
            The modular separation between semantic reasoning,
            symbolic validation,
            multimodal layout understanding,
            and deterministic rendering
            enables scalable generation of
            mathematically-valid educational content.
            """,
            styles,
        )
    )

    story.append(PageBreak())

    # =========================================================================
    # GENERATED OUTPUTS
    # =========================================================================

    story.append(section("4. AI-generated Variant Question Outputs", styles))
    story.append(Spacer(1, 6))

    story.append(
        Paragraph(
            """
            The following examples demonstrate generated JEE question variants
            created using semantic JSON extraction,
            symbolic parameter generation,
            and layout-aware rendering.
            The generated outputs preserve
            educational structure,
            diagram consistency,
            and visual readability.
            """,
            styles["BodyX"],
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        image_card(
            IMG1,
            "Example 1 — Statistical Mechanics Variant Generation",
            styles,
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        image_card(
            IMG2,
            "Example 2 — Electrodynamics Variant Generation",
            styles,
        )
    )

    story.append(PageBreak())

    # =========================================================================
    # JSON WORKFLOW
    # =========================================================================

    story.append(section("5. JSON-guided Variant Generation Workflow", styles))
    story.append(Spacer(1, 6))

    story.append(
        Paragraph(
            """
            The complete system is driven using a structured semantic JSON pipeline.
            GPT-4 Vision extracts the semantic representation of the original question.
            Constraint-aware parameter generation creates mathematically-valid samples.
            Qwen2-VL performs layout understanding and edit planning,
            while deterministic rendering engines generate the final variant image.
            """,
            styles["BodyX"],
        )
    )

    story.append(Spacer(1, 8))

    workflow = [
        ["Input", "Transformation", "Output"],
        ["Question Image", "GPT-4 Vision Extraction", "Semantic JSON"],
        ["Semantic JSON", "Constraint Validation", "Validated Parameters"],
        ["Validated JSON", "Qwen2-VL Region Mapping", "Edit Instructions"],
        ["Edit Instructions", "Pillow + SVG Rendering", "Generated Variant"],
    ]

    wt = Table(workflow, colWidths=[45 * mm, 75 * mm, 60 * mm])

    wt.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PURPLE),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]),
                ("BOX", (0, 0), (-1, -1), 1, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(wt)

    story.append(Spacer(1, 8))

    story.append(
        highlight(
            """
            The architecture enables scalable generation
            of visually-rich and mathematically-consistent
            educational content suitable for
            adaptive learning systems,
            personalized practice platforms,
            and AI-assisted EdTech workflows.
            """,
            styles,
        )
    )

    story.append(PageBreak())

    # =========================================================================
    # CONCLUSION
    # =========================================================================

    story.append(section("6. Conclusion", styles))
    story.append(Spacer(1, 6))

    story.append(
        Paragraph(
            """
            This architecture demonstrates a complete AI-native framework
            for automated educational content generation.
            By combining multimodal semantic reasoning,
            symbolic mathematics,
            layout-aware image understanding,
            and deterministic rendering,
            the system enables scalable generation
            of visually-consistent and mathematically-valid
            JEE/NEET question variants.

            The modular architecture supports future extensions
            including adaptive difficulty control,
            personalized practice generation,
            multilingual rendering,
            and large-scale educational dataset generation.
            """,
            styles["BodyX"],
        )
    )

    # =========================================================================
    # BUILD
    # =========================================================================

    doc.build(story)

    print(f"\nPDF Generated Successfully → {OUTPUT_FILE}\n")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    build_pdf()