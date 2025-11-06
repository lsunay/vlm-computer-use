"""
Preset prompts and templates for quick actions
"""

PRESET_PROMPTS = {
    "General Analysis": [
        {
            "name": "Describe Image",
            "prompt": "Describe this image in detail, including objects, people, colors, composition, and mood.",
            "icon": "📝"
        },
        {
            "name": "Extract All Text",
            "prompt": "Extract and transcribe ALL text visible in this image. Preserve formatting and structure.",
            "icon": "📄"
        },
        {
            "name": "Identify Objects",
            "prompt": "List all objects, items, and elements visible in this image with their approximate locations.",
            "icon": "🔍"
        },
        {
            "name": "Color Analysis",
            "prompt": "Analyze the color palette, dominant colors, color harmony, and overall color scheme of this image.",
            "icon": "🎨"
        }
    ],

    "Design & UI/UX": [
        {
            "name": "UI/UX Critique",
            "prompt": "Provide a comprehensive UI/UX critique of this design. Include: layout, visual hierarchy, typography, spacing, colors, accessibility, and usability. Suggest specific improvements.",
            "icon": "💎"
        },
        {
            "name": "Accessibility Check",
            "prompt": "Analyze this design for accessibility issues (WCAG compliance). Check: color contrast, font sizes, touch targets, alt text needs, keyboard navigation considerations.",
            "icon": "♿"
        },
        {
            "name": "Design System Analysis",
            "prompt": "Analyze this design and extract: color palette (hex codes), typography (fonts, sizes, weights), spacing system, component patterns, and design tokens.",
            "icon": "📐"
        },
        {
            "name": "Mobile Responsiveness",
            "prompt": "Evaluate how this design would translate to mobile. Identify: elements that need adaptation, breakpoint considerations, touch-friendly improvements.",
            "icon": "📱"
        },
        {
            "name": "Brand Consistency",
            "prompt": "Analyze this design for brand consistency. Evaluate: visual identity, tone, style adherence, and suggest improvements for brand alignment.",
            "icon": "🏷️"
        }
    ],

    "Code Generation": [
        {
            "name": "HTML/CSS Only",
            "prompt": "Generate clean, semantic HTML with embedded CSS. Use modern CSS (flexbox/grid). Make it responsive. Include comments.",
            "icon": "🌐"
        },
        {
            "name": "Tailwind CSS",
            "prompt": "Generate HTML using Tailwind CSS classes. Make it responsive with Tailwind breakpoints. Use Tailwind best practices.",
            "icon": "🎐"
        },
        {
            "name": "React Component",
            "prompt": "Generate a React functional component with hooks. Use modern React patterns. Include prop types. Make it reusable.",
            "icon": "⚛️"
        },
        {
            "name": "Vue Component",
            "prompt": "Generate a Vue 3 component using Composition API. Include proper script setup, template, and scoped styles.",
            "icon": "💚"
        },
        {
            "name": "Bootstrap",
            "prompt": "Generate HTML using Bootstrap 5 classes. Use Bootstrap grid system and components. Make it responsive.",
            "icon": "🅱️"
        },
        {
            "name": "With Dark Mode",
            "prompt": "Generate code with both light and dark mode support. Include CSS variables for theme switching. Make it pixel-perfect.",
            "icon": "🌓"
        }
    ],

    "Document Processing": [
        {
            "name": "Extract Table Data",
            "prompt": "Extract all table data from this image and format it as a markdown table. Preserve column headers and all rows.",
            "icon": "📊"
        },
        {
            "name": "Parse Form",
            "prompt": "Extract all form fields, labels, and values from this image. Structure the data as key-value pairs.",
            "icon": "📋"
        },
        {
            "name": "Receipt/Invoice",
            "prompt": "Extract structured data from this receipt/invoice: merchant name, date, items, prices, totals, tax, payment method.",
            "icon": "🧾"
        },
        {
            "name": "Business Card",
            "prompt": "Extract contact information from this business card: name, title, company, phone, email, address, website.",
            "icon": "💼"
        },
        {
            "name": "Screenshot Text",
            "prompt": "Extract all text from this screenshot, preserving structure and formatting. Include code snippets if present.",
            "icon": "🖥️"
        }
    ],

    "Development": [
        {
            "name": "Find Bugs",
            "prompt": "Analyze this screenshot for potential bugs, errors, or issues. Look for: UI glitches, alignment problems, broken elements, console errors, visual inconsistencies.",
            "icon": "🐛"
        },
        {
            "name": "Code Review",
            "prompt": "Review the code visible in this screenshot. Check for: code quality, best practices, potential bugs, security issues, performance concerns. Provide specific suggestions.",
            "icon": "👨‍💻"
        },
        {
            "name": "Architecture Analysis",
            "prompt": "Analyze this diagram/screenshot and explain the architecture, data flow, components, and interactions. Identify potential improvements.",
            "icon": "🏗️"
        },
        {
            "name": "Database Schema",
            "prompt": "Analyze this database diagram and extract: tables, columns, relationships, foreign keys, indexes. Suggest improvements.",
            "icon": "🗄️"
        }
    ],

    "Creative & Content": [
        {
            "name": "Generate Caption",
            "prompt": "Generate an engaging social media caption for this image. Include relevant hashtags and call-to-action.",
            "icon": "📸"
        },
        {
            "name": "Alt Text (SEO)",
            "prompt": "Generate SEO-optimized alt text for this image. Be descriptive but concise (125 characters max).",
            "icon": "🔤"
        },
        {
            "name": "Meme Template",
            "prompt": "Identify if this is a meme template. If yes, explain the format and suggest funny captions/text placements.",
            "icon": "😂"
        },
        {
            "name": "Story Ideas",
            "prompt": "Based on this image, generate 5 creative story ideas, blog post topics, or content angles for social media.",
            "icon": "💡"
        }
    ],

    "Education": [
        {
            "name": "Solve Math Problem",
            "prompt": "Solve this math problem step-by-step. Show all work and explain each step clearly.",
            "icon": "🔢"
        },
        {
            "name": "Explain Diagram",
            "prompt": "Explain this diagram in detail. Break down each component, show relationships, and describe the process or concept.",
            "icon": "📚"
        },
        {
            "name": "Study Guide",
            "prompt": "Create a study guide from this image. Extract key concepts, create definitions, and generate practice questions.",
            "icon": "📖"
        },
        {
            "name": "Translate Text",
            "prompt": "Extract all text from this image and translate it to English. Preserve formatting and context.",
            "icon": "🌍"
        }
    ],

    "Comparison": [
        {
            "name": "Compare Designs",
            "prompt": "Compare these images side-by-side. Analyze: differences, similarities, strengths/weaknesses of each, and recommend which is better and why.",
            "icon": "⚖️"
        },
        {
            "name": "Before/After",
            "prompt": "Analyze these before/after images. Identify all changes, improvements, and differences. Quantify changes where possible.",
            "icon": "🔄"
        },
        {
            "name": "A/B Test Analysis",
            "prompt": "Compare these A/B test variants. Evaluate: visual differences, expected performance, user experience, and predict which will perform better.",
            "icon": "📊"
        }
    ]
}


