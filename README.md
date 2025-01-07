# Lintoxic Backend

# Design

# Usage

Lintoxic provides an asynchronous RESTful API that can be easily integrated with other applications for integration of content moderation into their system without disruption of existing workflow or systems.

## Dependencies

To run Lintoxic's API locally, you need to have the following dependencies installed on your system for the solution to work:

### Shared Libraries and external dependencies

These dependencies are needed by PyTorch, HuggingFace and for audio and video processing
- `pkg-config`
- `sentencepiece`
- `protobuf`
- `ffmpeg`
- `cmake`


Install them via your prefered package manager and ensure that they are available on `PATH`.

### API specific dependencies

You need to have the following dependencies to successfully run the application server:

- **Poetry:** Used for dependency and project management
- **Tesseract:** Needed for performing OCR


### Installation

1. Clone the backend repository from Github

2. Run the following command to install the project using Poetry
```shell
poetry install
```
3. Activate the virtual environment if not activated using `poetry shell` command.

4. Set up the environment variables as described in the `.env.sample` file for your needs

5. Run the API server using the following command:
```shell
fastapi dev api/server.py
```

This should start the server at `http://localhost:8000`

Access the documentation for the API at `http://localhost:8000` for more information regarding payload and endpoints.