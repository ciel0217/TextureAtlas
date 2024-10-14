from PIL import Image
import csv

# Open the CSV file
with open('example.csv', mode='r', newline='') as file:
    csv_reader = csv.reader(file)
    # Loop through the rows in the CSV file

    sorted_data = sorted(csv_reader, key=lambda x: (x[1], x[2]))

    max_x = -1
    max_y = -1

    for data in sorted_data:
        if max_x < int(data[1]):
            max_x = int(data[1])
        
        if max_y < int(data[2]):
            max_y = int(data[2])

    atlas_height = [0] * (max_x + 1)
    atlas_width = [0] * (max_y + 1)

    for data in sorted_data:
        atlas_height[int(data[1])] += int(data[4])
        atlas_width[int(data[2])] += int(data[3])
        
    max_height = max(atlas_height)
    max_width = max(atlas_width)

    # まず最初の入力画像のフォーマットを確認して出力フォーマットを選択
    first_image_path = sorted_data[0][0]
    first_image = Image.open(first_image_path)
    image_format = first_image.format

    if image_format == 'JPEG':
        atlas_mode = 'RGB'  # JPEGにはアルファチャンネルがない
    elif image_format == 'PNG' and first_image.mode == 'I;16':
        atlas_mode = 'I;16'  # 16bit PNGの場合
    else:
        atlas_mode = 'RGBA'  # デフォルトでRGBA

    # 選択したモードに基づいてアトラスを作成
    atlas = Image.new(atlas_mode, (max_width, max_height))

    x = [0] * (max_y + 1)
    y = [0] * (max_x + 1)

    for data in sorted_data:
        image_path = data[0]
        image = Image.open(image_path)

        # 画像のリサイズ
        image = image.resize((int(data[3]), int(data[4])))

        in_x, in_y = 0, 0
        if int(data[1]) != 0:
            in_x = x[int(data[2])]
        
        in_y = y[int(data[1])]

        # アトラスに画像をペースト
        atlas.paste(image, (in_x, in_y))

        x[int(data[2])] += int(data[3])
        y[int(data[1])] += int(data[4])

    # 入力画像の形式に基づいたファイル名とフォーマットで保存
    output_format = image_format  # 入力フォーマットをそのまま使用
    output_file = f"atlas.{output_format.lower()}"

    # 適切なフォーマットで保存
    atlas.save(output_file, format=output_format)
    print(f"Atlas saved as {output_file} with format {output_format}")
