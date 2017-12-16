import numpy as np
from matplotlib import pyplot as plt


def get_index(array):
    """ Returns an index calculated with the ratio between the standard
    deviation and the mean of the values contained in the given array.
    """
    st_dev = np.std(array)
    mean = np.mean(array)
    index = st_dev / mean
    
    return index


def get_norm_index(array):
    """ Returns the index calculated with the ratio between the standard
    deviation and the mean of the values contained in the given array, 
    normalized by the maximum value it could take.
    """
    new_array = [sum(array)] + [0] * (len(array) - 1)
    max_index = get_index(new_array)
    unnorm_index = get_index(array)
    norm_index = unnorm_index / max_index
    
    return norm_index


def get_spikes(data):
    """ Returns a dictionary with the spikes found in the data. Each 
    consecutive key contains a list whose values are the indexes from the 
    original array that make up a spike.
    """
    mean= np.mean(data)
    new_data = [max(i - mean, 0) for i in data]
    spikes = new_data[:]
    former_item = False
    num_spike = 0
    for idx in range(len(spikes)):
        if spikes[idx] != 0:
            if not former_item:
                num_spike += 1
            spikes[idx] = num_spike
            former_item = True
        else:
            former_item = False
    
    if spikes[0] != 0 and spikes[-1] != 0:
        idx = -1
        while spikes[idx] != 0:
            spikes[idx] = 1
            idx -= 1
    
    num_spikes = max(spikes)
    spikes_dict = {}
    for spike in range(1, num_spikes + 1):
        spikes_dict[spike] = [i for i in range(len(spikes)) if spikes[i] == spike]   
    
    return spikes_dict


def get_spikes_indexes(spikes, data):
    """ Returns a dictionary in wich each consecutive key contains the
    index corresponding to a spike from the given dictionary of spikes.
    """
    spikes_indexes = {}
    
    for key, spike in spikes.items():
        mean_others = sum([data[i] for i in range(len(data)) if i not in spike]) / len(data)
        isolated_spike = [mean_others] * len(data)
        for i in range(len(data)):
            if i in spike:
                isolated_spike[i] = data[i]
        index = get_norm_index(isolated_spike)
        spikes_indexes[key] = index
    
    return spikes_indexes
        

def get_total_index(indexes_dict):
    """ Returns an index calculated from the indexes in the given dictionary.
    """
    if len(indexes_dict) <= 1:
        return indexes_dict[1]
        
    else:
        indexes_list = [val for key, val in indexes_dict.items()]
        max_index = max(indexes_list)
    
        return max_index


def get_seasonality_index(data_list):
    """ Returns the seasonality index for the data contained in the given list.
    """

    if len(set(data_list)) <= 1:
        return 0.0
        
    else:
        my_spikes = get_spikes(data_list)
        my_spikes_indexes = get_spikes_indexes(my_spikes, data_list)  
        total_index = get_total_index(my_spikes_indexes)
        
        return np.exp(total_index - 1)



if __name__ == '__main__':  
    
    test_arrays = [[0,0,0,0,5,0,0,0,0,0,0,0],
                   [10,10,10,10,10,10,10,10,10,10,10,10],
                   [10,10,8,8,8,8,8,8,8,8,8,8],
                   [10,10,0,1,10,1,10,1,1,0,10,10],
                   [0,17,0,5,5,5,5,5,5,5,5,5],
                   [10,1,0,0,0,0,0,0,0,0,0,0],
                   [10,10,6,6,6,6,6,6,6,6,6,6]]
    
    for array in test_arrays:
        my_index = get_seasonality_index(array)
        print(my_index)
        
        N = len(array)
        x = range(N)
        width = 1/1.5
        plt.bar(x, array, width, color="blue")
        plt.show()

    
