import numpy as np  

#img numpy geryscale
#map numpy[256] int8
def img_applymap (img, map):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i,j] = map[img[i,j]]
    return img

#brillo
def map_brightness (value):
    map = np.ndarray(256, dtype=np.uint16)
    for i in range(256):
        map[i] = min(max(i + value,0),255)         
    return map

def img_brightness (img, value):
    return img_applymap(img, map_brightness(value))

#constraste
def map_contrast (percent, offset=None):    
    coef = 1 + (percent/100)
    if offset is None:
        value = (1-coef)*256/2  
    else:
        value = -coef*offset  
    map = np.ndarray(256, dtype=np.uint16)
    for i in range(256):
        map[i] = min(max(i * coef + value,0),255)         
    return map

def img_contrast (img, percent, value = None):    
    return img_applymap(img, map_contrast(percent, value))

#negativo
def map_negative ():
    map = np.ndarray(256, dtype=np.uint16)
    for i in range(256):
        map[i] = 255-i
    return map

def img_negative (img):
    return img_applymap(img, map_negative())

#BIT-Plane
def map_bitplane (bit):
    map = np.ndarray(256, dtype=np.uint16)
    for i in range(256):
        map[i] = ((i >> bit) & 1) * 255
    return map

def img_bitplane (img, bit):
    return img_applymap(img, map_bitplane(bit))

def map_mask (mask):
    map = np.ndarray(256, dtype=np.uint16)
    for i in range(256):
        map[i] = i & mask
    return map

def img_mask (img, mask):
    return img_applymap(img, map_mask(mask))


#Contrast Stretching

# points np = [[x0, y0],[x1, y1]]
def interpol (x, points):
  return points[0][1] + (x - points[0][0]) * (points[1][1] - points[0][1]) / (points[1][0] - points[0][0])

def map_contrast_stretching (points):
    map = np.ndarray(256)

    # corrige points si le falta el 0,0 o el 255,255
    (len,par) = points.shape
    if (points[0][0] != 0):
        points = np.append([0,0], points)
        len = len + 1
        points = np.reshape(points,(len,par))

    if (points[len-1][0] != 255):
        points = np.append(points, [255,255])
        len = len + 1
        points = np.reshape(points,(len,par))

    #crea mapa con las interpolaciones
    j = 1
    for i in range(256):
        if (i > points[j][0]):
            j = j + 1
        map[i] = interpol (i, [points[j-1], points[j]])

    return map

def img_contrast_stretching (img, points):
    return img_applymap(img, map_contrast_stretching (points))