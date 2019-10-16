from numpy import double


def find_center(ul_lat: double, ul_lon: double, ur_lat: double, ur_lon: double, ll_lat: double, ll_lon: double,
                lr_lat: double, lr_lon: double):
    """
    find_center will find the center of a quadrilateral shape when the latitude and longitude
    are given for all four vertices. It will return the center point as tuple.

    :param ul_lat: upper left latitude
    :param ul_lon: upper left longitude
    :param ur_lat: upper right latitude
    :param ur_lon: upper right longitude
    :param ll_lat: lower left latitude
    :param ll_lon: lower left longitude
    :param lr_lat: lower right latitude
    :param lr_lon: lower right longitude
    :return: center of the shape as tuple
    """
    # Mid point of upper latitude using mid_point method
    mp1 = mid_point(ul_lat, ul_lon, ur_lat, ur_lon)
    # Mid point of lower latitude using mid_point method
    mp2 = mid_point(ll_lat, ll_lon, lr_lat, lr_lon)
    # Mid point of left longitude using mid_point method
    mp3 = mid_point(ul_lat, ul_lon, ll_lat, ll_lon)
    # Mid point of right longitude using mid_point method
    mp4 = mid_point(ur_lat, ur_lon, lr_lat, lr_lon)
    # Calculate the center of the shape using find_intersection method
    center = find_intersection(mp1[0], mp1[1], mp2[0], mp2[1], mp3[0], mp3[1], mp4[0], mp4[1])
    # Return center
    return center


def mid_point(x1, y1, x2, y2):
    """
    mid_point will find the mid point of a line segment when four coordinates are given.
    It will return the mid point as a tuple.

    :param x1: x-coordinate of left vertex
    :param y1: y-coordinate of left vertex
    :param x2: x-coordinate of right vertex
    :param y2: y-coordinate of right vertex
    :return: mid point of the line as tuple
    """
    # Find the midpoint of given x, y coordinates
    midpoint = ((x1 + x2) / 2, (y1 + y2) / 2)
    # Return mid point as tuple
    return midpoint


def find_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    """
    find_intersection will find the intersection point of two line segments when four coordinates
    are given for both line segments. It will return the intersection point as a tuple.

    :param x1: x-coordinate of vertex 1 in line 1
    :param y1: y-coordinate of vertex 2 in line 1
    :param x2: x-coordinate of vertex 1 in line 2
    :param y2: y-coordinate of vertex 2 in line 2
    :param x3: x-coordinate of vertex 1 in line 3
    :param y3: y-coordinate of vertex 2 in line 3
    :param x4: x-coordinate of vertex 1 in line 4
    :param y4: y-coordinate of vertex 2 in line 4
    :return: intersection point of two line segments as tuple
    """

    # Values that exist in both px and py
    cross_1 = (x1 * y2 - y1 * x2)
    cross_2 = (x3 * y4 - y3 * x4)
    denominator = ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

    # Find the x-coordinate of the center
    px = (cross_1 * (x3 - x4) - (x1 - x2) * cross_2) / denominator
    # Find the y-coordinate of the center
    py = (cross_1 * (y3 - y4) - (y1 - y2) * cross_2) / denominator
    # Return the center as tuple
    return px, py
