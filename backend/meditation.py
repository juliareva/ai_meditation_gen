from flask import Flask, Response, make_response, send_file, request, session
from flask_cors import CORS
from openai import OpenAI
from pydub import AudioSegment
from pymemcache.client import base
from TTS.api import TTS
import io
import random
import torch

app = Flask(__name__)
CORS(app)

# Configuration:
app.secret_key = ""
open_ai_key = ""
memcached_client = base.Client(("", 0))
origin = ""


@app.route("/text")
def provide_text():
    return Response(
        memcached_client.get("meditation_text"),
        headers={"Access-Control-Allow-Origin": origin},
    )


def get_random_topic():
    client = OpenAI(api_key=open_ai_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Limit reply to 3 words",
            },
            {
                "role": "user",
                "content": "Select three random words as a topic of meditation",
            },
        ],
    )
    return response.choices[0].message.content

def get_meditation_text(topic):
    client = OpenAI(api_key=open_ai_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Generate a 200 words meditation text for the topic",
            },
            {
                "role": "user",
                "content": topic,
            },
        ],
    )
    return response.choices[0].message.content


@app.route("/sound")
def provide_audio():
    topic_param = request.args.get("topic")
    voice_type_param = request.args.get("voice")
    music_param = request.args.get("music")

    # If it is a random meditation
    if topic_param == "":
        topic = get_random_topic()
        voice_type = random.choice(["female", "male"])
        music = random.choice(
            [
                "melodic",
                "nature",
                "ambient",
                "classical",
                "instrumental",
                "calm",
                "uplifting",
            ]
        )
    else:
        topic = topic_param
        music = music_param
        voice_type = voice_type_param

    
    if voice_type == "female":
        use_voice = "female_voice.wav"
    else:
        use_voice = "male_voice.wav"

    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")

    reply = get_meditation_text(topic)
    memcached_client.set("meditation_text", reply, expire=3600)
    tts.tts_to_file(
        text=reply,
        speaker_wav=use_voice,
        file_path="output.wav",
        language="en",
    )

    
    if music in ["nature", "ambient", "classical", "instrumental", "calm", "uplifting"]:
        song = music
    else:
        song = "melodic"

    sound_1 = AudioSegment.from_file("output.wav", format="wav")
    sound_2 = AudioSegment.from_file("music_meditation/" + song + ".mp3", format="mp3")
    sound_2_tuned = sound_2 - 5  # 5db less

    combined = sound_2_tuned.overlay(sound_1)
    path_to_file = "res.wav"
    file_handle = combined.export(path_to_file, format="wav")

    response = make_response(
        send_file(
            path_to_file,
            mimetype="audio/wav",
            as_attachment=True,
            download_name="result.wav",
        )
    )
    response.headers["Access-Control-Allow-Origin"] = origin
    return response
