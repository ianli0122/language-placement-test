# Adaptive Language Placement Test

An adaptive placement test for language learners. Includes reading, listening, speaking, and writing portion.

This application is still in development.

## Required Libraries

- [Flask](https://pypi.org/project/Flask/) (Website management)
- [catsim](https://pypi.org/project/catsim/) (Adaptive testing calculations)
- [customtkinter](https://pypi.org/project/customtkinter/) (GUI)
- [pygame](https://pypi.org/project/pygame/) (Audio management)

`pip install -r requirements.txt`

## To Run

`python gui.py`

## To Build
`pyinstaller --onedir --add-data="data;data" --add-data="templates;templates" --add-data="static;static" --add-data="scripts;scripts" --add-data="path/to/customtkinter;customtkinter" gui.py app.py sessions.py frq.py mcq.py`

After building, drag the "data" folder out from internals to the same directory as the executable

Prebuilt executables are avaliable [here](https://github.com/ianli0122/language-placement-test/releases/latest)

## Directory

```bash
├───data
│   ├───logs # Website logging
│   ├───question_data # question bank
│   │   └───audio
│   └───student_data # test results
├───scripts
├───static
└───templates
```

## json Format

### Reading/Listening Single-Question

```
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

```
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

```
[
    string,
    string...
]
```

## Creators

[@ianli0122](https://github.com/ianli0122), [@heolo1](https://github.com/heolo1), [@potato-potato-potato-potato](https://github.com/potato-potato-potato-potato)
