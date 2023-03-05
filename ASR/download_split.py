from concurrent.futures import ProcessPoolExecutor
import streamlit as st
from pydub import AudioSegment
from pytube import YouTube

bar = st.progress(0)
def split_audio(start, end, audio, output_filename):
    part = audio[start:end]
    part.export(output_filename, format="mp3")

def run_split_audio(URL):
    audio_file = YouTube(URL).streams.filter(only_audio=True).first().download(filename="audio/audio.mp3")
    audio = AudioSegment.from_file("audio/audio.mp3")
    print("En cours telechargement")
    bar.progress(25)
    audio_length = len(audio)
    part_duration = audio_length // 5
    bar.progress(50)

    with ProcessPoolExecutor(max_workers=2) as executor:
        futures = []
        futures.append(executor.submit(split_audio, 0, part_duration, audio, "audio/part1.mp3"))
        futures.append(executor.submit(split_audio, part_duration, part_duration * 2, audio, "audio/part2.mp3"))
        futures.append(executor.submit(split_audio, part_duration * 2, part_duration * 3, audio, "audio/part3.mp3"))
        futures.append(executor.submit(split_audio, part_duration * 3, part_duration * 4, audio, "audio/part4.mp3"))
        futures.append(executor.submit(split_audio, part_duration * 4, audio_length, audio, "audio/part5.mp3"))

        for future in futures:
            future.result()
        bar.progress(75)