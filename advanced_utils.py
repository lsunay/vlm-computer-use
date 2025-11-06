"""
Advanced utilities for OCR, batch processing, cost tracking, and more
"""

import os
import io
import json
import base64
import tempfile
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
import pandas as pd
from PIL import Image, ImageDraw
import tiktoken


# Cost tracking per provider/model
COST_PER_TOKEN = {
    "gpt-4o": {"input": 2.50 / 1_000_000, "output": 10.00 / 1_000_000},
    "gpt-4o-mini": {"input": 0.15 / 1_000_000, "output": 0.60 / 1_000_000},
    "gpt-4-turbo": {"input": 10.00 / 1_000_000, "output": 30.00 / 1_000_000},
    "claude-3-5-sonnet-20241022": {"input": 3.00 / 1_000_000, "output": 15.00 / 1_000_000},
    "claude-3-opus-20240229": {"input": 15.00 / 1_000_000, "output": 75.00 / 1_000_000},
    "claude-3-sonnet-20240229": {"input": 3.00 / 1_000_000, "output": 15.00 / 1_000_000},
    "claude-3-haiku-20240307": {"input": 0.25 / 1_000_000, "output": 1.25 / 1_000_000},
}


def estimate_image_tokens(image_path: str, detail: str = "high") -> int:
    """
    Estimate tokens used by an image
    Based on OpenAI's vision token calculation
    """
    try:
        img = Image.open(image_path)
        width, height = img.size

        if detail == "low":
            return 85

        # For high detail, calculate based on 512px tiles
        if width > 2048 or height > 2048:
            # Resize to fit
            aspect = width / height
            if aspect > 1:
                width, height = 2048, int(2048 / aspect)
            else:
                width, height = int(2048 * aspect), 2048

        # Shortest side scaled to 768px
        aspect = width / height
        if width < height:
            width, height = 768, int(768 / aspect)
        else:
            width, height = int(768 * aspect), 768

        # Count 512px tiles
        tiles = (width // 512 + (1 if width % 512 else 0)) * \
                (height // 512 + (1 if height % 512 else 0))

        return 85 + (tiles * 170)
    except Exception:
        return 1000  # Default estimate


def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Count tokens in text"""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception:
        # Rough estimate: 1 token ≈ 4 characters
        return len(text) // 4


def calculate_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    """Calculate cost for API call"""
    if model not in COST_PER_TOKEN:
        return 0.0

    costs = COST_PER_TOKEN[model]
    return (input_tokens * costs["input"]) + (output_tokens * costs["output"])


class BatchProcessor:
    """Process multiple images/videos in batch"""

    def __init__(self, provider, progress_callback=None):
        self.provider = provider
        self.progress_callback = progress_callback
        self.results = []

    def process_images(
        self,
        image_paths: List[str],
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Process multiple images with same prompt"""
        results = []
        total = len(image_paths)

        for idx, image_path in enumerate(image_paths):
            try:
                if self.progress_callback:
                    self.progress_callback(idx + 1, total, f"Processing {os.path.basename(image_path)}")

                # Create message with single image
                message = self.provider.format_message_with_images(
                    text=prompt,
                    image_paths=[image_path]
                )

                # Get response
                response = self.provider.chat(
                    messages=[message],
                    system_prompt=system_prompt
                )

                results.append({
                    "image": image_path,
                    "result": response,
                    "success": True,
                    "error": None
                })

            except Exception as e:
                results.append({
                    "image": image_path,
                    "result": None,
                    "success": False,
                    "error": str(e)
                })

        return results

    def export_results_csv(self, results: List[Dict], output_path: str):
        """Export batch results to CSV"""
        df = pd.DataFrame(results)
        df.to_csv(output_path, index=False)

    def export_results_json(self, results: List[Dict], output_path: str):
        """Export batch results to JSON"""
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)


class OCRProcessor:
    """Advanced OCR processing"""

    def __init__(self, engine="tesseract"):
        self.engine = engine

    def extract_text(self, image_path: str, lang: str = "eng") -> str:
        """Extract text from image using OCR"""
        try:
            if self.engine == "tesseract":
                import pytesseract
                img = Image.open(image_path)
                text = pytesseract.image_to_string(img, lang=lang)
                return text
            elif self.engine == "easyocr":
                import easyocr
                reader = easyocr.Reader([lang])
                result = reader.readtext(image_path)
                return "\n".join([text[1] for text in result])
        except Exception as e:
            return f"OCR Error: {str(e)}"

    def extract_table(self, image_path: str) -> pd.DataFrame:
        """Extract table data from image"""
        try:
            import pytesseract
            from PIL import Image

            img = Image.open(image_path)
            # Get table structure
            data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

            # Process into dataframe (simplified version)
            # In production, use more sophisticated table detection
            text = pytesseract.image_to_string(img)

            # Try to parse as CSV-like structure
            lines = [line.split() for line in text.split('\n') if line.strip()]
            if lines:
                return pd.DataFrame(lines[1:], columns=lines[0] if lines else None)

            return pd.DataFrame()
        except Exception as e:
            print(f"Table extraction error: {e}")
            return pd.DataFrame()


class CodeFormatter:
    """Format and beautify generated code"""

    @staticmethod
    def format_html(code: str) -> str:
        """Format HTML code"""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(code, 'html.parser')
            return soup.prettify()
        except Exception:
            return code

    @staticmethod
    def format_python(code: str) -> str:
        """Format Python code"""
        try:
            import black
            return black.format_str(code, mode=black.Mode())
        except Exception:
            return code

    @staticmethod
    def format_javascript(code: str) -> str:
        """Format JavaScript code"""
        # For now, return as-is
        # Could integrate with prettier or similar
        return code

    @staticmethod
    def add_syntax_highlighting(code: str, language: str) -> str:
        """Add syntax highlighting to code"""
        try:
            from pygments import highlight
            from pygments.lexers import get_lexer_by_name
            from pygments.formatters import HtmlFormatter

            lexer = get_lexer_by_name(language)
            formatter = HtmlFormatter(style='monokai', full=True)
            return highlight(code, lexer, formatter)
        except Exception:
            return f"<pre><code>{code}</code></pre>"


class ImageAnnotator:
    """Annotate images with boxes, text, etc."""

    @staticmethod
    def add_bounding_box(
        image_path: str,
        boxes: List[Tuple[int, int, int, int]],
        labels: Optional[List[str]] = None,
        output_path: Optional[str] = None
    ) -> str:
        """Add bounding boxes to image"""
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)

        for idx, box in enumerate(boxes):
            x1, y1, x2, y2 = box
            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)

            if labels and idx < len(labels):
                draw.text((x1, y1 - 10), labels[idx], fill="red")

        if output_path is None:
            temp_dir = tempfile.mkdtemp()
            output_path = os.path.join(temp_dir, "annotated_" + os.path.basename(image_path))

        img.save(output_path)
        return output_path

    @staticmethod
    def add_text(
        image_path: str,
        text: str,
        position: Tuple[int, int],
        output_path: Optional[str] = None
    ) -> str:
        """Add text to image"""
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        draw.text(position, text, fill="white")

        if output_path is None:
            temp_dir = tempfile.mkdtemp()
            output_path = os.path.join(temp_dir, "annotated_" + os.path.basename(image_path))

        img.save(output_path)
        return output_path


