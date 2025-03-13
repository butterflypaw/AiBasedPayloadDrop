from math import radians, cos

EARTH_RADIUS_METERS = 6371000

def calculate_square_geofence(center_lat, center_lon, side_length_meters):
    """
    Calculate the square geofence boundaries around the given center point.
    """
    half_side = side_length_meters / 2
    delta_lat = half_side / EARTH_RADIUS_METERS * (180 / 3.14159)
    delta_lon = half_side / (EARTH_RADIUS_METERS * cos(radians(center_lat))) * (180 / 3.14159)

    lat_min = center_lat - delta_lat
    lat_max = center_lat + delta_lat
    lon_min = center_lon - delta_lon
    lon_max = center_lon + delta_lon

    return [(lat_min, lon_min), (lat_max, lon_min), (lat_max, lon_max), (lat_min, lon_max)]


def is_within_square_geofence(lat, lon, geofence_edges):
    """
    Check if the drone's current latitude and longitude are within the square geofence.
    """
    lat_min, lon_min = geofence_edges[0]
    lat_max, lon_max = geofence_edges[2]
    return lat_min <= lat <= lat_max and lon_min <= lon <= lon_max


def generate_grid_points(geofence_edges, step_size):
    """
    Generate a grid of points within the geofence.
    """
    lat_min, lon_min = geofence_edges[0]
    lat_max, lon_max = geofence_edges[2]

    lat_points = int((lat_max - lat_min) / step_size)
    lon_points = int((lon_max - lon_min) / step_size)

    grid_points = []
    for i in range(lat_points + 1):
        for j in range(lon_points + 1):
            lat = lat_min + (i * step_size)
            lon = lon_min + (j * step_size)
            grid_points.append((lat, lon))

    return grid_points