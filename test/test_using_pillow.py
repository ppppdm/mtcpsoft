#import PIL
#help(PIL)

from PIL import Image
from PIL import ImageDraw, ImageFont

#help(Image)
# 2013041710510982-d137-0001-3.jpg 对于不完整的图片没有办法处理


imgfile = "../res/1.jpg"
f = open(imgfile)
print(1)
f.close()

img = Image.open("../res/1.jpg")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("arial.ttf", 50)
draw.text((100, 100), "hello", font=font)
#img.show()

img.save("../res/test_pillow_1.jpg")
