import json
from pathlib import Path


def load_transcript(transcript_path):
    with open(transcript_path, "r", encoding="utf-8") as file:
        return json.load(file)


def transcript_to_text(transcript):
    return " ".join(segment["text"] for segment in transcript)


def recursive_split(text, chunk_size, separators):
    if len(text) <= chunk_size:
        return [text]

    if not separators:
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    separator = separators[0]

    if separator == "":
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    parts = text.split(separator)

    chunks = []
    current = ""

    for part in parts:
        candidate = current + separator + part if current else part

        if len(candidate) <= chunk_size:
            current = candidate
        else:
            if current:
                chunks.append(current)

            if len(part) > chunk_size:
                chunks.extend(
                    recursive_split(part, chunk_size, separators[1:])
                )
                current = ""
            else:
                current = part

    if current:
        chunks.append(current)

    return chunks


def add_overlap(chunks, overlap=100):
    overlapped = []

    for i, chunk in enumerate(chunks):
        if i == 0:
            overlapped.append(chunk)
        else:
            previous = chunks[i - 1][-overlap:]
            overlapped.append(previous + chunk)

    return overlapped


def chunk_transcript(transcript_path):
    transcript = load_transcript(transcript_path)

    text = transcript_to_text(transcript)

    chunks = recursive_split(
        text,
        chunk_size=500,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = add_overlap(chunks)

    chunk_data = [{"id": i, "text": chunk} for i, chunk in enumerate(chunks)]

    output_dir = Path("chunks")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / f"{Path(transcript_path).stem}.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(chunk_data, file, indent=4)

    return str(output_path)