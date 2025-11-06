"""
Utility functions for the VLM demo app
"""

import os
import tempfile
from typing import List, Tuple
import cv2
from PIL import Image


def extract_frames_from_video(video_path: str, num_frames: int = 8) -> List[str]:
    """
    Extract evenly spaced frames from a video file

    Args:
        video_path: Path to the video file
        num_frames: Number of frames to extract

    Returns:
        List of paths to extracted frame images
    """
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames == 0:
        raise ValueError("Could not read video or video has no frames")

    # Calculate frame indices to extract
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


def resize_image(image_path: str, max_size: Tuple[int, int] = (1024, 1024)) -> str:
    """
    Resize image if it's too large, maintaining aspect ratio

    Args:
        image_path: Path to the image file
        max_size: Maximum width and height

    Returns:
        Path to resized image (or original if no resize needed)
    """
    img = Image.open(image_path)

    # Check if resize is needed
    if img.size[0] <= max_size[0] and img.size[1] <= max_size[1]:
        return image_path

    # Calculate new size maintaining aspect ratio
    img.thumbnail(max_size, Image.Resampling.LANCZOS)

    # Save to temporary file
    temp_dir = tempfile.mkdtemp()
    new_path = os.path.join(temp_dir, "resized_" + os.path.basename(image_path))
    img.save(new_path)

    return new_path


def validate_image(image_path: str) -> bool:
    """
    Validate if file is a valid image

    Args:
        image_path: Path to the image file

    Returns:
        True if valid image, False otherwise
    """
    try:
        img = Image.open(image_path)
        img.verify()
        return True
    except Exception:
        return False


def get_system_prompt(mode: str) -> str:
    """
    Get system prompt based on mode

    Args:
        mode: Operation mode (chat, code_generation, analysis)

    Returns:
        System prompt string
    """
    prompts = {
        "chat": "You are a helpful AI assistant with vision capabilities. You can analyze images, answer questions about visual content, and help with various tasks involving images and videos.",

        "code_generation": """You are an expert at converting visual designs into code. When given screenshots or designs:
1. Analyze the layout, components, and styling carefully
2. Generate clean, well-structured HTML/CSS code
3. Include modern CSS practices (flexbox, grid, etc.)
4. Make the design responsive when appropriate
5. Add comments explaining key sections
6. Ensure the code is production-ready

Provide complete, working code that can be directly used.""",

        "analysis": """You are an expert at analyzing images and visual content. Provide detailed, structured analysis covering:
1. Main elements and composition
2. Colors, style, and design patterns
3. Text content and its context
4. Any notable features or anomalies
5. Practical insights and interpretations

Be thorough, accurate, and insightful in your analysis.""",

        "thinking": """You are a thoughtful AI assistant with deep reasoning capabilities. When analyzing images or answering questions:
1. Think step-by-step through the problem
2. Consider multiple perspectives and interpretations
3. Explain your reasoning process
4. Validate your conclusions
5. Acknowledge uncertainties when present

Show your work and reasoning, not just the final answer."""
    }

    return prompts.get(mode, prompts["chat"])
