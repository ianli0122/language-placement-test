# Adaptive Language Placement Test

A placement test for language learners at MVHS. Will include reading, listening, speaking, and writing portions. Written majorly in Python using Flask.

This is still a work-in-progress project. Currently focused on the Mandarin program right now. Might branch out to others after.

## Required Libraries

- [Flask](https://pypi.org/project/Flask/) (Website management)
- [catsim](https://pypi.org/project/catsim/) (Adaptive testing calculations)

## To Run

`python app.py`

## Directory

```bash
├───question_data # question bank
│   └───audio # audio files for listening protion
├───scripts
├───static
├───student_data # scores
└───templates
```

## json Format

### Reading/Listening Single-Question

```json
[
    {
        "prompt": string (stimulus/audio file name),
        "difficulty": int,
        "question_data": {
            "question": string,
            "options": [string, string...],
            "correct": int
        }
    }
]
```
### Reading/Listening Multi-Question

```json
[
    {
        "prompt": string (stimulus/audio file name),
        "difficulty": int,
        "question_data": [
            {
            "question": string,
            "options": [string, string...],
            "correct": int
            },
            {
            "question": string,
            "options": [string, string...],
            "correct": int
            }...
        ]
    }
]
```
### Speaking/Writing Question

```json
[
    string,
    string...
]
```

## Creators

[@ianli0122](https://github.com/ianli0122), [@heolo1](https://github.com/heolo1), [@potato-potato-potato-potato](https://github.com/potato-potato-potato-potato)
