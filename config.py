"""
Configuration Module
Handles specification validation and default configurations
"""

from typing import Dict, Any, List
import json


DEFAULT_THEME = {
    "font_family": "Inter",
    "primary_color": "#1F2D3D",
    "accent_color": "#2979FF",
    "bg_color": "#FFFFFF"
}

DEFAULT_LENGTH_TARGET = {
    "summary_words": 500,
    "bullets_per_slide_max": 6
}

DEFAULT_FOOTER = {
    "text": "Confidential",
    "show_slide_numbers": True
}


def get_default_spec(language: str = "es") -> Dict:
    """
    Get a default specification template.
    
    Args:
        language: Language code ("es" or "en")
        
    Returns:
        Default specification dictionary
    """
    return {
        "language": language,
        "slides_count": 10,
        "user": {
            "name": "User",
            "brand_name": "Company",
            "logo_path": ""
        },
        "footer": DEFAULT_FOOTER.copy(),
        "theme": DEFAULT_THEME.copy(),
        "input": {
            "description": "",
            "images": [],
            "audio_paths": []
        },
        "length_target": DEFAULT_LENGTH_TARGET.copy(),
        "output_dir": "output",
        "enable_research": False
    }


def validate_spec(spec: Dict) -> tuple[bool, List[str]]:
    """
    Validate a specification dictionary.
    
    Args:
        spec: Specification dictionary to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Required fields
    required_fields = ["slides_count", "user", "theme", "input"]
    for field in required_fields:
        if field not in spec:
            errors.append(f"Missing required field: {field}")
    
    # Validate slides_count
    if "slides_count" in spec:
        if not isinstance(spec["slides_count"], int) or spec["slides_count"] < 3:
            errors.append("slides_count must be an integer >= 3")
    
    # Validate user
    if "user" in spec:
        if "name" not in spec["user"] and "brand_name" not in spec["user"]:
            errors.append("user must have 'name' or 'brand_name'")
    
    # Validate theme
    if "theme" in spec:
        theme = spec["theme"]
        if "primary_color" not in theme:
            errors.append("theme must have 'primary_color'")
    
    # Validate input
    if "input" in spec:
        input_data = spec["input"]
        has_content = (
            input_data.get("description") or
            input_data.get("audio_paths") or
            input_data.get("images")
        )
        if not has_content:
            errors.append("input must have description, audio_paths, or images")
    
    is_valid = len(errors) == 0
    return is_valid, errors


def merge_with_defaults(spec: Dict) -> Dict:
    """
    Merge user specification with default values.
    
    Args:
        spec: User-provided specification
        
    Returns:
        Complete specification with defaults filled in
    """
    language = spec.get("language", "es")
    default = get_default_spec(language)
    
    # Deep merge
    merged = default.copy()
    
    for key, value in spec.items():
        if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
            # Merge dictionaries
            merged[key] = {**merged[key], **value}
        else:
            merged[key] = value
    
    return merged


def save_spec(spec: Dict, filepath: str):
    """
    Save specification to JSON file.
    
    Args:
        spec: Specification dictionary
        filepath: Output file path
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)


def load_spec(filepath: str) -> Dict:
    """
    Load specification from JSON file.
    
    Args:
        filepath: Input file path
        
    Returns:
        Specification dictionary
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


class SpecBuilder:
    """
    Builder class for creating specifications programmatically.
    """
    
    def __init__(self, language: str = "es"):
        """Initialize with default spec."""
        self.spec = get_default_spec(language)
    
    def set_slides_count(self, count: int) -> 'SpecBuilder':
        """Set number of slides."""
        self.spec["slides_count"] = count
        return self
    
    def set_user(self, name: str = None, brand_name: str = None, logo_path: str = None) -> 'SpecBuilder':
        """Set user information."""
        if name:
            self.spec["user"]["name"] = name
        if brand_name:
            self.spec["user"]["brand_name"] = brand_name
        if logo_path:
            self.spec["user"]["logo_path"] = logo_path
        return self
    
    def set_footer(self, text: str, show_numbers: bool = True) -> 'SpecBuilder':
        """Set footer configuration."""
        self.spec["footer"]["text"] = text
        self.spec["footer"]["show_slide_numbers"] = show_numbers
        return self
    
    def set_theme(self, font_family: str = None, primary_color: str = None, 
                  accent_color: str = None, bg_color: str = None) -> 'SpecBuilder':
        """Set theme configuration."""
        if font_family:
            self.spec["theme"]["font_family"] = font_family
        if primary_color:
            self.spec["theme"]["primary_color"] = primary_color
        if accent_color:
            self.spec["theme"]["accent_color"] = accent_color
        if bg_color:
            self.spec["theme"]["bg_color"] = bg_color
        return self
    
    def set_description(self, description: str) -> 'SpecBuilder':
        """Set content description."""
        self.spec["input"]["description"] = description
        return self
    
    def add_image(self, path: str, alt: str = "") -> 'SpecBuilder':
        """Add an image to the presentation."""
        self.spec["input"]["images"].append({"path": path, "alt": alt})
        return self
    
    def add_audio(self, path: str) -> 'SpecBuilder':
        """Add an audio file for transcription."""
        self.spec["input"]["audio_paths"].append(path)
        return self
    
    def set_length_target(self, summary_words: int = None, bullets_per_slide: int = None) -> 'SpecBuilder':
        """Set length constraints."""
        if summary_words:
            self.spec["length_target"]["summary_words"] = summary_words
        if bullets_per_slide:
            self.spec["length_target"]["bullets_per_slide_max"] = bullets_per_slide
        return self
    
    def set_output_dir(self, directory: str) -> 'SpecBuilder':
        """Set output directory."""
        self.spec["output_dir"] = directory
        return self
    
    def enable_research(self, enable: bool = True) -> 'SpecBuilder':
        """Enable or disable content research/expansion."""
        self.spec["enable_research"] = enable
        return self
    
    def build(self) -> Dict:
        """Return the built specification."""
        return self.spec
