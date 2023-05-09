import os
import sys
from PIL import Image, ImageSequence

MAX_WIDTH = 1920
MAX_HEIGHT = 1080


def optimize_attachment(file_path):
    if '*' in file_path:
        return
    if os.path.splitext(file_path)[1].lower() == '.gif':
        return optimize_gif(file_path, 3, (300, 180))
    return optimize_image(file_path)


def optimize_gif(file_path, reduction_ratio, size):
    with Image.open(file_path) as im:
        frames = []
        # フレーム数を減らす＆リサイズする
        for i, frame in enumerate(ImageSequence.Iterator(im)):
            frame = frame.resize(size, Image.ANTIALIAS)
            if i % reduction_ratio == 0:
                frames.append(frame.copy())
        # 最適化して保存する
        frames[0].save(file_path, save_all=True, append_images=frames[1:],
                       optimize=True, quality="85")
        return file_path


def optimize_image(file_path):
    with Image.open(file_path) as im:
        w, h = im.size
        if w > MAX_WIDTH and h > MAX_HEIGHT:
            if w > MAX_WIDTH*3 or h > MAX_HEIGHT*3:
                im = im.resize((w//4, h//4))
            elif w > MAX_WIDTH*2 or h > MAX_HEIGHT*2:
                im = im.resize((w//3, h//3))
            else:
                im = im.resize((w//2, h//2))
            print(f'{file_path} {w}x{h} reduce {im.size[0]}x{im.size[1]}')
        name, ext = os.path.splitext(
            file_path)[0], os.path.splitext(file_path)[1]
        if ext.lower() in ('.png', '.jpg', '.jpeg', '.webp'):
            new_file_path = name + '.webp'
        else:
            new_file_path = file_path + '.webp'
        im.save(new_file_path, 'webp', optimize=True)
        os.remove(file_path)
        return new_file_path


if __name__ == "__main__":
    if not sys.argv[1]:
        sys.exit(1, 'Invalid argument')
    file_path = sys.argv[1]
    optimize_attachment(file_path)
