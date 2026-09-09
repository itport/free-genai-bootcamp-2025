from urllib.parse import urlparse, parse_qs
import requests
from format_azure_blob import format_azure_url

def test_azure_blob_access(url):
    """
    Test access to Azure Blob Storage using the provided URL.
    Validates URL structure and attempts to access the resource.
    
    Args:
        url (str): The Azure Blob Storage URL to test
        
    Returns:
        bool: True if access is successful, False otherwise
    """
    try:
        # Format and validate the URL structure
        formatted_url = format_azure_url(url)
        
        # Verify required parameters
        params = formatted_url['parameters']
        required_params = ['sp', 'st', 'se', 'spr', 'sv', 'sr', 'sig']
        
        for param in required_params:
            if not params[param]:
                print(f"Missing required parameter: {param}")
                return False
        
        # Test access to the blob
        print("\nTesting access to Azure Blob Storage...")
        response = requests.head(url)
        
        if response.status_code == 200:
            print("✓ Successfully accessed the blob")
            print(f"Content Type: {response.headers.get('Content-Type')}")
            print(f"Content Length: {response.headers.get('Content-Length')} bytes")
            return True
        else:
            print(f"✗ Failed to access blob. Status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error testing Azure Blob access: {str(e)}")
        return False

# Test URL from the previous example
test_url = "https://satranscription.blob.core.windows.net/transcription-unit-tests/That%20Little%20Voice.mp4?sp=r&st=2024-08-06T21:52:25Z&se=2027-04-01T05:52:25Z&spr=https&sv=2022-11-02&sr=b&sig=BMH0oUSmMlzne5%2BuFK0L6z2P6So8OOubieAk%2BVIpIiE%3D"

if __name__ == "__main__":
    print("Azure Blob Storage Access Test")
    print("-" * 30)
    
    # Display formatted URL structure
    formatted_url = format_azure_url(test_url)
    print("\nURL Structure:")
    print(f"Base URL: {formatted_url['base_url']}")
    print("\nParameters:")
    for key, value in formatted_url['parameters'].items():
        print(f"{key}: {value}")
    
    print("\nTesting Access:")
    success = test_azure_blob_access(test_url)
    
    if success:
        print("\n✓ All tests passed successfully!")
    else:
        print("\n✗ Some tests failed. Please check the output above for details.")