import numpy as np  

#histograma de una imágen
def img_histogram (img):
    hist = np.zeros(256, dtype=np.uint32)
    for i in img:
        for j in i:
            hist[j] += 1
    return hist    