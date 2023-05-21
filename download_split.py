from concurrent.futures import ProcessPoolExecutor
from pydub import AudioSegment
from pytube import YouTube
#import librosa

def split_audio(start, end, audio, output_filename):
    part = audio[start:end]
    part.export(output_filename, format="mp3")

"""def preprocessing(audio):
    y,sr = librosa.load("audio/audio.mp3", sr=44100)
    y_resampled = librosa.resample(y, sr, 22050)
    y_normalized = librosa.util.normalize(y_resampled)
    y_preemphasized = librosa.effects.preemphasis(y_normalized)
    librosa.output.write_mp3("audio/preprocessed_audio", y_preemphasized, sr=22050)"""


def run_split_audio(URL):
    audio_file = YouTube(URL).streams.filter(only_audio=True).first().download(filename="audio/audio.mp3")
    audio = AudioSegment.from_file("audio/audio.mp3")
    audio_length = len(audio)
    part_duration = audio_length // 5

    with ProcessPoolExecutor(max_workers=2) as executor:
        futures = []
        futures.append(executor.submit(split_audio, 0, part_duration, audio, "audio/part1.mp3"))
        futures.append(executor.submit(split_audio, part_duration, part_duration * 2, audio, "audio/part2.mp3"))
        futures.append(executor.submit(split_audio, part_duration * 2, part_duration * 3, audio, "audio/part3.mp3"))
        futures.append(executor.submit(split_audio, part_duration * 3, part_duration * 4, audio, "audio/part4.mp3"))
        futures.append(executor.submit(split_audio, part_duration * 4, audio_length, audio, "audio/part5.mp3"))

        for future in futures:
            future.result()