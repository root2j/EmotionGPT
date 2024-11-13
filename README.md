# Project README

## Overview

This project is a Flask-based web application that utilizes Flask-Routes and jsonlib-python3 for data handling. It also employs uuid for unique identifier generation.

## Requirements

* Flask
* jsonlib-python3
* Flask-Routes
* uuid

## Getting Started

To run this project, ensure you have the required dependencies installed. You can do this by running the following command: 
```bash
pip install -r requirements.txt
```

To start the server, navigate to the project directory in your terminal and run the following command (Currently for development purpose only):

```bash
python -m app.server
```

## Project Structure

```Structure
EmotionGPT/
├── app/
│   ├── __init__.py
│   ├── frontend/
│   │   ├── index.html
│   │   ├── script.js
│   │   └── styles.css
│   ├── server.py
│   ├── session_manager.py
│   ├── llm_routes.py
│   └── server_routes.py
├── docs/
│   ├── architecture.md
│   └── api_documentation.md
├── models/
│   ├── __init__.py
│   ├── emotion_detection.py
│   ├── state_management.py
│   └── text_generation.py
├── tests/
│   ├── __init__.py
│   ├── test_emotion_detection.py
│   ├── test_state_management.py
│   ├── test_text_generation.py
│   └── test_speech_integration.py
├── README.md
└── requirements.txt
```

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please submit a pull request with a clear description of your changes.
