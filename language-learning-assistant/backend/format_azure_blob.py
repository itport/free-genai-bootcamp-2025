from urllib.parse import urlparse, parse_qs

def format_azure_url(url):
    """
    Format an Azure Blob Storage URL for better readability.
    Parses the URL and organizes its components and query parameters.
    
    Args:
        url (str): The Azure Blob Storage URL to format
        
    Returns:
        dict: A dictionary containing the formatted URL components
    """
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Parse query parameters
    query_params = parse_qs(parsed_url.query)
    
    # Create a structured representation
    structured_url = {
        'base_url': f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}",
        'parameters': {
            'sp': query_params.get('sp', [None])[0],  # Read permission
            'st': query_params.get('st', [None])[0],  # Start time
            'se': query_params.get('se', [None])[0],  # Expiry time
            'spr': query_params.get('spr', [None])[0],  # Protocol
            'sv': query_params.get('sv', [None])[0],  # Storage version
            'sr': query_params.get('sr', [None])[0],  # Resource type
            'sig': query_params.get('sig', [None])[0]  # Signature
        }
    }
    
    return structured_url

# Example URL
test_url = "https://satranscription.blob.core.windows.net/transcription-unit-tests/That%20Little%20Voice.mp4?sp=r&st=2024-08-06T21:52:25Z&se=2027-04-01T05:52:25Z&spr=https&sv=2022-11-02&sr=b&sig=BMH0oUSmMlzne5%2BuFK0L6z2P6So8OOubieAk%2BVIpIiE%3D"

# Format and display the URL structure
if __name__ == "__main__":
    formatted_url = format_azure_url(test_url)
    
    print("Azure Blob Storage URL Structure:")
    print("\nBase URL:")
    print(formatted_url['base_url'])
    print("\nParameters:")
    for key, value in formatted_url['parameters'].items():
        print(f"{key}: {value}")