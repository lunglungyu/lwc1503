import statsmodels.api as sm
from statsmodels.compat.python import (iteritems, range, lrange, string_types, lzip,
                                zip, map)
import numpy as np
from statsmodels.regression.linear_model import OLS
from statsmodels.tools.tools import add_constant, Bunch
from statsmodels.tsa.tsatools import lagmat, lagmat2ds

def hacked_gct (x, maxlag, addconst=True, verbose=True):

    #from scipy import stats

    x = np.asarray(x)

    if x.shape[0] <= 3 * maxlag + int(addconst):
        raise ValueError("Insufficient observations. Maximum allowable "
                         "lag is {0}".format(int((x.shape[0] - int(addconst)) /
                                                 3) - 1))

    resli = {}

    for mlg in range(1, maxlag + 1):
        result = {}
        if verbose:
            print('\nGranger Causality')
            print('number of lags (no zero)', mlg)
        mxlg = mlg

        # create lagmat of both time series
        dta = lagmat2ds(x, mxlg, trim='both', dropex=1)

        #add constant
        if addconst:
            '''dtaown = add_constant(dta[:, 1:(mxlg + 1)], prepend=False)'''
            dtajoint = add_constant(dta[:, 1:], prepend=False)
        else:
            raise NotImplementedError('Not Implemented')
            #dtaown = dta[:, 1:mxlg]
            #dtajoint = dta[:, 1:]

        # Run ols on both models without and with lags of second variable
        '''res2down = OLS(dta[:, 0], dtaown).fit()'''
        res2down = 'skipped'
        res2djoint = OLS(dta[:, 0], dtajoint).fit()

        #print results
        #for ssr based tests see:
        #http://support.sas.com/rnd/app/examples/ets/granger/index.htm
        #the other tests are made-up
        '''
        # Granger Causality test using ssr (F statistic)
        fgc1 = ((res2down.ssr - res2djoint.ssr) /
                res2djoint.ssr / mxlg * res2djoint.df_resid)
        if verbose:
            print('ssr based F test:         F=%-8.4f, p=%-8.4f, df_denom=%d,'
                   ' df_num=%d' % (fgc1,
                                    stats.f.sf(fgc1, mxlg,
                                               res2djoint.df_resid),
                                    res2djoint.df_resid, mxlg))
        result['ssr_ftest'] = (fgc1,
                               stats.f.sf(fgc1, mxlg, res2djoint.df_resid),
                               res2djoint.df_resid, mxlg)

        # Granger Causality test using ssr (ch2 statistic)
        fgc2 = res2down.nobs * (res2down.ssr - res2djoint.ssr) / res2djoint.ssr
        if verbose:
            print('ssr based chi2 test:   chi2=%-8.4f, p=%-8.4f, '
                   'df=%d' % (fgc2, stats.chi2.sf(fgc2, mxlg), mxlg))
        result['ssr_chi2test'] = (fgc2, stats.chi2.sf(fgc2, mxlg), mxlg)

        #likelihood ratio test pvalue:
        lr = -2 * (res2down.llf - res2djoint.llf)
        if verbose:
            print('likelihood ratio test: chi2=%-8.4f, p=%-8.4f, df=%d' %
                   (lr, stats.chi2.sf(lr, mxlg), mxlg))
        result['lrtest'] = (lr, stats.chi2.sf(lr, mxlg), mxlg)
        '''
        # F test that all lag coefficients of exog are zero
        rconstr = np.column_stack((np.zeros((mxlg, mxlg)),
                                   np.eye(mxlg, mxlg),
                                   np.zeros((mxlg, 1))))
        ftres = res2djoint.f_test(rconstr)
        if verbose:
            print('parameter F test:         F=%-8.4f, p=%-8.4f, df_denom=%d,'
                   ' df_num=%d' % (ftres.fvalue, ftres.pvalue, ftres.df_denom,
                                    ftres.df_num))
        result['params_ftest'] = (np.squeeze(ftres.fvalue)[()],
                                  np.squeeze(ftres.pvalue)[()],
                                  ftres.df_denom, ftres.df_num)

        resli[mxlg] = (result, [res2down, res2djoint, rconstr])

    return resli
