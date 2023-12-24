import os
import eyed3
from PIL import Image

folder_path = ''

cover_image_path = os.path.join(folder_path, "cover.jpg")
compressed_cover_path = os.path.join(folder_path, "compressed_cover.jpg")

# Load cover image
with open(cover_image_path, "rb") as image_file:
    cover_image_data = image_file.read()

# Check if cover image size is greater than 20KB, compress if needed
if len(cover_image_data) > 20 * 1024:
    img = Image.open(cover_image_path)

    # Resize the image to 240x75 pixels
    img = img.resize((240, 75))

    # Compress the image until it is below 20KB
    while True:
        img.save(compressed_cover_path, format="JPEG", quality=85)  # Adjust quality as needed

        with open(compressed_cover_path, "rb") as compressed_image_file:
            cover_image_data = compressed_image_file.read()

        if len(cover_image_data) <= 20 * 1024:
            break

        # Reduce quality further if still above 20KB
        img = img.resize((240, 75), Image.ANTIALIAS)
        img.save(compressed_cover_path, format="JPEG", quality=img.info['quality'] - 5)

# Loop through all MP3 files in the folder
for filename in os.listdir():
    if filename.endswith(".mp3"):
        mp3_file_path = os.path.join(folder_path, filename)
        audiofile = eyed3.load(mp3_file_path)

        if audiofile.tag:
            # Remove existing images from the tag
            for image in audiofile.tag.images:
                audiofile.tag.images.remove(image.description)

            # Set the compressed cover image as the album cover
            audiofile.tag.images.set(0, cover_image_data, "image/jpeg")
            audiofile.tag.save()

            print(f"新的专辑封面已添加到 {filename}")
        else:
            print(f"无法修改 {filename} 的标签")
