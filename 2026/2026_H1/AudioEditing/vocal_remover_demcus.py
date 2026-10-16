import os
import sys

# --- FIX for torchcodec/ffmpeg error ---
# This line MUST be before the demucs import.
# It tells torchaudio to use the 'soundfile' backend instead of 'torchcodec',
# which avoids the FFmpeg DLL loading errors on Windows.
os.environ["TORCHAUDIO_AUDIO_BACKEND"] = "soundfile"
# -------------------------------------

# Try to import the main function from demucs
# This is our new way of "checking" if it's installed
try:
    from demucs.separate import main as demucs_main
except ImportError:
    print("Error: The 'demucs' library is not installed in this Python environment.")
    print("Please run: python -m pip install demucs")
    sys.exit(1)

# --- Configuration ---
# Set your input file here.
# Make sure this file is in the same directory as the script,
# or provide the full path (e.g., "C:/Users/YourUser/Music/my_song.mp3")
INPUT_FILE = "miracle_aligner.mp3"

# This is where the separated files will be saved.
OUTPUT_DIR = "output"
# ---------------------


def separate_vocals(input_path, output_path):
    """
    Separates a song into vocals and accompaniment using Demucs
    by calling its internal main function.
    """
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at '{input_path}'")
        print("Please update the INPUT_FILE variable in this script.")
        return

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    print(f"Initializing Demucs and processing '{input_path}'...")
    print("This may take a moment and will download the AI model on the first run.")

    # These are the command-line arguments we want to pass to demucs
    # -n mdx_extra: Uses a high-quality model
    # --two-stems vocals: Tells demucs to separate into 'vocals' and 'no_vocals'
    # -o: Specifies the output directory
    # The last argument is the input file
    demucs_args = ["-n", "mdx_extra", "--two-stems", "vocals", "-o", output_path, input_path]

    # We temporarily replace sys.argv with our arguments
    # The first item "demucs" is a placeholder for the script name (sys.argv[0])
    original_argv = sys.argv
    sys.argv = ["demucs"] + demucs_args

    try:
        # Run the demucs main function directly
        demucs_main()

        # Demucs creates a subfolder structure: output_path / model_name / file_name
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        model_name = "mdx_extra"  # The model we specified
        result_folder = os.path.join(output_path, model_name, base_name)

        if not os.path.exists(result_folder):
            # Fallback: try to find the folder if demucs modified the name
            model_folder = os.path.join(output_path, model_name)
            if os.path.exists(model_folder):
                all_subdirs = [d for d in os.listdir(model_folder) if os.path.isdir(os.path.join(model_folder, d))]
                if all_subdirs:
                    # Find the one most similar to base_name
                    # This handles cases where demucs sanitizes the name
                    best_match = max(all_subdirs, key=lambda d: os.path.commonprefix([d, base_name]))
                    result_folder = os.path.join(model_folder, best_match)

        if not os.path.exists(result_folder):
            print(f"\nError: Could not find expected output folder starting with: '{result_folder}'")
            print(f"Please check the '{os.path.join(output_path, model_name)}' directory manually.")
            return

        print("\n--- Separation Complete! ---")
        print(f"Files saved in: '{result_folder}'")
        print(f"  Music (Karaoke): {os.path.join(result_folder, 'no_vocals.wav')}")
        print(f"  Lyrics (Vocals): {os.path.join(result_folder, 'vocals.wav')}")

    except Exception as e:
        print(f"\nAn unexpected error occurred while running Demucs: {e}")
        print("This can happen for various reasons, including memory issues or a problem with the audio file.")
    finally:
        # Always restore the original sys.argv
        sys.argv = original_argv


if __name__ == "__main__":
    separate_vocals(INPUT_FILE, OUTPUT_DIR)
