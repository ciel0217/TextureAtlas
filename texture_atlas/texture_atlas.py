from PIL import Image

# 画像を読み込む
image1 = Image.open("1.jpeg")
image2 = Image.open("2.jpeg")

# アトラス用の大きなキャンバスを作成
atlas_width = image1.width + image2.width
atlas_height = image1.height + image2.height
atlas = Image.new('RGBA', (atlas_width, atlas_height))

# 画像を配置
atlas.paste(image1, (0, 0))
atlas.paste(image2, (0, image1.height))
##hello
# アトラスを保存
atlas.save("atlas.png")
