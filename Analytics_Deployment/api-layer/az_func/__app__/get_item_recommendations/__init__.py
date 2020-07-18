# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os, json, time, logging
import requests
import azure.functions as func
from __app__.shared_code.query_cosmos import CosmosQueryClient



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    scoring_uri = os.getenv("SCORING_URL")
    amls_key = os.getenv("AMLS_SERVICE_KEY")
    input_id = req.params.get('product_id')
    logging.info(input_id)
    inputdict = {"product_id":int(input_id)}
    logging.info(inputdict)
    input_data = json.dumps(inputdict)
    headers = {'Content-Type': 'application/json'}
    headers['Authorization'] = f'Bearer {amls_key}'

    cosmosQueryClient = CosmosQueryClient()
    try:
        resp = requests.post(scoring_uri, input_data, headers=headers)
        logging.info(resp.text)
        resp_get_id = [str(item) for item in json.loads(resp.json())["related_products"]]
        logging.info(resp_get_id)
        product_details = cosmosQueryClient.getProductDetails(resp_get_id)
        response = {"related_products": product_details}
        logging.info(response)
    except ValueError as ve:
        logging.info(ve)
        logging.info("No recommendations")
        response = {"related_products": []}
    except Exception as e:
        logging.error(e)
        response = {}["message"]=f"Recommendation Process Failed with exception {e}"

    return json.dumps(response)