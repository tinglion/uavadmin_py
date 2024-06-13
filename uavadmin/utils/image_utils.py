from PIL import Image


def resize_img(fn_src, fn_dst, scale_factor=2):
    try:
        # 打开图像文件
        image = Image.open(fn_src)

        # 获取原始图像的宽度和高度
        original_width, original_height = image.size

        # 计算新的宽度和高度
        new_width = original_width * scale_factor
        new_height = original_height * scale_factor

        # 使用resize()方法来放大图像
        enlarged_image = image.resize((new_width, new_height))

        # 保存放大后的图像
        enlarged_image.save(fn_dst)

        return True
    except Exception as e:
        print(f"ERROR {e}")

    return False
