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

def trim(sound):
    silences = silence.detect_silence(sound, silence_thresh=0)
    if len(silences) == 0:
        return sound
    elif len(silences) == 1:
        start = silences[0][0]
        return sound[start:]
    else:
        return sound[silences[0][1]:silences[-1][0]]

def get_max_len(sounds):
    m_len = 0
    for sound in sounds:
        ln = len(sound)
        if ln > m_len:
            m_len = ln
    return m_len

def get_avg_len(sounds):
    length = 0
    for s in sounds:
        length += len(s)
    print("Average length: ", end="")
    print(length / len(sounds))

def combiner(dir):
    files = get_files_in_directory(dir)

    if len(files) > 16:
        raise Exception("Too many files in directory")
    
    samples = []
    
    # Save all samples and get rid of silence
    for file in files:
        sound = AudioSegment.from_file(os.path.join(dir, file["name"] + file["extension"]), format=file["extension"][1:])
        samples.append(trim(sound))
    
    get_avg_len(samples)
    max_len = get_max_len(samples)
    print("Max length: ", end="")
    print(max_len)

    # Fill result with silent part if not enough samples were given
    # so that each sample has the same length
    if len(files) < 16:
        for _ in range(16 - len(files)):
            samples.append(AudioSegment.silent(max_len))
    
    combined = AudioSegment.empty()
    for sound in samples:
        combined += sound

    combined.export("./output.mp3", format="mp3", tags={"artist": "krstff"})

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python3 combiner.py <path_to_directory>")
        exit()

    combiner(sys.argv[1])
