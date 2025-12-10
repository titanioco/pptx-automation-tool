"""
HTML Generator Module
Creates HTML replicas of presentations with equivalent styling
"""

import os
from typing import Dict, List
from jinja2 import Template
from translations import get_text


HTML_TEMPLATE = """<!doctype html>
<html lang="{{ lang }}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ brand_name }} — {{ title_text }}</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  
  body {
    font-family: {{ font_family }}, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: {{ primary_color }};
    background: {{ bg_color }};
    line-height: 1.6;
  }
  
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .slide {
    width: 100%;
    max-width: 960px;
    min-height: 540px;
    margin: 24px auto;
    padding: 40px;
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    position: relative;
    page-break-after: always;
  }
  
  .logo {
    position: absolute;
    top: 16px;
    right: 40px;
    max-height: 40px;
    max-width: 150px;
  }
  
  .title {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 24px;
    color: {{ primary_color }};
    padding-top: 8px;
  }
  
  .subtitle {
    font-size: 16px;
    color: {{ accent_color }};
    margin-bottom: 16px;
    margin-top: -12px;
  }
  
  .content {
    display: flex;
    gap: 32px;
    margin-bottom: 40px;
  }
  
  .bullets {
    flex: 1;
    list-style-position: inside;
    padding-left: 0;
  }
  
  .bullets li {
    font-size: 18px;
    margin: 12px 0;
    padding-left: 8px;
    color: {{ primary_color }};
  }
  
  .image-container {
    flex: 0 0 320px;
    text-align: center;
  }
  
  .image-container img {
    max-width: 100%;
    height: auto;
    border-radius: 4px;
  }
  
  .footer {
    font-size: 11px;
    margin-top: 32px;
    padding-top: 16px;
    border-top: 1px solid #e0e0e0;
    color: {{ primary_color }};
    opacity: 0.8;
  }
  
  .cover-slide {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
  }
  
  .cover-slide .title {
    font-size: 42px;
    margin-bottom: 16px;
  }
  
  .takeaway {
    background: {{ accent_color }}15;
    border-left: 4px solid {{ accent_color }};
    padding: 12px 16px;
    margin: 16px 0;
    border-radius: 4px;
  }
  
  @media print {
    .slide {
      box-shadow: none;
      border: none;
      margin: 0;
      page-break-after: always;
    }
  }
  
  @media (max-width: 768px) {
    .slide {
      padding: 24px;
      min-height: auto;
    }
    
    .content {
      flex-direction: column;
    }
    
    .image-container {
      flex: 1;
    }
    
    .title {
      font-size: 24px;
    }
    
    .cover-slide .title {
      font-size: 32px;
    }
    
    .bullets li {
      font-size: 16px;
    }
  }
</style>
</head>
<body>
  <div class="container">
    
    <!-- Cover Slide -->
    <div class="slide cover-slide">
      {% if logo_path %}
      <img src="{{ logo_path }}" alt="{{ brand_name }} Logo" class="logo">
      {% endif %}
      <div class="title">{{ brand_name }}</div>
      {% if subtitle %}
      <div class="subtitle">{{ subtitle }}</div>
      {% endif %}
      <div class="footer">{{ footer_text }} {% if show_numbers %}| 1/{{ total }}{% endif %}</div>
    </div>
    
    <!-- Content Slides -->
    {% for i, s in enumerate(slides) %}
    <div class="slide">
      {% if logo_path %}
      <img src="{{ logo_path }}" alt="{{ brand_name }} Logo" class="logo">
      {% endif %}
      <div class="title">{{ s.title }}</div>
      <div class="content">
        <ul class="bullets">
          {% for b in s.bullets %}
          <li>{{ b }}</li>
          {% endfor %}
        </ul>
        {% if s.image_path %}
        <div class="image-container">
          <img src="{{ s.image_path }}" alt="{{ s.alt or '' }}">
        </div>
        {% endif %}
      </div>
      <div class="footer">{{ footer_text }} {% if show_numbers %}| {{ i + 2 }}/{{ total }}{% endif %}</div>
    </div>
    {% endfor %}
    
    <!-- Conclusion Slide -->
    <div class="slide">
      {% if logo_path %}
      <img src="{{ logo_path }}" alt="{{ brand_name }} Logo" class="logo">
      {% endif %}
      <div class="title">{{ conclusion_title }}</div>
      <div class="content">
        <ul class="bullets">
          {% for b in conclusion_bullets %}
          <li>{{ b }}</li>
          {% endfor %}
        </ul>
      </div>
      <div class="footer">{{ footer_text }} {% if show_numbers %}| {{ total }}/{{ total }}{% endif %}</div>
    </div>
    
  </div>
</body>
</html>
"""


def generate_html(spec: Dict, slides_content: List[Dict], out_path: str = "presentation.html", language: str = "es"):
    """
    Generate HTML replica of the presentation.
    
    Args:
        spec: Specification dictionary with theme, user info, etc.
        slides_content: List of slide content dictionaries
        out_path: Output file path
        language: Language code ("es" or "en")
    """
    theme = spec["theme"]
    user = spec["user"]
    footer = spec["footer"]
    
    # Prepare subtitle from description
    subtitle = ""
    if spec.get("input", {}).get("description"):
        desc = spec["input"]["description"]
        subtitle = desc[:150] + "..." if len(desc) > 150 else desc
    
    # Prepare conclusion bullets
    conclusion_bullets = [
        get_text("summary_learnings", language),
        get_text("immediate_actions", language),
        get_text("responsible_deadlines", language)
    ]
    
    # Render template
    html = Template(HTML_TEMPLATE).render(
        lang=language,
        brand_name=user.get("brand_name", user.get("name", "Presentation")),
        title_text=get_text("cover", language),
        subtitle=subtitle,
        font_family=theme.get("font_family", "Inter"),
        primary_color=theme["primary_color"],
        accent_color=theme.get("accent_color", theme["primary_color"]),
        bg_color=theme.get("bg_color", "#FFFFFF"),
        slides=slides_content,
        footer_text=footer["text"],
        show_numbers=footer.get("show_slide_numbers", True),
        total=spec["slides_count"],
        logo_path=user.get("logo_path", ""),
        conclusion_title=get_text("conclusions", language),
        conclusion_bullets=conclusion_bullets,
        enumerate=enumerate
    )
    
    # Save HTML file
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"{get_text('file_saved', language)}: {out_path}")


def generate_standalone_css(spec: Dict, out_path: str = "styles.css"):
    """
    Generate a standalone CSS file (optional).
    
    Args:
        spec: Specification dictionary with theme info
        out_path: Output file path for CSS
    """
    theme = spec["theme"]
    
    css_content = f"""
/* Presentation Styles */
:root {{
    --primary-color: {theme['primary_color']};
    --accent-color: {theme.get('accent_color', theme['primary_color'])};
    --bg-color: {theme.get('bg_color', '#FFFFFF')};
    --font-family: {theme.get('font_family', 'Inter')}, sans-serif;
}}

/* Add your custom styles here */
"""
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(css_content)
