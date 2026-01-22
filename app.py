"""
Vision Language Model Demo Application - Complete Version
All 30+ features integrated
"""

import os
import json
import tempfile
import base64
import asyncio
import requests
import gradio as gr
from typing import List, Tuple, Optional
from dotenv import load_dotenv

# Import from app_v2
from app_v2 import VLMAppV2
from presets import get_presets_by_category, get_all_categories
from database import db

load_dotenv()


# ==================== WHISPER FUNCTIONS ====================


def get_whisper_models():
    """Get available Whisper models from .env"""
    models_str = os.getenv(
        "WHISPER_MODELS",
        "tiny.en,tiny,base.en,base,small.en,small,medium.en,medium,large-v1,large-v2,large-v3,large",
    )
    return models_str.split(",")


def get_whisper_languages():
    """Get available languages from .env"""
    langs_str = os.getenv(
        "WHISPER_LANGUAGES",
        "auto,english,spanish,french,german,chinese,turkish,arabic,russian,japanese,korean",
    )
    return langs_str.split(",")


def get_whisper_formats():
    """Get available output formats from .env"""
    formats_str = os.getenv("WHISPER_OUTPUT_FORMATS", "SRT,VTT,TXT,JSON,TSV,WebVTT,LRC")
    return formats_str.split(",")


async def transcribe_file_whisper(file_path, model, language, output_format):
    """Transcribe audio/video file using Whisper-WebUI API"""
    try:
        base_url = os.getenv("WHISPER_WEBUI_BASE_URL", "http://192.168.1.12:7860")

        # Prepare file for upload
        with open(file_path, "rb") as f:
            file_data = base64.b64encode(f.read()).decode()

        # Prepare API payload with all 54 parameters (matching Whisper-WebUI exactly)
        payload = {
            "data": [
                [
                    {
                        "path": f"data:video/mp4;base64,{file_data}",
                        "meta": {"_type": "gradio.FileData"},
                    }
                ],  # files
                "",  # input_folder_path
                False,  # include_subdirectory
                True,  # save_same_dir
                output_format,  # file_format
                False,  # add_timestamp
                model,  # progress (model)
                language,  # param_7 (language)
                False,  # param_8 (translate)
                5.0,  # param_9 (beam_size)
                -1.0,  # param_10 (log_prob_threshold)
                0.6,  # param_11 (no_speech_threshold)
                "float16",  # param_12 (compute_type)
                5.0,  # param_13 (best_of)
                1.0,  # param_14 (patience)
                True,  # param_15 (condition_on_previous_text)
                0.5,  # param_16 (prompt_reset_on_temperature)
                "Hello!!",  # param_17 (initial_prompt)
                0.0,  # param_18 (temperature)
                2.4,  # param_19 (compression_ratio_threshold)
                1.0,  # param_20 (length_penalty)
                1.0,  # param_21 (repetition_penalty)
                0.0,  # param_22 (no_repeat_ngram_size)
                "Hello!!",  # param_23 (prefix)
                True,  # param_24 (suppress_blank)
                "[-1]",  # param_25 (suppress_tokens)
                1.0,  # param_26 (max_initial_timestamp)
                False,  # param_27 (word_timestamps)
                "'\"¿([{-",  # param_28 (prepend_punctuations)
                "'.。,，!！?？:：\"])},、",  # param_29 (append_punctuations)
                3.0,  # param_30 (max_new_tokens)
                30.0,  # param_31 (chunk_length)
                3.0,  # param_32 (hallucination_silence_threshold)
                "Hello!!",  # param_33 (hotwords)
                0.5,  # param_34 (language_detection_threshold)
                1.0,  # param_35 (language_detection_segments)
                24.0,  # param_36 (batch_size)
                True,  # param_37 (offload_submodel)
                True,  # param_38 (enable_silero_vad)
                0.5,  # param_39 (speech_threshold)
                250.0,  # param_40 (min_speech_duration)
                9999.0,  # param_41 (max_speech_duration)
                1000.0,  # param_42 (min_silence_duration)
                2000.0,  # param_43 (speech_padding)
                False,  # param_44 (enable_diarization)
                "cpu",  # param_45 (device)
                "",  # param_46 (huggingface_token)
                True,  # param_47 (offload_submodel_2)
                False,  # param_48 (enable_bgm_remover)
                "UVR-MDX-NET-Inst_HQ_4",  # param_49 (bgm_model)
                "cpu",  # param_50 (bgm_device)
                256.0,  # param_51 (segment_size)
                False,  # param_52 (save_separated_files)
                True,  # param_53 (offload_submodel_3)
            ]
        }

        # Make API call
        url = f"{base_url}/gradio_api/call/transcribe_file"
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()

        event_id = response.json()["event_id"]

        # Poll for results
        result_url = f"{url}/{event_id}"
        max_attempts = 60  # 5 minutes max
        attempt = 0

        while attempt < max_attempts:
            result_response = requests.get(result_url, timeout=10)

            if result_response.json().get("status") == "complete":
                transcription_text = result_response.json()["data"][0]
                # For now, return transcription text and None for download file
                # In future, we could save to a file and return the path
                return transcription_text, None

            await asyncio.sleep(5)
            attempt += 1

        error_msg = "❌ Transcription timed out after 5 minutes"
        return error_msg, None

    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        return error_msg, None


