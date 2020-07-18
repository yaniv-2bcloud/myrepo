from azure.cosmos import CosmosClient, PartitionKey, exceptions
import os, json, logging

class CosmosQueryClient ():

    def __init__(self):
        
        self.auth_key = os.getenv("COSMOS_KEY")
        self.account_name = os.getenv("COSMOS_DB_ACCOUNT_NAME")
        self.db_name = os.getenv("COSMOS_DB_DATABASE_NAME")
        self.detail_coll_name = os.getenv("DETAIL_COLLECTION")
        self.user_rec_coll_name = os.getenv("USER_REC_COLLECTION")
        self.url = f"https://{self.account_name}.documents.azure.com:443/"
        try:
            self.client = CosmosClient(self.url, credential=self.auth_key)
            self.db_client = self.client.get_database_client(self.db_name)
            self.prod_detail_container = self.db_client.get_container_client(self.detail_coll_name)
            self.user_rec_container = self.db_client.get_container_client(self.user_rec_coll_name)
        except Exception as e:
            print(e)
            print("Default Settings Required By Demo:\n(1) Database Named: product_data\n(2) Product Detail Collection Named: product_details\n(3) User Recommendation Collection Named: user_recommendations\n\nOther Potential Issues:\n(1) Incorrect key provided in local.settings.json and/or the Function App settings.\n(2) Incorrect Account Name for the Cosmos Account Name parameter in local.settings.json and/or the Function App settings.")
    
    def getProductDetails(self, productIDs):
        if (len(productIDs) == 0):
            product_id_query_string = f"c.productID = '{productIDs[0]}'"
        else:
            product_id_query_string = " ".join([f"OR c.productID = '{x}'" if idx != 0 else f"c.productID = '{x}'" for idx, x in enumerate(productIDs)])

        query_statement = f"SELECT * FROM c WHERE {product_id_query_string}"
        logging.info(query_statement)
        query_result_items = self.prod_detail_container.query_items(query=f'{query_statement}',
                                                                    enable_cross_partition_query=True)

        product_details = [x for x in query_result_items]
        
        return product_details

    def getUserRecommendations(self, userID):
        query_statement = f"SELECT * FROM c WHERE c.user_id = '{userID}'"
        try:
            
            query_result_items = self.user_rec_container.query_items(query=f'{query_statement}',
                                                                        enable_cross_partition_query=True)
            logging.info(query_statement)
        except Exception as e:
            print(e)
            logging.error(f"ISSUE {e}")
        productIDs = json.loads([json.dumps(x) for x in query_result_items][0])["recommendations"]
        user_rec_object = {"user_id": userID, "items": self.getProductDetails(productIDs)} 
        return user_rec_object