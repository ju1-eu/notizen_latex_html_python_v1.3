"""YouTube Text Extraktor.

Dieses Skript ermöglicht das Extrahieren von Text aus YouTube-Videos durch:
1. Abrufen vorhandener Untertitel
2. Falls keine Untertitel verfügbar sind: Download und Transkription der Audiospur

Hauptfunktionalitäten:
- Extraktion von Untertiteln aus YouTube-Videos
- Download der Audiospur, falls keine Untertitel verfügbar sind
- Transkription der Audiospur mit Whisper
- Speicherung des extrahierten Textes in einer Datei

Hauptfunktionen:
- extrahiere_text_aus_video: Hauptfunktion zur Textextraktion aus einem Video
- hole_untertitel: Versucht, Untertitel aus einem Video zu extrahieren
- extrahiere_audio: Lädt die Audiospur eines Videos herunter
- transkribiere_audio: Transkribiert eine Audiodatei mit Whisper

Verwendung:
    python youtube_text_extraktor.py

    Oder als Modul:
    from youtube_text_extraktor import extrahiere_text_aus_video
    text = extrahiere_text_aus_video("VIDEO_URL")

Voraussetzungen:
- youtube-transcript-api
- pytube
- whisper

Version: 1.0
Autor: Jan Unger
Datum: 26.11.2024
"""

import os
import re

import whisper
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi


def prüfe_url(url: str) -> bool:
    """
    Überprüft die Gültigkeit einer YouTube-URL.

    Args:
        url (str): Zu prüfende YouTube-URL

    Returns:
        bool: True wenn URL gültig

    Raises:
        ValueError: Wenn URL ungültig
    """
    youtube_regex = r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/"
    if not re.match(youtube_regex, url):
        raise ValueError("Die eingegebene URL ist keine gültige YouTube-URL")
    return True


def hole_video_id(url: str) -> str:
    """Extrahiert die Video-ID aus der URL"""
    try:
        if "watch?v=" in url:
            return url.split("watch?v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1]
        else:
            return url.split("/")[-1]
    except Exception as e:
        raise ValueError(f"Konnte Video-ID nicht aus URL extrahieren: {e}")


def hole_untertitel(video_id: str) -> str | None:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["de"])
        return " ".join([eintrag["text"] for eintrag in transcript])
    except Exception as e:
        print(f"Keine manuellen deutschen Untertitel gefunden: {e}")
        try:
            transcript_auto = YouTubeTranscriptApi.get_transcript(
                video_id, languages=["de-generated"]
            )
            return " ".join([eintrag["text"] for eintrag in transcript_auto])
        except YouTubeTranscriptApi.TranscriptsDisabled:
            return None


def extrahiere_audio(url: str, ausgabepfad: str = "audio.mp3") -> str | None:
    """Lädt die Audiospur herunter"""
    try:
        yt = YouTube(url)
        print(f"Verarbeite Video: {yt.title}")
        video = yt.streams.filter(only_audio=True).order_by("abr").desc().first()
        if not video:
            raise Exception("Kein Audio-Stream gefunden")
        if os.path.exists(ausgabepfad):
            os.remove(ausgabepfad)
        print("Lade Audio herunter...")
        video.download(filename=ausgabepfad)
        return ausgabepfad
    except Exception as e:
        print(f"Fehler beim Herunterladen des Audios: {e}")
        return None


def transkribiere_audio(audio_pfad: str) -> str | None:
    """Transkribiert eine Audiodatei"""
    try:
        print("Lade Whisper Modell...")
        model = whisper.load_model("base")
        print("Transkribiere Audio...")
        ergebnis = model.transcribe(audio_pfad, language="de")
        text: str = ergebnis["text"]
        return text
    except Exception as e:
        print(f"Fehler bei der Transkription: {e}")
        return None


def extrahiere_text_aus_video(url: str) -> str:
    """Hauptfunktion zur Textextraktion"""
    try:
        prüfe_url(url)
        video_id = hole_video_id(url)
        print(f"Video-ID: {video_id}")
        print("Suche nach vorhandenen Untertiteln...")
        text = hole_untertitel(video_id)
        if text:
            print("✓ Untertitel erfolgreich geladen!")
            return text
        print("Keine Untertitel gefunden. Starte Audio-Download...")
        audio_pfad = extrahiere_audio(url)
        if not audio_pfad:
            raise Exception("Audio konnte nicht heruntergeladen werden")
        text = transkribiere_audio(audio_pfad)
        if os.path.exists(audio_pfad):
            os.remove(audio_pfad)
            print("✓ Audio-Datei aufgeräumt")
        if not text:
            raise Exception("Transkription fehlgeschlagen")
        return text
    except Exception as e:
        return f"Fehler bei der Textextraktion: {e}"


def speichere_text(text: str, ausgabedatei: str = "youtube_transkript.txt") -> None:
    """Speichert den Text in eine Datei"""
    try:
        ausgabe_verzeichnis = os.path.dirname(ausgabedatei)
        if ausgabe_verzeichnis and not os.path.exists(ausgabe_verzeichnis):
            os.makedirs(ausgabe_verzeichnis)
        with open(ausgabedatei, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"✓ Text wurde in {ausgabedatei} gespeichert")
    except Exception as e:
        print(f"Fehler beim Speichern: {e}")


if __name__ == "__main__":
    try:
        # YouTube-URL des Videos
        url = "http://youtu.be/GRKYOWYs1gM"

        print("\nYouTube Text Extraktor")
        print("-" * 50)

        print("\nStarte Textextraktion...")
        text = extrahiere_text_aus_video(url)

        if text and not text.startswith("Fehler"):
            print("\nExtrahierter Text:")
            print("-" * 50)
            print(text)
            print("-" * 50)

            # Speichere den Text in eine Datei
            speichere_text(text)
        else:
            print("\nFehler:")
            print("-" * 50)
            print(text)

    except KeyboardInterrupt:
        print("\n\nProgramm wurde durch Benutzer abgebrochen.")
    except Exception as e:
        print(f"\nUnerwarteter Fehler: {e}")
