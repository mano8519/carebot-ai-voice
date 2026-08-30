# CareBot AI Voice Backend

This small HTTPS service keeps the OpenAI API key off the CareBot tablet.

## Environment variable
Set:

OPENAI_API_KEY=your_key_here

## Run locally
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000

## App endpoint
After deployment, your CareBot app should use:

https://YOUR-SERVER/speak

The app sends:
{"text":"Good morning. I am CareBot."}

The server returns an MP3 generated with OpenAI `gpt-4o-mini-tts`.
