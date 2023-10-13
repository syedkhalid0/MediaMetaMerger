import os
import argparse
import zipfile
import json
import shutil
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def extract_metadata(media_file_path, metadata_folder):
    # Extract metadata from a JSON file associated with the media file
    media_filename = os.path.basename(media_file_path)
    metadata_filename = os.path.splitext(media_filename)[0] + '.json'
    metadata_path = os.path.join(metadata_folder, metadata_filename)

    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as metadata_file:
            return json.load(metadata_file)
    else:
        return None

def merge_media_with_metadata(input_folder, output_folder):
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            media_file_path = os.path.join(root, filename)

            if filename.lower().endswith(('.avif', '.bmp', '.gif', '.heic', '.ico', '.jpg', '.png', '.tiff', '.webp', '.3gp', '.3g2', '.asf', '.avi', '.divx', '.m2t', '.m2ts', '.m4v', '.mkv', '.mmv', '.mod', '.mov', '.mp4', '.mpg', '.mts', '.tod', '.wmv', '.jpeg')):
                # Extract metadata
                metadata = extract_metadata(media_file_path, input_folder)

                if metadata:
                    # Copy the media file to the output folder
                    media_dest_path = os.path.join(output_folder, filename)
                    shutil.copy(media_file_path, media_dest_path)

                    # You can now use the 'metadata' variable to work with the metadata as needed.
                    print(f'Merged {filename} with metadata.')

def main():
    parser = argparse.ArgumentParser(description="MediaMetaMerger is designed to be straightforward, efficient, and compatible with Google Takeout photos.")
    parser.add_argument('-z', '--zip', help="Path to a zip file containing media and metadata.")
    parser.add_argument('-i', '--input', help="Path to a folder containing media and metadata.")
    parser.add_argument('-o', '--output', help="Path to the output folder.")
    args = parser.parse_args()

    if args.zip and args.input:
        print("Choose either '-z' or '-i', not both.")
        return
    

    if not args.output:
        args.output = os.path.join(os.getcwd(), "Output")

    os.makedirs(args.output, exist_ok=True)

    if args.zip:
        with zipfile.ZipFile(args.zip, 'r') as zip_ref:
            zip_ref.extractall(args.output)
    
    merge_media_with_metadata(args.input if args.input else args.output, args.output)

if __name__ == "__main__":
    main()