from simple_salesforce import Salesforce
import pandas as pd


class SOQL_query:
    # this utility queries SOQL db and cleans a nasty structure into a nice list of all SKUs
    # that should be available on a configurator
    def __init__(self):
        return

    def get_all_SKU_list(self, sku):

        sf = Salesforce(username='sa-bi@pxg.com.devint', password='ygw3muv!pxa7dpz8FNB', security_token='03Nj4Ih7PuGsWHF1iIgNuZjcq', instance = "https://pxgorg--devint.lightning.force.com/", domain = 'test')
        sf_data = sf.query(f"SELECT Id FROM Product2 WHERE ProductCode = '{sku}'")
        df = pd.DataFrame(sf_data)
        records_df = df.iloc[0]["records"]
        product_key = records_df["Id"]
        query_string = f"SELECT Option_Acumatica_SKU__c FROM SBQQ__ProductOption__c WHERE SBQQ__ConfiguredSKU__c = '{product_key}'"
        product_opt_soql = sf.query(query_string)
        prod_opt_df = pd.DataFrame(product_opt_soql["records"])
        all_skus = prod_opt_df["Option_Acumatica_SKU__c"].to_list()

        return all_skus

    #this will run a nested loop to test each sku in the above function (get_all_sku_list)
    # to see if the SKU has the channel permission (Direct)
    #arg channel_permission_list is a list of permissions to filter by
    #i.e. channel_permission ='direct'
    def get_all_online_skus_by_master(self, master_sku, channel_permission):
        sf = Salesforce(username='sa-bi@pxg.com.devint', password='ygw3muv!pxa7dpz8FNB',
                        security_token='03Nj4Ih7PuGsWHF1iIgNuZjcq',
                        instance="https://pxgorg--devint.lightning.force.com/", domain='test')
        sf_data = sf.query(f"SELECT Id FROM Product2 WHERE ProductCode = '{master_sku}'")
        df = pd.DataFrame(sf_data)
        records_df = df.iloc[0]["records"]
        product_key = records_df["Id"]
        query_string = f"SELECT Option_Acumatica_SKU__c FROM SBQQ__ProductOption__c WHERE SBQQ__ConfiguredSKU__c = '{product_key}'"
        product_opt_soql = sf.query(query_string)
        prod_opt_df = pd.DataFrame(product_opt_soql["records"])
        all_skus = prod_opt_df["Option_Acumatica_SKU__c"].to_list()
        final_sku_list = []
        counter = 0
        for sku in all_skus:
            if "HC2-" in sku:
                continue
            counter += 1
            permission_query_str = f"SELECT Acumatica_Description__c, Acumatica_SKU__c, Channel_Permission__c, IsActive FROM Product2 WHERE Acumatica_SKU__c = '{sku}'"
            query_out = sf.query(permission_query_str)
            sku_df = pd.DataFrame(query_out["records"])
            permissions = sku_df['Channel_Permission__c'].values[0]
            active_status = sku_df['IsActive'].values[0]
            if permissions is None:
                continue
            if channel_permission in permissions and active_status == "true":
                final_sku_list.append(sku)
        return final_sku_list
