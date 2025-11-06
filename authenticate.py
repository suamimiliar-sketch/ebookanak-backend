"""
🔐 Google Drive Authentication Setup
Interactive authentication for Pelangi Pintar PDF Processor
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pickle

# Load environment
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
    """
    Interactive authentication with Google Drive
    """
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  🔐 Google Drive Authentication Setup                   ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    
    creds = None
    token_path = ROOT_DIR / 'token.pickle'
    creds_path = ROOT_DIR / 'credentials.json'
    
    # Check if we already have a token
    if token_path.exists():
        print("📁 Found existing token...")
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
        
        # Check if token is still valid
        if creds and creds.valid:
            print("✅ Token is valid! You're already authenticated.")
            print()
            print("🚀 You can now run: ./generate_images.sh")
            print()
            return True
        
        # Try to refresh expired token
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired token...")
            try:
                creds.refresh(Request())
                with open(token_path, 'wb') as token:
                    pickle.dump(creds, token)
                print("✅ Token refreshed successfully!")
                print()
                print("🚀 You can now run: ./generate_images.sh")
                print()
                return True
            except Exception as e:
                print(f"⚠️  Could not refresh token: {str(e)}")
                print("   Starting new authentication...")
    
    # Check if credentials.json exists
    if not creds_path.exists():
        print("❌ credentials.json not found!")
        print()
        print("📝 Please place your credentials.json file in:")
        print(f"   {ROOT_DIR}")
        print()
        return False
    
    print("🔐 Starting authentication process...")
    print()
    print("=" * 70)
    print("IMPORTANT: A local web server will start on port 8090")
    print("=" * 70)
    print()
    print("📝 Instructions:")
    print("1. A browser will attempt to open automatically")
    print("2. If it doesn't open, copy the URL shown below")
    print("3. Log in with your Google account")
    print("4. Click 'Allow' to grant permissions")
    print("5. You'll be redirected back - authentication complete!")
    print()
    print("=" * 70)
    print()
    
    try:
        # Create the flow with proper redirect URI for web credentials
        flow = InstalledAppFlow.from_client_secrets_file(
            str(creds_path),
            SCOPES
        )
        
        # Run local server (works with web credentials)
        print("🌐 Starting local authentication server on port 8090...")
        print()
        print("⚠️  If browser doesn't open automatically, copy this URL:")
        print()
        
        creds = flow.run_local_server(
            port=8090,
            open_browser=False,
            authorization_prompt_message='Please visit this URL to authorize: {url}',
            success_message='Authentication successful! You can close this window.'
        )
        
        # Save the credentials for next time
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
        
        print()
        print("=" * 70)
        print("✅ Authentication successful!")
        print("=" * 70)
        print()
        print("💾 Token saved to:", token_path)
        print()
        print("🚀 You can now run the PDF processor:")
        print("   cd /app/backend")
        print("   ./generate_images.sh")
        print()
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n❌ Authentication cancelled by user.")
        return False
    except Exception as e:
        print(f"\n❌ Authentication error: {str(e)}")
        print()
        print("💡 Troubleshooting:")
        print("   - Make sure port 8090 is not in use")
        print("   - Check that your credentials.json is correct")
        print("   - Try running the script again")
        print()
        return False


if __name__ == "__main__":
    success = authenticate()
    exit(0 if success else 1)
