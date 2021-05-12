import cv2
import argparse
import numpy as np
from Errors import *

np.random.seed(123) 

class Produce:
	def __init__(self,imagePath,charNum,resizeSZ,shuffleNum):
		self.image = cv2.imread(imagePath,0)
		h,w = self.image.shape
		self.num = charNum
		self.resizeSZ = resizeSZ
		self.limitw,self.limith = resizeSZ,resizeSZ
		if float(w) / h <= 1.2 and float(w) / h >= 0.9 :
			pass
		else:
			if w > h:
				self.limitw += 0.4
			else:
				self.limith += 0.4
		self.shuffleNum = shuffleNum
		self.validNums = [3,5,15,17] 
		self.chars = ['`', '!', '#', '$', '%', '^','&', '*', '(', ')', '-', '_', '[', ']', '{', '.', '/',
					'}', '|',"'", ',', '<', '>', ';', ':',"ɘ","ɿ","ƚ","ɒ","ƨ","ʇ","ǫ","ʜ","ʞ","ɔ"]
		for _ in range(self.shuffleNum): np.random.shuffle(self.chars)


	def separate(self,image):
		H,W = image.shape
		sepSize = 0
		org = 255 // self.num 
		ps = {}
		for i in range(self.num+1):
			p = cv2.inRange(image,sepSize,sepSize+org+1 if i == self.num else sepSize+org)
			sepSize += org
			ps[sepSize] = p
		mask = np.zeros((H,W),np.uint8)
		for val,p in ps.items():
			mask[p > 0] = val
		return mask,list(ps.keys())

	def transform(self,image,keys):
		H,W = image.shape 
		img = list(image.flatten())
		chars = {}
		copied = self.chars.copy()
		for i,key in enumerate(keys):
			chars[key] = copied[i]
			copied.remove(copied[i])
		for v,c in chars.items():
			img = [c if i == v else i for i in img]
		img = np.array(img)
		img = img.reshape(H,W)
		for i in range(H):
			print(" ".join(img[i]))

	def resizeW(self,image):
		H,W = image.shape
		while W > self.limitw*100:
			W = int(W*self.resizeSZ)
		return cv2.resize(image,(W,H))

	def resizeH(self,image):
		H,W = image.shape 
		while H > self.limith*100:
			H = int(H*self.resizeSZ)
		return cv2.resize(image,(W,H))


	def validate(self,num,nums):
		if num not in nums: return InvalidCharNumber("Character number should be one of these => <3, 5, 15, 17, 51>")
		if self.resizeSZ < 0.2 or self.resizeSZ > 0.9: return EnormousSize("Resizing scale should be between 0.2 and 0.9")
		h,w = self.image.shape 
		if h > 350 or w > 350: return ValueError("Too big dims, Width and Height should be both smaller than 350")
		return True

	def render(self):
		validated = self.validate(self.num,self.validNums)
		if validated != True:
			raise validated
		image = self.resizeW(self.image)
		image = self.resizeH(image)
		res,keys = self.separate(image)
		self.transform(res,keys)
		#print(res.shape,self.image.shape,self.limitw,self.limith)
		cv2.imshow("WINDOW",self.image)
		#cv2.imshow("WINDOW2",res)
		cv2.waitKey(0)

def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("-p","--path",type=str,required=True,help="The path to your image")
	ap.add_argument("-n","--number",type=int,default=5,help="Number of the characters, Should one of these numbers => 3,5,15,17")
	ap.add_argument("-r","--resizeSZ",type=float,default=0.7,help="Resizing scale, Should be between 0.2 and 0.9")
	ap.add_argument("-s","--shuffle",type=int,default=10,help="Shuffling chars")
	args = vars(ap.parse_args())
	#print(args["path"],args["number"])
	p = Produce(args["path"],args["number"],args["resizeSZ"],args["shuffle"])
	p.render()

if __name__ == "__main__":
	main()