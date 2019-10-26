import Augmentor
import csv
from os import listdir, rename, system
from os.path import isfile, join

DASIZE=2204*5

p = Augmentor.Pipeline("/peltarion/data/train/image")
p.ground_truth("/peltarion/data/train/mask")
p.rotate(probability=1, max_left_rotation=5, max_right_rotation=5)
p.flip_left_right(probability=0.5)
p.zoom_random(probability=0.5, percentage_area=0.8)
p.flip_top_bottom(probability=0.5)
p.sample(DASIZE)

system('mkdir -p /peltarion/data/train/image/output/image')
system('mkdir -p /peltarion/data/train/image/output/mask')
system('mv /peltarion/data/train/image/output/i* /peltarion/data/train/image/output/image')
system('mv /peltarion/data/train/image/output/_* /peltarion/data/train/image/output/mask')


with open('/peltarion/data/train/image/output/index.csv', mode='w') as mywriter:
    mywriter = csv.writer(mywriter, delimiter=',')
    mywriter.writerow(['image', 'mask', 'subset'])
    images_path='/peltarion/data/train/image/output/image/'
    images = [f for f in listdir(images_path) if isfile(join(images_path, f))]
    mask_path='/peltarion/data/train/image/output/mask/'
    masks = [f for f in listdir(mask_path) if isfile(join(mask_path, f))]
    for i, f in enumerate(images):
        mywriter.writerow(['image/{}'.format(f), 'mask/{}'.format(masks[i]), 'T'])
