from math import cos,sin,tan,asin,atan,atan2,radians,degrees,floor,sqrt
from rich.console import Console
from rich.table import Table
import json

# DO NOT MODIFY THIS CELL
def dms_to_decimal(deg,min,sec,dir):
    '''
    Functions to convert latitude/longitude from degrees,minutes,seconds
    to decimal degrees
    
        * Args:
        ----
        deg : degrees
        min : minutes
        sec : seconds
        dir : direction, "N" or "S" for latitude; "E" or "W" for longitude [string]
              None is used for no direction 
        
        * Returns:
        dec : decimal degree
    '''
    dec = float(deg) + float(min)/60 + float(sec)/3600
    
    if (dir=="N" or dir=="E" or dir==None):
        dec*=1
    elif (dir=="S" or dir=="W"):
        dec*=-1
    else:
        print("direction symbol not recognized!!")
        return -1
    
    return dec


# DO NOT MODIFY THIS CELL
def decimal_to_dms(dec,comp):
    '''
    Functions to convert latitude/longitude decimal degrees to degrees,minutes,seconds
    
        * Args:
        ----
        dec : decimal degree
        comp : "latitude" or "longitude"
        
        * Returns:
        deg : degrees
        min : minutes
        sec : seconds
        dir : direction, "N" or "S" for latitude; "E" or "W" for longitude [string]
        
    '''
    south = False
    west = False
    
    if(dec < 0 and comp=="latitude"): 
        dec*=-1
        south = True
    if(dec < 0 and comp=="longitude"): 
        dec*=-1
        west = True
    
    deg = floor(dec)
    min = floor((dec - deg) * 60)
    sec = dec*3600 - deg*3600 - min*60
    
    if (comp=="latitude"):
        if south:
            dir = 'S'
        else: 
            dir = 'N'
    elif (comp=="longitude"):
        if west:
            dir = 'W'
        else:
            dir = 'E'
    
    return deg,min,sec,dir


def llh_to_xyz(phi,lamda,h,a,b):
    '''
    Function to convert lat,lon coordinate to cartesian XYZ

        * Args:
        ----
            - phi : latitude in degree,minute,seconds,direction [dictionary]
            - lambda : longitude in degree,minute,seconds,direction [dictionary]
            - lat : height in m
            - a : semi-major axis ellipsoid
            - b : semi-minor axis ellipsoid
        
        * Returns:
        ----
                - x,y,z
    '''
    # convert to degree decimal
    phi_decimal = dms_to_decimal(phi['deg'],phi['min'],phi['sec'],phi['dir'])
    lamda_decimal = dms_to_decimal(lamda['deg'],lamda['min'],lamda['sec'],lamda['dir'])

    # we convert to radians
    phi = radians(phi_decimal)
    lamda = radians(lamda_decimal)

    e_2 = (a**2-b**2)/a**2

    nu = a/sqrt(1-e_2*sin(phi)**2)

    X = (nu + h)*cos(phi)*cos(lamda)
    Y = (nu + h)*cos(phi)*sin(lamda)
    Z = (nu*(1-e_2) + h)*sin(phi)
    
    return X,Y,Z

def xyz_to_llh(X,Y,Z,a,b):
    '''
    Function to convert Cartesian X,Y,Z coordinates to Ellipsoidal

        * Args:
        ----
            - X :
            - Y :
            - Z :
            - a :
            - b :
        * Returns:
        ----
            lat:
            lon:

    '''
    e_2 = (a**2-b**2)/a**2
    epsilon = e_2/(1-e_2)
    p = sqrt(X**2+Y**2)
    u = atan((Z*a)/(p*b))

    phi_A = atan( (Z+epsilon*b*sin(u)**3)  /  (p-e_2*a*cos(u)**3)  )
    lambda_A = atan2(Y,X)

    nu = a/sqrt(1-e_2*sin(phi_A)**2)

    h = (X/(cos(phi_A)*cos(lambda_A)))-nu
    
    phi_A_decimal = degrees(phi_A)
    lambda_A_decimal = degrees(lambda_A)

    # latitude
    phi_A_degrees,phi_A_minutes,phi_A_seconds,phi_A_direction = decimal_to_dms(phi_A_decimal,"latitude")

    # longitude
    lambda_A_degrees,lambda_A_minutes,lambda_A_seconds,lambda_A_direction = decimal_to_dms(lambda_A_decimal,"longitude")

    lat = {"deg":phi_A_degrees,
            "min":phi_A_minutes,
            "sec":phi_A_seconds,
            "dir":phi_A_direction
            }

    
    lon = {"deg":lambda_A_degrees,
            "min":lambda_A_minutes,
            "sec":lambda_A_seconds,
            "dir":lambda_A_direction
            }

    return lat,lon,h


def print_1d_xyz(x,y,z,title):
    '''
    Print an array 3x1 using rich

    Args:
    -----
        * x : element to print x
        * y : element to print y
        * z : element to print z
    '''
    # DO NOT MODIFY THIS CELL
    table = Table(title=title)
    table.add_column("X")
    table.add_column("Y")
    table.add_column("Z")
    table.add_row(str(x),str(y),str(z))
    console = Console()
    console.print(table)

    return

def print_1d_xyz(x,y,z,title,type="xyz"):
    '''
    Print an array 3x1 using rich

    Args:
    -----
        * x : element to print x
        * y : element to print y
        * z : element to print z
    '''
    # DO NOT MODIFY THIS CELL
    table = Table(title=title)
    if (type=="xyz"):
        table.add_column("X")
        table.add_column("Y")
        table.add_column("Z")
    elif (type=="ll"):
        table.add_column("Latitude")
        table.add_column("Longitude")
        table.add_column("Height")
    elif (type=="en"):
        table.add_column("Easting")
        table.add_column("Northing")
        table.add_column("Height")
    elif (type=="ba"):
        table.add_column("Delta Easting")
        table.add_column("Delta Northing")
        table.add_column("Delta Height")
    elif (type=="tr"):
        table.add_column("Tx")
        table.add_column("Ty")
        table.add_column("Tz")
    elif (type=="dif"):
        table.add_column("Diff. Easting")
        table.add_column("Diff. Northing")
        table.add_column("Diff. height")

    table.add_row(str(x),str(y),str(z))
    console = Console()
    console.print(table)

    return