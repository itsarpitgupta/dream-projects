import cv2 as cv

img = cv.imread("D:\Vision_Application\hul_bad_230219\Bad\Image00111.BMP")
# img = cv.imread("D:\github-repos\dream-projects\deep-vision-py\DATA\template.jpg")
# plt.imshow(img)
# plt.show()
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# plt.imshow(gray_img)

edges = cv.Canny(gray_img, threshold1=60, threshold2=200)
# plt.imshow(edges)
# np.set_printoptions(threshold=np.inf)
# print(edges)

rows = edges[:, 1].size
cols = edges[1, :].size

thickness = 2
points = []

count = 1
for x in range(0, rows):
    for y in range(0, cols):
        if edges[x,y] == 255:
            for t in range(y+1,y+thickness):
                if t < cols:
                    if edges[x,t] == 255:
                        count +=1
                    else:
                        break
            if count >= thickness:
                points.append([x,y])
        count = 1


print(points)
