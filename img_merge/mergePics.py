# -*- coding:utf-8 -*-
# auther : pdm
# email : ppppdm@gmail.com

# In : 3 pics of one group , info str for whole merge imgs , watermark for each imgs, close_up_para
# Out: merged pic

from PIL import Image, ImageDraw, ImageFont

info_box_scale = 0.08
info_text_scale = 0.8
watermask_scale = 0.08
watermask_color = (255, 128, 0)
info_text_color = (255, 255, 255)
info_text_pos = (0, 0)
watermask_pos = (0, 0)
info_text_font = "simsun.ttc"
watermask_font = "simsun.ttc"

def merge_pic(imgfiles, infos_str, marks, close_up_para):
    
    imgs = list()
    
    if len(imgfiles) == 0 or len(imgfiles) != len(marks):
        print('parameter error')
        return
    
    # open the img files
    try:
        for i in imgfiles:
            imgs.append(Image.open(i))
    except Exception as e:
        print(e)
        return
        
    # get img infos
    img1 = imgs[0]
    size = img1.size
    mode = img1.mode
    bbox = img1.getbbox()
    info_box_y = int(size[1]*info_box_scale)
    
    # compose the imgs
    new_size = ((len(imgs)+1)*size[0], info_box_y+size[1])
    new_img = Image.new(mode, new_size)
    
    # draw the close-up pic
    close_up_num = close_up_para[0]
    crop_img = imgs[close_up_num]
    x = close_up_para[1][0]
    y = close_up_para[1][1]
    delta_x = close_up_para[2]
    delta_y = int(delta_x * size[1] / size[0])
    close_up_img = crop_img.transform(size, Image.EXTENT, (x-delta_x, y-delta_y, x+delta_x, y+delta_y))
    imgs.append(close_up_img)
    marks.append(marks[close_up_num])
    
    
    # draw the watermask to each imgs
    watermask_pixel_size = int(size[1]*watermask_scale)
    for i in imgs:
        draw = ImageDraw.Draw(i)
        font = ImageFont.truetype(watermask_font, watermask_pixel_size)
        index = imgs.index(i)
        watermask = marks[index]
        draw.text(watermask_pos, watermask, font=font, fill=watermask_color)
    
    count = 0
    for i in imgs:
        new_img.paste(i, (bbox[0]+count*bbox[2], bbox[1]+info_box_y, bbox[2]+count*bbox[2], bbox[3]+info_box_y))
        count+=1
    
    # draw the info str
    info_str_size = int(info_box_y * info_text_scale)
    draw=ImageDraw.Draw(new_img)
    font = ImageFont.truetype(info_text_font, info_str_size)
    draw.text(info_text_pos, infos_str, font=font, fill=info_text_color)
    
    
    # save the new merged pic
    # void
    
    #new_img.show()
    return new_img

info_items = [('设备编号：', 'MAC'), 
              ('违法地点：', 'ROAD'),
              ('方向：', 'DIRECT'), 
              ('违法时间：', 'RTC'), 
              ('禁行时间：', 'ROAD TIME')]

def merge_group_imgs(infos_list, save_path):
    if len(infos_list) != 3:
        print('infos not enough or too much!')
        return
    
    imgfiles = list()
    infostr = ''
    marks = list()
    
    for i in infos_list:
        imgfiles.append(i['FILE'])
        marks.append(i['RTC'])
    
    infos = infos_list[0]
    for i in info_items:
        s = infos.get(i[1], '')
        if s == '':
            print('get '+ i[0] +' item from pic None!')
            return
        infostr += i[0]+s+' '
    
    close_up_para = [2, (650, 600), 250]
    new_img = merge_pic(imgfiles, infostr, marks, close_up_para)
    
    # save new_img
    new_img.save(save_path)

    return

if __name__=='__main__':
    print(__file__, 'test')
    imgfiles = ['../res/6.26_hefei/20130626064148-dcd0-0001-1.jpg', '../res/6.26_hefei/20130626064154-dcd0-0001-2.jpg', '../res/6.26_hefei/20130626064154-dcd0-0001-3.jpg']
    infostr = '设备编号：08-00-28-12-dc-10  违法地点：人民中路(无为路-环城南路)  方向：西向东  违法时间：2013-06-28 17:33:49.471  禁行时间：7:00-20:00'
    marks = ['2013-06-28 17:33:49.471', '2013-06-28 17:33:50.233', '2013-06-28 17:33:50.409']
    close_up_para = [2, (650, 600), 250]
    new_img = merge_pic(imgfiles, infostr, marks, close_up_para)
    new_img.show()
    
    
    
    
