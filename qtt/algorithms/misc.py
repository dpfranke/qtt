# -*- coding: utf-8 -*-
""" Misc algorithms
Created on Wed Aug 31 16:19:30 2016

@author: eendebakpt
"""

#%%
import itertools
import numpy as np

def point_in_poly(x, y, poly):
    """ Return true if a point is contained in a polygon 
    
    Args:
        x (float)
        y (float):
        poly (kx2 array): polygon vertices
    Returns:
        inside (bool): True if the point is inside the polygon
    """
    n = len(poly)
    inside = False

    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


def points_in_poly(points, poly_verts):
    """ Determine whether points are contained in a polygon or not
    
    Args:
        points (kx2 array)
        poly_verts (array)
    """
    nn = points.shape[0]
    rr = np.zeros((nn,))
    for ii in range(nn):
        rr[ii] = point_in_poly(points[ii, 0], points[ii, 1], poly_verts)

    rr = rr.astype(np.bool)
    return rr

def fillPoly(im, poly_verts, color=None):
    """ Fill a polygon in an image with the specified color

    Replacement for OpenCV function cv2.fillConvexPoly

    Arugments:
        im (array): array to plot into
        poly_verts (kx2 array): polygon vertices
        color (array or float): color to fill the polygon
    Returns:
        grid (array): resulting array

    """
    ny, nx = im.shape[0], im.shape[1]

    # Create vertex coordinates for each grid cell...
    # (<0,0> is at the top left of the grid in this system)
    x, y = np.meshgrid(np.arange(nx), np.arange(ny))
    x, y = x.flatten(), y.flatten()

    points = np.vstack((y, x)).T

    npts = int(poly_verts.size / 2)
    poly_verts = poly_verts.reshape((npts, 2))
    poly_verts = poly_verts[:, [1, 0]]

    try:
        from matplotlib.path import Path
        pp = Path(poly_verts)
        r = pp.contains_points(points)
    except:
        # slow version...
        r = points_in_poly(points, poly_verts)
        pass
    im.flatten()[r] = 1
    grid = r
    grid = grid.reshape((ny, nx))

    return grid

def polyfit2d(x, y, z, order=3):
    """ Fit a polynomial on 2D data
    
    Args:
        x (array): 1D array
        y (array): 1D array
        z (array): 2D array with data
        order (int): order of polynomial to fit
    Returns:
        m (array): order of the polynomial        
    """
    ncols = (order + 1)**2
    G = np.zeros((x.size, ncols))
    ij = itertools.product(range(order + 1), range(order + 1))
    for k, (i, j) in enumerate(ij):
        G[:, k] = x**i * y**j
    rcond=None
    import distutils    
    if distutils.version.StrictVersion(np.__version__) <= distutils.version.StrictVersion('1.13'):
        rcond=-1
    m, _, _, _ = np.linalg.lstsq(G, z, rcond=rcond)
    return m


def polyval2d(x, y, m):
    """ Evaluate a 2D polynomial
    
    Args:
        x (array)
        y (array)
        m (array): coefficients of polynomial
    Returns:
        z (array)
    """
    order = int(np.sqrt(len(m))) - 1
    ij = itertools.product(range(order + 1), range(order + 1))
    z = np.zeros_like(x).astype(np.float)
    for a, (i, j) in zip(m, ij):
        z += a * x**i * y**j
    return z

def test_polyfitting():
    
    x=np.arange(10, 20)
    y=np.arange(20,30)
    z=np.random.rand( 10, 10)
    
    p=polyfit2d(x,y,z)
    zz=polyval2d(x,y, p)

    
if __name__=='__main__':
    test_polyfitting()
    
        