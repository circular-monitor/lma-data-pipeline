"""
This module filters useful columns and data points in the original data file
logs how many erroneous data points have been filtered on which basis
and returns a dataframe ready for the further analysis
"""
import logging
import numpy as np
import variables as var


def run(dataframe):
    # selection of the columns we want to include in our analysis
    LMA_columns = var.LMA_columns

    # filter the requested columns from the original dataframe
    try:
        LMA = dataframe[LMA_columns]
        logging.info(f'Original dataset length: {len(LMA.index)} lines')
    except Exception as error:
        logging.critical(error)
        raise

    original_length = len(LMA.index)

    # if 'Herkomst' has all columns empty, copy from 'Ontdoener'
    Herkomst_columns = [col for col in LMA.columns if 'Herkomst' in col]
    all_null = [LMA[col].isnull() for col in Herkomst_columns]
    idx = LMA[np.bitwise_and.reduce(all_null)].index
    for col in Herkomst_columns:
        orig_col = 'Ontdoener_' + col.split('_')[-1]
        LMA.loc[idx, col] = LMA[orig_col]

    # filter empty fields
    # log all empty fields before removing them
    # empty role columns
    roles = var.roles
    for role in roles:
        # empty company name
        # note: Herkomst does not have company name!
        if role != 'Herkomst':
            e = len(LMA[LMA[role].isnull()].index)
            if e:
                LMA = LMA[LMA[role].notnull()]
                logging.warning(f'{e} lines do not have a {role} specified and will be removed')

        # empty postcode
        postcode = role + '_Postcode'
        e = len(LMA[LMA[postcode].isnull()].index)
        if e:
            LMA = LMA[LMA[postcode].notnull()]
            logging.warning(f'{e} lines do not have a {postcode} specified and will be removed')

    # empty year
    e = len(LMA[LMA['MeldPeriodeJAAR'].isnull()].index)
    if e:
        LMA = LMA[LMA.MeldPeriodeJAAR.notnull()]
        logging.warning(f'{e} lines do not have a year specified and will be removed')

    # empty month
    e = len(LMA[LMA['MeldPeriodeMAAND'].isnull()].index)
    if e:
        LMA = LMA[LMA.MeldPeriodeMAAND.notnull()]
        logging.warning(f'{e} lines do not have a month specified and will be removed')

    # zero amount
    e = len(LMA[LMA['Gewicht_KG'] < 1].index)
    if e:
        LMA = LMA[LMA['Gewicht_KG'] >= 1]
        logging.warning(f'{e} lines have specified 0 weight and will be removed')

    # zero trips
    e = len(LMA[LMA['Aantal_vrachten'] < 1].index)
    if e:
        LMA = LMA[LMA['Aantal_vrachten'] >= 1]
        logging.warning(f'{e} lines have specified 0 trips and will be removed')

    if original_length:
        perc = round(len(LMA.index) / original_length * 100, 1)
        logging.info(f'Final dataset length: {len(LMA.index)} lines ({perc}%)')

    return LMA
