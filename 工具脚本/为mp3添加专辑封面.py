'''
专辑封面命名为cover.jpg   mp3放在同一目录下 运行本脚本即可
'''
import os
import eyed3
from PIL import Image

#限制jpg大小
JPGKB=30

folder_path = ''

cover_image_path = os.path.join(folder_path, "cover.jpg")
compressed_cover_path = os.path.join(folder_path, "compressed_cover.jpg")

with open(cover_image_path, "rb") as image_file:
    cover_image_data = image_file.read()

if len(cover_image_data) > JPGKB * 1024:
    img = Image.open(cover_image_path)

    img = img.resize((240, 75))

    while True:
        img.save(compressed_cover_path, format="JPEG", quality=85)  

        with open(compressed_cover_path, "rb") as compressed_image_file:
            cover_image_data = compressed_image_file.read()

        if len(cover_image_data) <= 20 * 1024:
            break

        img = img.resize((240, 75), Image.ANTIALIAS)
        img.save(compressed_cover_path, format="JPEG", quality=img.info['quality'] - 5)


for filename in os.listdir():
    if filename.endswith(".mp3"):
        mp3_file_path = os.path.join(folder_path, filename)
        audiofile = eyed3.load(mp3_file_path)

        if audiofile.tag:
            for image in audiofile.tag.images:
                audiofile.tag.images.remove(image.description)

            audiofile.tag.images.set(0, cover_image_data, "image/jpeg")
            audiofile.tag.save()

            print(f"新的专辑封面已添加到 {filename}")
        else:
            print(f"无法修改 {filename} 的标签")
