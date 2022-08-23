matlab_feautre_list_french_data = [
'Sync_CC_selinger',
'Sync_STTC',
'Sync_MI1',
'Sync_MI2',
'Sync_PS',
'Sync_PS_M',
'Sync_Contrast',
'Sync_Contrast_fixed',
'Sync_ISIDistance',
'Sync_SpikeDistance',
'Sync_SpikeSynchronization',
'Sync_ASpikeSynchronization',
'Sync_AISIDistance',
'Sync_ASpikeDistance',
'Sync_RISpikeDistance',
'Sync_RIASpikeDistance',
'Sync_EarthMoversDistance',
'Connectivity_TSPE']

matlab_feautre_list_french_data_test = [
'Sync_RIASpikeDistance',
'Sync_Contrast',
'Connectivity_TSPE'
]

def get_list_of_files(path, file_type):
    """
        Generates a list with all file path from a given path.
        Parameters
        ----------
        path : string
            Either a path from a single file or a path of a directory.
        file_type : string, list of string
            The extension of the file type which should be taken into account.
            Can be one or more than one extension.

        Returns
        -------
        list_of_files : list of string
            Returns the synchrony of the input spike trains.

        """
    from import_file import getListOfFiles
    import os
    all_files = []
    # check if path is a file or directory
    if os.path.isdir(path):
        all_files = getListOfFiles(path, file_type)
    else:
        all_files.append(path)
    return all_files


def calculate_save_matlab_feature(data):
    """
            Calculates, saves and exports the Data in a csv file.
            Parameters
            ----------
            data : list of strings
                List of all files which will be included in the analysis .
            Returns
            -------
            path_of_csv : string
                Returns the path of the csv file where all calculated features and plots are saved.

            """

    from matlab_apy import matlab_calc_feature
    from import_file import import_h5
    from export_feature import export_feature_in_csv, export_feature_in_hdf5
    for file in data:
        spike_list, amp, rec_dur, SaRa = import_h5(file)
        for feature in matlab_feautre_list_french_data:
            # calculates the features via matlab
            feature_mean, feature_values, feature_std, feature_pref, feature_label = matlab_calc_feature(spike_list, amp, rec_dur, SaRa, feature)
            # saves the feature in csv file, csv_filename is path
            csv_path = export_feature_in_csv(feature, feature_mean, feature_std, feature_values, feature_pref, feature_label, csv_filename="Feature.csv", feature_file=file)
            # saves the feature in hdf5 file
            # export_feature_in_hdf5(feature, feature_mean, feature_std, feature_values, feature_pref, feature_label, af_filename="Feature.hdf5", feature_file=file)
            # plots the feature if necessary

    return csv_path

def post_process_feature(csv_path, h5_path):
    """
            Manipulates the features if necessary.
            Parameters
            ----------
            data : list of strings
                List of all files which will be included in the analysis .
            Returns
            -------
            path_of_csv : string
                Returns the path of the csv file where all calculated features and plots are saved.

            """

    from manipulate_feature import read_csv_file, apply_DDT_to_CM, TSPE_DDT, CM_number_of_connections,\
        calculate_n_moment_of_CM, CM_ratio_of_mean_of_strenght_connections, find_div_of_file, find_group_of_file,\
        get_sync_data_frame
    from plot_feature import plot_CM, plot_data_over_div_con
    import numpy as np
    import pandas as pd
    data_frame = read_csv_file(csv_path)
    # read_h5_file(h5_path)
    # manipulates CMs with DDT
    FM = apply_DDT_to_CM(data_frame, faktor_std=2)
    connectivity_feature_count = 3
    # connectivity_feature = np.array(shape=(FM.size, connectivity_feature_count))
    data = []

    for counter, dataset in enumerate(FM):
        CM = dataset[1]
        file_name = dataset[0]
        plot_CM(CM, file_name)
        ratio_noc = CM_number_of_connections(CM)
        ratio_msc = CM_ratio_of_mean_of_strenght_connections(CM)
        # connectivity_feature
        total_moment, moment_of_inh, moment_of_exc = calculate_n_moment_of_CM(CM, n_moment=2)
        div = find_div_of_file(file_name)
        group = find_group_of_file(file_name)
        row = [file_name, div, group, CM, total_moment, moment_of_inh, moment_of_exc, ratio_noc, ratio_msc]
        data.append(row)

    connectivity_data_frame = pd.DataFrame(data, columns=["file_name", "DIV", "Group", "CM", "K2 both connections", "K2 inhibitory connections", "K2 excitatory connections", "Number Ratio", "Strength Ratio"])
    synchrony_data_frame = get_sync_data_frame(data_frame)
    plot_data_over_div_con(connectivity_data_frame)
    # plot_data_over_div_sync(synchrony_data_frame)
    print("here")


    return 0


if __name__ == '__main__':
    path = "/mnt/HDD/Data/FrenchData/"
    # path = "/mnt/HDD/Data/FrenchData/culture du 10_01_2022 version matlab_experience 2"
    # path = "/mnt/HDD/Data/FrenchData/culture du 10_01_2022 version matlab_experience 2/7div"
    # path = "/mnt/HDD/Data/FrenchData/culture du 10_01_2022 version matlab_experience 2/7div/CTRL"
    path = "/mnt/HDD/Data/FrenchData/culture du 10_01_2022 version matlab_experience 2/7div/CTRL/2021-10-23T14-51-29SC_10_01_2021_7DIV_38709_cortex.h5"
    # path = "/mnt/HDD/Data/FrenchData/culture_du_29_11_2021_version_matlab_experience_1/4div/ctrl"
    # path = "/mnt/HDD/Data/FrenchData/culture_du_29_11_2021_version_matlab_experience_1/7div/GST"

    print("Import of data ...")
    all_h5_files = get_list_of_files(path, [".h5"])
    print(all_h5_files)
    print("Total number of files: " + str(len(all_h5_files)))
    csv_feature_path = calculate_save_matlab_feature(all_h5_files)
    print("Feature Calculation completly finished")
    # sv_feature_path = "/mnt/HDD/Programmieren/Python/FrenchDataH5/Feature.csv"
    post_process_feature(csv_feature_path, "/mnt/HDD/Programmieren/Python/FrenchDataH5/AF/Feature.hdf5")
    print("Post Processing of Connectivty Matrix finished")









