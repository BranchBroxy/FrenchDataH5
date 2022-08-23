import numpy as np
import unittest

# how to run:
# python software_test.py -v

class Test_meta_functions(unittest.TestCase):
    def test_get_div(self):
        from manipulate_feature import find_div_of_file
        filename = "/mnt/HDD/Data/FrenchData/culture_du_29_11_2021_version_matlab_experience_1/17div/GST/2021-10-22T15-50-08SC_29_11_2021_7DIV_38818_cortex.h5"
        self.assertEqual(find_div_of_file(filename), 17)

    def test_get_group(self):
        from manipulate_feature import find_group_of_file
        filename = "/mnt/HDD/Data/FrenchData/culture_du_29_11_2021_version_matlab_experience_1/17div/GST/2021-10-22T15-50-08SC_29_11_2021_7DIV_38818_cortex.h5"
        self.assertEqual(find_group_of_file(filename), "GST")

class Test_CM_manipulation(unittest.TestCase):
    def test_CM_number_of_connections(self):
        from manipulate_feature import CM_number_of_connections
        CM = np.array([[0, -3, 5, 7, -2], [5, 0, 4, 6, 3], [2, -4, 0, -4, 7], [-5, 3, 2, 0, 5], [2, 1, -4, 2, 0]])
        number_of_negatives_values = 6
        number_of_positive_values = 14
        ratio = number_of_positive_values/number_of_negatives_values
        self.assertEqual(ratio, CM_number_of_connections(CM))

    def test_n_moment_of_CM_one(self):
        from manipulate_feature import calculate_n_moment_of_CM
        CM = np.array([[1, 2, -3, -4, 5], [-1, 2, 3, -4, -5], [1, 2, -3, 4, -5]])
        # 2nd moment =  Populationsvarianz (σ 2 ) not Stichprobenvarianz (s 2 ):
        self.assertAlmostEqual((10.88888888888889, 1.6734693877551021, 1.75), calculate_n_moment_of_CM(CM, n_moment=2))

    def test_ratio_of_mean_of_strenght_connections_1(self):
        from manipulate_feature import CM_ratio_of_mean_of_strenght_connections
        CM = np.array([[-1, -1, -1, 1], [-2, 2, 2, -2], [1, 1, -1, 1], [-2, 2, -2, 2]])
        calculated_ratio = CM_ratio_of_mean_of_strenght_connections(CM)
        expected_ratio = 1
        self.assertEqual(calculated_ratio, expected_ratio)

