from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os

from services.video_compressor import VideoCompressor
from models.db_manager import DatabaseManager

app = FastAPI()

# Create instances of VideoCompressor and DatabaseManager classes
video_compressor = VideoCompressor()
db_manager = DatabaseManager()

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    """Upload a video file for compression and store the result."""
    try:
        # Save the uploaded file temporarily
        upload_folder = 'uploaded_videos'
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Check if the video already exists in the database
        existing_video = db_manager.find_video_by_filename(file.filename)
        if existing_video:
            return JSONResponse(content={
                "message": "This video has already been uploaded and compressed.",
                "original_file": existing_video[1],
                "compressed_file": existing_video[2],
                "original_size": existing_video[3],
                "compressed_size": existing_video[4],
                "compression_ratio": existing_video[5]
            })

        # If not a duplicate, compress the video
        original_size, compressed_size, output_file = video_compressor.compress_video(file_path)

        # Return success response with file metadata
        return JSONResponse(content={
            "message": "Video uploaded and compressed successfully.",
            "original_size": original_size,
            "compressed_size": compressed_size,
            "compression_ratio": compressed_size / original_size,
            "compressed_file": output_file
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video file: {e}")

@app.get("/videos/")
def get_video_metadata():
    """Retrieve all video metadata from the SQLite database."""
    try:
        metadata = db_manager.fetch_all_metadata()
        # Return the metadata as a JSON response
        return JSONResponse(content=[{
            "id": row[0],
            "original_file": row[1],
            "compressed_file": row[2],
            "original_size": row[3],
            "compressed_size": row[4],
            "compression_ratio": row[5]
        } for row in metadata])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching video metadata: {e}")