"""Bildverarbeitung für Web und Präsentationen.

Dieses Skript konvertiert Bilder in WebP-Format für Web-Verwendung und in PDF für Präsentationen.
Es nutzt ImageMagick für die Konvertierung und Ghostscript für PDF-Optimierung.

Hauptfunktionalitäten:
1. Konvertierung von Bildern in WebP-Format für Web-Verwendung
2. Konvertierung von Bildern in PDF für Präsentationen
3. Optimierung von PDF-Dateien mit Ghostscript
4. Multithreading für parallele Verarbeitung mehrerer Bilder
5. Konfiguration über Kommandozeilenargumente

Hauptkomponenten:
- ImageProcessorConfig: Dataclass für die Konfiguration der Bildverarbeitung
- ImageProcessor: Klasse zur Verarbeitung von Bildern

Verwendung:
    python image_resizer.py [Optionen]

Optionen:
    --input: Eingabeverzeichnis für Bilder
    --web-output: Ausgabeverzeichnis für Web-Bilder
    --pres-output: Ausgabeverzeichnis für Präsentations-PDFs
    --resolution: Zielauflösung (ImageMagick-Format)
    --web-quality: WebP-Qualität (1-100)
    --pdf-dpi: PDF-Auflösung in DPI
    --pdf-quality: PDF-Qualität (1-100)
    --gs-quality: Ghostscript PDF-Qualitätsprofil
    --force: Bestehende Dateien überschreiben
    --verbose: Ausführliche Logging-Ausgabe

Voraussetzungen:
- ImageMagick muss installiert sein
- Ghostscript muss installiert sein

Version: 1.0
Autor: Jan Unger
Datum: 26.11.2024
"""

import argparse
import logging
import multiprocessing
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from tqdm import tqdm

# Logging-Konfiguration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@dataclass
class ImageProcessorConfig:
    """Konfiguration für die Bildverarbeitung."""

    input_folder: Path
    output_folder_web: Path
    output_folder_pres: Path
    resolution: str = "1600x1600>"
    web_quality: int = 80
    pdf_dpi: int = 72
    pdf_quality: int = 80
    gs_quality: str = "ebook"
    force: bool = False

    def __post_init__(self) -> None:
        """Validiert und erstellt die notwendigen Verzeichnisse."""
        self.output_folder_web.mkdir(parents=True, exist_ok=True)
        self.output_folder_pres.mkdir(parents=True, exist_ok=True)


