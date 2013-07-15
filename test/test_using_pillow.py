#import PIL
#help(PIL)
# -*- coding: gbk

from PIL import Image
from PIL import ImageDraw, ImageFont
import datetime

#help(Image)
# 2013041710510982-d137-0001-3.jpg 对于不完整的图片没有办法处理


imgfile = "../res/1.jpg"
f = open(imgfile)
print(1)
f.close()

t = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
img = Image.open("../res/1.jpg")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("arial.ttf", 50)
draw.text((100, 100), "hello " + t, font=font)
#img.show()

img.save("../res/test_pillow_1.jpg")


print(img.getbbox())
a, b, c, d = img.getbbox()
img.paste(img, (a, d))

img.save("../res/test_pillow_2.jpg")
#img.show()




img2 = Image.open("../res/6.26_hefei/20130626064148-dcd0-0001-1.jpg")
#print(img2.getbbox())
#print(img2.size)

# resize img
x1, y1 = img.size
x2, y2 = img.size
print(img.size)
img.resize((x1+x2, y1+y2))
print(img.size)
a, b, c, d = img.getbbox()

# montage img and img2
(a1, b1, c1, d1) = img2.getbbox()
#img.paste(img2, (a, d, c1, d+d1))
#img.show()


# create a new img
delta_y = 200
new_img = Image.new('RGB', (4*x1, y1+delta_y))

new_img.paste(img, (a, b+delta_y, c, d+delta_y))
new_img.paste(img, (a+c, b+delta_y, c+c, d+delta_y))
new_img.paste(img, (a+c+c, b+delta_y, c+c+c, d+delta_y))

draw = ImageDraw.Draw(new_img)
font = ImageFont.truetype("simsun.ttc", 200)
draw.text((0, 0), u'2013041710510982-d137-0001-3 违章地点： 方向： ', font=font)

close_up_img = img.transform(img.size, Image.EXTENT, (0, 0, 1000, 1000))
new_img.paste(close_up_img, (a+c+c+c, b+delta_y, c+c+c+c, d+delta_y))

new_img.show(img)


