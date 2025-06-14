def hex_palette(hex_list):
    return [tuple(int(h[i:i+2], 16) for i in (0,2,4)) for h in hex_list]

def to_hex(rgb):
    return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"
