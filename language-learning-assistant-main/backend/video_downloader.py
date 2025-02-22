from typing import Optional
import yt_dlp
import os

class YouTubeVideoDownloader:
    def __init__(self):
        """Initialize YouTubeVideoDownloader"""
        # Ensure videos directory exists
        os.makedirs("./videos", exist_ok=True)
        
        # Configure yt-dlp options
        self.ydl_opts = {
            'format': 'bestaudio[format_note!*=DRM][format_note!*=DRC]/bestaudio/best',  # Select best non-DRM/DRC audio
            'outtmpl': os.path.join(os.path.abspath('./videos'), '%(id)s.%(ext)s'),  # Absolute path output template
            'quiet': True,  # Suppress output
            'no_warnings': True,  # Suppress warnings
            'extract_flat': False,  # Extract video info
            'keepvideo': True,  # Keep the original downloaded file
        #    'postprocessors': [{
        #        'key': 'FFmpegExtractAudio',
        #        'preferredcodec': 'wav',  # Highest quality lossless format
        #        'preferredquality': '192',  # Highest bitrate
        #    }],
        }
        
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL
        
        Args:
            url (str): YouTube URL
            
        Returns:
            Optional[str]: Video ID if found, None otherwise
        """
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info.get('id')
        except Exception as e:
            print(f"Error extracting video ID: {str(e)}")
            return None
    
    def download_video(self, url: str) -> Optional[str]:
        """Download YouTube video and extract best quality audio
        
        Args:
            url (str): YouTube URL
            
        Returns:
            Optional[str]: Path to downloaded audio if successful, None otherwise
        """
        try:
            # Extract video ID
            video_id = self.extract_video_id(url)
            if not video_id:
                raise ValueError("Invalid video ID or URL - Please check if the video exists and is accessible")
            
            # Download video and extract audio
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                print("\nExtracting video information...")
                try:
                    info = ydl.extract_info(url, download=False)
                except yt_dlp.utils.DownloadError as e:
                    raise ValueError(f"Failed to access video: {str(e)}")
                    
                print(f"Video title: {info.get('title')}")
                
                # List available formats
                formats = info.get('formats', [])
                # Filter out DRM/DRC formats and keep only audio streams
                audio_formats = [f for f in formats 
                               if f.get('acodec') != 'none' 
                               and not any(drm in str(f.get('format_note', '')).upper() 
                                          for drm in ['DRM', 'DRC'])]
                
                if not audio_formats:
                    raise ValueError("No non-DRM audio formats available for this video")
                
                print("\nAvailable audio formats:")
                for f in audio_formats:
                    abr = f.get('abr')
                    if abr is not None:
                        print(f"- {f.get('format')} ({abr}kbps)")
                    else:
                        print(f"- {f.get('format')} (bitrate unknown)")
                
                # Sort by quality (bitrate), handling None values
                audio_formats.sort(key=lambda x: float(x.get('abr', 0) or 0), reverse=True)
                
                best_audio = audio_formats[0]
                abr = best_audio.get('abr')
                if abr is not None:
                    print(f"\nSelected format: {best_audio.get('format')} - {abr}kbps")
                else:
                    print(f"\nSelected format: {best_audio.get('format')} (bitrate unknown)")
                print("Starting download...")
            
                try:
                    # Download with best audio quality
                    info = ydl.extract_info(url)
                    audio_path = ydl.prepare_filename(info)
                except yt_dlp.utils.DownloadError as e:
                    raise ValueError(f"Failed to download video: {str(e)}")
                
                # Ensure the file exists after download
                if not os.path.exists(audio_path):
                    raise ValueError("Download completed but file not found - Check disk space and permissions")
                
                return audio_path
                
        except ValueError as e:
            print(f"Error: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error during video processing: {str(e)}")
            return None

def main():
    """Command line interface for testing video downloads"""
    print("YouTube Audio Downloader CLI")
    print("-" * 30)
    
    # Initialize downloader
    downloader = YouTubeVideoDownloader()
    
    while True:
        url = input("\nEnter YouTube URL (or 'q' to quit): ").strip()
        if url.lower() == 'q':
            break
            
        print("\nProcessing URL:", url)
        video_id = downloader.extract_video_id(url)
        if video_id:
            print(f"Extracted video ID: {video_id}")
            audio_path = downloader.download_video(url)
            if audio_path:
                print(f"\nSuccess! Audio saved to: {audio_path}")
            else:
                print("\nFailed to download audio")
        else:
            print("Failed to extract video ID")

if __name__ == "__main__":
    main()