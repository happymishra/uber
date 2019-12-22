def convert_str_to_lat_long(coord):
    if isinstance(coord, str):
        return tuple([float(x) for x in coord.split(",")])
    elif isinstance(coord, list):
        return tuple(coord)

    return coord
