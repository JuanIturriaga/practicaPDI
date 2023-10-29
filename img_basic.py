import numpy as np  
from math import log, fabs, floor

#img numpy geryscale
#map numpy[256] int8
def img_applymap (img, map):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i,j] = map[img[i,j]]
    return img

#normal map
def map_normal ():
    map = np.ndarray(256, dtype=np.uint16)
    for i in range(256):
        map[i] = i
    return map


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



#Gray - level slicing
# dos variables de umbral, valor fijo, y tipo lineal o cero

def slicing_type_linear (input, t1, t2, value):
    if (input >= t1 and input <= t2):
        return value
    else:
        return input

def slicing_type_zero (input, t1, t2, value):
    if (input >= t1 and input <= t2):
        return value
    else:
        return 0

def slicing_type_glow (input, t1, t2, value):
    if (input >= t1 and input <= t2):
        return input + value
    else:
        return input
    
def slicing_type_glow_zero (input, t1, t2, value):
    if (input >= t1 and input <= t2):
        return input + value
    else:
        return 0


def map_gray_level_slicing (t1, t2, value, type = 'linear'):
    slicing_func = {
        'linear': slicing_type_linear,
        'zero': slicing_type_zero,
        'glow': slicing_type_glow,
        'glow_zero': slicing_type_glow_zero
    }

    map = np.ndarray(256)    
    for i in range(256):
        map[i] = min(max(slicing_func[type](i, t1, t2, value),0),255)

    return map

def img_gray_level_slicing (img, t1, t2, value, type = 'linear'):
    return img_applymap(img, map_gray_level_slicing (t1, t2, value, type))

#Compresión de rango dinámico
def map_dynamic_range_compression_b (c):
    map = np.ndarray(256)
    for i in range(256):
        map[i] = 255 * (i/255)**(1/c)
    return map    

def img_dynamic_range_compression_b (img,c):
    return img_applymap(img, map_dynamic_range_compression_b(c))      

def map_dynamic_range_compression ():
    c = 255 / log(256,10)
    map = np.ndarray(256)
    for i in range(256):
        map[i] = floor(c * log(fabs(i)+1,10))
    return map  

def img_dynamic_range_compression (img):
    return img_applymap(img, map_dynamic_range_compression())      



