def del_outliers(series):
    d = series.sort_values()
    nplus= d.shape[0] + 1
    q1_loc = nplus // 4 - 1
    q1 = d.iloc[q1_loc] + (nplus / 4 - nplus//4) * d.iloc[q1_loc+1]
    # q2 = np.median(d)
    q3_loc = 3 * (q1_loc+1)
    q3 = d.iloc[q3_loc]
    IQR = q3 - q1
    out_m = 1.5 * IQR
    series = series[series > q1-out_m]
    return series[series < out_m + q3]