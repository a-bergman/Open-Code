"""

This module contains functions that render statistics and corresponding p-values in dataframes.

"""

#  Standard Imports
import pandas        as pd

# Stastical Imports
from scipy.stats import pearsonr, pointbiserialr
from scipy.stats import chi2_contingency

"""

The docstrings for each function contain the following:

- parameters  : values which must be entered, some of which have defaults
- description : what each function does
- returns     : the output of each function

The parameters section of each docstring is set up as:

parameter : definition : type : possible values (if applicable)

These functions are designed to build off of what is available in already sci-kit learn: 
either to add a metric that does not exist or to improve something does already exist.

"""
  
# Numeric - Numeric Data

def pearsonr_dataframe(df, x, y, columns):
    """
    Parameters:
    -----------
    df      : dataframe source of data                     : DataFrame : :
    x       : column to find correlations against          : str       : :
    y       : list of columns to be correlated against x   : str       : :
    columns : list of columns to be named in the dataframe : str       : :

    Description:
    ------------
    Generates a list of Pearson's r correlation coefficients and accompanying p-values for two numeric variables.

    Null Hypothesis:
    ----------------
    There is no correlation between two numeric variables

    Returns:
    --------
    A dataframe with two columns: the float Pearson's r coefficient (a float from -1 to 1) and the corresponding p-value; both are rounded to 
    5 decimal placs.
    """
    r_coef = [round(pearsonr(x = df[x], y = df[i])[0],5) for i in y]
    r_pval = [round(pearsonr(x = df[x], y = df[i])[1],5) for i in y]
    pval_sig = ["True" if i < 0.05 else "False" for i in r_pval]
    pr_df = pd.DataFrame([r_coef, r_pval, pval_sig],
                         index = ["Corr. Coef.", "P-Value", "Significant"],
                         columns = columns).T
    return pr_df

# Numeric - Binary Data

def pointbiserialr_dataframe(df, x, y, columns):
    """
    Parameters:
    -----------
    df      : the dataframe source of data                 : DataFrame : :
    x       : column with binary data                      : str       : :
    y       : list of columns with numeric data            : str       : :
    columns : list of columns to be named in the dataframe : str       : :

    Description:
    ------------
    Generates a list of point-biserial r coefficients and accompanying p-values for a **binary** variable and numeric variables.
    This correlation test assumes that the binary variable is _naturally_ binary _not_ artificially binary, i.e pass/fail.

    Null Hypothesis:
    ----------------
    There variables are independant.

    Returns:
    --------
    A dataframe with two columns: the float point-biserial r coefficient (a float from -1 to 1) and the corresponding p-value; both are rounded to 
    5 decimal places.
    """
    pbr_coef = [round(pointbiserialr(x = df[x], y = df[i])[0],5) for i in y]
    pbr_pval = [round(pointbiserialr(x = df[x], y = df[i])[1],5) for i in y]
    pval_sig = ["True" if i < 0.05 else "False" for i in pbr_pval]
    pbr_dataframe = pd.DataFrame([pbr_coef, pbr_pval, pval_sig], 
                                 index = ["Corr. Coef.", "P-Value", "Significant"],
                                 columns = columns).T
    return pbr_dataframe

# Categorical - Categorical Data

def chisquared_dataframe(df, x, y, columns):
    """
    Parameters:
    -----------
    df      : dataframe source of data : DataFrame             : DataFrame : :
    x       : name of categorical variable to be correlated to : str       : :
    y       : list of categorical variables to correlated to x : str       : :
    columns : list of columns to be named in the dataframe     : str       : :

    Description:
    ------------
    Generates a list of chi squared statistics, corresponding p-values, and degrees of freedom for pairs of categorical variables.

    Null Hypothesis:
    ----------------
    The variables are independant.
    
    Returns:
    --------
    A dataframe with three columns, the chi squared statistic (a float from 0 to +∞), the accompanying p-value, and the degrees of freedom.  They are all rounded
    to 5 decimal places.
    """
    chi2_coefs = []
    chi2_pvals = []
    chi2_dofs  = []
    for col in y:
        ct = pd.crosstab(df[x], df[col])
        chi2 = chi2_contingency(ct)
        chi2_coefs.append(round(chi2[0],5))
        chi2_pvals.append(round(chi2[1],5))
        chi2_dofs.append(round(chi2[2],5))
    pval_sig = ["True" if i < 0.05 else "False" for i in chi2_pvals]
    chi2_df = pd.DataFrame([chi2_coefs, chi2_pvals, pval_sig, chi2_dofs], 
                           index = ["Coefficient", "P Value", "Significant", "DOF"], 
                           columns = columns).T
    return chi2_df