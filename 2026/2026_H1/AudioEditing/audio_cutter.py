import os

import stable_whisper
from pydub import AudioSegment


def find_and_cut_word(audio_file_path, word_to_find, output_file_path):
    """
    Finds a specific word in an audio file, cuts the corresponding audio segment,
    and saves it as a new file.

    Args:
        audio_file_path (str): Path to the input audio file (e.g., mp3, wav).
        word_to_find (str): The word to search for in the audio.
        output_file_path (str): Path to save the resulting audio clip.
    """
    # Check if the input file exists
    if not os.path.exists(audio_file_path):
        print(f"Error: Input file not found at '{audio_file_path}'")
        return

    try:
        # 1. Load the speech recognition model.
        print("Loading speech recognition model...")
        model = stable_whisper.load_model("base")

        # 2. Transcribe the audio to get word-level timestamps.
        print(f"Transcribing '{audio_file_path}' to find the word '{word_to_find}'...")
        result = model.transcribe(audio_file_path, language="en")

        # --- NEW: Print the full detected transcript for debugging ---
        print("\n--- Full Transcript Detected by Model ---")
        if result.text:
            print(f"'{result.text}'")
        else:
            print("[No text detected in the audio]")
        print("-------------------------------------------\n")
        # -----------------------------------------------------------

        # 3. Search for the word in the transcription results.
        word_found = False
        start_time = 0
        end_time = 0

        for segment in result.segments:
            for word in segment.words:
                # Compare the detected word (cleaned of punctuation) with our target word.
                if word.word.strip().lower() == word_to_find.lower():
                    start_time = word.start
                    end_time = word.end
                    word_found = True
                    print(f"Found '{word_to_find}' from {start_time:.2f}s to {end_time:.2f}s.")
                    break  # Exit inner loop once word is found
            if word_found:
                break  # Exit outer loop

        # 4. If the word was found, use pydub to cut the audio.
        if word_found:
            print("Slicing the audio...")
            # Load the original audio file with pydub
            audio = AudioSegment.from_file(audio_file_path)

            # pydub works in milliseconds
            start_ms = int(start_time * 1000)
            end_ms = int(end_time * 1000)

            # Cut the audio segment
            word_clip = audio[start_ms:end_ms]

            # Export the cut segment to the output file
            output_format = os.path.splitext(output_file_path)[1][1:] or "mp3"
            word_clip.export(output_file_path, format=output_format)
            print(f"Successfully created audio clip: '{output_file_path}'")
        else:
            # --- NEW: Updated message for failure ---
            print(f"The word '{word_to_find}' was not found in the transcription logic.")
            print("Please review the full transcript printed above to see what was detected instead.")
            # ----------------------------------------

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure ffmpeg is installed and accessible in your system's PATH.")
        print("You can install the required python libraries with: pip install stable-ts pydub")


# --- Main execution block ---
if __name__ == "__main__":
    # --- PLEASE CONFIGURE THESE VARIABLES ---

    # 1. Set the path to your input audio file
    input_file = "2025_H2/my_english_speech.mp3"  # <--- CHANGE THIS

    # 2. Set the word you want to find
    target_word = "birds"

    # 3. Set the desired name for the output file
    output_file = "2025_H2/clip.mp3"  # <--- CHANGE THIS

    # --- Run the function ---
    find_and_cut_word(input_file, target_word, output_file)
