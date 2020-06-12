import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.metrics import pairwise_distances_argmin
from sklearn.utils import shuffle
from skimage import io, color
from time import time

n_colors = 50
#orange = io.imread("ThinkstockPhotos-494037394.jpg")
orange = io.imread("core.png")

#print(orange)
orange = color.rgb2hsv(orange)
#print(orange)

#orange = np.array(orange, dtype=np.float64) / 255
orange = np.array(orange, dtype=np.float64)

w, h, d = original_shape = tuple(orange.shape)
image_array = np.reshape(orange, (w * h, d))

print("Fitting k-means model on a small sub-sample of the data")
t0 = time()
image_array_sample = shuffle(image_array, random_state=0)[:1000]
k_means = KMeans(n_clusters=n_colors, random_state=0).fit(image_array_sample)
#k_means = KMeans(n_clusters=n_colors, random_state=0).fit(image_array)
print("done in %0.3fs." % (time() - t0))

print("Fitting Gaussian model on a small sub-sample of the data")
t0 = time()
image_array_sample = shuffle(image_array, random_state=0)[:1000]
gm = GaussianMixture(n_components=n_colors, init_params='kmeans', covariance_type='spherical').fit(image_array_sample)
#gm = GaussianMixture(n_components=n_colors, init_params='kmeans', covariance_type='spherical').fit(image_array)
print("done in %0.3fs." % (time() - t0))

print("Fitting Spectral model on a small sub-sample of the data")
t0 = time()
image_array_sample = shuffle(image_array, random_state=0)[:]
sc = SpectralClustering(n_clusters=n_colors, eigen_solver='arpack',
        affinity="nearest_neighbors").fit(image_array_sample)
#gm = GaussianMixture(n_components=n_colors, init_params='kmeans', covariance_type='spherical').fit(image_array)
print("done in %0.3fs." % (time() - t0))

print("Predicting color indices on the full image (k-means)")
t0 = time()
labels = k_means.predict(image_array)
print("done in %0.3fs." % (time() - t0))

print("Predicting color indices on the full image (Gaussian)")
t0 = time()
labels_gaussian = gm.predict(image_array)
print("done in %0.3fs." % (time() - t0))

codebook_random = shuffle(image_array, random_state=0)[:n_colors + 1]
print("Predicting color indices on the full image (random)")
t0 = time()
labels_random = pairwise_distances_argmin(codebook_random,
                                          image_array,
                                          axis=0)
print("done in %0.3fs." % (time() - t0))


def recreate_image(codebook, labels, w, h):
    """Recreate the (compressed) image from the code book & labels"""
    d = codebook.shape[1]
    image = np.zeros((w, h, d))
    label_idx = 0
    for i in range(w):
        for j in range(h):
            image[i][j] = codebook[labels[label_idx]]
            label_idx += 1
    return image

# Display all results, alongside original image
plt.figure(1)
plt.clf()
ax = plt.axes([0, 0, 1, 1])
plt.axis('off')
plt.title('Original image (96,615 colors)')
plt.imshow(color.hsv2rgb(orange))

plt.figure(2)
plt.clf()
ax = plt.axes([0, 0, 1, 1])
plt.axis('off')
plt.title('Quantized image ('+str(n_colors)+' colors, K-Means)')
#plt.imshow(color.hsv2rgb(recreate_image(k_means.cluster_centers_, labels, w, h)))
print(k_means.cluster_centers_)
plt.imshow(recreate_image(k_means.cluster_centers_, labels, w, h))

plt.figure(3)
plt.clf()
ax = plt.axes([0, 0, 1, 1])
plt.axis('off')
plt.title('Quantized image ('+str(n_colors)+' colors, Gaussian)')
#plt.imshow(color.hsv2rgb(recreate_image(gm.means_, labels_gaussian, w, h)))
plt.imshow(recreate_image(gm.means_, labels_gaussian, w, h))

#plt.figure(4)
#plt.clf()
#ax = plt.axes([0, 0, 1, 1])
#plt.axis('off')
#plt.title('Quantized image ('+str(n_colors)+' colors, Random)')
#plt.imshow(recreate_image(codebook_random, labels_random, w, h))

plt.show()