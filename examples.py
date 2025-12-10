"""
Example usage of the PPTX Automation Tool
Demonstrates both programmatic and file-based approaches
"""

from config import SpecBuilder, validate_spec, save_spec
from main import build_presentation


def example_1_spanish_programmatic():
    """Example 1: Create a Spanish presentation programmatically."""
    print("\n=== Example 1: Spanish Presentation (Programmatic) ===\n")
    
    spec = (SpecBuilder(language="es")
            .set_slides_count(8)
            .set_user(name="María García", brand_name="Innovación Digital")
            .set_footer("Confidencial — Innovación Digital 2026", show_numbers=True)
            .set_theme(
                font_family="Helvetica",
                primary_color="#2C3E50",
                accent_color="#3498DB",
                bg_color="#FFFFFF"
            )
            .set_description(
                "Plan de transformación digital para pequeñas y medianas empresas. "
                "Incluye estrategias de adopción de tecnología en la nube, automatización "
                "de procesos, capacitación de equipos y medición de resultados. "
                "El programa tiene una duración de 6 meses con hitos mensuales."
            )
            .set_length_target(summary_words=300, bullets_per_slide=5)
            .set_output_dir("output/example1")
            .build()
    )
    
    # Validate
    is_valid, errors = validate_spec(spec)
    if not is_valid:
        print("Validation errors:", errors)
        return
    
    # Generate
    result = build_presentation(spec, language="es")
    print(f"✓ Generated: {result['pptx']}")
    print(f"✓ Generated: {result['html']}")


def example_2_english_programmatic():
    """Example 2: Create an English presentation programmatically."""
    print("\n=== Example 2: English Presentation (Programmatic) ===\n")
    
    spec = (SpecBuilder(language="en")
            .set_slides_count(10)
            .set_user(name="John Smith", brand_name="Global Solutions")
            .set_footer("Internal Use Only — Global Solutions", show_numbers=True)
            .set_theme(
                font_family="Arial",
                primary_color="#1A1A1A",
                accent_color="#FF6B35",
                bg_color="#F8F9FA"
            )
            .set_description(
                "Annual strategy review focusing on market expansion, product innovation, "
                "and customer satisfaction improvements. Key initiatives include launching "
                "in 3 new markets, developing 2 new product lines, and implementing a "
                "comprehensive customer feedback system. Expected ROI of 25% by year end."
            )
            .set_length_target(summary_words=450, bullets_per_slide=6)
            .set_output_dir("output/example2")
            .build()
    )
    
    # Validate
    is_valid, errors = validate_spec(spec)
    if not is_valid:
        print("Validation errors:", errors)
        return
    
    # Save spec for reference
    save_spec(spec, "output/example2/spec.json")
    
    # Generate
    result = build_presentation(spec, language="en")
    print(f"✓ Generated: {result['pptx']}")
    print(f"✓ Generated: {result['html']}")


def example_3_with_images():
    """Example 3: Presentation with images (Spanish)."""
    print("\n=== Example 3: Presentation with Images ===\n")
    
    spec = (SpecBuilder(language="es")
            .set_slides_count(6)
            .set_user(brand_name="Empresa ABC")
            .set_description(
                "Resultados del primer trimestre y proyecciones. "
                "Crecimiento del 15% en ventas, expansión del equipo, "
                "nuevas alianzas estratégicas."
            )
            .add_image("assets/chart1.png", "Gráfico de ventas Q1")
            .add_image("assets/team.jpg", "Nuevo equipo")
            .set_output_dir("output/example3")
            .build()
    )
    
    # Validate
    is_valid, errors = validate_spec(spec)
    if not is_valid:
        print("Validation errors:", errors)
        return
    
    # Generate
    result = build_presentation(spec, language="es")
    print(f"✓ Generated: {result['pptx']}")
    print(f"✓ Generated: {result['html']}")
    print("\nNote: Image files are referenced but may not exist yet.")


def example_4_bilingual_comparison():
    """Example 4: Same content in both languages."""
    print("\n=== Example 4: Bilingual Comparison ===\n")
    
    base_description = (
        "Customer satisfaction survey results showing 85% positive feedback. "
        "Main areas of improvement: faster response times, better documentation, "
        "and more training resources. Action plan includes hiring 2 support staff "
        "and creating a knowledge base."
    )
    
    # Spanish version
    spec_es = (SpecBuilder(language="es")
               .set_slides_count(7)
               .set_user(brand_name="Servicios XYZ")
               .set_description(
                   "Resultados de encuesta de satisfacción del cliente mostrando 85% "
                   "de retroalimentación positiva. Principales áreas de mejora: tiempos "
                   "de respuesta más rápidos, mejor documentación y más recursos de "
                   "capacitación. El plan de acción incluye contratar 2 empleados de "
                   "soporte y crear una base de conocimiento."
               )
               .set_output_dir("output/example4_es")
               .build()
    )
    
    result_es = build_presentation(spec_es, language="es")
    print(f"✓ Spanish: {result_es['pptx']}")
    
    # English version
    spec_en = (SpecBuilder(language="en")
               .set_slides_count(7)
               .set_user(brand_name="XYZ Services")
               .set_description(base_description)
               .set_output_dir("output/example4_en")
               .build()
    )
    
    result_en = build_presentation(spec_en, language="en")
    print(f"✓ English: {result_en['pptx']}")


def run_all_examples():
    """Run all examples."""
    print("=" * 70)
    print("PPTX Automation Tool - Examples")
    print("=" * 70)
    
    try:
        example_1_spanish_programmatic()
    except Exception as e:
        print(f"Error in Example 1: {e}")
    
    try:
        example_2_english_programmatic()
    except Exception as e:
        print(f"Error in Example 2: {e}")
    
    try:
        example_3_with_images()
    except Exception as e:
        print(f"Error in Example 3: {e}")
    
    try:
        example_4_bilingual_comparison()
    except Exception as e:
        print(f"Error in Example 4: {e}")
    
    print("\n" + "=" * 70)
    print("Examples completed! Check the output/ directory for results.")
    print("=" * 70)


if __name__ == "__main__":
    run_all_examples()
