# TTS-STT-Tools

## Create virtual environment by running the command 

	python3 -m venv .venv

## Activate your venv 

	### For linux:
	source .venv/bin/activate

	### For windows:
	.\.venv\Scripts\bin\activate

## Install requirements

	pip install -r requirements.txt

## Run the API

	uvicorn main:app
