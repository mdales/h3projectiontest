from multiprocessing import Pool, cpu_count

import h3
import numpy as np

from yirgacheffe.layers import Layer, UniformAreaLayer

mag = 8

def process_line(workload):
    area_per_pixel, latitude, width, initial_longitude, longitude_step = workload

    areas = dict()
    for x in range(width):
        longitude = initial_longitude + (x * longitude_step)
        cell = h3.geo_to_h3(latitude, longitude, mag)
        try:
            areas[cell] += area_per_pixel
        except KeyError:
            areas[cell] = area_per_pixel
    return areas

jung_og = Layer.layer_from_file('/maps/biodiversity/jung_aoh_basemaps/ModLibSRF_merge.tif')
area_layer = UniformAreaLayer.layer_from_file('small.tiff')

print(jung_og.window)
print(jung_og.geo_transform)
print(cpu_count())


workloads = []
for y in range(int(jung_og.window.ysize / 2)):
    area_per_pixel = area_layer.read_array(0, y, 1, 1)[0][0]
    latitude = jung_og.geo_transform[3] + (y * jung_og.geo_transform[5])
    workloads.append((area_per_pixel, latitude, int(jung_og.window.xsize / 2), jung_og.geo_transform[0], jung_og.geo_transform[1]))

areas = dict()
chunksize = 100
for i in range(0, len(workloads), chunksize):
    count = chunksize
    if i + chunksize > len(workloads):
        count = len(workloads) - i
    subset = workloads[i:i + count]

    res = []
    with Pool(cpu_count()) as p:
        res = p.map(process_line, subset)

    for r in res:
        for cell in r:
            try:
                areas[cell] += r[cell]
            except KeyError:
                areas[cell] = r[cell]

data = np.array(list(areas.values()))

print("average: ", np.average(data))
print("max: ", np.max(data))
print("min: ", np.min(data))
print("stddev: ", np.std(data))

with open(f'/maps/mwd24/res_{mag}.csv', 'w') as f:
    for key in areas:
        f.write(f"{key}, {areas[key]}\n")
