"""
PPTX Automation Tool - Main Application
Generates PPTX and HTML presentations from content (audio, text, images)
Supports Spanish and English
"""

import json
import os
from typing import Dict, List, Optional
from pptx_generator import generate_pptx
from html_generator import generate_html
from content_processor import ContentProcessor
from translations import get_text


def build_presentation(spec: Dict, language: str = "es") -> Dict[str, str]:
    """
    Main orchestrator for the presentation generation flow.
    
    Args:
        spec: Configuration dictionary with slides_count, user data, content, etc.
        language: "es" for Spanish or "en" for English
        
    Returns:
        Dictionary with paths to generated files
    """
    processor = ContentProcessor(language=language)
    input_data = spec["input"]
    
    # Process content based on input type
    if input_data.get("audio_paths"):
        text = processor.transcribe_audio(input_data["audio_paths"])
    else:
        text = input_data.get("description", "")
        if spec.get("enable_research", False):
            text = processor.research_and_expand(text, spec["length_target"]["summary_words"])
    
    # Generate summary and slide structure
    slides_content = processor.summarize_and_outline(
        text,
        slides_count=spec["slides_count"],
        target_words=spec["length_target"]["summary_words"]
    )
    
    # Add user-provided images to slides
    imgs = input_data.get("images", [])
    for i, img in enumerate(imgs):
        if i < len(slides_content):
            slides_content[i]["image_path"] = img["path"]
            slides_content[i]["alt"] = img.get("alt", "")
    
    # Generate output files
    output_dir = spec.get("output_dir", "output")
    os.makedirs(output_dir, exist_ok=True)
    
    pptx_path = os.path.join(output_dir, "presentation.pptx")
    html_path = os.path.join(output_dir, "presentation.html")
    
    generate_pptx(spec, slides_content, pptx_path, language=language)
    generate_html(spec, slides_content, html_path, language=language)
    
    return {
        "pptx": pptx_path,
        "html": html_path,
        "status": "success"
    }


def load_spec_from_file(filepath: str) -> Dict:
    """Load specification from JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    """Main entry point for the application."""
    print("=" * 60)
    print("PPTX Automation Tool / Herramienta de Automatización PPTX")
    print("=" * 60)
    
    # Example usage with a spec file
    spec_file = "example_spec.json"
    
    if os.path.exists(spec_file):
        spec = load_spec_from_file(spec_file)
        language = spec.get("language", "es")  # Default to Spanish
        
        print(f"\n{get_text('processing', language)}...")
        
        result = build_presentation(spec, language=language)
        
        print(f"\n{get_text('success', language)}!")
        print(f"PPTX: {result['pptx']}")
        print(f"HTML: {result['html']}")
    else:
        print(f"\nExample spec file not found: {spec_file}")
        print("Please create an example_spec.json file or use the API directly.")


if __name__ == "__main__":
    main()
