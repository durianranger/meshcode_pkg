# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 11:03:13 2025

@author: du
"""

from shapely.geometry import Polygon
def decode_japan_mesh(meshcode):
    """
    mesh 番号（4〜10位）から (center_lat, center_lon), polygon
    5次meshまで自動識別
    """
    meshcode = str(meshcode)
    length = len(meshcode)

    if length < 4 or length > 10:
        raise ValueError("length of meshcode should between 4〜10 ")

    # 基础位置：1次mesh南西角
    lat_code = int(meshcode[:2])
    lon_code = int(meshcode[2:4])
    lat_base = lat_code / 1.5
    lon_base = lon_code + 100

    # 单位サイズ
    lat_unit_2nd = 1 / 12      # 5'
    lon_unit_2nd = 1 / 8       # 7.5'
    lat_unit_3rd = 1 / 120     # 30"
    lon_unit_3rd = 1 / 80      # 45"
    lat_unit_4th = 1 / 240     # 15"
    lon_unit_4th = 1 / 160     # 22.5"
    lat_unit_5th = 1 / 480     # 7.5"
    lon_unit_5th = 1 / 320     # 11.25"

    # 起点
    lat0 = lat_base
    lon0 = lon_base

    # ===== 第2次细分 =====
    if length >= 6:
        row_2nd = int(meshcode[4])
        col_2nd = int(meshcode[5])
        lat0 += row_2nd * lat_unit_2nd
        lon0 += col_2nd * lon_unit_2nd

    # ===== 第3次细分 =====
    if length >= 8:
        row_3rd = int(meshcode[6])
        col_3rd = int(meshcode[7])
        lat0 += row_3rd * lat_unit_3rd
        lon0 += col_3rd * lon_unit_3rd

    # ===== 第4次细分=====
    if length >= 9:
        sub4 = int(meshcode[8])
        offset_lat_4 = {1: 0, 2: 0, 3: lat_unit_4th, 4: lat_unit_4th}
        offset_lon_4 = {1: 0, 2: lon_unit_4th, 3: 0, 4: lon_unit_4th}
        lat0 += offset_lat_4[sub4]
        lon0 += offset_lon_4[sub4]

    # ===== 第5次细分=====
    if length == 10:
        sub5 = int(meshcode[9])
        offset_lat_5 = {1: 0, 2: 0, 3: lat_unit_5th, 4: lat_unit_5th}
        offset_lon_5 = {1: 0, 2: lon_unit_5th, 3: 0, 4: lon_unit_5th}
        lat0 += offset_lat_5[sub5]
        lon0 += offset_lon_5[sub5]

    # ===== メッシュサイズ计算 =====
    if length == 4:
        lat_unit = 2 / 3        # 40分 = 2/3度
        lon_unit = 1
    elif length == 6:
        lat_unit = lat_unit_2nd
        lon_unit = lon_unit_2nd
    elif length == 8:
        lat_unit = lat_unit_3rd
        lon_unit = lon_unit_3rd
    elif length == 9:
        lat_unit = lat_unit_4th
        lon_unit = lon_unit_4th
    elif length == 10:
        lat_unit = lat_unit_5th
        lon_unit = lon_unit_5th

    # ===== polygon & center =====
    polygon = Polygon([
        (lon0, lat0),
        (lon0 + lon_unit, lat0),
        (lon0 + lon_unit, lat0 + lat_unit),
        (lon0, lat0 + lat_unit),
        (lon0, lat0)
    ])
    center_lat = lat0 + lat_unit / 2
    center_lon = lon0 + lon_unit / 2

    return (center_lat, center_lon), polygon

def latlon_to_meshcode(lat, lon, level=4):
    # 第1次メッシュ
    lat_code = int(lat * 1.5)
    lon_code = int(lon) - 100
    meshcode = f"{lat_code:02d}{lon_code:02d}"

    if level == 1:
        return meshcode

    lat_min = lat - (lat_code / 1.5)
    lon_min = lon - (lon_code + 100)

    # 第2次
    row_2nd = int(lat_min / (1 / 12))  # 5分 = 1/12度
    col_2nd = int(lon_min / (1 / 8))   # 7.5分 = 1/8度
    meshcode += f"{row_2nd}{col_2nd}"

    if level == 2:
        return meshcode

    # 第3次
    lat_min -= row_2nd * (1 / 12)
    lon_min -= col_2nd * (1 / 8)
    row_3rd = int(lat_min / (1 / 120))
    col_3rd = int(lon_min / (1 / 80))
    meshcode += f"{row_3rd}{col_3rd}"

    if level == 3:
        return meshcode

    # 第4次
    lat_min -= row_3rd * (1 / 120)
    lon_min -= col_3rd * (1 / 80)
    sub_4 = (
        1 if lat_min < (1 / 240) and lon_min < (1 / 160) else
        2 if lat_min < (1 / 240) else
        3 if lon_min < (1 / 160) else 4
    )
    meshcode += f"{sub_4}"

    if level == 4:
        return meshcode

    # 第5次
    lat_min -= (0 if sub_4 in [1,2] else (1 / 240))
    lon_min -= (0 if sub_4 in [1,3] else (1 / 160))
    sub_5 = (
        1 if lat_min < (1 / 480) and lon_min < (1 / 320) else
        2 if lat_min < (1 / 480) else
        3 if lon_min < (1 / 320) else 4
    )
    meshcode += f"{sub_5}"

    return meshcode