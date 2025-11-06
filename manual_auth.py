"""
🔐 Google Drive Manual Authentication
Copy/Paste authentication for remote servers
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import pickle

# Load environment
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive']

def manual_authenticate():
    """
    Manual authentication - user copies authorization code
    """
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  🔐 Google Drive Manual Authentication                  ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    
    token_path = ROOT_DIR / 'token.pickle'
    creds_path = ROOT_DIR / 'credentials.json'
    
    # Check existing token
    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
        
        if creds and creds.valid:
            print("✅ Already authenticated!")
            return True
    
    if not creds_path.exists():
        print("❌ credentials.json not found!")
        return False
    
    # Create flow with manual redirect
    flow = InstalledAppFlow.from_client_secrets_file(
        str(creds_path),
        SCOPES,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    )
    
    # Generate authorization URL
    auth_url, _ = flow.authorization_url(
        access_type='offline',
        prompt='consent'
    )
    
    print("=" * 70)
    print("STEP 1: Open this URL in your browser")
    print("=" * 70)
    print()
    print(auth_url)
    print()
    print("=" * 70)
    print("STEP 2: Log in and authorize the application")
    print("=" * 70)
    print()
    print("=" * 70)
    print("STEP 3: Google will show you an authorization code")
    print("        Copy the ENTIRE code (it's long!)")
    print("=" * 70)
    print()
    
    code = input("📋 Paste the authorization code here: ").strip()
    
    if not code:
        print("❌ No code provided")
        return False
    
    try:
        print()
        print("🔄 Verifying code...")
        
        # Exchange code for token
        flow.fetch_token(code=code)
        creds = flow.credentials
        
        # Save token
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
        
        print()
        print("=" * 70)
        print("✅ Authentication successful!")
        print("=" * 70)
        print()
        print(f"💾 Token saved to: {token_path}")
        print()
        print("🚀 Now run: ./generate_images.sh")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print()
        print("💡 Make sure you copied the entire code")
        return False

if __name__ == "__main__":
    success = manual_authenticate()
    exit(0 if success else 1)
