# image manipulation
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.transforms as mtransforms
import numpy as np

#fig, ((ax, ax2), (ax3, ax4)) = plt.subplots(2, 2)
fig, ax = plt.subplots()
transform = mtransforms.Affine2D().clear()
#
im=mpimg.imread('OregonDucks.png')
ax.axis('off')
im = ax.imshow(im, interpolation='none',
               origin='upper',
               aspect='equal',
               extent=[-im.shape[1]/2., im.shape[1]/2., -im.shape[0]/2., im.shape[0]/2. ],
               clip_on=True)
#im = plt.imshow(im)

# normal
transform = mtransforms.Affine2D().clear()
transform = mtransforms.Affine2D().scale(0.5,0.5)
trans_data = transform+ax.transData
im.set_transform(trans_data)
im.figure.savefig('img0.png')

# stretch y
transform = mtransforms.Affine2D().clear()
transform = mtransforms.Affine2D().scale(1,0.5)
trans_data = transform+ax.transData
im.set_transform(trans_data)
im.figure.savefig('img1.png')

# stretch x
transform = mtransforms.Affine2D().clear()
transform = mtransforms.Affine2D().scale(0.5,1)
trans_data = transform+ax.transData
im.set_transform(trans_data)
im.figure.savefig('img2.png')

# squeeze y
transform = mtransforms.Affine2D().clear()
transform = mtransforms.Affine2D().scale(0.2,0.5)
trans_data = transform+ax.transData
im.set_transform(trans_data)
im.figure.savefig('img3.png')

# reflection -1 0 0 1
transform = mtransforms.Affine2D().clear()
transform = mtransforms.Affine2D().scale(-0.5,0.5)
trans_data = transform+ax.transData
im.set_transform(trans_data)
im.figure.savefig('img4.png')

# rotation
transform = mtransforms.Affine2D().clear()
transform = mtransforms.Affine2D().rotate_deg(45).scale(0.5,0.5)
trans_data = transform+ax.transData
im.set_transform(trans_data)
im.figure.savefig('img5.png')


# shear
transform = mtransforms.Affine2D().clear()
transform = mtransforms.Affine2D().skew_deg(65,0).scale(0.5,0.5)
trans_data = transform+ax.transData
im.set_transform(trans_data)
im.figure.savefig('img6.png')


# # display intended extent of the image
# x1, x2, y1, y2 = im.get_extent()
# ax.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1],
#         transform=trans_data)
# #imgplot = plt.imshow(im)
# x = np.matrix('0 1; 1 0')
# plt.axis('off')
# plt.show()
