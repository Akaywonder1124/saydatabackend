import os
import speech_recognition as sr
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError


def audio_extractor(video_file, audio_output_file):
    try:
        video = VideoFileClip(video_file)
        audio = video.audio
        return audio.write_audiofile(audio_output_file)
    except Exception as e:
        return {"audio_extraction_error": str(e)}


def mp3_to_wav(mp3_file, wav_file):
    try:
        audio = AudioSegment.from_mp3(mp3_file)
        audio.export(wav_file, format="wav")
    except Exception as e:
        return {"mp3_to_wav_conversion_error": str(e)}


def text_extractor(audio_file):
    print(audio_file)
    try:
        r = sr.Recognizer()
        audio_data = sr.AudioFile(audio_file)

        with audio_data as source:
            audio = r.record(source)
        print("Converting audio to text:")
        return r.recognize_google(audio)

    except sr.UnknownValueError:
        return {
            "speech_recognition_error": "Speech Recognition could not understand the audio."
        }

    except sr.RequestError as e:
        return {
            "speech_recognition_error": f"Could not request results from Google Speech Recognition service; {e}"
        }

    except Exception as e:
        return {"text_extraction_error": str(e)}


def extract_and_recognize_text(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    file_name = os.path.splitext(file_path)[0]

    if file_extension == ".mp4":
        audio_output_file = file_name + "audio.wav"

        try:
            audio_extractor(file_path, audio_output_file)
            return text_extractor(audio_output_file)
        except CouldntDecodeError as e:
            return {"audio_decoding_error": str(e)}
        except Exception as e:
            return {"video_processing_error": str(e)}

    elif file_extension == ".wav":
        return text_extractor(file_path)

    elif file_extension == ".mp3":
        temp_wav_file = file_name + "temp.wav"
        mp3_to_wav(file_path, temp_wav_file)
        print(temp_wav_file)
        text_result = text_extractor(temp_wav_file)
        return text_result

    else:
        return {"message": "Unsupported file format"}


def get_duration(audio_path):
    audio = AudioSegment.from_file(audio_path)
    duration = len(audio) / 1000
    return duration
