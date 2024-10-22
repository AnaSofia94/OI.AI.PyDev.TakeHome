import os
import ffmpeg

from models.db_manager import DatabaseManager


class VideoCompressor:
    def __init__(self, compressed_folder: str = 'compressed_videos'):
        self.compressed_folder = compressed_folder
        os.makedirs(self.compressed_folder, exist_ok=True)
        self.db_manager = DatabaseManager()

    def compress_video(self, input_file: str):
        """Compress video to 1/5 of its original size using ffmpeg."""
        original_size = os.path.getsize(input_file)
        output_file = os.path.join(self.compressed_folder, f"compressed_{os.path.basename(input_file)}")

        # Use ffmpeg to compress the video
        ffmpeg.input(input_file).output(output_file, video_bitrate='500k').run(overwrite_output=True)
        compressed_size = os.path.getsize(output_file)

        # Log metadata in the database
        self.db_manager.log_metadata(input_file, output_file, original_size, compressed_size)

        return original_size, compressed_size, output_file