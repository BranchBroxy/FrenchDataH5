sync_list = ['Sync_CC_selinger', 'Sync_STTC', 'Sync_MI1', 'Sync_MI2', 'Sync_PS', 'Sync_PS_M', 'Sync_Contrast',
                 'Sync_Contrast_fixed', 'Sync_ISIDistance', 'Sync_SpikeDistance', 'Sync_SpikeSynchronization',
                 'Sync_ASpikeSynchronization', 'Sync_AISIDistance', 'Sync_ASpikeDistance', 'Sync_RISpikeDistance',
                 'Sync_RIASpikeDistance', 'Sync_EarthMoversDistance']

con_list = ["K2 both connections", "K2 inhibitory connections", "K2 excitatory connections", "Number Ratio", "Strength Ratio"]
def read_csv_file(csv_path):
    """
                Imports a csv file and returns a Pandas Data Frame
                Parameters
                ----------
                csv_path : string
                    Path of csv file which will be imported
                Returns
                -------
                df : pandas.DataFrame
                    DataFrame which contains the file,feature,feature_mean,feature_std,feature_values,feature_pref and feature_label.

                """
    import pandas
    import numpy as np
    df = pandas.read_csv(csv_path)
    #  np.fromstring(string=CM, dtype=int, count=3600)
    return df


def apply_DDT_to_CM(df, faktor_std=1, verbose=False):
    """
                Applies the Double-Treshold-Algorithm (DDT) to a given Dataset
                Parameters
                ----------
                df : pandas.DataFrame
                    Path of csv file which will be imported

                faktor_std : float or int, optional
                    Faktor of how many times the standard deviation is multiplied and added to the mean of the data to generate a threshold.
                    Default: 1

                Returns
                -------
                FMs : np.array
                    Numpy array which contains the filename and the Connectivity Matrix with DDT applied.

                """
    import numpy as np
    TSPE_index = df[df["feature"] == "Connectivity_TSPE"].index.values.tolist()
    TSPE_df = df[df["feature"] == "Connectivity_TSPE"]
    shape_of_CM = csv_string_to_nparray(TSPE_df["feature_values"].iloc[0]).shape
    file = df.iloc[TSPE_index[0]]["file"]
    dt = np.dtype([('File', str, 2 * len(file)), ('CM_DDT', np.float64, shape_of_CM), ('CM', np.float64, shape_of_CM)])
    FMs = np.zeros(shape=(len(TSPE_index)), dtype=dt)
    for count, i in enumerate(TSPE_index):
        if verbose:
            print(f'Applying DDT to CM number {count+1} of {len(TSPE_index)}')
        CM = df.iloc[i]["feature_values"]
        file = df.iloc[i]["file"]
        CM = csv_string_to_nparray(CM)
        FM = TSPE_DDT(CM, faktor_std)
        FMs[count][0] = file
        FMs[count][1] = FM
        FMs[count][2] = CM

    return FMs

def get_con_data_frame(FM):
    from plot_feature import plot_CM
    import pandas as pd
    data = []

    for counter, dataset in enumerate(FM):
        CM = dataset[2]
        CM_DDT = dataset[1]
        file_name = dataset[0]

        ratio_noc = CM_number_of_connections(CM_DDT)
        ratio_msc = CM_ratio_of_mean_of_strenght_connections(CM_DDT)
        # connectivity_feature
        total_moment, moment_of_inh, moment_of_exc = calculate_n_moment_of_CM(CM_DDT, n_moment=2)
        div = find_div_of_file(file_name)
        group = find_group_of_file(file_name)
        row = [file_name, div, group, CM_DDT, CM, total_moment, moment_of_inh, moment_of_exc, ratio_noc, ratio_msc]
        data.append(row)

    connectivity_data_frame = pd.DataFrame(data, columns=["file_name", "DIV", "Group", "CM_DDT", "CM", "K2 both connections", "K2 inhibitory connections", "K2 excitatory connections", "Number Ratio", "Strength Ratio"])
    return connectivity_data_frame
def read_h5_file(h5_path):
    import numpy as np
    import h5py  # hdf5
    h5 = h5py.File(h5_path, 'r')
    h5_data = h5["Feature"]


def csv_string_to_nparray(s):
    """
                Converts a string to a numpy array.
                Parameters
                ----------
                s : string
                    String which contains a 2D numpy like array (e.g. "[[0, 3, 4] , [3, 8, 6]").
                Returns
                -------
                array : np.array
                    Converted 2D numpy array.

                """
    import re
    import ast
    import numpy as np
    # Remove space after [
    s=re.sub('\[ +', '[', s.strip())
    # Replace commas and spaces
    s=re.sub('[,\s]+', ', ', s)
    array = np.array(ast.literal_eval(s))
    return array


