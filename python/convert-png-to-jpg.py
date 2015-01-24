from PIL import Image
import glob

#im = Image.open(r"C:\jk.png")
#bg = Image.new("RGB", im.size, (255,255,255))
#bg.paste(im,im)
#bg.save(r"C:\jk2.jpg")

print glob.glob('E:/lifome/product-img-edited/*.png')

# box = im.crop(left_up_x,left_up_y, right_down_x, right_down_y)
