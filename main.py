#!/usr/bin/env python3

import logging
import pandas as pd

import filtering
import clean
import prepare_kvk
import connect_nace
# import classify.run
# import save.run

import warnings  # ignore unnecessary warnings
warnings.simplefilter(action="ignore", category=FutureWarning)
pd.options.mode.chained_assignment = None

roles = ['Ontdoener', 'Herkomst', 'Verwerker']

if __name__ == '__main__':
    # logging: timestamp, warning level & message
    logging.basicConfig(filename='full.log',  # file name
                        filemode='w',  # overwrite
                        level=logging.DEBUG,  # lowest warning level
                        format='%(asctime)s [%(levelname)s]: %(message)s')  # message format

    # start pipeline
    logging.info('START PIPELINE...')

    # TEST DATAFRAME
    logging.info('LOAD DATASET...')
    try:
        dataframe = pd.read_excel('Testing_data/1_full_dataset.xlsx')
    except Exception as error:
        logging.critical(error)
        raise

    # # load KvK dataset
    # logging.info('PREPARE KVK DATASET...')
    # dataframe = prepare_kvk.run(dataframe)

    # filter
    dataframe = dataframe[:1]
    logging.info('FILTER DATASET...')
    dataframe = filtering.run(dataframe, roles)

    # clean
    logging.info('CLEAN DATASET...')
    dataframe = clean.run(dataframe, roles)

    # connect nace
    logging.info('CONNECT NACE...')
    dataframe = connect_nace.run(dataframe)

    # end pipeline
    logging.info('END PIPELINE...')

    # # classify
    # classified_df = classify.run(connected_df)

    # # save
    # saved_df = save.run(analyzed_df)
