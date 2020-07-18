# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os, json, time, logging
import requests
import azure.functions as func
from __app__.shared_code.query_cosmos import CosmosQueryClient


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    cosmosQueryClient = CosmosQueryClient()
    product_id = req.params.get('product_id')

    try:
        if "," in product_id:
            productIDs = product_id.split(",")
        else:
            productIDs = [product_id]
        product_details = cosmosQueryClient.getProductDetails(productIDs)
        response = json.dumps({"items": product_details})
        logging.info(response)
    except Exception as e:
        logging.error(e)
        response = {}["message"]=f"Recommendation Process Failed with exception {e}"

    return response