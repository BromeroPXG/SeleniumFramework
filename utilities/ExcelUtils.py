# This script will be used to get different test data from a .csv file
# important note: EVERY RETURN FROM THIS PAGE WILL BE EITHER A LIST OR DICTIONARY (I HAVEN'T DECIDED YET)

import pandas as pd
from configurations.config import TestData


# use pd.set_option('display.max_colwidth', None) to view your ugly ass DF

class ExcelData:
    file_location = "C:/Users/bromero/PycharmProjects/SeleniumFramework/TestData/TestData_XLSX.xlsx"

    def __init__(self):
        return

    def get_URL_from_page(self, sheet, page):
        page_df = pd.read_excel(self.file_location, sheet_name=sheet, dtype=str)
        out_val = page_df.loc[page_df['Page'] == page, TestData.environment].iloc[0]
        return out_val

    def get_user_data_dict(self, user_type):
        user_df = pd.read_excel(self.file_location, sheet_name="Logins", dtype=str)
        single_row = user_df.loc[user_df['Account Type'] == user_type]
        out_dict = single_row.to_dict(orient='records')
        return out_dict[0]

    # list_of_SKUs param is optional
    # if left blank, function will generate all SKU/URL tupels in a list for given sheet
    # i.e. get_sku_validation_params(drivers) will yeild:
    # ...[url..., DR-PXG15), (url..., DR-PXG14), (url..., DR-PXG13),... etc]
    # note: list_of_SKUs must be passed as an ARG
    def get_SKU_validation_params(self, environment, sheet, *list_of_SKUs):
        if environment == "production":
            white_list = "005"
        else:
            white_list = "production"
        user_df = pd.read_excel(self.file_location, sheet_name=sheet, usecols=lambda x: white_list not in x)
        out_dict = user_df.set_index('production').T.to_dict(orient='records')
        out_tuple_list = list(out_dict[0].items())
        return out_tuple_list

#print(ExcelData().get_user_data_dict("guest"))