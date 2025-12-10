"""
Content Processor Module
Handles audio transcription, text summarization, and content structuring
"""

import os
import re
from typing import Dict, List, Optional, Tuple
from translations import get_text


class ContentProcessor:
    """
    Processes various types of content (audio, text) and structures it for presentations.
    """
    
    def __init__(self, language: str = "es"):
        """
        Initialize the content processor.
        
        Args:
            language: Language code ("es" or "en")
        """
        self.language = language
    
    def transcribe_audio(self, audio_paths: List[str]) -> str:
        """
        Transcribe audio files to text.
        
        Args:
            audio_paths: List of paths to audio files
            
        Returns:
            Transcribed text
            
        Note:
            This is a placeholder. Implement with your preferred transcription library:
            - OpenAI Whisper (local or API)
            - Google Speech-to-Text
            - AssemblyAI
            - Vosk (offline)
        """
        print(f"{get_text('transcribing', self.language)}...")
        
        transcripts = []
        for audio_path in audio_paths:
            if not os.path.exists(audio_path):
                print(f"{get_text('file_not_found', self.language)}: {audio_path}")
                continue
            
            # TODO: Implement actual transcription
            # Example with OpenAI Whisper:
            # import whisper
            # model = whisper.load_model("base")
            # result = model.transcribe(audio_path, language=self.language[:2])
            # transcripts.append(result["text"])
            
            # Placeholder
            transcripts.append(f"[Transcribed text from {os.path.basename(audio_path)}]")
        
        return "\n\n".join(transcripts)
    
    def research_and_expand(self, description: str, target_words: int) -> str:
        """
        Expand a short description by researching and adding relevant information.
        
        Args:
            description: Short description to expand
            target_words: Target word count
            
        Returns:
            Expanded text
            
        Note:
            This is a placeholder. Implement with:
            - OpenAI GPT API
            - Anthropic Claude API
            - Local LLM (Ollama, LM Studio)
            - Web scraping + summarization
        """
        print(f"{get_text('researching', self.language)}...")
        
        # TODO: Implement actual research and expansion
        # Example with OpenAI:
        # import openai
        # response = openai.ChatCompletion.create(
        #     model="gpt-4",
        #     messages=[{
        #         "role": "user",
        #         "content": f"Expand this topic to ~{target_words} words: {description}"
        #     }]
        # )
        # return response.choices[0].message.content
        
        # Placeholder: repeat and pad the description
        words_needed = target_words
        current_words = len(description.split())
        repetitions = (words_needed // current_words) + 1
        
        expanded = (description + " ") * repetitions
        return " ".join(expanded.split()[:target_words])
    
    def summarize_and_outline(self, text: str, slides_count: int, target_words: int = 500) -> List[Dict]:
        """
        Summarize text and structure it into slides.
        
        Args:
            text: Input text to process
            slides_count: Desired number of slides
            target_words: Target word count for summary
            
        Returns:
            List of slide content dictionaries
        """
        print(f"{get_text('summarizing', self.language)}...")
        print(f"{get_text('structuring', self.language)}...")
        
        # Calculate number of content slides (excluding cover and conclusion)
        content_slides = slides_count - 2
        
        # TODO: Implement intelligent summarization and structuring
        # Example with OpenAI:
        # import openai
        # response = openai.ChatCompletion.create(
        #     model="gpt-4",
        #     messages=[{
        #         "role": "system",
        #         "content": f"You are a presentation expert. Create {content_slides} slides from the following text."
        #     }, {
        #         "role": "user",
        #         "content": text
        #     }]
        # )
        
        # Placeholder implementation: simple text splitting
        slides = []
        
        # Split text into sentences
        sentences = self._split_into_sentences(text)
        
        # Distribute sentences across slides
        sentences_per_slide = max(3, len(sentences) // content_slides)
        
        for i in range(content_slides):
            start_idx = i * sentences_per_slide
            end_idx = start_idx + sentences_per_slide
            slide_sentences = sentences[start_idx:end_idx]
            
            if not slide_sentences:
                break
            
            # Create slide title and bullets
            section_num = i + 1
            title = self._generate_title(section_num, slide_sentences)
            bullets = self._generate_bullets(slide_sentences)
            
            slides.append({
                "title": title,
                "bullets": bullets,
                "image_path": None,
                "alt": ""
            })
        
        return slides
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences.
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        # Simple sentence splitting (can be improved with NLP libraries)
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _generate_title(self, section_num: int, sentences: List[str]) -> str:
        """
        Generate a title for a slide section.
        
        Args:
            section_num: Section number
            sentences: Sentences in this section
            
        Returns:
            Generated title
        """
        # Simple title generation - use first few words or section number
        if sentences:
            first_sentence = sentences[0]
            words = first_sentence.split()[:5]
            title = " ".join(words)
            if len(first_sentence.split()) > 5:
                title += "..."
            return title
        
        return f"{get_text('section', self.language)} {section_num}"
    
    def _generate_bullets(self, sentences: List[str], max_bullets: int = 6) -> List[str]:
        """
        Generate bullet points from sentences.
        
        Args:
            sentences: List of sentences
            max_bullets: Maximum number of bullets
            
        Returns:
            List of bullet points
        """
        bullets = []
        
        for sentence in sentences[:max_bullets]:
            # Clean up and truncate if needed
            bullet = sentence.strip()
            if len(bullet) > 120:
                bullet = bullet[:117] + "..."
            bullets.append(bullet)
        
        return bullets
    
    def extract_key_ideas(self, text: str, count: int = 5) -> List[str]:
        """
        Extract key ideas from text.
        
        Args:
            text: Input text
            count: Number of key ideas to extract
            
        Returns:
            List of key ideas
        """
        # TODO: Implement with NLP or LLM
        # Placeholder: return first N sentences
        sentences = self._split_into_sentences(text)
        return sentences[:count]
    
    def validate_content(self, slides_content: List[Dict], spec: Dict) -> Tuple[bool, List[str]]:
        """
        Validate slide content against specification rules.
        
        Args:
            slides_content: List of slide content dictionaries
            spec: Specification dictionary
            
        Returns:
            Tuple of (is_valid, list_of_warnings)
        """
        print(f"{get_text('validating', self.language)}...")
        
        warnings = []
        max_bullets = spec["length_target"].get("bullets_per_slide_max", 6)
        
        for i, slide in enumerate(slides_content):
            # Check bullet density
            bullets = slide.get("bullets", [])
            if len(bullets) > max_bullets:
                warnings.append(f"Slide {i+1} has {len(bullets)} bullets (max: {max_bullets})")
            
            # Check for long bullets
            for j, bullet in enumerate(bullets):
                if len(bullet) > 150:
                    warnings.append(f"Slide {i+1}, bullet {j+1} is too long ({len(bullet)} chars)")
            
            # Check image existence
            image_path = slide.get("image_path")
            if image_path and not os.path.exists(image_path):
                warnings.append(f"Slide {i+1}: Image not found: {image_path}")
        
        is_valid = len(warnings) == 0
        return is_valid, warnings
