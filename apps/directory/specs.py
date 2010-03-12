from imagekit.specs import ImageSpec 
from imagekit import processors 

# first we define our thumbnail resize processor 
class ResizeThumb(processors.Resize): 
    width = 250 
    height = 250 

# and adminthumbnail resize processor 
class ResizeAdminThumb(processors.Resize): 
    width = 40 
    height = 40 
    crop = True

# now we define a display size resize processor
class ResizeDisplay(processors.Resize):
    width = 800
    height = 800

# now lets create an adjustment processor to enhance the image at small sizes 
class EnchanceThumb(processors.Adjustment): 
    contrast = 1.2 
    sharpness = 1.1 

# now we can define our thumbnail spec 
class Thumbnail(ImageSpec): 
    access_as = 'thumbnail_image' 
    pre_cache = True 
    processors = [ResizeThumb, EnchanceThumb] 

# now we can define our thumbnail spec 
class AdminThumbnail(ImageSpec): 
    access_as = 'admin_thumbnail' 
    pre_cache = True 
    processors = [ResizeAdminThumb, EnchanceThumb] 

# and our display spec
class Display(ImageSpec):
    # increment_count = True
    processors = [ResizeDisplay]