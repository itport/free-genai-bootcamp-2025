import yt_dlp

def explore_video_formats(url):
    try:
        # Configure yt-dlp options
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True
        }
        
        # Create yt-dlp object
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info
            info = ydl.extract_info(url, download=False)
            
            print(f'\nVideo Title: {info.get("title")}\n')
            
            # Get available formats
            formats = info.get('formats', [])
            
            print('Available Video Formats:')
            for f in formats:
                if f.get('vcodec') != 'none':
                    print(f'\nFormat ID: {f.get("format_id")}')
                    print(f'Extension: {f.get("ext")}')
                    print(f'Resolution: {f.get("resolution")}')
                    print(f'FPS: {f.get("fps")}')
                    print(f'Video Codec: {f.get("vcodec")}')
                    print(f'Audio Codec: {f.get("acodec")}')
                    print(f'Filesize: {f.get("filesize", 0) // 1024 // 1024} MB')
                    print('-' * 50)
            
            print('\nAvailable Audio-Only Formats:')
            for f in formats:
                if f.get('vcodec') == 'none' and f.get('acodec') != 'none':
                    print(f'\nFormat ID: {f.get("format_id")}')
                    print(f'Extension: {f.get("ext")}')
                    print(f'Audio Codec: {f.get("acodec")}')
                    print(f'Audio Quality: {f.get("format_note", "N/A")}')
                    print(f'Filesize: {f.get("filesize", 0) // 1024 // 1024} MB')
                    print('-' * 50)
                    
    except Exception as e:
        print(f'Error exploring video formats: {str(e)}')

if __name__ == '__main__':
    url = input('Enter YouTube URL: ')
    explore_video_formats(url)