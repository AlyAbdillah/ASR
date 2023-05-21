from concurrent.futures import ProcessPoolExecutor
import torch
import whisper

def load_model():
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    return whisper.load_model('base', device=DEVICE)

def transcribing(audio):
    whisper_model = load_model()
    language_whisper= "french"
    options = dict(language=language_whisper, beam_size=5, best_of=5)
    transcribe_options = dict(task="transcribe", **options)
    transcription = whisper_model.transcribe(audio, **transcribe_options,fp16=False)["text"]
    return transcription

def run(audio):
    whisper_model = load_model()
    audio_file = whisper.load_audio("audio/" + audio)
    language_whisper= "french"
    options = dict(language=language_whisper, beam_size=5, best_of=5)
    transcribe_options = dict(task="transcribe", **options)
    transcription = whisper_model.transcribe(audio_file, **transcribe_options,fp16=False)["text"]
    return transcription

def transcribe_audio(audio_files):
    transcriptions = []
    with ProcessPoolExecutor(max_workers=2) as executor:
        futures = []
        for audio_file in audio_files:
            futures.append(executor.submit(run, audio_file))
        for future in futures:
            transcriptions.append(future.result())
    executor.shutdown()
    return transcriptions