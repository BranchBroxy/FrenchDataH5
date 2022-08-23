import os
import numpy as np
import h5py  # hdf5

def getListOfFiles(dirName, file_extension):
    extension_list = []
    if isinstance(file_extension, str):
        extension_list.append(file_extension)
    if isinstance(file_extension, list):
        extension_list = file_extension
    # create a list of file and subdirectories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath, extension_list)
        else:
            name, extension = os.path.splitext(fullPath)
            if any(extension in s for s in extension_list):
            # if extension == file_extension:
                allFiles.append(fullPath)

    return allFiles


def import_h5(path):
    import re


    TSE_ID_to_Label = {
                21:  0, 31:  1, 41:  2, 51:  3, 61:  4, 71:  5,
        12:  6, 22:  7, 32:  8, 42:  9, 52: 10, 62: 11, 72: 12, 82: 13,
        13: 14, 23: 15, 33: 16, 43: 17, 53: 18, 63: 19, 73: 20, 83: 21,
        14: 22, 24: 23, 34: 24, 44: 25, 54: 26, 64: 27, 74: 28, 84: 29,
        15: 30, 25: 31, 35: 32, 45: 33, 55: 34, 65: 35, 75: 36, 85: 37,
        16: 38, 26: 39, 36: 40, 46: 41, 56: 42, 66: 43, 76: 44, 86: 45,
        17: 46, 27: 47, 37: 48, 47: 49, 57: 50, 67: 51, 77: 52, 87: 53,
                28: 54, 38: 55, 48: 56, 58: 57, 68: 58, 78: 59,
    }

    spikes = []
    max_length_array = 0
    rec_dur = 0
    SaRa = 10000
    # os.listdir(os.path.split(path)[0])
    h5 = h5py.File(path, 'r')
    h5_data = h5["Data/Recording_0/TimeStampStream/Stream_0"]
    # SoureChannel
    for i in h5_data:
        if i != "InfoTimeStamp":
            if np.array(h5_data[i]).max()/1000000 > rec_dur:
                rec_dur = np.array(h5_data[i]).max()/1000000

            if np.array(h5_data[i]).size > max_length_array:
                max_length_array = np.array(h5_data[i]).size

    spikes = np.zeros(shape=(60, max_length_array))
    x = 0
    y = 0

    for counter, a in enumerate(h5_data):
        if a != "InfoTimeStamp":
            electrode = np.array(h5_data[a])/1000000

            time_stamp_entity_id = int(re.search(r'\d+', a).group())
            TimeStampEntityID = h5_data["InfoTimeStamp"]["TimeStampEntityID"]
            index = int(np.where(TimeStampEntityID == time_stamp_entity_id)[0])
            label = int(h5_data["InfoTimeStamp"]["Label"][index])

            electrode_row = TSE_ID_to_Label[label]

            spikes[electrode_row:electrode_row+electrode.shape[0], y:y+electrode.shape[1]] = electrode
    spike_list = spikes
    #spike_list = np.transpose(spikes)
    amp = np.zeros([spike_list.shape[1], spike_list.shape[0]])

    np.array(h5["Data/Recording_0/TimeStampStream/Stream_0/InfoTimeStamp"])["Label"]
    np.array(h5["Data/Recording_0/TimeStampStream/Stream_0/InfoTimeStamp"])["Label"]
    return spike_list, amp, rec_dur, SaRa

