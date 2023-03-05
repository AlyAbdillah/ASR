import streamlit as st
from app import transcribe_audio
from download_split import run_split_audio,bar

st.
with st.sidebar.form(key='my_form'):
	URL = st.text_input('Enter URL of YouTube video:')
	submit_button = st.form_submit_button(label='Go')
audio_files = ["part1.mp3","part2.mp3","part3.mp3","part4.mp3","part5.mp3"]
if submit_button:
    run_split_audio(URL)
    transcriptions = transcribe_audio(audio_files)
    for i in range (len(transcriptions)):
        st.write(transcriptions[i])
    bar.progress(100)
st.audio()


