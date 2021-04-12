import imagehash
import videohash
from PIL import Image

def gethash_by_image(img_to_hash):
    return str(imagehash.average_hash(img_to_hash))

def compare_pics_hash(hashstr1,hashstr2):
    hash1=imagehash.hex_to_hash(hashstr1)
    hash2=imagehash.hex_to_hash(hashstr2)
    # Minus operand in imagehash library has defined like abs of minus . so we don't need to get abs of the result .
    if hash1-hash2 <=1 :
        #print(hash1 - hash2)
        return True
    else:
        #print(hash1 - hash1)
        return False

def compare_videos(vid1,vid2):
    vid1_hash=videohash.from_path(vid1)
    vid2_hash=videohash.from_path(vid2)
    pass

def test_compare_pics():
    print(compare_pics_hash(gethash_by_image(Image.open("1.jpg")),gethash_by_image(Image.open("2.jpg"))))

def test_compare_videos():
    compare_videos("","")
    pass

test_compare_pics()