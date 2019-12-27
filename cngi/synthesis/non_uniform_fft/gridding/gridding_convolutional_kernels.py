#defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION"
#https://cython.readthedocs.io/en/latest/src/userguide/numpy_tutorial.html
from __future__ import print_function
import numba
import numpy as np
import math
import ctypes
from numba import jit
import time
from .helper_functions_imaging_coords import coordinates
print("numba version: %s\n numpy version: %s" % (numba.__version__,np.__version__))

def create_prolate_spheroidal_kernel(oversampling, support, n_u):
    # support//2 is the index of the zero value of the support values
    # oversampling//2 is the index of the zero value of the oversampling value
    support_center = support//2
    oversampling_center = oversampling//2
    
    support_values =  (np.arange(support) - support_center)
    if (oversampling % 2) == 0: 
        oversampling_values = ((np.arange(oversampling+1) - oversampling_center)/oversampling)[:,None]
        kernel_points_1D = (np.broadcast_to(support_values, (oversampling+1,support)) + oversampling_values)
    else:
        oversampling_values = ((np.arange(oversampling) - oversampling_center)/oversampling)[:,None]
        kernel_points_1D = (np.broadcast_to(support_values, (oversampling,support)) + oversampling_values)
        
    kernel_points_1D = kernel_points_1D/support_center
    
    _ , kernel_1D = prolate_spheroidal_function(kernel_points_1D)
    #kernel_1D /= np.sum(np.real(kernel_1D[oversampling_center,:]))
    

    if (oversampling % 2) == 0: 
        kernel = np.zeros((oversampling+1, oversampling+1, support, support),dtype=np.double) #dtype=np.complex128
    else:   
        kernel = np.zeros((oversampling, oversampling, support, support),dtype=np.double)
        
        
    for x in range(oversampling):
        for y in range(oversampling):
            kernel[x, y, :, :] = np.outer(kernel_1D[x, :], kernel_1D[y, :])
                
    #norm = np.sum(np.real(kernel))
    #kernel /= norm
    
    # Gridding correction function (applied after dirty image is created)
    kernel_image_points_1D = np.abs(2.0 * coordinates(n_u))
    kernel_image_1D = prolate_spheroidal_function(kernel_image_points_1D)[0]
    kernel_image = np.outer(kernel_image_1D, kernel_image_1D)
    #kernel_image[kernel_image > 0.0] = kernel_image.max() / kernel_image[kernel_image > 0.0]
    
    #kernel_image =  kernel_image/kernel_image.max()
    return kernel, kernel_image

#@jit not working due to boolean slicing of array not working    
def prolate_spheroidal_function(u):
    """Calculate PSWF using an old SDE routine re-written in Python
        Find Spheroidal function with M = 6, alpha = 1 using the rational
        approximations discussed by Fred Schwab in 'Indirect Imaging'.
        This routine was checked against Fred's SPHFN routine, and agreed
        to about the 7th significant digit.
        The griddata function is (1-NU**2)*GRDSF(NU) where NU is the distance
        to the edge. The grid correction function is just 1/GRDSF(NU) where NU
        is now the distance to the edge of the image.
    """
    p = np.array([[8.203343e-2, -3.644705e-1, 6.278660e-1, -5.335581e-1, 2.312756e-1],[4.028559e-3, -3.697768e-2, 1.021332e-1, -1.201436e-1, 6.412774e-2]])
    q = np.array([[1.0000000e0, 8.212018e-1, 2.078043e-1],[1.0000000e0, 9.599102e-1, 2.918724e-1]])
                     
    _, n_p = p.shape
    _, n_q = q.shape
                     
    u = np.abs(u)
    uend = np.zeros(u.shape,dtype=np.float64)
    part = np.zeros(u.shape, dtype=np.int64)
    
    part[(u >= 0.0) & (u < 0.75)] = 0
    part[(u >= 0.75) & (u <= 1.0)] = 1
    uend[(u >= 0.0) & (u < 0.75)] = 0.75
    uend[(u >= 0.75) & (u <= 1.0)] = 1.0
                     
    delusq = u ** 2 - uend ** 2
    
    top = p[part, 0]
    for k in range(1, n_p): #small constant size loop
        top += p[part, k] * np.power(delusq, k)
    
    bot = q[part, 0]
    for k in range(1, n_q): #small constant size loop
        bot += q[part, k] * np.power(delusq, k)
    
    grdsf = np.zeros(u.shape,dtype=np.float64)
    ok = (bot > 0.0)
    grdsf[ok] = top[ok] / bot[ok]
    ok = np.abs(u > 1.0)
    grdsf[ok] = 0.0
    
    # Return the griddata function and the grid correction function
    return grdsf, (1 - u ** 2) * grdsf
  
  
def create_prolate_spheroidal_kernel_1D(oversampling, support):
   support_center = support//2
   oversampling_center = oversampling//2
   u = np.arange(oversampling*(support_center))/(support_center*oversampling)

   
   long_half_kernel_1D = np.zeros(oversampling*(support_center+1))
   _, long_half_kernel_1D[0:oversampling*(support_center)] = prolate_spheroidal_function(u)
   return long_half_kernel_1D
 
 
 
 
 
 
 
 
 
 