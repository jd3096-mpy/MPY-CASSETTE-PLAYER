#同级目录自动添加cover.jpg到所有mp3文件  分辨率要求240x75 大小5K-15k
import os
import eyed3

folder_path = ""

cover_image_path = os.path.join(folder_path, "cover.jpg")
with open(cover_image_path, "rb") as image_file:
    cover_image_data = image_file.read()

for filename in os.listdir(folder_path):
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
