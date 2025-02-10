import os
from datetime import datetime, timedelta
from pathlib import Path
from config import AUDIO_FILES_DIR

# Utility function that cleans up old audio files
async def cleanup_audio_files():
    for file_name in os.listdir(AUDIO_FILES_DIR):
        file_path = os.path.join(AUDIO_FILES_DIR, file_name)
        creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
        if datetime.now() - creation_time > timedelta(days=1):
            os.remove(file_path)

def md_to_whatsapp_md(text):
    """
    Converts standard Markdown text to WhatsApp Markdown format.
    :param text: str - The Markdown text to convert.
    :return: str - The text converted to WhatsApp Markdown format.
    """
    # Convert bold (Standard Markdown can use ** or __)
    text = text.replace('**', '*').replace('__', '*')
    # Wrap lines starting with ### or #### in asterisks for bold in WhatsApp
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('###') or line.startswith('####'):
            lines[i] = '*' + line.strip('# ').strip() + '*'
    converted_text = '\n'.join(lines)
    return converted_text
