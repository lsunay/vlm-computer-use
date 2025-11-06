"""
Vision Language Model Demo Application
Supports multiple providers: OpenAI, Anthropic, Ollama, and custom APIs
"""

import os
import gradio as gr
from typing import List, Tuple, Optional
from dotenv import load_dotenv

from providers import ProviderFactory, VLMProvider
from utils import extract_frames_from_video, resize_image, validate_image, get_system_prompt

# Load environment variables
load_dotenv()


class VLMApp:
    """Main application class for VLM demo"""

    def __init__(self):
        self.provider: Optional[VLMProvider] = None
        self.chat_history: List[dict] = []

    def initialize_provider(
        self,
        provider_type: str,
        api_key: str,
        base_url: str,
        model: str
    ) -> str:
        """Initialize the selected provider"""
        try:
            # Handle empty strings
            api_key = api_key.strip() if api_key else None
            base_url = base_url.strip() if base_url else None
            model = model.strip() if model else None

            self.provider = ProviderFactory.create_provider(
                provider_type=provider_type,
                api_key=api_key if api_key else None,
                base_url=base_url if base_url else None,
                model=model if model else None
            )
            return f"✓ Successfully initialized {provider_type} provider with model: {model or 'default'}"
        except Exception as e:
            return f"✗ Error initializing provider: {str(e)}"

    def chat_with_images(
        self,
        message: str,
        images: List[str],
        mode: str,
        history: List[Tuple[str, str]]
    ) -> Tuple[List[Tuple[str, str]], str]:
        """Handle chat with images"""
        if not self.provider:
            return history, "Please configure and initialize a provider first!"

        if not message and not images:
            return history, "Please provide a message or upload images!"

        try:
            # Prepare images
            image_paths = []
            if images:
                for img_path in images:
                    if validate_image(img_path):
                        # Resize if needed
                        resized = resize_image(img_path)
                        image_paths.append(resized)

            # Create user message
            user_message = self.provider.format_message_with_images(
                text=message,
                image_paths=image_paths
            )

            # Add to chat history
            self.chat_history.append(user_message)

            # Get system prompt based on mode
            system_prompt = get_system_prompt(mode)

            # Get response
            response = self.provider.chat(
                messages=self.chat_history,
                system_prompt=system_prompt
            )

            # Add assistant response to history
            self.chat_history.append({
                "role": "assistant",
                "content": response
            })

            # Format for Gradio
            display_msg = message if message else "[Image(s) uploaded]"
            history.append((display_msg, response))

            return history, ""

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            history.append((message or "[Image(s) uploaded]", error_msg))
            return history, ""

    def analyze_video(
        self,
        video_path: str,
        question: str,
        num_frames: int
    ) -> str:
        """Analyze video by extracting frames"""
        if not self.provider:
            return "Please configure and initialize a provider first!"

        if not video_path:
            return "Please upload a video!"

        try:
            # Extract frames
            frames = extract_frames_from_video(video_path, num_frames)

            # Create message with frames
            message = self.provider.format_message_with_images(
                text=question or "Please analyze this video and describe what you see.",
                image_paths=frames
            )

            # Get response
            system_prompt = get_system_prompt("analysis")
            response = self.provider.chat(
                messages=[message],
                system_prompt=system_prompt
            )

            return response

        except Exception as e:
            return f"Error analyzing video: {str(e)}"

    def generate_code_from_screenshot(
        self,
        images: List[str],
        instructions: str
    ) -> str:
        """Generate code from screenshot(s)"""
        if not self.provider:
            return "Please configure and initialize a provider first!"

        if not images:
            return "Please upload at least one screenshot!"

        try:
            # Prepare images
            image_paths = []
            for img_path in images:
                if validate_image(img_path):
                    resized = resize_image(img_path)
                    image_paths.append(resized)

            # Create prompt
            prompt = f"""Generate complete, production-ready code for this design.

{instructions if instructions else 'Create a pixel-perfect implementation of this design.'}

Requirements:
- Generate clean HTML with embedded CSS
- Make it responsive
- Use modern CSS (flexbox/grid)
- Include all visual details
- Add helpful comments

Provide ONLY the code, no explanations outside code comments."""

            # Create message
            message = self.provider.format_message_with_images(
                text=prompt,
                image_paths=image_paths
            )

            # Get response
            system_prompt = get_system_prompt("code_generation")
            response = self.provider.chat(
                messages=[message],
                system_prompt=system_prompt
            )

            return response

        except Exception as e:
            return f"Error generating code: {str(e)}"

    def clear_chat(self):
        """Clear chat history"""
        self.chat_history = []
        return []


