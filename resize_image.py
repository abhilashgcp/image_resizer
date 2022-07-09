import os
import enum
import argparse
from PIL import Image
from PIL.Image import Resampling

class SIZE_UNIT(enum.Enum):
   BYTES = 1
   KB = 2
   MB = 3
   GB = 4

def convert_unit(size_in_bytes, unit):
   if unit == SIZE_UNIT.KB:
       return size_in_bytes/1024
   elif unit == SIZE_UNIT.MB:
       return size_in_bytes/(1024*1024)
   elif unit == SIZE_UNIT.GB:
       return size_in_bytes/(1024*1024*1024)
   else:
       return size_in_bytes

class DestImage:
    def __init__(self, source, dest, resize, optimize, quality):
        self.dest = dest
        self.source = source
        self.resize = resize
        self.optimize = optimize
        self.quality = quality
        self.image = Image.open(self.source)
        print ("Orginal Picture Dimensions")
        print ("==========================")
        print ("Width: {} , Height: {}".format(self.image.size[0],self.image.size[1]))
        print ("Disk Size: {} KB".format(convert_unit(os.stat(self.source).st_size, SIZE_UNIT.KB)))
        print ("++++++++++++++++++++++++++++\n")

    def resize_image(self):
        self.image = self.image.resize((int(self.resize[0]),int(self.resize[1])), Resampling.LANCZOS)
    
    def optimize_save(self):
        print ("Updated Picture Dimensions")
        print ("==========================")
        print ("Width: {} , Height: {}".format(self.image.size[0],self.image.size[1]))
        self.image.save(self.dest, optimize=self.optimize, quality=95)
        print ("Disk Size: {} KB".format(convert_unit(os.stat(self.dest).st_size, SIZE_UNIT.KB)))
        print ("++++++++++++++++++++++++++++\n")

def main():
    parser = argparse.ArgumentParser(description='!!!!!!!! IMAGE ReSIZER !!!!!!')   
    parser.add_argument ('-p', '--pixels', dest = 'pixels', nargs=2)
    parser.add_argument ('-s', '--source_image', dest = 'source_image')
    parser.add_argument ('-d', '--dest_image', dest = 'dest_image' )
    parser.add_argument ('-o', '--optimize', dest = 'optimize', default = True )
    parser.add_argument ('-q', '--quality', dest = 'quality', default = 95 )
    args = parser.parse_args()

    image = DestImage(args.source_image, args.dest_image, args.pixels, args.optimize, args.quality)
    image.resize_image()
    image.optimize_save()

if __name__ == "__main__":
    main ()

'''
SAMPLE COMMAND FOR RESIZING IMAGE
 python3 resize_image.py -p Width Height -s source.jpg -d dest.jpg
'''