class TestDDT(unittest.TestCase):

    def test_DDT(self):
        from manipulate_feature import TSPE_DDT
        CM = np.array([[0, 3, 5, 7, 2], [5, 0, 4, 6, 3], [2, 4, 0, 4, 7], [5, 3, 2, 0, 5], [2, 1, 4, 2, 0]])
        FM_DDT = TSPE_DDT(CM)
        FM_real = np.array([[0, 0, 5, 7, 0], [5, 0, 0, 6, 0], [0, 0, 0, 0, 7], [5, 0, 0, 0, 5], [0, 0, 4, 0, 0]])
        self.assertEqual(True, np.array_equal(FM_real, FM_DDT))

    def test_apply_DDT_to_pos_CM(self):
        from manipulate_feature import apply_DDT_to_CM
        import pandas as pd
        CM = [[0, 3, 5, 7, 2], [5, 0, 4, 6, 3], [2, 4, 0, 4, 7], [5, 3, 2, 0, 5], [2, 1, 4, 2, 0]]
        FM_real_pos = np.array([[0, 0, 5, 7, 0], [5, 0, 0, 6, 0], [0, 0, 0, 0, 7], [5, 0, 0, 0, 5], [0, 0, 4, 0, 0]], dtype=np.float64)

        file = "file"
        feature = "Connectivity_TSPE"
        feature_mean = 35.0
        feature_std = 0.0
        feature_values = str(CM)
        feature_pref = "{'pref': matlab.double([])}"
        feature_label = "Mean node degree(TSPE)"
        test_df = {'file': [file], 'feature': [feature], 'feature_mean': [feature_mean], "feature_std": [feature_std],
                   'feature_values': [feature_values], 'feature_pref': [feature_pref], 'feature_label': [feature_label]}
        test_df = pd.DataFrame(data=test_df)

        """TSPE_df = test_df[test_df["feature"] == "Connectivity_TSPE"]
        shape_of_CM = csv_string_to_nparray(TSPE_df["feature_values"][0]).shape
        dt = np.dtype([('File', str, 2 * len(file)), ('CM', np.float64, shape_of_CM)])"""

        FM_DDT = apply_DDT_to_CM(test_df, faktor_std=1)
        self.assertEqual(True, np.array_equal(FM_real_pos, FM_DDT[0][1]))

    def test_apply_DDT_to_CM(self):
        from manipulate_feature import apply_DDT_to_CM
        import pandas as pd
        CM = [[0, -3, 5, 7, -2], [5, 0, 4, 6, 3], [2, -4, 0, -4, 7], [-5, 3, 2, 0, 5], [2, 1, -4, 2, 0]]
        FM_real = np.array([[0, 0, 5, 7, 0], [5, 0, 0, 6, 0], [2, 0, 0, 0, 7], [-5, 0, 0, 0, 5], [0, 0, -4, 0, 0]], dtype=np.float64)

        file = "file"
        feature = "Connectivity_TSPE"
        feature_mean = 35.0
        feature_std = 0.0
        feature_values = str(CM)
        feature_pref = "{'pref': matlab.double([])}"
        feature_label = "Mean node degree(TSPE)"
        test_df = {'file': [file], 'feature': [feature], 'feature_mean': [feature_mean], "feature_std": [feature_std],
                   'feature_values': [feature_values], 'feature_pref': [feature_pref], 'feature_label': [feature_label]}
        test_df = pd.DataFrame(data=test_df)

        """TSPE_df = test_df[test_df["feature"] == "Connectivity_TSPE"]
        shape_of_CM = csv_string_to_nparray(TSPE_df["feature_values"][0]).shape
        dt = np.dtype([('File', str, 2 * len(file)), ('CM', np.float64, shape_of_CM)])"""

        FM_DDT = apply_DDT_to_CM(test_df, faktor_std=1)
        self.assertEqual(True, np.array_equal(FM_real, FM_DDT[0][1]))

    def test_apply_DDT_to_neg_CM(self):
        from manipulate_feature import apply_DDT_to_CM
        import pandas as pd
        CM = [[0, -3, -5, -7, -2], [-5, 0, -4, -6, -3], [-2, -4, 0, -4, -7], [-5, -3, -2, 0, -5], [-2, -1, -4, -2, 0]]
        FM_real_neg = np.array([[0, 0, -5, -7, 0], [-5, 0, 0, -6, 0], [0, 0, 0, 0, -7], [-5, 0, 0, 0, -5], [0, 0, -4, 0, 0]], dtype=np.float64)

        file = "file"
        feature = "Connectivity_TSPE"
        feature_mean = 35.0
        feature_std = 0.0
        feature_values = str(CM)
        feature_pref = "{'pref': matlab.double([])}"
        feature_label = "Mean node degree(TSPE)"
        test_df = {'file': [file], 'feature': [feature], 'feature_mean': [feature_mean], "feature_std": [feature_std],
                   'feature_values': [feature_values], 'feature_pref': [feature_pref], 'feature_label': [feature_label]}
        test_df = pd.DataFrame(data=test_df)

        """TSPE_df = test_df[test_df["feature"] == "Connectivity_TSPE"]
        shape_of_CM = csv_string_to_nparray(TSPE_df["feature_values"][0]).shape
        dt = np.dtype([('File', str, 2 * len(file)), ('CM', np.float64, shape_of_CM)])"""

        FM_DDT = apply_DDT_to_CM(test_df, faktor_std=1)
        self.assertEqual(True, np.array_equal(FM_real_neg, FM_DDT[0][1]))

if __name__ == '__main__':
    unittest.main()