CODE_TEMPLATES = {
    "html": {
        "name": "HTML/CSS",
        "extension": "html",
        "template": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
        }}

        {styles}
    </style>
</head>
<body>
    {content}
</body>
</html>"""
    },
    "react": {
        "name": "React",
        "extension": "jsx",
        "template": """import React from 'react';

const {component_name} = () => {{
    return (
        {content}
    );
}};

export default {component_name};"""
    },
    "vue": {
        "name": "Vue 3",
        "extension": "vue",
        "template": """<script setup>
import {{ ref }} from 'vue';

{script_content}
</script>

<template>
    {content}
</template>

<style scoped>
{styles}
</style>"""
    },
    "tailwind": {
        "name": "Tailwind CSS",
        "extension": "html",
        "template": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    {content}
</body>
</html>"""
    }
}


SYSTEM_PROMPTS = {
    "code_generation": {
        "html": "You are an expert frontend developer specializing in semantic HTML and modern CSS. Generate clean, accessible, responsive code.",
        "react": "You are an expert React developer. Generate modern React components using functional components, hooks, and best practices.",
        "vue": "You are an expert Vue.js developer. Generate Vue 3 components using Composition API and modern patterns.",
        "tailwind": "You are an expert in Tailwind CSS. Generate responsive, well-structured HTML using Tailwind utility classes.",
        "bootstrap": "You are an expert in Bootstrap. Generate responsive layouts using Bootstrap 5 components and grid system."
    }
}


def get_presets_by_category(category=None):
    """Get preset prompts by category"""
    if category:
        return PRESET_PROMPTS.get(category, [])
    return PRESET_PROMPTS


def get_all_categories():
    """Get all preset categories"""
    return list(PRESET_PROMPTS.keys())


def get_code_template(framework):
    """Get code template for framework"""
    return CODE_TEMPLATES.get(framework, CODE_TEMPLATES["html"])
