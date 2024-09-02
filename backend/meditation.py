from flask import Flask, Response, make_response, send_file, request, session, stream_with_context, abort
from flask_cors import CORS
from openai import OpenAI
from pydub import AudioSegment
from pymemcache.client import base
from TTS.api import TTS
import io
import random
import torch
from werkzeug.wsgi import FileWrapper
import hashlib

app = Flask(__name__)
CORS(app)

# Configuration:
app.secret_key = ""
open_ai_key = ""
memcached_client = base.Client(("localhost", 11211))
origin = "http://localhost:8000"
enable_rate_limiting = False


# push context manually to app
with app.app_context():
    memcached_client.flush_all()
    print("Memcached cleared at startup.")


def calculate_file_hash(file_path, hash_algorithm="sha256"):
    # Initialize the hash algorithm
    hash_func = hashlib.new(hash_algorithm)

    # Open the file in binary mode and read in chunks
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)

    # Return the hexadecimal digest of the hash
    return hash_func.hexdigest()

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
    ip_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    lock_by_ip = 'lock_{}'.format(ip_addr)
    current_lock = memcached_client.get(lock_by_ip)

    if current_lock is not None and current_lock.decode('utf-8') == "1" and enable_rate_limiting:
        abort(429, description="Too many requests - try again later.")

    memcached_client.set(lock_by_ip, "1", expire=90)

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
        use_voice = "voices/female_voice.wav"
    else:
        use_voice = "voices/male_voice.wav"

    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")

    reply = get_meditation_text(topic)
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
    slowdown_factor = 0.9
    new_frame_rate = int(sound_1.frame_rate * slowdown_factor)
    slowed_down_audio = sound_1._spawn(sound_1.raw_data, overrides={'frame_rate': new_frame_rate})
    slowed_down_audio = slowed_down_audio.set_frame_rate(sound_1.frame_rate)

    sound_2 = AudioSegment.from_file("music/" + song + ".mp3", format="mp3")
    sound_2_tuned = sound_2 - 5  # 5db less

    combined = sound_2_tuned.overlay(slowed_down_audio)
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

    file_hash = calculate_file_hash(path_to_file, "sha256")
    memcached_client.set(file_hash, reply, expire=3600)
    memcached_client.set("meditation_text", reply, expire=3600)
    memcached_client.set(lock_by_ip, "0", expire=90)

    return response