async def transcribe_youtube_whisper(youtube_url, model, language, output_format):
    """Transcribe YouTube video using Whisper-WebUI API"""
    try:
        base_url = os.getenv("WHISPER_WEBUI_BASE_URL", "http://192.168.1.12:7860")

        # For YouTube, we need to use a different endpoint or prepare URL
        payload = {
            "data": [
                youtube_url,  # YouTube URL
                output_format,  # output_format
                True,  # srt_timestamps
                # ... similar parameters as file transcription
            ]
        }

        # Note: YouTube transcription would need separate implementation
        # For now, return a placeholder
        placeholder_msg = "🎵 YouTube transcription feature coming soon!"
        return placeholder_msg, None

    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        return error_msg, None


async def record_and_transcribe_whisper(model, language, output_format):
    """Record audio and transcribe using Whisper-WebUI API"""
    try:
        base_url = os.getenv("WHISPER_WEBUI_BASE_URL", "http://192.168.1.12:7860")

        # For microphone recording, we'd need to handle audio upload
        # This is a placeholder for the recording functionality
        placeholder_msg = "🎤 Audio recording and transcription feature coming soon!"
        return placeholder_msg, None

    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        return error_msg, None


def create_comprehensive_ui():
    """Create comprehensive Gradio UI with all features"""
    app = VLMAppV2()

    # Custom CSS for better UI
    custom_css = """
    .gradio-container {
        font-family: 'Inter', sans-serif;
    }
    .gr-button-primary {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border: none;
    }
    .cost-display {
        background: #f0f9ff;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    """

    with gr.Blocks(title="VLM Demo - Complete Edition") as demo:
        gr.Markdown("""
        # 🎨 Vision Language Model Demo - Complete Edition
        ### 30+ Features | Multi-Provider | Privacy-First | Production-Ready

        Advanced VLM application with chat, code generation, batch processing, OCR, analytics, and more.
        """)

        # State variables
        current_provider = gr.State("")
        current_model = gr.State("")

        with gr.Tabs() as main_tabs:
            # ==================== CONFIGURATION TAB ====================
            with gr.Tab("⚙️ Configuration"):
                gr.Markdown("### Configure Your VLM Provider")

                with gr.Row():
                    with gr.Column(scale=1):
                        provider_select = gr.Dropdown(
                            choices=["openai", "anthropic", "ollama", "custom"],
                            value=os.getenv("DEFAULT_PROVIDER", "openai"),
                            label="Provider",
                            info="Select your LLM provider",
                        )

                        api_key_input = gr.Textbox(
                            label="API Key",
                            type="password",
                            placeholder="Leave empty to use .env",
                            info="Your API key (optional for Ollama)",
                        )

                        base_url_input = gr.Textbox(
                            label="Base URL (Optional)",
                            placeholder="e.g., http://localhost:11434/v1",
                            info="Custom endpoint URL",
                        )

                        model_input = gr.Textbox(
                            label="Model Name (Optional)",
                            placeholder="e.g., gpt-4o, claude-3-5-sonnet-20241022",
                            info="Leave empty for defaults",
                        )

                        init_btn = gr.Button(
                            "🚀 Initialize Provider", variant="primary", size="lg"
                        )

                    with gr.Column(scale=1):
                        status_box = gr.Textbox(
                            label="Status", interactive=False, lines=3
                        )

                        gr.Markdown("""
                        ### Quick Start Examples

                        **Ollama (Free & Local):**
                        - Provider: `ollama`
                        - Model: `llava:latest`
                        - No API key needed

                        **OpenAI:**
                        - Provider: `openai`
                        - Model: `gpt-4o`
                        - Add API key

                        **Anthropic:**
                        - Provider: `anthropic`
                        - Model: `claude-3-5-sonnet-20241022`
                        - Add API key
                        """)

                init_btn.click(
                    fn=app.initialize_provider,
                    inputs=[
                        provider_select,
                        api_key_input,
                        base_url_input,
                        model_input,
                    ],
                    outputs=status_box,
                )

            # ==================== CHAT TAB ====================
            with gr.Tab("💬 Chat with Images"):
                gr.Markdown("### Multi-Image Chat with History & Export")

                with gr.Row():
                    with gr.Column(scale=1):
                        chat_mode = gr.Radio(
                            choices=["chat", "analysis", "thinking"],
                            value="chat",
                            label="Conversation Mode",
                        )

                        chat_images = gr.File(
                            label="Upload Images",
                            file_count="multiple",
                            type="filepath",
                            file_types=["image"],
                        )

                        save_chat_db = gr.Checkbox(label="Save to History", value=True)

                        with gr.Row():
                            clear_btn = gr.Button("🗑️ Clear", variant="secondary")
                            export_btn = gr.Button("📥 Export", variant="secondary")

                        export_format = gr.Dropdown(
                            choices=["markdown", "json", "pdf"],
                            value="markdown",
                            label="Export Format",
                        )

                        export_file = gr.File(label="Download Export")

                    with gr.Column(scale=2):
                        chatbot = gr.Chatbot(label="Conversation", height=500)
                        cost_display = gr.Textbox(
                            label="💰 Cost Tracking", interactive=False
                        )
                        msg_input = gr.Textbox(
                            label="Message",
                            placeholder="Ask about the images...",
                            lines=3,
                        )
                        with gr.Row():
                            send_btn = gr.Button("📤 Send", variant="primary", scale=3)
                            preset_btn = gr.Button(
                                "⚡ Use Preset", variant="secondary", scale=1
                            )

                # Preset prompts panel
                with gr.Accordion("⚡ Preset Prompts", open=False):
                    preset_category = gr.Dropdown(
                        choices=get_all_categories(),
                        value="General Analysis",
                        label="Category",
                    )
                    preset_buttons = gr.Radio(choices=[], label="Quick Actions")

                    def update_presets(category):
                        presets = get_presets_by_category(category)
                        return gr.Radio(
                            choices=[f"{p['icon']} {p['name']}" for p in presets]
                        )

                    preset_category.change(
                        fn=update_presets,
                        inputs=preset_category,
                        outputs=preset_buttons,
                    )

                # Event handlers
                send_btn.click(
                    fn=app.chat_with_images,
                    inputs=[msg_input, chat_images, chat_mode, chatbot, save_chat_db],
                    outputs=[chatbot, msg_input, cost_display],
                )

                msg_input.submit(
                    fn=app.chat_with_images,
                    inputs=[msg_input, chat_images, chat_mode, chatbot, save_chat_db],
                    outputs=[chatbot, msg_input, cost_display],
                )

                clear_btn.click(fn=app.clear_chat, outputs=[chatbot, cost_display])

                export_btn.click(
                    fn=app.export_chat_history,
                    inputs=export_format,
                    outputs=export_file,
                )

            # ==================== CODE GENERATION TAB ====================
            with gr.Tab("🖼️ Screenshot to Code"):
                gr.Markdown("### Generate Code from Screenshots with Live Preview")

                with gr.Row():
                    with gr.Column(scale=1):
                        code_images = gr.File(
                            label="Upload Screenshots",
                            file_count="multiple",
                            type="filepath",
                            file_types=["image"],
                        )

                        code_framework = gr.Dropdown(
                            choices=["html", "react", "vue", "tailwind", "bootstrap"],
                            value="html",
                            label="Framework",
                        )

                        code_instructions = gr.Textbox(
                            label="Additional Instructions",
                            placeholder="e.g., Add dark mode, make it responsive...",
                            lines=3,
                        )

                        with gr.Row():
                            generate_code_btn = gr.Button(
                                "✨ Generate Code", variant="primary"
                            )
                            save_code_db = gr.Checkbox(
                                label="Save to Database", value=True
                            )

                        code_status = gr.Textbox(label="Status", interactive=False)

                    with gr.Column(scale=1):
                        code_output = gr.Code(
                            label="Generated Code", language="html", lines=20
                        )

                        with gr.Row():
                            copy_code_btn = gr.Button("📋 Copy", variant="secondary")
                            download_code_btn = gr.Button(
                                "💾 Download", variant="secondary"
                            )

                        code_file = gr.File(label="Download Code")

                # Code refinement section
                with gr.Accordion("🔧 Refine Code", open=False):
                    refinement_request = gr.Textbox(
                        label="Refinement Request",
                        placeholder="e.g., Add animations, improve accessibility, fix alignment...",
                        lines=2,
                    )
                    refine_btn = gr.Button("♻️ Refine Code", variant="primary")

                    refine_btn.click(
                        fn=app.refine_code,
                        inputs=[code_output, refinement_request, code_framework],
                        outputs=[code_output, code_status],
                    )

                # Live preview section
                with gr.Accordion("👁️ Live Preview", open=False):
                    preview_html = gr.HTML(label="Preview")

                    def update_preview(code):
                        if code and "<!DOCTYPE html>" in code:
                            return code
                        return "<p>Generate code to see preview</p>"

                    code_output.change(
                        fn=update_preview, inputs=code_output, outputs=preview_html
                    )

                generate_code_btn.click(
                    fn=app.generate_code_from_screenshot,
                    inputs=[
                        code_images,
                        code_framework,
                        code_instructions,
                        save_code_db,
                    ],
                    outputs=[code_output, code_status],
                )

            # ==================== BATCH PROCESSING TAB ====================
            with gr.Tab("📦 Batch Processing"):
                gr.Markdown("### Process Multiple Images at Once")

                with gr.Row():
                    with gr.Column():
                        batch_images = gr.File(
                            label="Upload Multiple Images",
                            file_count="multiple",
                            type="filepath",
                            file_types=["image"],
                        )

                        batch_prompt = gr.Textbox(
                            label="Prompt for All Images",
                            placeholder="This prompt will be applied to each image...",
                            lines=3,
                        )

                        batch_export_format = gr.Dropdown(
                            choices=["csv", "json", "txt"],
                            value="csv",
                            label="Export Format",
                        )

                        batch_process_btn = gr.Button(
                            "⚡ Process Batch", variant="primary", size="lg"
                        )

                    with gr.Column():
                        batch_status = gr.Textbox(
                            label="Status", interactive=False, lines=3
                        )
                        batch_results = gr.File(label="Download Results")

                        gr.Markdown("""
                        ### Use Cases:
                        - Analyze multiple product images
                        - Extract text from documents
                        - Generate descriptions for image library
                        - Classify or categorize images
                        - Quality control checks
                        """)

                batch_process_btn.click(
                    fn=app.batch_process_images,
                    inputs=[batch_images, batch_prompt, batch_export_format],
                    outputs=[batch_results, batch_status],
                )

            # ==================== IMAGE COMPARISON TAB ====================
            with gr.Tab("⚖️ Image Comparison"):
                gr.Markdown("### Compare Multiple Images Side-by-Side")

                with gr.Row():
                    with gr.Column():
                        comparison_images = gr.File(
                            label="Upload 2+ Images to Compare",
                            file_count="multiple",
                            type="filepath",
                            file_types=["image"],
                        )

                        comparison_prompt = gr.Textbox(
                            label="Comparison Prompt (Optional)",
                            placeholder="Leave empty for default comparison...",
                            lines=3,
                            value="Compare these images in detail. Analyze differences, similarities, and which is better for what purpose.",
                        )

                        compare_btn = gr.Button(
                            "🔍 Compare", variant="primary", size="lg"
                        )

                    with gr.Column():
                        comparison_result = gr.Textbox(
                            label="Comparison Analysis", lines=20
                        )

                compare_btn.click(
                    fn=app.compare_images,
                    inputs=[comparison_images, comparison_prompt],
                    outputs=comparison_result,
                )

            # ==================== OCR & DOCUMENTS TAB ====================
            with gr.Tab("📄 OCR & Documents"):
                gr.Markdown("### Extract Text and Tables from Images")

                with gr.Tabs():
                    with gr.Tab("Text Extraction"):
                        with gr.Row():
                            with gr.Column():
                                ocr_image = gr.Image(
                                    label="Upload Image", type="filepath"
                                )
                                ocr_lang = gr.Dropdown(
                                    choices=["eng", "spa", "fra", "deu", "chi_sim"],
                                    value="eng",
                                    label="Language",
                                )
                                extract_text_btn = gr.Button(
                                    "📝 Extract Text", variant="primary"
                                )

                            with gr.Column():
                                extracted_text = gr.Textbox(
                                    label="Extracted Text", lines=15
                                )

                        extract_text_btn.click(
                            fn=app.extract_text_ocr,
                            inputs=[ocr_image, ocr_lang],
                            outputs=extracted_text,
                        )

                    with gr.Tab("Table Extraction"):
                        with gr.Row():
                            with gr.Column():
                                table_image = gr.Image(
                                    label="Upload Table Image", type="filepath"
                                )
                                extract_table_btn = gr.Button(
                                    "📊 Extract Table", variant="primary"
                                )

                            with gr.Column():
                                table_output = gr.Dataframe(label="Extracted Table")
                                table_status = gr.Textbox(
                                    label="Status", interactive=False
                                )

                        extract_table_btn.click(
                            fn=app.extract_table,
                            inputs=table_image,
                            outputs=[table_output, table_status],
                        )

            # ==================== VIDEO ANALYSIS TAB ====================
            with gr.Tab("🎥 Video Analysis"):
                gr.Markdown("### Analyze Videos by Extracting Key Frames")

                with gr.Row():
                    with gr.Column():
                        video_input = gr.Video(label="Upload Video")

                        video_question = gr.Textbox(
                            label="Question",
                            placeholder="What would you like to know about this video?",
                            lines=3,
                        )

                        num_frames_slider = gr.Slider(
                            minimum=4,
                            maximum=16,
                            value=8,
                            step=1,
                            label="Frames to Extract",
                        )

                        analyze_video_btn = gr.Button(
                            "🎬 Analyze Video", variant="primary", size="lg"
                        )

                    with gr.Column():
                        video_analysis = gr.Textbox(label="Analysis", lines=20)

                analyze_video_btn.click(
                    fn=app.analyze_video,
                    inputs=[video_input, video_question, num_frames_slider],
                    outputs=video_analysis,
                )

            # ==================== WHISPER FILE TRANSCRIPTION TAB ====================
            with gr.Tab("🎵 Whisper"):
                gr.Markdown("### Transcribe Audio/Video Files with Whisper")

                with gr.Row():
                    with gr.Column():
                        whisper_file_input = gr.File(
                            label="Upload Audio/Video File",
                            file_types=[
                                ".mp3",
                                ".wav",
                                ".m4a",
                                ".mp4",
                                ".avi",
                                ".mov",
                                ".flac",
                            ],
                        )

                        whisper_model_select = gr.Dropdown(
                            choices=get_whisper_models(),
                            value="tiny.en",
                            label="Model",
                            info="Select Whisper model (larger = better quality, slower)",
                        )

                        whisper_lang_select = gr.Dropdown(
                            choices=get_whisper_languages(),
                            value="auto",
                            label="Language",
                            info="Select language or 'auto' for automatic detection",
                        )

                        whisper_format_select = gr.Dropdown(
                            choices=get_whisper_formats(),
                            value="SRT",
                            label="Output Format",
                            info="Select subtitle/transcription format",
                        )

                        transcribe_file_btn = gr.Button(
                            "🎵 Transcribe File", variant="primary", size="lg"
                        )

                    with gr.Column():
                        whisper_file_output = gr.Textbox(
                            label="Transcription Result", lines=20
                        )

                        whisper_file_download = gr.File(
                            label="Download Result", interactive=False
                        )

                transcribe_file_btn.click(
                    fn=transcribe_file_whisper,
                    inputs=[
                        whisper_file_input,
                        whisper_model_select,
                        whisper_lang_select,
                        whisper_format_select,
                    ],
                    outputs=[whisper_file_output, whisper_file_download],
                )

            # ==================== WHISPER YOUTUBE TAB ====================
            with gr.Tab("📺 YouTube"):
                gr.Markdown("### Transcribe YouTube Videos with Whisper")

                with gr.Row():
                    with gr.Column():
                        youtube_url_input = gr.Textbox(
                            label="YouTube URL",
                            placeholder="https://www.youtube.com/watch?v=...",
                            info="Paste YouTube video URL here",
                        )

                        youtube_thumbnail = gr.Image(
                            label="Video Thumbnail", visible=False
                        )

                        youtube_model_select = gr.Dropdown(
                            choices=get_whisper_models(), value="tiny.en", label="Model"
                        )

                        youtube_lang_select = gr.Dropdown(
                            choices=get_whisper_languages(),
                            value="auto",
                            label="Language",
                        )

                        youtube_format_select = gr.Dropdown(
                            choices=get_whisper_formats(),
                            value="SRT",
                            label="Output Format",
                        )

                        transcribe_youtube_btn = gr.Button(
                            "📺 Transcribe YouTube", variant="primary", size="lg"
                        )

                    with gr.Column():
                        youtube_output = gr.Textbox(
                            label="Transcription Result", lines=20
                        )

                        youtube_download = gr.File(
                            label="Download Result", interactive=False
                        )

                # Show thumbnail when URL is entered
                youtube_url_input.change(
                    fn=lambda url: gr.Image(visible=bool(url)),
                    inputs=youtube_url_input,
                    outputs=youtube_thumbnail,
                )

                transcribe_youtube_btn.click(
                    fn=transcribe_youtube_whisper,
                    inputs=[
                        youtube_url_input,
                        youtube_model_select,
                        youtube_lang_select,
                        youtube_format_select,
                    ],
                    outputs=[youtube_output, youtube_download],
                )

            # ==================== WHISPER RECORD TAB ====================
            with gr.Tab("🎤 Record"):
                gr.Markdown("### Record and Transcribe Audio with Whisper")

                with gr.Row():
                    with gr.Column():
                        record_audio = gr.Audio(
                            label="Record Audio",
                            sources=["microphone"],
                            type="filepath",
                            interactive=True,
                        )

                        record_model_select = gr.Dropdown(
                            choices=get_whisper_models(), value="tiny.en", label="Model"
                        )

                        record_lang_select = gr.Dropdown(
                            choices=get_whisper_languages(),
                            value="auto",
                            label="Language",
                        )

                        record_format_select = gr.Dropdown(
                            choices=get_whisper_formats(),
                            value="TXT",
                            label="Output Format",
                        )

                        record_btn = gr.Button(
                            "🎤 Record & Transcribe", variant="primary", size="lg"
                        )

                    with gr.Column():
                        record_output = gr.Textbox(
                            label="Transcription Result", lines=20
                        )

                        record_download = gr.File(
                            label="Download Result", interactive=False
                        )

                record_btn.click(
                    fn=record_and_transcribe_whisper,
                    inputs=[
                        record_model_select,
                        record_lang_select,
                        record_format_select,
                    ],
                    outputs=[record_output, record_download],
                )

            # ==================== ANALYTICS TAB ====================
            with gr.Tab("📊 Analytics & Usage"):
                gr.Markdown("### Track Your API Usage and Costs")

                with gr.Row():
                    with gr.Column():
                        stats_days = gr.Slider(
                            minimum=1,
                            maximum=90,
                            value=30,
                            step=1,
                            label="Days to Analyze",
                        )

                        refresh_stats_btn = gr.Button(
                            "🔄 Refresh Stats", variant="primary"
                        )

                    with gr.Column():
                        stats_output = gr.Textbox(label="Usage Statistics", lines=15)

                refresh_stats_btn.click(
                    fn=app.get_usage_stats, inputs=stats_days, outputs=stats_output
                )

                # Session history
                with gr.Accordion("💾 Chat History", open=False):
                    gr.Markdown("View and load previous chat sessions")

                    def list_sessions():
                        sessions = db.list_chat_sessions(limit=50)
                        return [
                            [s["id"], s["title"], s["created_at"], s["message_count"]]
                            for s in sessions
                        ]

                    history_table = gr.Dataframe(
                        headers=["ID", "Title", "Created", "Messages"],
                        label="Chat Sessions",
                    )

                    with gr.Row():
                        load_session_id = gr.Number(label="Session ID", precision=0)
                        load_session_btn = gr.Button("📂 Load Session")

                    load_session_btn.click(
                        fn=app.load_chat_session,
                        inputs=load_session_id,
                        outputs=[chatbot, status_box],
                    )

            # ==================== HELP & DOCS TAB ====================
            with gr.Tab("❓ Help & Documentation"):
                gr.Markdown("""
                # 📚 VLM Demo - Complete Edition Guide

                ## Features Overview

                ### 💬 Chat with Images
                - Multi-image conversations
                - Multiple modes (Chat, Analysis, Thinking)
                - History saved automatically
                - Export to Markdown, JSON, or PDF
                - Cost tracking per conversation

                ### 🖼️ Screenshot to Code
                - Generate code from design screenshots
                - Support for HTML, React, Vue, Tailwind, Bootstrap
                - Live preview of generated code
                - Iterative refinement
                - Download generated code

                ### 📦 Batch Processing
                - Process multiple images at once
                - Export results to CSV, JSON, or TXT
                - Perfect for large-scale analysis
                - Bulk image description, classification, or OCR

                ### ⚖️ Image Comparison
                - Compare 2+ images side-by-side
                - Detailed analysis of differences
                - A/B testing evaluations
                - Technical similarity scores

                ### 📄 OCR & Documents
                - Extract text from images (multiple languages)
                - Table extraction to structured data
                - Receipt/invoice processing
                - Form data extraction

                ### 🎥 Video Analysis
                - Analyze videos by extracting key frames
                - Adjustable frame count
                - Scene understanding
                - Temporal analysis

                ### 📊 Analytics
                - Track API usage and costs
                - View usage statistics
                - Load previous conversations
                - Export analytics data

                ## Quick Start

                1. **Configure Provider**: Go to Configuration tab
                2. **Initialize**: Select provider and click Initialize
                3. **Start Using**: Try any feature tab!

                ## Tips & Tricks

                - Use **Ollama** for free, local processing
                - Save conversations for future reference
                - Use presets for common tasks
                - Batch process for efficiency
                - Export results for documentation

                ## Cost Optimization

                - Use smaller models for simple tasks
                - Reduce video frame count when appropriate
                - Use Ollama for development/testing
                - Monitor costs in Analytics tab

                ## Support

                - Check README.md for detailed docs
                - See QUICKSTART.md for setup help
                - GitHub: [Report Issues](https://github.com)

                ---

                **Version:** 2.0 Complete | **Features:** 30+ | **Providers:** 4+
                """)

        gr.Markdown("""
        ---
        ### 🚀 Made with ❤️ for the open source community
        Supports: OpenAI • Anthropic • Ollama • Custom APIs
        """)

    return demo


if __name__ == "__main__":
    demo = create_comprehensive_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=8080,  # Use a different port inside container
        share=False,
        show_error=True,
    )
