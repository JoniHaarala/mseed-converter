# Copyright 2023 Jonatan Haarala. All Rights Reserved.
# MIT Licensed & Apache License 2.0.
__author__ = 'Jonatan Haarala'

import math
import time

from obspy import read
import numpy as np
from save_thread_result import ThreadWithResult
import threading


def max_amplitude(eje):
    return np.amax(eje)


def read_file(fileName):
    st = read(fileName)
    results = []
    for trace in st:
        trace_values = trace.data
        results.extend(trace_values)

    return results


def show_data(x, y, z):
    t1 = ThreadWithResult(target=read_file, args=(x,))
    t2 = ThreadWithResult(target=read_file, args=(y,))
    t3 = ThreadWithResult(target=read_file, args=(z,))
    data = []
    #
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    dp2 = t1.result
    dp1 = t2.result
    dpz = t3.result

    time.sleep(2)

    for i in range(len(dp2) - 1):
        data.append(f'{dpz[i]} {dp2[i]} {dp1[i]}\n')

    return data


def read_metadata(fileName: str, maxVal: int):
    header = []
    st = read(fileName)
    metadata = st[0].stats
    starttime = str(metadata.starttime).split('T')
    endtime = str(metadata.endtime).split('T')
    hz = math.trunc(metadata.sampling_rate)

    ##
    header.append(f"Original file name: {fileName}")
    header.append(f"Transformed into: {metadata.network}{metadata.station}.txt")
    header.append("ReadCity version: 1.0")
    header.append(f"Station serial number: {metadata.station}")
    header.append("Station software version: 0000")
    header.append("Channel number: 3")
    # time data
    header.append(f"Starting date: {starttime[0]}")
    header.append(f"Starting time: {starttime[1].split('.')[0]}")
    header.append(f"Ending date: {endtime[0]}")
    header.append(f"Ending time: {endtime[1].split('.')[0]}")

    header.append(f"Sample rate: {hz} Hz")
    header.append(f"Sample number: {metadata.npts}")
    header.append("Recording duration: {0:.3f} mn".format((metadata.npts - 1) / (hz * 60)))
    header.append("Conversion factor: 52428.8")
    header.append("Gain: 512")
    header.append("Clipped samples: 2.00%")
    header.append("Latitude :   0  0.000")
    header.append("Longitude:   0  0.000")
    header.append("Altitude : 0 m")
    header.append("No. satellites: 0")
    header.append('Maximum amplitude: {} / {}'.format(maxVal, maxVal))
    return header


def create_file(data: list[str], header: list[str], fileName: str, newName: str):
    st = read(fileName)
    metadata = st[0].stats

    resultfilename = f'{newName}{metadata.network}{metadata.station}.txt'

    with (open(resultfilename, 'w') as TXT_FILE):
        for value in header:
            TXT_FILE.write(f"{value}\n")

        for value in data:
            TXT_FILE.write(''.join(value))

        TXT_FILE.write("0 ")
        print(f"{resultfilename} created successfully")

        TXT_FILE.close()


#
#   PLOT SECTION
#
def plot_seismograms(x: str, y: str, z: str):
    threechannels = read(x)
    threechannels += read(y)
    threechannels += read(z)
    threechannels.plot(size=(800, 600))
