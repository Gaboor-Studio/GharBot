import imagehash
import videohash
from PIL import Image
import cv2
import numpy as np

def gethash_by_image(img_to_hash):
    """
    :param img_to_hash: should be PIL.Image format
    :return: string hash
    """
    return str(imagehash.average_hash(img_to_hash))

def gethasharray_by_video(video_address_to_hash):
    """
    :param video_address_to_hash: should be an url or filesystem address
    :return: big string hash
    """
    hash_string=""
    cap = cv2.VideoCapture(video_address_to_hash)
    frames, img = cap.read()
    while frames:
        hash_string+=gethash_by_image(Image.fromarray(np.uint8(img)).convert('RGB'))+","
        # read next frame
        frames, img = cap.read()
    return hash_string

def compare_pics_hash(hash_str1,hash_str2):
    hash1=imagehash.hex_to_hash(hash_str1)
    hash2=imagehash.hex_to_hash(hash_str2)
    # Minus operand in imagehash library has defined like abs of minus . so we don't need to get abs of the result .
    if hash1-hash2 <=5 :
        #print(hash1 - hash2)
        return True
    else:
        #print(hash1 - hash1)
        return False

def compare_videos(hash_vid1,hash_vid2):
    if len(hash_vid1)!=len(hash_vid2):
        return False
    first_hasharray=hash_vid1.split(",")
    second_hasharray=hash_vid2.split(",")
    diffrence_number=0
    for i in range(0,len(first_hasharray)-1):
        diffrence_number+=(imagehash.hex_to_hash(first_hasharray[i])-imagehash.hex_to_hash(second_hasharray[i]))
    if diffrence_number<=10:
        return True
    else:
        return False

def compare_sound():
    pass

def test_compare_pics():
    print(compare_pics_hash(gethash_by_image(Image.open("1.jpg")),gethash_by_image(Image.open("2.jpg"))))

def test_compare_videos():
    #compare_videos("https://raw.githubusercontent.com/akamhy/videohash/main/assets/rocket.mkv","https://www.youtube.com/watch?v=PapBjpzRhnA")
    print(compare_videos(gethasharray_by_video("first.mp4"),gethasharray_by_video("second.mp4")))
#test_compare_pics()
test_compare_videos()