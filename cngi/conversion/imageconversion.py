#   Copyright 2019 AUI, Inc. Washington DC, USA
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.



##########################################
def image_to_zarr(infile, outfile=None, membudget=1e9):
    """
    .. todo::
        This function is not yet implemented

    Convert legacy format Image to xarray compatible zarr format image

    This function requires CASA6 casatools module. 

    Parameters
    ----------
    infile : str
        Input image filename
    outfile : str
        Output zarr filename. If None, will use infile name with .zarr extension
    membudget : float
        Target in-memory byte size of a chunk, Default = 1e9 (~= 1GB)
    
    Returns
    -------
    """    
    return True



###########################################
def zarr_to_image(infile, outfile=None):
    """
    .. todo::
        This function is not yet implemented

    Convert xarray compatible zarr format to legacy CASA Image format

    Parameters
    ----------
    infile : str
        Input zarr image filename
    outfile : str
        Output image filename. If None, will use infile name with .image extension

    Returns
    -------
    """
    return True




###########################################
def fits_to_zarr(infile, outfile=None):
    """
    .. todo::
        This function is not yet implemented

    Convert FITS format Image to xarray compatible zarr format image (future)
    
    Parameters
    ----------
    infile : str
        Input FITS filename
    outfile : str
        Output zarr filename. If None, will use infile name with .zarr extension

    Returns
    -------
    """
    return True



############################################
def zarr_to_fits(infile, outfile=None):
    """
    .. todo::
        This function is not yet implemented

    Convert xarray compatible zarr image to FITS format image (future)
    
    Parameters
    ----------
    infile : str
        Input zarr filename
    outfile : str
        Output FITS filename. If None, will use infile name with .fits extension

    Returns
    -------
    """
    return True