def create_ui():
    """Create Gradio UI"""
    app = VLMApp()

    with gr.Blocks(title="VLM Demo - Bring Your Own Provider", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 🎨 Vision Language Model Demo
        ### Bring Your Own Provider - OpenAI, Anthropic, Ollama, or Custom API

        Chat with images, analyze videos, and generate code from screenshots using your own LLM provider.
        """)

        with gr.Tabs() as tabs:
            # Configuration Tab
            with gr.Tab("⚙️ Configuration"):
                gr.Markdown("### Configure Your Provider")

                with gr.Row():
                    provider_type = gr.Dropdown(
                        choices=["openai", "anthropic", "ollama", "custom"],
                        value=os.getenv("DEFAULT_PROVIDER", "openai"),
                        label="Provider Type",
                        info="Select your LLM provider"
                    )

                with gr.Row():
                    api_key_input = gr.Textbox(
                        label="API Key",
                        type="password",
                        placeholder="Enter your API key (leave empty to use .env)",
                        info="Your API key (not needed for Ollama)"
                    )

                with gr.Row():
                    base_url_input = gr.Textbox(
                        label="Base URL (Optional)",
                        placeholder="e.g., http://localhost:11434/v1 or https://api.openai.com/v1",
                        info="Leave empty to use defaults"
                    )

                with gr.Row():
                    model_input = gr.Textbox(
                        label="Model Name (Optional)",
                        placeholder="e.g., gpt-4o, claude-3-5-sonnet-20241022, llava:latest",
                        info="Leave empty to use defaults from .env"
                    )

                init_btn = gr.Button("Initialize Provider", variant="primary", size="lg")
                status_output = gr.Textbox(label="Status", interactive=False)

                init_btn.click(
                    fn=app.initialize_provider,
                    inputs=[provider_type, api_key_input, base_url_input, model_input],
                    outputs=status_output
                )

                gr.Markdown("""
                ### Provider Examples:

                **OpenAI:**
                - Provider: `openai`
                - Model: `gpt-4o` or `gpt-4o-mini`
                - Base URL: `https://api.openai.com/v1` (default)

                **Anthropic:**
                - Provider: `anthropic`
                - Model: `claude-3-5-sonnet-20241022`

                **Ollama (Local):**
                - Provider: `ollama`
                - Model: `llava:latest` or `llava:13b`
                - Base URL: `http://localhost:11434/v1` (default)
                - No API key needed

                **Custom (OpenAI-compatible):**
                - Provider: `custom`
                - Configure your own endpoint
                """)

            # Chat Tab
            with gr.Tab("💬 Chat with Images"):
                gr.Markdown("### Multi-Image Chat Interface")

                with gr.Row():
                    with gr.Column(scale=1):
                        mode_selector = gr.Radio(
                            choices=["chat", "analysis", "thinking"],
                            value="chat",
                            label="Mode",
                            info="Select conversation mode"
                        )

                        chat_images = gr.File(
                            label="Upload Images",
                            file_count="multiple",
                            type="filepath",
                            file_types=["image"]
                        )

                        clear_btn = gr.Button("Clear Chat", variant="secondary")

                    with gr.Column(scale=2):
                        chatbot = gr.Chatbot(label="Conversation", height=500)
                        msg_input = gr.Textbox(
                            label="Message",
                            placeholder="Ask a question about the images...",
                            lines=3
                        )
                        send_btn = gr.Button("Send", variant="primary")

                send_btn.click(
                    fn=app.chat_with_images,
                    inputs=[msg_input, chat_images, mode_selector, chatbot],
                    outputs=[chatbot, msg_input]
                )

                msg_input.submit(
                    fn=app.chat_with_images,
                    inputs=[msg_input, chat_images, mode_selector, chatbot],
                    outputs=[chatbot, msg_input]
                )

                clear_btn.click(
                    fn=app.clear_chat,
                    outputs=chatbot
                )

            # Screenshot to Code Tab
            with gr.Tab("🖼️ Screenshot to Code"):
                gr.Markdown("### Generate Code from Screenshots")

                with gr.Row():
                    with gr.Column():
                        code_images = gr.File(
                            label="Upload Screenshots",
                            file_count="multiple",
                            type="filepath",
                            file_types=["image"]
                        )

                        code_instructions = gr.Textbox(
                            label="Additional Instructions (Optional)",
                            placeholder="e.g., Make it responsive, add dark mode, use Tailwind CSS...",
                            lines=3
                        )

                        generate_btn = gr.Button("Generate Code", variant="primary", size="lg")

                    with gr.Column():
                        code_output = gr.Code(
                            label="Generated Code",
                            language="html",
                            lines=20
                        )

                generate_btn.click(
                    fn=app.generate_code_from_screenshot,
                    inputs=[code_images, code_instructions],
                    outputs=code_output
                )

            # Video Analysis Tab
            with gr.Tab("🎥 Video Analysis"):
                gr.Markdown("### Analyze Videos by Extracting Key Frames")

                with gr.Row():
                    with gr.Column():
                        video_input = gr.Video(
                            label="Upload Video",
                            sources=["upload"]
                        )

                        video_question = gr.Textbox(
                            label="Question",
                            placeholder="What would you like to know about this video?",
                            lines=3
                        )

                        num_frames = gr.Slider(
                            minimum=4,
                            maximum=16,
                            value=8,
                            step=1,
                            label="Number of Frames to Extract",
                            info="More frames = more detail but higher cost"
                        )

                        analyze_btn = gr.Button("Analyze Video", variant="primary", size="lg")

                    with gr.Column():
                        video_output = gr.Textbox(
                            label="Analysis Result",
                            lines=20
                        )

                analyze_btn.click(
                    fn=app.analyze_video,
                    inputs=[video_input, video_question, num_frames],
                    outputs=video_output
                )

        gr.Markdown("""
        ---
        ### 📝 Tips:
        - Configure your provider in the Configuration tab first
        - Use `.env` file for default settings
        - For local models, try Ollama with llava or similar vision models
        - Screenshot-to-code works best with clean, full-page designs
        - Video analysis extracts key frames - adjust the number based on video length
        """)

    return demo


if __name__ == "__main__":
    demo = create_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("APP_PORT", 7860)),
        share=False  # Set to True if you want a public link
    )
