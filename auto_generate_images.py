"""
🚀 Pelangi Pintar - PDF to Google Drive Auto-Upload Script
==========================================================

This script will:
1. Read your PDF files from Google Drive folder
2. Extract first 3 pages as images
3. Upload images to Google Drive automatically
4. Update MongoDB with image links

Requirements:
- Your PDFs must be in the Google Drive folder you shared
- Google Drive API credentials
"""

import asyncio
import os
import io
from pathlib import Path
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pdf2image import convert_from_path
from PIL import Image
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import pickle

# Load environment
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

# Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Configuration
GOOGLE_DRIVE_FOLDER_ID = "1c1pMnMYeCvMwIz2gVx5XG3XANEd-u2h2"  # Your shared folder ID
PDF_TEMP_DIR = "/tmp/ebook_pdfs"
IMAGE_TEMP_DIR = "/tmp/ebook_images"

# Create temp directories
os.makedirs(PDF_TEMP_DIR, exist_ok=True)
os.makedirs(IMAGE_TEMP_DIR, exist_ok=True)


def get_drive_service():
    """
    Authenticate with Google Drive API
    """
    creds = None
    token_path = ROOT_DIR / 'token.pickle'
    
    # Load saved credentials
    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # You need to create credentials.json from Google Cloud Console
            creds_path = ROOT_DIR / 'credentials.json'
            if not creds_path.exists():
                print("❌ credentials.json not found!")
                print("📝 Please follow Google Drive API setup guide")
                return None
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(creds_path), SCOPES)
                # Use run_local_server which works for both desktop and web credentials
                creds = flow.run_local_server(port=8090, open_browser=False)
                
                print("\n" + "="*60)
                print("✅ Authentication successful!")
                print("="*60 + "\n")
            except Exception as e:
                print(f"❌ Authentication error: {str(e)}")
                print("\n💡 Try running this command to authenticate:")
                print(f"   {str(creds_path)}")
                return None
        
        # Save credentials for next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('drive', 'v3', credentials=creds)


def download_pdf_from_drive(service, file_id, file_name):
    """
    Download PDF from Google Drive
    """
    try:
        request = service.files().get_media(fileId=file_id)
        file_path = os.path.join(PDF_TEMP_DIR, file_name)
        
        with open(file_path, 'wb') as f:
            downloader = request.execute()
            f.write(downloader)
        
        return file_path
    except Exception as e:
        print(f"❌ Error downloading {file_name}: {str(e)}")
        return None


def extract_pdf_pages(pdf_path, output_prefix, num_pages=3):
    """
    Extract first 3 pages from PDF as images
    """
    try:
        # Convert PDF pages to images
        images = convert_from_path(
            pdf_path,
            first_page=1,
            last_page=num_pages,
            dpi=150,
            fmt='jpeg'
        )
        
        image_paths = []
        for i, image in enumerate(images, start=1):
            # Resize to reasonable size (max width 800px)
            max_width = 800
            if image.width > max_width:
                ratio = max_width / image.width
                new_height = int(image.height * ratio)
                image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # Save image
            image_path = os.path.join(IMAGE_TEMP_DIR, f"{output_prefix}_page{i}.jpg")
            image.save(image_path, 'JPEG', quality=85, optimize=True)
            image_paths.append(image_path)
        
        return image_paths
    except Exception as e:
        print(f"❌ Error extracting pages: {str(e)}")
        return []


