import numpy as np
import scipy.integrate as integrate
from scipy.signal import argrelextrema
from scipy.optimize import curve_fit
from scipy.stats import norm


def normal(x, mu, sigma):
    return (1 / np.sqrt((2 * np.pi * sigma ** 2))) * np.exp(-(x - mu)**2 / 2 * sigma ** 2)


def genome_model(x, a, b, c, d, mu, sigma):
    # decay = exp_decay(x, init, decay)
    N1 = normal(x, mu, sigma)
    N2 = normal(x, 2 * mu, 2 * sigma)
    N3 = normal(x, 3 * mu, 3 * sigma)
    N4 = normal(x, 4 * mu, 4 * sigma)
    sum_normals = a * N1 + b * N2 + c * N3 + d * N4
    return sum_normals


def simple_model(x, a, mu, sigma):
    N1 = normal(x, mu, sigma)
    sum_normals = a * N1
    return sum_normals


def get_model(xdata, ydata, model_type="genome", error_dist=True):
    if error_dist:
        first_minima = argrelextrema(ydata, np.less_equal)[0][0]
    else:
        first_minima = 2
    mode = np.argmax(ydata[first_minima:]) + first_minima + 1
    sqrt_mode = np.round(np.sqrt(mode)).astype(int)
    # first_maxima = argrelextrema(ydata[first_minima: ], np.greater)[0][0] + first_minima + 1
    # print('first minima: ', first_minima, 'mode: ', mode)
    err_mode = mode * 0.00000000000001
    err_mode_h = ydata[mode] * 0.05
    # print(first_maxima)
    if model_type == "genome":
        # init_vals = [ydata[first_maxima], 1, 1, 1, first_maxima, 1]
        init_vals = [ydata[mode], 1, 1, 1, mode, 1]
        bounds = ((0, 0, 0, 0, mode - err_mode, -np.inf),
                  (ydata[mode] + err_mode_h, np.inf, np.inf, np.inf, mode + err_mode, np.inf))
        model = genome_model
        num_vars = 6
    elif model_type == "simple":
        init_vals = [ydata[mode], mode, 1]
        bounds = ((0, mode - err_mode, 0),
                  (ydata[mode]+err_mode_h, mode+err_mode, np.inf))
        model = simple_model
        num_vars = 3
    else:
        raise ValueError("model_type must be either 'genome' or 'simple'")
    try:
        best_vals, covar = curve_fit(model, xdata[mode-sqrt_mode: mode+sqrt_mode], ydata[mode-sqrt_mode: mode+sqrt_mode], p0=init_vals, bounds=bounds)
    except RuntimeError:
        return tuple([-1] * num_vars)
    return tuple(best_vals)


def cdf_model(coefs, mu, sigma):
    mult = 1
    cum_cdf = 0
    for coef in coefs:
        cum_cdf += coef*norm.cdf((1-mult*mu)/mult*sigma)
        mult += 1
    return cum_cdf


def fit_model(xdata, ydata, model_type="genome"):
    if model_type == "genome":
        num_vars = 6
    elif model_type == "simple":
        num_vars = 3
    else:
        raise ValueError("model_type must be either 'genome' or 'simple'")
    best_vals = get_model(xdata, ydata, model_type=model_type)
    if (np.array(best_vals) == -1).all():
        return tuple([-1, -1, -1, -1])
    integrals = []
    for i in range(num_vars-2):
        a = best_vals[i]
        mu = best_vals[num_vars-2]
        sigma = best_vals[num_vars-1]
        normal_func = lambda x: a * normal(x, (i + 1) * mu, (i + 1) * sigma)
        integrals.append(integrate.quad(normal_func, 0, len(xdata)))
    return tuple([integral[0] for integral in integrals])


def main():
    print()


if __name__ == "__main__":
    main()
