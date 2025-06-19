import os
import subprocess
from tqdm import tqdm
import wave
import whisper
import numpy as np

def convert_video_to_audio(video_path, audio_path):
    command = ['ffmpeg', '-i', video_path, audio_path]
    subprocess.run(command, check=True)

def transcribe_audio(audio_path, model_name='large', segment_duration=30, language='pt', task='transcribe'):
    model = whisper.load_model(model_name)
    with wave.open(audio_path, 'rb') as wf:
        framerate = wf.getframerate()
        nframes = wf.getnframes()
        duration = nframes / float(framerate)
    segments = int(np.ceil(duration / segment_duration))
    texts = []
    for i in tqdm(range(segments), desc="Transcrevendo áudio"):
        start = i * segment_duration
        end = min((i + 1) * segment_duration, duration)
        segment_path = f"segment_{i}.wav"
        command = [
            'ffmpeg', '-y', '-i', audio_path, '-ss', str(start), '-to', str(end), '-ar', '16000', '-ac', '1', segment_path
        ]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        result = model.transcribe(segment_path, language=language, task=task, fp16=False)
        texts.append(result['text'])
        os.remove(segment_path)
    return '\n'.join(texts)


def main():
    input_path = './input'
    opcoes = os.listdir(input_path)

    if not opcoes:
        print("No video files found in the input directory.")
        return

    print("Select a video file to transcribe:")
    for i, option in enumerate(opcoes):
        print(f"{i + 1}: {option}")
    choice = int(input("Enter the number of your choice: ")) - 1
    if choice < 0 or choice >= len(opcoes):
        print("Invalid choice.")
        return
    video_file = opcoes[choice]
    video_path = os.path.join(input_path, video_file)

    audio_path = 'audio.wav'
    transcription_path = 'transcription.txt'

    if os.path.exists(audio_path):
        time = os.path.getmtime(audio_path)
        os.rename(audio_path, f'audio_{time}.wav')

    if os.path.exists(transcription_path):
        time = os.path.getmtime(transcription_path)
        os.rename(transcription_path, f'transcription_{time}.txt')

    convert_video_to_audio(video_path, audio_path)

    transcription = transcribe_audio(audio_path)

    with open(transcription_path, 'w', encoding='utf-8') as f:
        f.write(transcription)

    print(f'Transcription saved to {transcription_path}')

if __name__ == '__main__':
    main()