def upload_image_to_drive(service, image_path, folder_id=None):
    """
    Upload image to Google Drive and return shareable link
    """
    try:
        file_name = os.path.basename(image_path)
        
        file_metadata = {
            'name': file_name,
            'mimeType': 'image/jpeg'
        }
        
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        media = MediaIoBaseUpload(
            io.BytesIO(open(image_path, 'rb').read()),
            mimetype='image/jpeg',
            resumable=True
        )
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        file_id = file.get('id')
        
        # Make file publicly accessible
        service.permissions().create(
            fileId=file_id,
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()
        
        # Return direct view link
        return f"https://drive.google.com/uc?export=view&id={file_id}"
    
    except Exception as e:
        print(f"❌ Error uploading {image_path}: {str(e)}")
        return None


def list_pdfs_in_folder(service, folder_id):
    """
    List all PDF files in Google Drive folder
    """
    try:
        query = f"'{folder_id}' in parents and mimeType='application/pdf' and trashed=false"
        results = service.files().list(
            q=query,
            fields="files(id, name)",
            pageSize=100
        ).execute()
        
        files = results.get('files', [])
        return files
    except Exception as e:
        print(f"❌ Error listing files: {str(e)}")
        return []


async def update_ebook_images(ebook_id, image_links):
    """
    Update ebook in MongoDB with image links
    """
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        # Update pages array with image links
        pages = [
            {"page": 1, "color": "", "imageUrl": image_links[0]},
            {"page": 2, "color": "", "imageUrl": image_links[1] if len(image_links) > 1 else ""},
            {"page": 3, "color": "", "imageUrl": image_links[2] if len(image_links) > 2 else ""}
        ]
        
        result = await db.ebooks.update_one(
            {"id": ebook_id},
            {"$set": {"pages": pages, "hasRealImages": True}}
        )
        
        return result.modified_count > 0
    except Exception as e:
        print(f"❌ Error updating database: {str(e)}")
        return False
    finally:
        client.close()


async def match_pdf_to_ebook(pdf_name):
    """
    Match PDF filename to ebook in database
    Returns ebook ID if found
    """
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        # Try exact match first
        ebook = await db.ebooks.find_one({"fileName": pdf_name})
        
        if not ebook:
            # Try partial match
            clean_name = pdf_name.lower().replace('.pdf', '').replace('-', ' ').replace('_', ' ')
            ebooks = await db.ebooks.find().to_list(100)
            
            for eb in ebooks:
                eb_clean = eb['fileName'].lower().replace('.pdf', '').replace('-', ' ').replace('_', ' ')
                if clean_name in eb_clean or eb_clean in clean_name:
                    return eb['id'], eb['title']
        
        return (ebook['id'], ebook['title']) if ebook else (None, None)
    
    finally:
        client.close()


async def process_all_pdfs():
    """
    Main processing function
    """
    print("🚀 Starting PDF to Image Processing")
    print("=" * 60)
    
    # Step 1: Authenticate with Google Drive
    print("\\n📁 Connecting to Google Drive...")
    service = get_drive_service()
    
    if not service:
        print("❌ Failed to authenticate with Google Drive")
        print("\\n📝 Setup Instructions:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a new project or select existing")
        print("3. Enable Google Drive API")
        print("4. Create OAuth 2.0 credentials")
        print("5. Download as 'credentials.json' and place in /app/backend/")
        return
    
    print("✅ Connected to Google Drive")
    
    # Step 2: List all PDFs in folder
    print(f"\\n📂 Listing PDFs in folder...")
    pdfs = list_pdfs_in_folder(service, GOOGLE_DRIVE_FOLDER_ID)
    
    if not pdfs:
        print("❌ No PDFs found in folder!")
        print(f"   Folder ID: {GOOGLE_DRIVE_FOLDER_ID}")
        return
    
    print(f"✅ Found {len(pdfs)} PDF files")
    
    # Step 3: Process each PDF
    processed = 0
    skipped = 0
    
    for pdf_file in pdfs:
        pdf_id = pdf_file['id']
        pdf_name = pdf_file['name']
        
        print(f"\\n📄 Processing: {pdf_name}")
        print("-" * 60)
        
        # Match to ebook
        ebook_id, ebook_title = await match_pdf_to_ebook(pdf_name)
        
        if not ebook_id:
            print(f"   ⚠️  No matching ebook found in database, skipping...")
            skipped += 1
            continue
        
        print(f"   ✅ Matched to: {ebook_title} (ID: {ebook_id})")
        
        # Download PDF
        print(f"   📥 Downloading PDF...")
        pdf_path = download_pdf_from_drive(service, pdf_id, pdf_name)
        
        if not pdf_path:
            skipped += 1
            continue
        
        # Extract pages
        print(f"   🖼️  Extracting first 3 pages...")
        image_paths = extract_pdf_pages(pdf_path, f"ebook_{ebook_id}")
        
        if not image_paths:
            skipped += 1
            continue
        
        print(f"   ✅ Extracted {len(image_paths)} pages")
        
        # Upload images to Drive
        print(f"   ☁️  Uploading images to Google Drive...")
        image_links = []
        
        for img_path in image_paths:
            link = upload_image_to_drive(service, img_path, GOOGLE_DRIVE_FOLDER_ID)
            if link:
                image_links.append(link)
                print(f"      ✅ Uploaded page {len(image_links)}")
        
        if not image_links:
            skipped += 1
            continue
        
        # Update database
        print(f"   💾 Updating database...")
        success = await update_ebook_images(ebook_id, image_links)
        
        if success:
            print(f"   ✅ Successfully processed {pdf_name}")
            processed += 1
        else:
            print(f"   ❌ Failed to update database")
            skipped += 1
        
        # Cleanup temp files
        try:
            os.remove(pdf_path)
            for img_path in image_paths:
                os.remove(img_path)
        except:
            pass
    
    # Summary
    print("\\n" + "=" * 60)
    print("🎉 Processing Complete!")
    print(f"✅ Processed: {processed}")
    print(f"⚠️  Skipped: {skipped}")
    print("=" * 60)


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════╗
║  🚀 Pelangi Pintar - PDF Auto-Processor                  ║
║  Extracts PDF pages & uploads to Google Drive           ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    asyncio.run(process_all_pdfs())
