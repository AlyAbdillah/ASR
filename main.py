import streamlit as st
from app import transcribe_audio, transcribing
from download_split import run_split_audio

st.title("Application de transcription")
audio_file = st.file_uploader("Upload Audio",type=["wav","mp3","m4a","mp4"])
if audio_file is None:
    st.warning("En attente de l'audio.")
URL = st.text_input('Entrer le URL YouTube video:')
if URL == '':
    st.warning("En attente de l'URL.")

with st.expander('Example URL'):
	st.code('https://www.youtube.com/watch?v=twG4mr6Jov0')
audio_files = ["part1.mp3","part2.mp3","part3.mp3","part4.mp3","part5.mp3"]

if st.sidebar.button("Transcrire"):
    if audio_file is not None and URL=='':
        st.sidebar.success("Transcription Audio")
        transcriptions = transcribing("audio/"+audio_file.name)
        st.markdown(transcriptions)
        st.sidebar.success("Transcription Terminée")
    elif audio_file is None and URL is not None:
        st.sidebar.success("Téléchargement Audio")
        run_split_audio(URL)
        st.sidebar.success("Téléchargement Terminée")
        st.sidebar.success("Transcription Audio")
        transcriptions = transcribe_audio(audio_files)
        for i in range(len(transcriptions)):
            st.markdown(transcriptions[i])
        st.sidebar.success("Transcription Terminée")
    elif audio_file is not None and URL!='':
        st.sidebar.error("Operation impossible")
    elif audio_file is None and URL=='':
        st.sidebar.error("Ajouter un ficher ou un lien")

st.sidebar.header("Audio original")
if audio_file is not None:
    st.sidebar.audio(audio_file)
elif audio_file is None:
    st.sidebar.audio("audio/audio.mp3")





