import matlab.engine
# https://www.mathworks.com/content/dam/mathworks/mathworks-dot-com/support/sysreq/files/python-compatibility.pdf
# https://de.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html
# funktioniert nur mit python 3.7/8
import numpy as np
import os

def matlab_calc_feature(spike_list, amp, rec_dur, SaRa, feature):

    feature_value = matlab_all_feature(TS=spike_list, AMP=amp, rec_dur=rec_dur, SaRa=SaRa,
                                           Selection=feature, time_win=rec_dur, FR_min=6)
    feature_mean = feature_value[0][0]
    feature_std = feature_value[1][0]
    feature_values = feature_value[2][0]
    feature_pref = feature_value[3][0]
    feature_label = feature_value[4][0]
    return feature_mean, feature_values, feature_std, feature_pref, feature_label



def matlab_all_feature(TS, AMP, rec_dur, SaRa, Selection, time_win, FR_min, N=0, binSize=0):
    TS = np.transpose(TS)
    TS = matlab.double(TS.tolist())
    AMP = matlab.double(AMP.tolist())
    os.path.abspath(os.getcwd())
    drcell_path = os.path.abspath(os.getcwd())
    path_manuell_python = drcell_path + '/DrCell/shared/Engines/Python'
    eng = matlab.engine.start_matlab()  # MatLab Umgebung aufrufen
    eng.cd(path_manuell_python)
    values = eng.adapter_python(drcell_path, TS, AMP, float(rec_dur), float(SaRa), Selection, float(time_win), float(FR_min))
    eng.quit()
    print(f"Mean of {Selection}: {values[0][0]}")
    print("Done Calculating " + Selection)
    return values
    # eng.adapter(TS, AMP, rec_dur, SaRa, Selection, time_win, FR_min, N, binSize)
