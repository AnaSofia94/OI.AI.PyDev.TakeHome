# OI.AI.PyDev.TakeHome

## Video Compression Service

This project is a Python-based service for handling video compression using FastAPI. It monitors a folder for new video files, compresses the videos to a maximum of 1/5 of their original size, and logs metadata of the processed videos into an SQLite database.

## Folder Structure

```bash 
OI.AI.PyDev.TakeHome/
│
├── config/
│   ├── Dockerfile                # Dockerfile for building the image
│   ├── .dockerignore             # Dockerignore to exclude unnecessary files
│   ├── Pipfile                   # Pipfile for dependency management
│   ├── Pipfile.lock              # Lockfile to ensure consistent dependencies
│
├── data/
│   ├── uploaded_videos/          # Folder where videos will be uploaded
│   ├── compressed_videos/        # Folder where compressed videos will be saved
│   ├── video_metadata.db         # SQLite database (runtime)
│
├── src/
│   ├── __init__.py
│   ├── batch.py                  # FastAPI application
│   ├── main.py                   # Entry point for running the app
│   ├── models/                   # Holds database-related models
│   │   ├── __init__.py
│   │   ├── db_manager.py         # Manages SQLite database operations
│   ├── services/                 # Contains service classes
│   │   ├── __init__.py
│   │   ├── video_compressor.py   # Contains the logic for compressing videos
│
├── tests/
│   ├── __init__.py
│   ├── test_service.py           # Test cases
│
├── README.md                     # Project documentation
```

## Key Folders and Files:

	•	config/: Contains configuration files like Dockerfile, Pipfile, and .dockerignore.
	•	data/: This folder holds the runtime data such as uploaded videos, compressed videos, and the SQLite database file (video_metadata.db).
	•	src/: Contains the FastAPI application and core logic, including:
	•	batch.py: The main FastAPI app where API routes are defined.
	•	main.py: The entry point for running the FastAPI app.
	•	models/db_manager.py: Handles the database operations for logging video metadata.
	•	services/video_compressor.py: Contains the video compression logic using FFmpeg.
	•	tests/: Holds the test cases for the project.

## Running the Project Without Docker

Prerequisites

	•	Python 3.11
	•	FFmpeg: You need FFmpeg installed on your system to handle video compression.
	•	Pipenv: Pipenv is used for managing Python dependencies.


### Steps:

1.	Clone the repository:
        ```bash
        git clone <repository-url>
        cd OI.AI.PyDev.TakeHome
        ```

2.	Install the dependencies:
        ```bash
        pipenv install
        ```
	Then install project dependencies using:
        ```bash
        pipenv install 
        ```
3.	Run the FastAPI application:
        ```bash
        pipenv run python src/main.py
        ```
4.	Access the FastAPI application at http://127.0.0.1:8000/docs to access the FastAPI Swagger UI and interact with the API.


## Running the Project with Docker

### Prerequisites
    
        •	Docker: Make sure Docker is installed on your system.

### Steps:
    
1.	Clone the repository:
	```bash
	git clone <repository-url>
	cd OI.AI.PyDev.TakeHome
	```
    
2.	Build the Docker image:
    ```bash
    docker build -t fastapi-video-app .
    ```
3.	Run the Docker container:
    ```bash
    docker run -p 8000:8000 fastapi-video-app
    ```
4.	http://127.0.0.1:8000/docs to access the FastAPI Swagger UI.


## API Endpoints

### 1. Upload a Video

	- URL: POST /upload/
	- Description: Upload a video file, which will be compressed and stored.
	- Request:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/upload/' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/your/video.mp4'
```

- Response:
```json
{
  "message": "Video uploaded and compressed successfully.",
  "original_size": 5000000,
  "compressed_size": 1000000,
  "compression_ratio": 0.2,
  "compressed_file": "compressed_videos/compressed_video.mp4"
}
```

### 2. Get All Video Metadata

- URL: GET /videos/
- Description: Retrieve the metadata for all processed videos from the SQLite database.
- Request:
- 
```bash 
 curl -X 'GET' 'http://127.0.0.1:8000/videos/'
```
- Response:
```json
[
  {
    "id": 1,
    "original_file": "uploaded_videos/video.mp4",
    "compressed_file": "compressed_videos/compressed_video.mp4",
    "original_size": 5000000,
    "compressed_size": 1000000,
    "compression_ratio": 0.2
  }
]
```


#### Notes

- The compressed videos are stored in data/compressed_videos/ and the original uploaded videos are stored in data/uploaded_videos/.
-  The metadata for each video, including the original size and compressed size, is stored in an SQLite database located at data/video_metadata.db.

