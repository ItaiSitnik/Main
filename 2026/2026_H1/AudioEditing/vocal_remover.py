import logging
import sys
from pathlib import Path

import torch
from audio_separator.separator import Separator

# --- Configuration ---
# Your song file (must be in the same folder as this script)
# Example: 'my_song.mp3', 'song.wav', etc.
INPUT_SONG = "miracle_aligner.mp3"
# The folder where the split files will be saved
OUTPUT_DIR = "output"
# The model to use. 'UVR_MDXNET_KARA_2.onnx' is specifically for karaoke.
# Another high-quality option is 'htdemucs_ft' (Hybrid Transformer Demucs Fine-Tuned)
MODEL_NAME = "UVR_MDXNET_KARA_2.onnx"
MODEL_NAME = "model_bs_roformer_ep_317_sdr_12.9755.ckpt"  # slower but better
# ---------------------


def split_song_demucs(input_file, output_path_str, model_name):
    """
    Splits a song into vocals and accompaniment using the audio-separator library.
    """
    input_path = Path(input_file)
    output_path = Path(output_path_str)

    # Check if the input file exists
    if not input_path.exists():
        print(f"Error: Input file not found at {input_file}")
        print("Please make sure the file is in the same folder as this script.")
        return

    # Create the output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Loading model '{model_name}' via audio-separator...")
    print("(This might download the model on the first run)")

    try:
        # --- 1. Separate Vocals (Lyrics) ---
        print("\nStep 1/2: Initializing separator for Vocals...")
        separator_vocals = Separator(
            output_dir=output_path_str, output_format="mp3", log_level=logging.INFO, output_single_stem="vocals"
        )

        # Check for GPU
        if torch.cuda.is_available():
            print("NVIDIA GPU (CUDA) detected. Using GPU for processing.")
            separator_vocals.device = "cuda"
        else:
            print("No GPU detected. Using CPU (this may be much slower).")

        # **Explicitly load the model**
        print(f"Loading model '{model_name}' for vocals...")
        separator_vocals.load_model(model_name)

        print(f"Processing audio file for Vocals: {input_file}")
        # Call separate with ONLY the input file
        separator_vocals.separate(input_file)
        print("Vocals file saved.")

        # --- 2. Separate Instrumental (Music) ---
        print("\nStep 2/2: Initializing separator for Instrumental...")
        separator_instrumental = Separator(
            output_dir=output_path_str, output_format="mp3", log_level=logging.INFO, output_single_stem="instrumental"
        )

        # Set device for this instance too
        if torch.cuda.is_available():
            separator_instrumental.device = "cuda"

        # **Explicitly load the model**
        print(f"Loading model '{model_name}' for instrumental...")
        separator_instrumental.load_model(model_name)

        print(f"Processing audio file for Instrumental: {input_file}")
        # Call separate with ONLY the input file
        separator_instrumental.separate(input_file)
        print("Instrumental file saved.")

        print("\n--- Success! ---")
        print(f"Separation complete. Check the '{output_path_str}' folder.")

        # The library automatically names the files
        base_name = input_path.stem

        print("Your files should be named something like:")
        print(f"1. {base_name}_({model_name})_Vocals.mp3")
        print(f"2. {base_name}_({model_name})_Instrumental.mp3")

    except Exception as e:
        print("\n--- An Error Occurred During Separation ---")
        print(e)
        if "Initialization failed" in str(e) or "Model file" in str(e) or "not found" in str(e):
            print("\n--- Developer Note ---")
            print("This error means the model couldn't be loaded.")
            print(
                f"Make sure the model name '{model_name}' is correct (including any .onnx or .ckpt extension) and you are connected to the internet."
            )
        elif "unexpected keyword argument" in str(e):
            print("\n--- Developer Note ---")
            print("This error means the library API has changed.")
            print("Ensure 'output_single_stem' is a valid parameter for the Separator() constructor.")

        # Check for ffmpeg error
        if "ffmpeg" in str(e).lower():
            print("\n--- FFmpeg Note ---")
            print(
                "The error mentions 'ffmpeg'. Even if it's installed, ensure its location is in your system's PATH variable."
            )
        else:
            print("\nPlease ensure 'ffmpeg' is installed and in your system's PATH.")
            print("See the README.md file for setup instructions.")


if __name__ == "__main__":
    # Workaround for a potential multiprocessing bug on Windows
    if sys.platform == "win32":
        torch.multiprocessing.set_start_method("spawn")

    split_song_demucs(INPUT_SONG, OUTPUT_DIR, MODEL_NAME)
