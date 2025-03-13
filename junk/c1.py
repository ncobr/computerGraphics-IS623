import numpy as np
import matplotlib.pyplot as plt
import imageProcessing as ip

myImage = np.array(plt.imread("utplogo.jpg"))/255

# plt.figure(1)
# plt.subplot(2, 2, 1)
# plt.imshow(myImage)
# plt.title("Original image")
#
# plt.subplot(2, 2, 2)
# imageBrightness = ip.brightnessImg(myImage, 0.5)
# plt.imshow(imageBrightness)
# plt.title("Brightness image")
#
#
# plt.subplot(2, 2, 3)
# channelAdjust = ip.adjustChannel(myImage, 100, 0)
# plt.imshow(channelAdjust)
# plt.title("channel adjust")
#
# plt.subplot(2, 2, 4)
# imageContrast = ip.contrastImg(myImage, 0.5, 1)
# plt.imshow(imageContrast)
# plt.title("contrast image")


plt.figure(1)
imgInvert = ip.imgInvert(myImage)
plt.imshow(imgInvert, "Greys_r")
plt.title("imagen invertida")
plt.show()
