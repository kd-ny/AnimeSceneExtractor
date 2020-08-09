import os

import cv2
import imagehash
from PIL import Image


def cv2pil(image):
    """
    cv2 → pil 変換
    :param image:
    :return:
    """
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)

    return new_image


def save_all_frames(video_path, output_path, hash_distance, ext='jpg'):
    """
    指定した動画ファイルから、全フレームを画像として展開する

    :param video_path:
    :param output_path:
    :param ext:
    :return:
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(video_path)

    capture = cv2.VideoCapture(video_path)
    if not capture.isOpened():
        print('aaa')
        return

    n = 0
    before_image_hash = None

    while True:
        ret, frame = capture.read()
        if not ret:
            return

        image_path = output_path + '{}.{}'.format(n, ext)

        n += 1
        pil_img = cv2pil(frame)
        current_image_hash = imagehash.dhash(pil_img)
        if before_image_hash is None:
            pil_img.save(image_path)
            before_image_hash = current_image_hash
            print('save file. :{}'.format(image_path))
            continue

        if current_image_hash - before_image_hash > hash_distance:
            pil_img.save(image_path)
            before_image_hash = current_image_hash
            print('save file. :{}'.format(image_path))
            continue

        print('not scene. :{}'.format(n))
        continue


# 抽出対象動画ファイル
video_path = 'd:/test.mp4'
# 抽出先ディレクトリ
output_path = 'd:/tmp/'
# 抽出対象ハミング距離
hash_distance = 30

try:
    t = save_all_frames(video_path, output_path, hash_distance)
except Exception as e:
    print('{}: {}'.format(e.__class__, e))
