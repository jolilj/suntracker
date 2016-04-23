from thresh_image import ThreshImage

im = ThreshImage("image.jpg")
im.show()
im.thresh(230)
center = im.getCenterOfMass()

im.image.putpixel((center[0],center[1]),150)
im.image.putpixel((center[0]+1,center[1]+1),150)
im.image.putpixel((center[0]-1,center[1]+1),150)
im.image.putpixel((center[0]+1,center[1]-1),150)
im.image.putpixel((center[0]-1,center[1]-1),150)
im.show()