import logging
import sys
from pathlib import Path

import torch
from audio_separator.separator import Separator

# --- Configuration ---
# The folder containing your song files
INPUT_DIR = "input"
# The folder where the split files will be saved
OUTPUT_DIR = "output"
# The model to use. 'UVR_MDXNET_KARA_2.onnx' is for karaoke.
# 'model_bs_roformer_ep_317_sdr_12.9755.ckpt' is slower but higher quality.
MODEL_NAME = "model_bs_roformer_ep_317_sdr_12.9755.ckpt"
# Supported audio file extensions to look for
SUPPORTED_EXTENSIONS = ('.mp3', '.wav', '.flac', '.m4a', '.ogg')
# ---------------------


def split_song(input_file_str, separator_vocals, separator_instrumental):
    """
    Splits a single song using the pre-loaded separator instances.
    """
    input_path = Path(input_file_str)
    print(f"\n--- Processing: {input_path.name} ---")

    try:
        # --- 1. Separate Vocals ---
        print("Step 1/2: Separating Vocals...")
        separator_vocals.separate(input_file_str)
        print("Vocals file saved.")

        # --- 2. Separate Instrumental ---
        print("Step 2/2: Separating Instrumental...")
        separator_instrumental.separate(input_file_str)
        print("Instrumental file saved.")

        print(f"\n--- Success for {input_path.name}! ---")

    except Exception as e:
        print(f"\n--- An Error Occurred During Separation for {input_path.name} ---")
        print(e)
        # Check for ffmpeg error
        if "ffmpeg" in str(e).lower():
            print("\n--- FFmpeg Note ---")
            print("The error mentions 'ffmpeg'.")
            # User-specific note: You mentioned ffmpeg is in your PATH,
            # but this check is kept in case something goes wrong.
        else:
            # General advice from original script
            print("\nPlease ensure 'ffmpeg' is installed and in your system's PATH.")


if __name__ == "__main__":
    # Workaround for a potential multiprocessing bug on Windows
    if sys.platform == "win32":
        torch.multiprocessing.set_start_method("spawn")

    input_dir_path = Path(INPUT_DIR)
    output_dir_path = Path(OUTPUT_DIR)

    # Check if input directory exists
    if not input_dir_path.is_dir():
        print(f"Error: Input directory not found at '{INPUT_DIR}'")
        print("Please create it and add your audio files.")
        sys.exit(1)  # Exit the script

    # Create the output directory if it doesn't exist
    output_dir_path.mkdir(parents=True, exist_ok=True)

    # Find all supported audio files in the input directory
    print(f"Scanning '{INPUT_DIR}' for audio files ({', '.join(SUPPORTED_EXTENSIONS)})...")
    audio_files = [f for f in input_dir_path.iterdir() if f.suffix.lower() in SUPPORTED_EXTENSIONS and f.is_file()]

    if not audio_files:
        print(f"No audio files found in '{INPUT_DIR}'.")
        sys.exit(0)  # Exit gracefully

    print(f"Found {len(audio_files)} audio file(s) to process.")

    # --- Load Models ONCE ---
    print(f"\nLoading model '{MODEL_NAME}' for all separations...")
    print("(This might download the model on the first run)")

    separator_vocals = None
    separator_instrumental = None
    device_type = "cpu"

    if torch.cuda.is_available():
        device_type = "cuda"
        print("NVIDIA GPU (CUDA) detected. Using GPU for processing.")
    else:
        print("No GPU detected. Using CPU (this may be much slower).")

    try:
        # --- 1. Load Vocals Separator ---
        print("Loading vocals separator instance...")
        separator_vocals = Separator(
            output_dir=OUTPUT_DIR,
            output_format="mp3",
            log_level=logging.INFO,
            output_single_stem="vocals"
            # device=device_type  <- This was the mistake, removed.
        )
        # Set device attribute AFTER initialization (the correct way)
        if device_type == "cuda":
            separator_vocals.device = "cuda"

        separator_vocals.load_model(MODEL_NAME)

        # --- 2. Load Instrumental Separator ---
        print("Loading instrumental separator instance...")
        separator_instrumental = Separator(
            output_dir=OUTPUT_DIR,
            output_format="mp3",
            log_level=logging.INFO,
            output_single_stem="instrumental"
            # device=device_type  <- This was the mistake, removed.
        )
        # Set device attribute AFTER initialization (the correct way)
        if device_type == "cuda":
            separator_instrumental.device = "cuda"

        separator_instrumental.load_model(MODEL_NAME)

        print("\nModel loaded successfully. Starting batch processing...")

    except Exception as e:
        print(f"\n--- FATAL ERROR: Could not load model '{MODEL_NAME}' ---")
        print(e)
        if "unexpected keyword argument" in str(e):
            print("\nDeveloper Note: This error likely means the 'device' argument was")
            print("incorrectly passed to the Separator constructor, which I have now fixed.")
        print("Cannot proceed. Please check the model name, your internet connection,")
        print("or if the model file is correctly placed (if manually downloaded).")
        sys.exit(1)

    # --- Process All Files ---
    for i, file_path in enumerate(audio_files):
        print(f"\n---== Processing file {i + 1} of {len(audio_files)} ==---")
        # Call the processing function with the pre-loaded models
        split_song(str(file_path), separator_vocals, separator_instrumental)

    print("\n--- Batch complete! ---")
    print(f"All {len(audio_files)} file(s) processed.")
    print(f"Check the '{OUTPUT_DIR}' folder for your files.")
