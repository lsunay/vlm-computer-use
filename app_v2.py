"""
Vision Language Model Demo Application - V2 with ALL Features
Comprehensive VLM application with 30+ features
"""

import os
import json
import tempfile
import shutil
import gradio as gr
from typing import List, Tuple, Optional, Dict, Any
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

from providers import ProviderFactory, VLMProvider
from utils import (
    extract_frames_from_video,
    resize_image,
    validate_image,
    get_system_prompt,
)
from advanced_utils import (
    BatchProcessor,
    OCRProcessor,
    CodeFormatter,
    ImageAnnotator,
    estimate_image_tokens,
    count_tokens,
    calculate_cost,
    export_chat_to_markdown,
    export_chat_to_pdf,
    compare_images_similarity,
)
from database import db
from presets import (
    get_presets_by_category,
    get_all_categories,
    get_code_template,
    SYSTEM_PROMPTS,
)

# Load environment variables
load_dotenv()


class VLMAppV2:
    """Enhanced VLM application with all features"""

    def __init__(self):
        self.provider: Optional[VLMProvider] = None
        self.provider_name: str = ""
        self.model_name: str = ""
        self.chat_history: List[dict] = []
        self.current_session_id: Optional[int] = None
        self.total_cost: float = 0.0
        self.total_tokens: int = 0

    # ==================== CONFIGURATION ====================

    def initialize_provider(
        self, provider_type: str, api_key: str, base_url: str, model: str
    ) -> str:
        """Initialize the selected provider"""
        try:
            api_key = api_key.strip() if api_key else None
            base_url = base_url.strip() if base_url else None
            model = model.strip() if model else None

            self.provider = ProviderFactory.create_provider(
                provider_type=provider_type,
                api_key=api_key,
                base_url=base_url,
                model=model,
            )
            self.provider_name = provider_type
            self.model_name = model or "default"

            return f"✅ Successfully initialized {provider_type} provider with model: {self.model_name}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    # ==================== CHAT WITH IMAGES ====================

    def chat_with_images(
        self,
        message: str,
        images: List[str],
        mode: str,
        history: List[Tuple[str, str]],
        save_to_db: bool = True,
    ) -> Tuple[List[Tuple[str, str]], str, str]:
        """Enhanced chat with cost tracking"""
        if not self.provider:
            return history, "", "⚠️ Please configure provider first!"

        if not message and not images:
            return history, "", "⚠️ Provide a message or images!"

        try:
            # Prepare images
            image_paths = []
            if images:
                for img_path in images:
                    if validate_image(img_path):
                        resized = resize_image(img_path)
                        image_paths.append(resized)

            # Create session if needed
            if save_to_db and not self.current_session_id:
                self.current_session_id = db.create_chat_session(
                    title=message[:50] if message else "Image Chat",
                    provider=self.provider_name,
                    model=self.model_name,
                    mode=mode,
                )

            # Create message
            user_message = self.provider.format_message_with_images(
                text=message, image_paths=image_paths
            )

            # Calculate input tokens
            input_tokens = count_tokens(message, self.model_name)
            for img in image_paths:
                input_tokens += estimate_image_tokens(img)

            self.chat_history.append(user_message)

            # Get response
            system_prompt = get_system_prompt(mode)
            response = self.provider.chat(
                messages=self.chat_history, system_prompt=system_prompt
            )

            # Calculate cost
            output_tokens = count_tokens(response, self.model_name)
            cost = calculate_cost(input_tokens, output_tokens, self.model_name)
            self.total_cost += cost
            self.total_tokens += input_tokens + output_tokens

            # Add to history
            self.chat_history.append({"role": "assistant", "content": response})

            # Save to database
            if save_to_db and self.current_session_id:
                db.add_message(
                    self.current_session_id,
                    "user",
                    message,
                    image_paths,
                    input_tokens,
                    0,
                )
                db.add_message(
                    self.current_session_id,
                    "assistant",
                    response,
                    None,
                    output_tokens,
                    cost,
                )

            # Format for display (Gradio 6.x compatible)
            display_msg = message if message else "[Image(s) uploaded]"
            history.append({"role": "user", "content": display_msg})
            history.append({"role": "assistant", "content": response})

            # Cost info
            cost_info = f"💰 Cost: ${cost:.4f} | Tokens: {input_tokens + output_tokens} | Total: ${self.total_cost:.4f}"

            return history, "", cost_info

        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            return history, "", error_msg

    def clear_chat(self):
        """Clear chat and start new session"""
        self.chat_history = []
        self.current_session_id = None
        return [], ""

    def load_chat_session(self, session_id: int):
        """Load existing chat session"""
        try:
            messages = db.get_session_history(session_id)
            self.chat_history = []
            history = []

            for msg in messages:
                if msg["role"] == "user":
                    self.chat_history.append(
                        {
                            "role": "user",
                            "content": [{"type": "text", "text": msg["content"]}],
                        }
                    )
                    history.append((msg["content"], ""))
                else:
                    self.chat_history.append(
                        {"role": "assistant", "content": msg["content"]}
                    )
                    if history:
                        history[-1] = (history[-1][0], msg["content"])

            self.current_session_id = session_id
            return history, "✅ Session loaded!"
        except Exception as e:
            return [], f"❌ Error: {str(e)}"

    def export_chat_history(self, format_type: str) -> str:
        """Export chat history"""
        try:
            if not self.current_session_id:
                return "⚠️ No active session to export"

            messages = db.get_session_history(self.current_session_id)
            temp_dir = tempfile.mkdtemp()

            if format_type == "markdown":
                output_path = os.path.join(temp_dir, "chat_export.md")
                export_chat_to_markdown(messages, output_path)
            elif format_type == "pdf":
                output_path = os.path.join(temp_dir, "chat_export.pdf")
                export_chat_to_pdf(messages, output_path)
            elif format_type == "json":
                output_path = os.path.join(temp_dir, "chat_export.json")
                with open(output_path, "w") as f:
                    json.dump(messages, f, indent=2, default=str)
            else:
                return "⚠️ Invalid format"

            return output_path
        except Exception as e:
            return f"❌ Error: {str(e)}"

    # ==================== SCREENSHOT TO CODE ====================

    def generate_code_from_screenshot(
        self,
        images: List[str],
        framework: str,
        instructions: str,
        save_to_db: bool = True,
    ) -> Tuple[str, str]:
        """Enhanced code generation with templates"""
        if not self.provider:
            return "", "⚠️ Please configure provider first!"

        if not images:
            return "", "⚠️ Upload at least one screenshot!"

        try:
            # Prepare images
            image_paths = []
            for img_path in images:
                if validate_image(img_path):
                    resized = resize_image(img_path)
                    image_paths.append(resized)

            # Get template
            template = get_code_template(framework)

            # Create prompt
            base_prompt = f"Generate {template['name']} code for this design."
            if instructions:
                base_prompt += f"\n\nAdditional requirements:\n{instructions}"

            base_prompt += "\n\nRequirements:\n"
            base_prompt += "- Generate clean, production-ready code\n"
            base_prompt += "- Make it responsive\n"
            base_prompt += "- Use modern best practices\n"
            base_prompt += "- Include helpful comments\n"
            base_prompt += "- Match the design pixel-perfect\n"

            # Create message
            message = self.provider.format_message_with_images(
                text=base_prompt, image_paths=image_paths
            )

            # Get system prompt
            system_prompt = SYSTEM_PROMPTS["code_generation"].get(
                framework, SYSTEM_PROMPTS["code_generation"]["html"]
            )

            # Generate
            code = self.provider.chat(messages=[message], system_prompt=system_prompt)

            # Calculate cost
            input_tokens = count_tokens(base_prompt, self.model_name)
            for img in image_paths:
                input_tokens += estimate_image_tokens(img)
            output_tokens = count_tokens(code, self.model_name)
            cost = calculate_cost(input_tokens, output_tokens, self.model_name)

            # Save to database
            if save_to_db:
                db.save_generated_code(
                    title=instructions[:50] if instructions else "Generated Code",
                    code=code,
                    framework=framework,
                    description=instructions,
                    image_paths=image_paths,
                    provider=self.provider_name,
                    model=self.model_name,
                    tokens=input_tokens + output_tokens,
                    cost=cost,
                )

            info = f"✅ Generated {framework} code | Cost: ${cost:.4f}"
            return code, info

        except Exception as e:
            return "", f"❌ Error: {str(e)}"

    def refine_code(
        self, current_code: str, refinement_request: str, framework: str
    ) -> Tuple[str, str]:
        """Iteratively refine generated code"""
        if not self.provider:
            return current_code, "⚠️ Please configure provider first!"

        try:
            prompt = (
                f"Here is the current code:\n\n```{framework}\n{current_code}\n```\n\n"
            )
            prompt += f"Please make the following changes:\n{refinement_request}\n\n"
            prompt += "Return ONLY the updated code, no explanations."

            message = {"role": "user", "content": prompt}

            response = self.provider.chat(messages=[message])

            return response, "✅ Code refined successfully!"
        except Exception as e:
            return current_code, f"❌ Error: {str(e)}"

    # ==================== BATCH PROCESSING ====================

    def batch_process_images(
        self, images: List[str], prompt: str, export_format: str
    ) -> Tuple[str, str]:
        """Batch process multiple images"""
        if not self.provider:
            return None, "⚠️ Please configure provider first!"

        if not images or len(images) == 0:
            return None, "⚠️ Upload images to process!"

        try:
            processor = BatchProcessor(self.provider)
            results = processor.process_images(images, prompt)

            # Export results
            temp_dir = tempfile.mkdtemp()

            if export_format == "csv":
                output_path = os.path.join(temp_dir, "batch_results.csv")
                processor.export_results_csv(results, output_path)
            elif export_format == "json":
                output_path = os.path.join(temp_dir, "batch_results.json")
                processor.export_results_json(results, output_path)
            else:
                # Create text summary
                output_path = os.path.join(temp_dir, "batch_results.txt")
                with open(output_path, "w") as f:
                    for r in results:
                        f.write(f"Image: {os.path.basename(r['image'])}\n")
                        f.write(f"Result: {r['result']}\n")
                        f.write("-" * 80 + "\n\n")

            success_count = sum(1 for r in results if r["success"])
            info = f"✅ Processed {success_count}/{len(results)} images successfully"

            return output_path, info

        except Exception as e:
            return None, f"❌ Error: {str(e)}"

    # ==================== IMAGE COMPARISON ====================

    def compare_images(self, images: List[str], comparison_prompt: str) -> str:
        """Compare multiple images"""
        if not self.provider:
            return "⚠️ Please configure provider first!"

        if not images or len(images) < 2:
            return "⚠️ Upload at least 2 images to compare!"

        try:
            # Prepare images
            image_paths = []
            for img_path in images:
                if validate_image(img_path):
                    resized = resize_image(img_path)
                    image_paths.append(resized)

            # Create message
            prompt = (
                comparison_prompt
                or "Compare these images in detail. Analyze differences, similarities, strengths and weaknesses of each."
            )
            message = self.provider.format_message_with_images(
                text=prompt, image_paths=image_paths
            )

            # Get response
            system_prompt = get_system_prompt("analysis")
            response = self.provider.chat(
                messages=[message], system_prompt=system_prompt
            )

            # Add similarity scores if exactly 2 images
            if len(image_paths) == 2:
                similarity = compare_images_similarity(image_paths[0], image_paths[1])
                response += f"\n\n**Technical Similarity Score:** {similarity:.2%}"

            return response

        except Exception as e:
            return f"❌ Error: {str(e)}"

    # ==================== OCR & DOCUMENT PROCESSING ====================

    def extract_text_ocr(self, image: str, lang: str = "eng") -> str:
        """Extract text using OCR"""
        if not image:
            return "⚠️ Upload an image!"

        try:
            ocr = OCRProcessor()
            text = ocr.extract_text(image, lang)
            return f"**Extracted Text:**\n\n{text}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def extract_table(self, image: str) -> Tuple[Any, str]:
        """Extract table from image"""
        if not image:
            return None, "⚠️ Upload an image!"

        try:
            ocr = OCRProcessor()
            df = ocr.extract_table(image)

            if df.empty:
                return None, "⚠️ No table detected"

            return df, "✅ Table extracted successfully!"
        except Exception as e:
            return None, f"❌ Error: {str(e)}"

    # ==================== VIDEO ANALYSIS ====================

    def analyze_video(self, video_path: str, question: str, num_frames: int) -> str:
        """Enhanced video analysis"""
        if not self.provider:
            return "⚠️ Please configure provider first!"

        if not video_path:
            return "⚠️ Upload a video!"

        try:
            # Extract frames
            frames = extract_frames_from_video(video_path, num_frames)

            # Create message
            prompt = (
                question
                or "Analyze this video and describe what you see. Include key moments, actions, and overall narrative."
            )
            message = self.provider.format_message_with_images(
                text=prompt, image_paths=frames
            )

            # Get response
            system_prompt = get_system_prompt("analysis")
            response = self.provider.chat(
                messages=[message], system_prompt=system_prompt
            )

            return response

        except Exception as e:
            return f"❌ Error: {str(e)}"

    # ==================== MODEL COMPARISON ====================

    def compare_models(
        self, message: str, images: List[str], models: List[Dict[str, str]]
    ) -> str:
        """Compare responses from multiple models"""
        if not message and not images:
            return "⚠️ Provide a message or images!"

        results = []

        for model_config in models:
            try:
                # Create provider
                provider = ProviderFactory.create_provider(
                    provider_type=model_config["provider"],
                    api_key=model_config.get("api_key"),
                    base_url=model_config.get("base_url"),
                    model=model_config.get("model"),
                )

                # Prepare message
                if images:
                    msg = provider.format_message_with_images(
                        text=message, image_paths=images
                    )
                else:
                    msg = {"role": "user", "content": message}

                # Get response
                response = provider.chat(messages=[msg])

                results.append(
                    {
                        "model": f"{model_config['provider']} - {model_config.get('model', 'default')}",
                        "response": response,
                        "success": True,
                    }
                )

            except Exception as e:
                results.append(
                    {
                        "model": f"{model_config['provider']} - {model_config.get('model', 'default')}",
                        "response": f"Error: {str(e)}",
                        "success": False,
                    }
                )

        # Format comparison
        output = "# Model Comparison Results\n\n"
        for idx, result in enumerate(results, 1):
            output += f"## Model {idx}: {result['model']}\n\n"
            output += f"{result['response']}\n\n"
            output += "---\n\n"

        return output

    # ==================== PRESET PROMPTS ====================

    def apply_preset(
        self, preset_prompt: str, images: List[str]
    ) -> Tuple[List[Tuple[str, str]], str, str]:
        """Apply preset prompt"""
        return self.chat_with_images(preset_prompt, images, "analysis", [])

    # ==================== USAGE STATS ====================

    def get_usage_stats(self, days: int = 30) -> str:
        """Get usage statistics"""
        try:
            stats = db.get_usage_stats(days=days)

            output = f"# Usage Statistics (Last {days} days)\n\n"
            output += f"**Total Requests:** {stats['total_requests']}\n"
            output += f"**Total Cost:** ${stats['total_cost']:.2f}\n"
            output += f"**Total Tokens:** {stats['total_tokens']:,}\n"
            output += f"**Success Rate:** {stats['success_rate']:.1f}%\n\n"

            return output
        except Exception as e:
            return f"❌ Error: {str(e)}"


# Continue in next part...
