# %%
import easyocr
import PIL
from PIL import ImageDraw
# %%
reader = easyocr.Reader(['bn'])

image_name = '../input/1.JPG'

result = reader.readtext(image_name)
result
# %%
# img = cv2.imread('chinese_tra.jpg')
# result = reader.readtext(img)

# Draw bounding boxes
def draw_boxes(image, bounds, color='green', width=2):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        p0, p1, p2, p3 = bound[0]
        draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
    return image
im = PIL.Image.open(image_name)
draw_boxes(im, result)
# %%