class VideoProcessor:
    """Advanced video processing"""

    @staticmethod
    def extract_frames_smart(video_path: str, num_frames: int = 8, scene_detection: bool = False) -> List[str]:
        """Extract frames with optional scene detection"""
        import cv2

        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        if scene_detection:
            # Extract more frames and detect scenes
            # Simplified version - extract at regular intervals
            pass

        # Extract evenly spaced frames
        frame_indices = [int(i * total_frames / num_frames) for i in range(num_frames)]

        extracted_frames = []
        temp_dir = tempfile.mkdtemp()

        for idx, frame_idx in enumerate(frame_indices):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()

            if ret:
                frame_path = os.path.join(temp_dir, f"frame_{idx:03d}.jpg")
                cv2.imwrite(frame_path, frame)
                extracted_frames.append(frame_path)

        cap.release()
        return extracted_frames

    @staticmethod
    def create_gif_from_frames(frame_paths: List[str], output_path: str, duration: int = 500):
        """Create GIF from frames"""
        images = [Image.open(fp) for fp in frame_paths]
        images[0].save(
            output_path,
            save_all=True,
            append_images=images[1:],
            duration=duration,
            loop=0
        )


def export_chat_to_markdown(messages: List[Dict[str, Any]], output_path: str):
    """Export chat history to markdown"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Chat History\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")

        for msg in messages:
            role = msg.get('role', 'unknown').title()
            content = msg.get('content', '')
            timestamp = msg.get('timestamp', '')

            f.write(f"## {role}\n")
            if timestamp:
                f.write(f"*{timestamp}*\n\n")
            f.write(f"{content}\n\n")
            f.write("---\n\n")


def export_chat_to_pdf(messages: List[Dict[str, Any]], output_path: str):
    """Export chat history to PDF"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import inch

        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title = Paragraph("Chat History", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 0.5 * inch))

        # Messages
        for msg in messages:
            role = msg.get('role', 'unknown').title()
            content = msg.get('content', '')

            role_para = Paragraph(f"<b>{role}:</b>", styles['Heading2'])
            story.append(role_para)

            content_para = Paragraph(content, styles['Normal'])
            story.append(content_para)
            story.append(Spacer(1, 0.3 * inch))

        doc.build(story)
    except Exception as e:
        print(f"PDF export error: {e}")


def compare_images_similarity(image_path1: str, image_path2: str) -> float:
    """Calculate similarity between two images"""
    try:
        from skimage.metrics import structural_similarity as ssim
        import cv2

        img1 = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(image_path2, cv2.IMREAD_GRAYSCALE)

        # Resize to same dimensions
        height = min(img1.shape[0], img2.shape[0])
        width = min(img1.shape[1], img2.shape[1])
        img1 = cv2.resize(img1, (width, height))
        img2 = cv2.resize(img2, (width, height))

        similarity = ssim(img1, img2)
        return float(similarity)
    except Exception as e:
        print(f"Similarity calculation error: {e}")
        return 0.0
