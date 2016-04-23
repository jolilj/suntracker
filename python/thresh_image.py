from PIL import Image
import math

class ThreshImage:
	def __init__(self, im_string, w=-1, h=-1):
		if(w==-1 or h==-1):
			self.image = Image.open(im_string).convert('LA')
		else:
			self.image = Image.fromstring("RGBA",(w,h),im_string).convert('LA')
		self.isThreshed = 0
	
	#Threshold the image	
	def thresh(self,level):
		self.image = self.image.point(lambda i: i > level and 255)
		self.isThreshed = 1

	def resize(self, w, h):
		self.image = self.image.resize((w, h))

	#Get region of interest, returns array with pixel indices
	def getROI(self):
		h = self.image.size[1]
		w = self.image.size[0]
		if not self.isThreshed:
			print("Threshold image first by image.thresh(level)")
			return []
		#Get pixels in vector form
		pixels = list(self.image.getdata(0))

		#array for storing region id's, each connected region has a unique id
		regionIds = []
		for i in range(0,len(pixels)):
			regionIds.append(-1)

		#counters
		prevc = 0
		c = 0

		#Generate region ids
		for i in range(0,h):
			for j in range(0, w):
				index = j+i*w
				if pixels[index]==255:
					if c == 0:
						regionIds[index]=c
						c+=1
					elif (i>0 and pixels[index-w]==255):
							regionIds[index] = regionIds[index-w]
							if prevc > 0:
								for k in range(0,prevc):
									regionIds[index-k-1] = regionIds[index]
					elif (prevc > 0):
							regionIds[index]=regionIds[index-1]
					else:
						c += 1
						regionIds[index] = c

					prevc +=1
				else:
					prevc = 0
			prevc=0

		#Get regions
		regions = []
		for i in range(0, c+1):
			regions.append([])

		maxLen = 0
		idx = 0
		for i in range(0, len(regionIds)):
			if (regionIds[i] != -1):
				regions[regionIds[i]].append(i)
				l = len(regions[regionIds[i]])
				if ( l > maxLen):
					maxLen = l 
					idx = regionIds[i]

		#Region of interest(ROI) - biggest region
		if (len(regions)!=0):			
			maxRegion = regions[idx]
		return maxRegion

	#Get center of mass of region of interest, returns x,y and corresponding 1D vector index
	def getCenterOfMass(self):
		h = self.image.size[1]
		w = self.image.size[0]
		maxRegion = self.getROI()
		if (len(maxRegion) == 0):
			return []
		x = 0
		y = 0

		# Calculate center of mass
		for i in range(0, len(maxRegion)):
			index = maxRegion[i]
			x += index%w
			y += math.floor(index/w)

		center_x = int(x/len(maxRegion))
		center_y = int(y/len(maxRegion))
		pixel_idx = center_y*w + center_x

		return [center_x, center_y, pixel_idx]

	def show(self):
		self.image.show()

