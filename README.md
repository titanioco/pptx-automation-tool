# PPTX Automation Tool

Automated presentation generator that creates both PPTX and HTML presentations from content (audio, text, or images). Fully supports Spanish and English.

## 🌟 Features

- **Bilingual Support**: Works seamlessly in Spanish and English
- **Multiple Input Types**: Process text descriptions, audio files, or images
- **Dual Output**: Generates both PowerPoint (.pptx) and HTML presentations
- **Customizable Themes**: Full control over colors, fonts, and branding
- **Content Intelligence**: Automatic summarization and slide structuring
- **Easy Personalization**: Customizable logos, footers, and slide numbers

## 📋 Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## 🚀 Quick Start

### Installation

```bash
# Install core dependencies
pip install -r requirements.txt

# Optional: Install audio transcription support
pip install openai-whisper

# Optional: Install LLM support for content generation
pip install openai anthropic
```

### Basic Usage

#### Option 1: Using JSON Configuration

```python
python main.py
```

This will use the `example_spec.json` file. Customize it to your needs.

#### Option 2: Programmatic API

```python
from config import SpecBuilder
from main import build_presentation

# Build specification
spec = (SpecBuilder(language="es")
        .set_slides_count(10)
        .set_user(brand_name="Mi Empresa")
        .set_description("Estrategia de marketing digital para 2026...")
        .set_output_dir("output")
        .build())

# Generate presentations
result = build_presentation(spec, language="es")
print(f"PPTX: {result['pptx']}")
print(f"HTML: {result['html']}")
```

## 📖 Examples

Run the examples to see different use cases:

```bash
python examples.py
```

This generates:
- Spanish presentations with custom themes
- English presentations with different layouts
- Presentations with images
- Bilingual comparison examples

## 🎨 Configuration

### Specification Structure

```json
{
  "language": "es",
  "slides_count": 12,
  "user": {
    "brand_name": "ACME",
    "logo_path": "path/to/logo.png"
  },
  "footer": {
    "text": "Confidencial — ACME 2026",
    "show_slide_numbers": true
  },
  "theme": {
    "font_family": "Inter",
    "primary_color": "#1F2D3D",
    "accent_color": "#2979FF",
    "bg_color": "#FFFFFF"
  },
  "input": {
    "description": "Your content here...",
    "images": [
      {"path": "image1.png", "alt": "Description"}
    ],
    "audio_paths": ["audio1.mp3"]
  },
  "length_target": {
    "summary_words": 500,
    "bullets_per_slide_max": 6
  }
}
```

### Theme Customization

Choose your brand colors and fonts:

```python
.set_theme(
    font_family="Roboto",
    primary_color="#2C3E50",
    accent_color="#E74C3C",
    bg_color="#FFFFFF"
)
```

## 🌍 Language Support

Switch between Spanish and English:

```python
# Spanish
spec = SpecBuilder(language="es")
result = build_presentation(spec, language="es")

# English
spec = SpecBuilder(language="en")
result = build_presentation(spec, language="en")
```

All UI text, slide titles, and system messages adapt automatically.

## 📁 Project Structure

```
pptx-automation-tool/
├── main.py                 # Main application entry point
├── config.py              # Configuration and validation
├── translations.py        # Bilingual support
├── pptx_generator.py      # PowerPoint generation
├── html_generator.py      # HTML generation
├── content_processor.py   # Content processing & AI
├── examples.py            # Usage examples
├── requirements.txt       # Dependencies
├── example_spec.json      # Example configuration (Spanish)
├── example_spec_en.json   # Example configuration (English)
└── README.md             # This file
```

## 🔧 Advanced Features

### Audio Transcription

```python
spec = (SpecBuilder(language="es")
        .add_audio("presentation_notes.mp3")
        .build())
```

Note: Requires `openai-whisper` or similar library to be installed and configured in `content_processor.py`.

### Content Research & Expansion

Enable automatic content expansion:

```python
spec = (SpecBuilder(language="en")
        .set_description("Brief topic description")
        .enable_research(True)
        .build())
```

Note: Requires OpenAI API key or similar LLM service configured.

### Content Validation

```python
from content_processor import ContentProcessor

processor = ContentProcessor(language="es")
is_valid, warnings = processor.validate_content(slides, spec)

if warnings:
    for warning in warnings:
        print(f"⚠️ {warning}")
```

## 🎯 Best Practices

1. **Slide Count**: Keep between 6-15 slides for optimal engagement
2. **Bullets**: Maximum 5-6 bullets per slide
3. **Images**: Use high-resolution images (min 1024x768)
4. **Text Length**: Keep bullet points under 120 characters
5. **Colors**: Ensure sufficient contrast for readability

## 🔌 Extending the Tool

### Adding New Languages

Edit `translations.py`:

```python
TRANSLATIONS = {
    "es": {...},
    "en": {...},
    "fr": {  # Add French
        "cover": "Couverture",
        "conclusions": "Conclusions",
        # ... more translations
    }
}
```

### Custom Content Processors

Implement your own content processor:

```python
from content_processor import ContentProcessor

class CustomProcessor(ContentProcessor):
    def summarize_and_outline(self, text, slides_count, target_words):
        # Your custom logic here
        return slides_content
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: Images not appearing in slides
- **Solution**: Check that image paths are absolute or relative to the working directory

**Issue**: Fonts not displaying correctly
- **Solution**: Ensure the font is installed on the system viewing the presentation

**Issue**: Audio transcription not working
- **Solution**: Install whisper: `pip install openai-whisper`

## 📝 TODO / Roadmap

- [ ] Implement actual audio transcription (Whisper integration)
- [ ] Implement LLM-based content generation
- [ ] Add support for video embeds in HTML
- [ ] Create web UI for non-technical users
- [ ] Add PDF export option
- [ ] Implement slide templates library
- [ ] Add chart/graph generation
- [ ] Support for presenter notes

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📄 License

MIT License - feel free to use this tool for personal or commercial projects.

## 🙋 Support

For questions or issues, please open a GitHub issue or contact the maintainer.

---

**Made with ❤️ for creating beautiful presentations in Spanish and English**