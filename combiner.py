from pydub import AudioSegment, silence
import os
import sys

def get_files_in_directory(directory):
    files_info = []
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        if os.path.isfile(file_path):
            name, extension = os.path.splitext(filename)
            if extension == "":
                continue
            files_info.append({"name": name, "extension": extension})
    
    for file in files_info:
        print(f"Name: {file['name']}, Extension: {file['extension']}")
    
    return files_info

def combiner(dir):
    files = get_files_in_directory(dir)

    if len(files) > 16:
        raise Exception("Too many files in directory")
    
    samples = []
    
    for file in files:
        sound = AudioSegment.from_file(os.path.join(dir, file["name"] + file["extension"]), format=file["extension"][1:])
        samples.append(sound)

    if len(files) < 16:
        for _ in range(16 - len(files)):
            samples.append(AudioSegment.silent(2000))
    
    combined = AudioSegment.empty()
    for sound in samples:
        combined += sound

    combined.export("./output.mp3", format="mp3", tags={"artist": "krstff"})
    # file_handle.close()

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python3 combiner.py <path_to_directory>")
        exit()

    combiner(sys.argv[1])