def TSPE_HT(CM, faktor_std=1):
    import numpy as np
    # CM = np.array([[0, 3, 5, 7, 2], [5, 0, 4, 6, 3], [2, 4, 0, 4, 7], [5, 3, 2, 0, 5], [2, 1, 4, 2, 0]])
    CM1 = np.ma.masked_equal(CM, 0)
    std = np.std(CM1, ddof=1)
    mean = np.mean(CM1)
    if mean > 0:
        HT = mean + faktor_std * std
        T1CM = np.where(CM > HT, CM, 0)
    else:
        HT = mean - faktor_std * std
        T1CM = np.where(CM < HT, CM, 0)
    return T1CM


def TSPE_DDT(CM, faktor_std=1):
    import numpy as np

    real_CM = CM
    CM_neg = np.where(CM < 0, CM, 0)
    CM_pos = np.where(CM > 0, CM, 0)
    T1CM_neg = TSPE_HT(CM_neg, faktor_std)
    T1CM_pos = TSPE_HT(CM_pos, faktor_std)
    T1CM = T1CM_pos + T1CM_neg
    # T1CM = np.array([[0, 0, 0, 7, 0], [0, 0, 0, 6, 0], [0, 0, 0, 0, 7], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])

    # RM = np.array([[0, 3, 5, 0, 2], [5, 0, 4, 0, 3], [2, 4, 0, 4, 0], [5, 3, 2, 0, 5], [2, 1, 4, 2, 0]])
    FM_pos = DDT(CM_pos, T1CM_pos, faktor_std)
    FM_neg = DDT(CM_neg, T1CM_neg, faktor_std)
    FM = FM_pos + FM_neg
    return FM

def DDT(CM, T1CM, faktor_std):
    import numpy as np
    import numpy.ma as ma

    mean = np.mean(CM)
    if mean > 0:
        RM = CM - T1CM
        RM1 = np.ma.masked_equal(RM, 0)
        El_anzahl = T1CM.shape[0]
        TM = np.zeros(shape=(El_anzahl, El_anzahl))
        for i in range(0, RM.shape[0]):
            iRow = RM1[i]
            i_Row = RM[i]
            if np.count_nonzero(i_Row) == 0:
                # @TODO: pass oder TM[i] = np.mean(iRow) oder TM[i] = 0
                TM[i] = 0
            elif np.count_nonzero(i_Row) == 1:
                TM[i] = 0
            elif np.count_nonzero(i_Row) == 2:
                TM[i] = np.mean(iRow) + faktor_std * np.std(iRow, ddof=1)
            else:
                for y in range(0, RM.shape[0]):
                    iRow.mask[y] = True
                    TM[i, y] = np.mean(iRow) + faktor_std * np.std(iRow, ddof=1)
                    if i_Row[y] != 0:
                        iRow.mask[y] = False
        T2CM = RM > TM
        T2CM = ma.masked_where(~T2CM, RM, copy=True)
        T2CM = T2CM.filled(0)
        FM = T1CM + T2CM
    else:
        RM = CM - T1CM
        RM1 = np.ma.masked_equal(RM, 0)
        El_anzahl = T1CM.shape[0]
        TM = np.zeros(shape=(El_anzahl, El_anzahl))
        for i in range(0, RM.shape[0]):
            iRow = RM1[i]
            i_Row = RM[i]
            if np.count_nonzero(i_Row) == 0:
                # @TODO: pass oder TM[i] = np.mean(iRow) oder TM[i] = 0
                TM[i] = 0
            elif np.count_nonzero(i_Row) == 1:
                TM[i] = 0
            elif np.count_nonzero(i_Row) == 2:
                TM[i] = np.mean(iRow) - faktor_std * np.std(iRow, ddof=1)
            else:
                for y in range(0, RM.shape[0]):
                    iRow.mask[y] = True
                    TM[i, y] = np.mean(iRow) - faktor_std * np.std(iRow, ddof=1)
                    if i_Row[y] != 0:
                        iRow.mask[y] = False
        T2CM = RM < TM
        T2CM = ma.masked_where(~T2CM, RM, copy=True)
        T2CM = T2CM.filled(0)
        FM = T1CM + T2CM


    return FM

def CM_number_of_connections(CM):
    """
        Counts the number of inhibitory and excitatory connctions and calculates the e/i ratio.
            Parameters
            ----------
            CM : np.array
                Connectivity Matrix.
            Returns
            -------
            ratio_number_of_connections : float
                Ratio of excitatory to inhibitory connections (R = number_of_excitatory_connections/number_of_inhibitory_connections).
            """
    import numpy as np
    CM_neg = np.where(CM < 0, CM, 0)
    CM_pos = np.where(CM > 0, CM, 0)
    CM_pos_masked = np.ma.masked_equal(CM_pos, 0)
    CM_pos_compressed = np.ma.compressed(CM_pos_masked)

    CM_neg_masked = np.ma.masked_equal(CM_neg, 0)
    CM_neg_compressed = np.ma.compressed(CM_neg_masked)

    number_of_inhibitory_connections = int(CM_neg_compressed.size)
    number_of_excitatory_connections = int(CM_pos_compressed.size)
    ratio_number_of_connections = number_of_excitatory_connections/number_of_inhibitory_connections
    return ratio_number_of_connections


