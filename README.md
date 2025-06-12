# meshcode_pkg

`meshcode_pkg` is a simple Python package for converting between Japanese mesh codes and geographic coordinates (latitude and longitude). It supports up to 5th-level meshes and can generate polygon boundaries and mesh centers for mapping and analysis.

## Features

- Convert latitude and longitude to Japanese mesh codes (1st to 5th level)
- Decode a mesh code to its center coordinates and polygon geometry
- Supports standard Japanese mesh system used for spatial data in Japan

## Installation

You can install the package directly from GitHub:

```bash
pip install git+https://github.com/durianranger/meshcode_pkg.git
```

## Usage

After installing, you can import the functions like this:

```python
from meshcode_pkg import latlon_to_meshcode, decode_japan_mesh
```

### 1. Convert Latitude/Longitude to Meshcode

```python
lat = 35.0
lon = 135.0
meshcode = latlon_to_meshcode(lat, lon, level=4)
print("Meshcode:", meshcode)
# Output example: '523504324'
```

### 2. Decode Meshcode to Center Coordinates and Polygon

```python
center, polygon = decode_japan_mesh(meshcode)
print("Center coordinates:", center)
print("Polygon object:", polygon)
# Output:
# Center coordinates: (35.004166..., 135.008...)
# Polygon: shapely.geometry.polygon.Polygon([...])
```

> ✅ `latlon_to_meshcode()` supports mesh levels from 1 to 5.
>  
> ✅ `decode_japan_mesh()` returns the center (lat, lon) and a `shapely.geometry.Polygon` object for spatial analysis.

## License

MIT License