class ImageProcessor:
    """Verarbeitet Bilder für Web und Präsentationen."""

    SUPPORTED_FORMATS = {".png", ".heic", ".jpg", ".jpeg", ".webp"}

    def __init__(self, config: ImageProcessorConfig):
        """Initialisiert den Bildprozessor."""
        self.config = config

    def convert_to_webp(self, input_path: Path, output_path: Path) -> None:
        """Konvertiert ein Bild in das WebP-Format.

        Args:
            input_path: Pfad zur Eingabedatei
            output_path: Pfad zur Ausgabedatei

        Raises:
            subprocess.CalledProcessError: Bei Fehlern während der Konvertierung
        """
        if output_path.exists() and not self.config.force:
            logger.debug("WebP-Datei existiert bereits: %s", output_path)
            return

        try:
            cmd = [
                "magick",
                str(input_path),
                "-resize",
                self.config.resolution,
                "-quality",
                str(self.config.web_quality),
                str(output_path),
            ]
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.info("WebP-Konvertierung erfolgreich: %s", output_path)
        except subprocess.CalledProcessError as e:
            logger.error("Fehler bei WebP-Konvertierung: %s\n%s", e, e.stderr)
            raise

    def convert_to_pdf(self, webp_path: Path, pdf_path: Path) -> None:
        """Konvertiert ein WebP-Bild in PDF.

        Args:
            webp_path: Pfad zur WebP-Datei
            pdf_path: Pfad zur PDF-Ausgabedatei

        Raises:
            subprocess.CalledProcessError: Bei Fehlern während der Konvertierung
        """
        try:
            cmd = [
                "magick",
                str(webp_path),
                "-density",
                str(self.config.pdf_dpi),
                "-quality",
                str(self.config.pdf_quality),
                "-compress",
                "jpeg",
                str(pdf_path),
            ]
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.debug("PDF-Konvertierung erfolgreich: %s", pdf_path)
        except subprocess.CalledProcessError as e:
            logger.error("Fehler bei PDF-Konvertierung: %s\n%s", e, e.stderr)
            raise

    def optimize_pdf(self, input_path: Path, output_path: Path) -> None:
        """Optimiert eine PDF-Datei mit Ghostscript.

        Args:
            input_path: Pfad zur Eingabe-PDF
            output_path: Pfad zur optimierten PDF

        Raises:
            subprocess.CalledProcessError: Bei Fehlern während der Optimierung
        """
        try:
            cmd = [
                "gs",
                "-sDEVICE=pdfwrite",
                f"-dPDFSETTINGS=/{self.config.gs_quality}",
                "-dCompatibilityLevel=1.4",
                "-dNOPAUSE",
                "-dQUIET",
                "-dBATCH",
                f"-sOutputFile={output_path}",
                str(input_path),
            ]
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.debug("PDF-Optimierung erfolgreich: %s", output_path)
        except subprocess.CalledProcessError as e:
            logger.error("Fehler bei PDF-Optimierung: %s\n%s", e, e.stderr)
            raise

    def process_single_image(self, image_path: Path) -> Tuple[Path, bool]:
        """Verarbeitet ein einzelnes Bild.

        Args:
            image_path: Pfad zum Eingabebild

        Returns:
            Tuple[Path, bool]: (Bildpfad, Erfolgsstatus)
        """
        try:
            webp_path = self.config.output_folder_web / f"{image_path.stem}.webp"
            pdf_path = self.config.output_folder_pres / f"{image_path.stem}.pdf"
            temp_pdf = pdf_path.with_stem(f"{image_path.stem}_temp")

            self.convert_to_webp(image_path, webp_path)
            self.convert_to_pdf(webp_path, temp_pdf)
            self.optimize_pdf(temp_pdf, pdf_path)
            temp_pdf.unlink()

            return image_path, True

        except Exception as e:
            logger.error("Fehler bei Verarbeitung von %s: %s", image_path, e)
            return image_path, False

    def find_images(self) -> List[Path]:
        """Findet alle unterstützten Bilddateien im Eingabeverzeichnis.

        Returns:
            List[Path]: Liste der gefundenen Bilddateien
        """
        return [
            path
            for path in self.config.input_folder.iterdir()
            if path.suffix.lower() in self.SUPPORTED_FORMATS
        ]

    def process_all_images(self) -> None:
        """Verarbeitet alle gefundenen Bilder parallel."""
        images = self.find_images()
        if not images:
            logger.warning("Keine Bilder zum Verarbeiten gefunden in: %s", self.config.input_folder)
            return

        with multiprocessing.Pool() as pool:
            results = list(
                tqdm(
                    pool.imap(self.process_single_image, images),
                    total=len(images),
                    desc="Verarbeite Bilder",
                )
            )

        successful = sum(1 for _, success in results if success)
        logger.info(
            "Verarbeitung abgeschlossen: %d von %d Bilder erfolgreich verarbeitet",
            successful,
            len(images),
        )


def parse_args() -> argparse.Namespace:
    """Verarbeitet die Kommandozeilenargumente.

    Returns:
        argparse.Namespace: Verarbeitete Argumente
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("images/input"),
        help="Eingabeverzeichnis für Bilder",
    )
    parser.add_argument(
        "--web-output",
        type=Path,
        default=Path("images/output/web"),
        help="Ausgabeverzeichnis für Web-Bilder",
    )
    parser.add_argument(
        "--pres-output",
        type=Path,
        default=Path("images/output/presentation"),
        help="Ausgabeverzeichnis für Präsentations-PDFs",
    )
    parser.add_argument(
        "--resolution",
        default="1600x1600>",
        help="Zielauflösung (ImageMagick-Format)",
    )
    parser.add_argument(
        "--web-quality",
        type=int,
        default=80,
        help="WebP-Qualität (1-100)",
    )
    parser.add_argument(
        "--pdf-dpi",
        type=int,
        default=72,
        help="PDF-Auflösung in DPI",
    )
    parser.add_argument(
        "--pdf-quality",
        type=int,
        default=80,
        help="PDF-Qualität (1-100)",
    )
    parser.add_argument(
        "--gs-quality",
        choices=["screen", "ebook", "printer", "prepress"],
        default="ebook",
        help="Ghostscript PDF-Qualitätsprofil",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Bestehende Dateien überschreiben",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Ausführliche Logging-Ausgabe",
    )

    return parser.parse_args()


def main() -> None:
    """Hauptfunktion des Skripts."""
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        config = ImageProcessorConfig(
            input_folder=args.input,
            output_folder_web=args.web_output,
            output_folder_pres=args.pres_output,
            resolution=args.resolution,
            web_quality=args.web_quality,
            pdf_dpi=args.pdf_dpi,
            pdf_quality=args.pdf_quality,
            gs_quality=args.gs_quality,
            force=args.force,
        )

        processor = ImageProcessor(config)
        processor.process_all_images()

    except Exception as e:
        logger.error("Unerwarteter Fehler: %s", e)
        raise


if __name__ == "__main__":
    main()
