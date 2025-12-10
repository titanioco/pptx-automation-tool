"""
Bilingual translations for the PPTX Automation Tool
Supports Spanish (es) and English (en)
"""

TRANSLATIONS = {
    "es": {
        # General
        "processing": "Procesando",
        "success": "¡Éxito",
        "error": "Error",
        "generating": "Generando",
        
        # Slide content
        "cover": "Portada",
        "agenda": "Agenda",
        "introduction": "Introducción",
        "conclusions": "Conclusiones y próximos pasos",
        "section": "Sección",
        "takeaway": "Punto Clave",
        
        # Bullets
        "summary_learnings": "Resumen de aprendizajes",
        "immediate_actions": "Acciones inmediatas",
        "responsible_deadlines": "Responsables y plazos",
        "key_point": "Punto",
        
        # Content processing
        "transcribing": "Transcribiendo audio",
        "summarizing": "Resumiendo contenido",
        "researching": "Investigando y expandiendo",
        "structuring": "Estructurando slides",
        
        # Validation
        "validating": "Validando contenido",
        "checking_images": "Verificando imágenes",
        "checking_density": "Verificando densidad de contenido",
        
        # File operations
        "saving_pptx": "Guardando presentación PPTX",
        "saving_html": "Guardando réplica HTML",
        "file_saved": "Archivo guardado",
        
        # Errors
        "file_not_found": "Archivo no encontrado",
        "invalid_spec": "Especificación inválida",
        "transcription_failed": "Falló la transcripción",
        "generation_failed": "Falló la generación",
    },
    "en": {
        # General
        "processing": "Processing",
        "success": "Success",
        "error": "Error",
        "generating": "Generating",
        
        # Slide content
        "cover": "Cover",
        "agenda": "Agenda",
        "introduction": "Introduction",
        "conclusions": "Conclusions and Next Steps",
        "section": "Section",
        "takeaway": "Key Takeaway",
        
        # Bullets
        "summary_learnings": "Summary of learnings",
        "immediate_actions": "Immediate actions",
        "responsible_deadlines": "Responsibilities and deadlines",
        "key_point": "Point",
        
        # Content processing
        "transcribing": "Transcribing audio",
        "summarizing": "Summarizing content",
        "researching": "Researching and expanding",
        "structuring": "Structuring slides",
        
        # Validation
        "validating": "Validating content",
        "checking_images": "Checking images",
        "checking_density": "Checking content density",
        
        # File operations
        "saving_pptx": "Saving PPTX presentation",
        "saving_html": "Saving HTML replica",
        "file_saved": "File saved",
        
        # Errors
        "file_not_found": "File not found",
        "invalid_spec": "Invalid specification",
        "transcription_failed": "Transcription failed",
        "generation_failed": "Generation failed",
    }
}


def get_text(key: str, language: str = "es") -> str:
    """
    Get translated text for a given key.
    
    Args:
        key: Translation key
        language: Language code ("es" or "en")
        
    Returns:
        Translated text or the key itself if not found
    """
    lang = language.lower()
    if lang not in TRANSLATIONS:
        lang = "es"  # Default to Spanish
    
    return TRANSLATIONS[lang].get(key, key)


def get_all_texts(language: str = "es") -> dict:
    """
    Get all translations for a specific language.
    
    Args:
        language: Language code ("es" or "en")
        
    Returns:
        Dictionary with all translations
    """
    lang = language.lower()
    if lang not in TRANSLATIONS:
        lang = "es"
    
    return TRANSLATIONS[lang]