def calculate_n_moment_of_CM(CM, n_moment=1):

    """
        Calculates the n-moment of the whole CM, exc_CM and inh_CM.
            Parameters
            ----------
            CM : np.array
                Connectivity Matrix.

            n_moment : int
                Nth moment which is going to be calculated from the whole CM, exc_CM and inh_CM.
            Returns
            -------
            total_moment: float
                Total nth moment of the complet CM.

            moment_of_inh : float
                Nth moment of the inhibitory CM.

            moment_of_exc : float
                Nth moment of the excitatory CM.
            """
    import numpy as np
    from scipy.stats import moment

    CM_neg = np.where(CM < 0, CM, 0)
    CM_pos = np.where(CM > 0, CM, 0)
    CM_pos_masked = np.ma.masked_equal(CM_pos, 0)
    CM_pos_compressed = np.ma.compressed(CM_pos_masked)

    CM_neg_masked = np.ma.masked_equal(CM_neg, 0)
    CM_neg_compressed = np.ma.compressed(CM_neg_masked)

    CM = CM.flatten()

    moment_of_inh = moment(CM_neg_compressed, moment=n_moment)
    moment_of_exc = moment(CM_pos_compressed, moment=n_moment)
    total_moment = moment(CM, moment=n_moment)

    return total_moment, moment_of_inh, moment_of_exc


def CM_ratio_of_mean_of_strenght_connections(CM):
    """
        Calculates the total ratio of the mean strength excitatory to the mean strength inhibitory
            Parameters
            ----------
            CM : np.array
                Connectivity Matrix.
            Returns
            -------
            ratio_mean_strength_of_connections : float
                Ratio of mean strength of excitatory to inhibitory connections.
            """
    import numpy as np
    CM_neg = np.where(CM < 0, CM, 0)
    CM_neg = CM_neg * -1
    CM_pos = np.where(CM > 0, CM, 0)
    CM_pos_masked = np.ma.masked_equal(CM_pos, 0)
    CM_pos_compressed = np.ma.compressed(CM_pos_masked)

    CM_neg_masked = np.ma.masked_equal(CM_neg, 0)
    CM_neg_compressed = np.ma.compressed(CM_neg_masked)

    mean_of_strength_inhibitory_connections = CM_neg_compressed.mean()
    mean_of_strength_excitatory_connections = CM_pos_compressed.mean()
    ratio_mean_strength_of_connections = mean_of_strength_excitatory_connections/mean_of_strength_inhibitory_connections
    return ratio_mean_strength_of_connections

def find_div_of_file(filename):
    div_string_position = filename.find("div")
    if filename[div_string_position-2].isnumeric():
        div = int(str(filename[div_string_position - 2]) + str(filename[div_string_position - 1]))
    else:
        div = filename[div_string_position-1]
    return div

def find_group_of_file(filename):

    if "CTRL" in filename.upper():
        return "CTRL"
    elif "FIBRILLAR TAU" in filename.upper() or "FIBRILLAR  TAU" in filename.upper():
        return "FIBRILLAR TAU"
    elif "GST" in filename.upper():
        return "GST"
    elif "SOLUBLE TAU" in filename.upper() or "SOLULE TAU" in filename.upper():
        return "SOLUBLE TAU"
    else:
        return False


def get_sync_data_frame(df):
    import pandas as pd
    from manipulate_feature import find_div_of_file, find_group_of_file

    # b = df[(df[['xk', 'yk']] == 0).all(1)].index.tolist()
    sync_index = df.loc[df["feature"].isin(sync_list)]
    data = []
    for index, row in sync_index.iterrows():
        file_name = row["file"]
        feature_name = row["feature"]
        feature_value = row["feature_mean"]
        div = find_div_of_file(file_name)
        group = find_group_of_file(file_name)
        row = [file_name, div, group, feature_name, feature_value]
        data.append(row)

    synchrony_data_frame = pd.DataFrame(data, columns=["file_name", "DIV", "Group", "Feature", "Value"])
    synchrony_data_frame['DIV'] = pd.to_numeric(synchrony_data_frame['DIV'])
    synchrony_data_frame = synchrony_data_frame.sort_values(by=["DIV", "Group"])
    return synchrony_data_frame

