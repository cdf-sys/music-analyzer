# music-analyzer

This is a collection of programs and scripts made to organize and modify music files in accordance to metadata and user-specified constraints. Though applicable elsewhere, these scripts have been made with enhancing the DJ performance experience in mind.

## Installation
The installation guide will soon be found in docs/installation.md

## Usage
The usage guide will soon be found in docs/usage.md

## Current features

- Search for files by ID3 tag, and swap two of a song's ID3 tag values
- Compute the BPM of a song after a key change, and vice versa
- Convert a song's key into the camelot scale

## Planned features

- Create scripts to wrap everything together and suggest songs to mix into an input song based on BPM, camelot and other factors (energy, loudness, etc.)
- Calculate a song's BPM and key from scratch; Calculate whether a song contains a key or BPM change
- Make BPM changes (with or without changing the key) as specified by the user
- Create file converters so that all audio file types are compatible with the analyzer