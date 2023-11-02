#同级目录自动添加cover.jpg到所有mp3文件  分辨率要求240x75 大小5K-15k
import os
import eyed3

# 文件夹路径
folder_path = "/your/folder/path"

# 读取封面图像数据
cover_image_path = os.path.join(folder_path, "cover.jpg")
with open(cover_image_path, "rb") as image_file:
    cover_image_data = image_file.read()

# 遍历文件夹中的每个文件
for filename in os.listdir(folder_path):
    if filename.endswith(".mp3"):
        mp3_file_path = os.path.join(folder_path, filename)
        audiofile = eyed3.load(mp3_file_path)

        if audiofile.tag:
            for image in audiofile.tag.images:
                audiofile.tag.images.remove(image.description)

            # 设置封面图像
            audiofile.tag.images.set(0, cover_image_data, "image/jpeg")
            audiofile.tag.save()

            print(f"新的专辑封面已添加到 {filename}")
        else:
            print(f"无法修改 {filename} 的标签")

