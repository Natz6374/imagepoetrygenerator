import google.generativeai as genai
import gradio as gr
from PIL import Image
from gtts import gTTS
import os

# Set up Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def suggest_theme(image):
    model = genai.GenerativeModel("gemini-1.5-flash")
    img = image.convert("RGB").resize((256, 256))
    prompt = "Suggest a poetic theme or idea that matches this image."
    response = model.generate_content([img, prompt])
    return response.text.strip()

def generate_poem_and_audio(image, prompt, language):
    if not language:
        return "Please select a language.", None

    model = genai.GenerativeModel("gemini-1.5-flash")
    img = image.convert("RGB").resize((256, 256))
    full_prompt = f"Generate a short poem in {language} based on this image and theme: {prompt}."
    response = model.generate_content([img, full_prompt])
    poem = response.text.strip()

    # Language-to-gTTS mapping
    gtts_lang_map = {
        "Hindi": "hi",
        "Tamil": "ta",
        "Telugu": "te",
        "Malayalam": "ml",
        "Kannada": "kn",
        "Marathi": "mr",
        "Bengali": "bn",
        "Urdu": "ur",
        "Gujarati": "gu",
        "Punjabi": "pa",
    }

    # Generate audio
    try:
        lang_code = gtts_lang_map.get(language, "en")
        tts = gTTS(text=poem, lang=lang_code)
        audio_path = "poem_audio.mp3"
        tts.save(audio_path)
    except Exception as e:
        audio_path = None

    return poem, audio_path

language_choices = [
    "Hindi", "Tamil", "Telugu", "Malayalam", "Kannada",
    "Marathi", "Bengali", "Urdu", "Gujarati", "Punjabi"
]

with gr.Blocks() as demo:
    gr.Markdown("# AI-Powered Multilingual Image Poetry Generator")
    gr.Markdown("Upload an image to generate poetic magic in your language. Optional: Let AI suggest a theme!")

    with gr.Row():
        image_input = gr.Image(type="pil", label="Upload Image")
        theme_output = gr.Textbox(label="AI-Suggested Theme", interactive=False)
        suggest_btn = gr.Button("Suggest Theme")

    theme_input = gr.Textbox(label="Or Enter Your Own Theme (in English)")
    language_input = gr.Dropdown(language_choices, label="Select Output Language")

    generate_btn = gr.Button("Generate Poem")
    poem_output = gr.Textbox(label="Generated Poem")
    audio_output = gr.Audio(label="Listen to the Poem", type="filepath")

    suggest_btn.click(fn=suggest_theme, inputs=image_input, outputs=theme_output)
    generate_btn.click(
        fn=generate_poem_and_audio,
        inputs=[image_input, theme_input, language_input],
        outputs=[poem_output, audio_output]
    )

if __name__ == "__main__":
    demo.launch()
