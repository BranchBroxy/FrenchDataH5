def export_feature_in_csv(feature, feature_mean, feature_std, feature_values, feature_pref, feature_label, csv_filename, feature_file):
    import os
    cwd = os.getcwd()
    csv_path = cwd + "/" + csv_filename

    append_data_to_csv(feature, feature_mean, feature_std, feature_values, feature_pref, feature_label, csv_path, feature_file)
    return csv_path


def append_data_to_csv(feature, feature_mean, feature_std, feature_values, feature_pref, feature_label, csv_path, feature_file):
    import pandas as pd
    try:
        import numpy as np
        df = pd.read_csv(csv_path)
        # df["new_column"] = "abc"
        df.loc[len(df.index)] = [feature_file, feature, feature_mean, feature_std, np.array(feature_values).tolist(), feature_pref, feature_label]
        df.to_csv(csv_path, index=False, decimal=".")
        # np.save("test", np.array(feature_values))
    except:
        import csv
        import os
        # print(os.getcwd())
        # path = os.getcwd() + "/Feature.csv"
        # print(csv_path)
        with open(csv_path, 'w') as my_file:

            writer = csv.writer(my_file, quoting=csv.QUOTE_ALL)
            header = ["file", "feature", "feature_mean", "feature_std", "feature_values", "feature_pref",
                      "feature_label"]
            writer.writerow(header)
        append_data_to_csv(feature, feature_mean, feature_std, feature_values, feature_pref, feature_label, csv_path, feature_file)


def export_feature_in_hdf5(feature, feature_mean, feature_std, feature_values, feature_pref, feature_label, af_filename, feature_file):
    import os

    cwd = os.getcwd()
    hdf5_path = cwd + "/AF/" + af_filename
    create_hdf5_file(feature, feature_mean, feature_std, feature_values, feature_pref, feature_label, hdf5_path, feature_file)
    return hdf5_path


def create_hdf5_file(feature, feature_mean, feature_std, feature_values, feature_pref, feature_label, af_path, feature_file):
    import h5py
    import numpy as np
    with h5py.File(af_path, "w") as f:
        print("Start creating .af file")
        feature_grp = f.create_group("Feature")
        #rec_info_grp = f.create_group("3BRecInfo")
        #user_info_grp = f.create_group("3BUserInfo")

        #########################################################
        #######################Attributes########################
        #########################################################
        print("Attributes")
        f.attrs["Version"] = "0.1"
        f.attrs["Description"] = "Alpha Version of Feature Save"


        #########################################################
        ####################A-Data############################
        #########################################################
        feature_grp.create_dataset("Feature", data=feature)
        feature_grp.create_dataset("Feature Mean", data=feature_mean)
        feature_grp.create_dataset("Feature Standard Deviation", data=feature_std)
        feature_grp.create_dataset("Feature Values", data=np.array(feature_values))
        #feature_grp.create_dataset("Feature Preferences", data=feature_pref)
        feature_grp.create_dataset("Feature Label", data=feature_label)
        # print("3BData: Attributes")
        # feature_grp.attrs.create(name="Version", data=101, shape=None, dtype=np.int32)
        # print("3BData")
        # results_ch_events = feature_grp.create_dataset("Raw", data=Raw)

