# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os, json, time, logging
import requests
from __app__.shared_code.query_cosmos import CosmosQueryClient
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    cosmosQueryClient = CosmosQueryClient()
    user_id = req.params.get('user_id')
    try:
        response = cosmosQueryClient.getUserRecommendations(user_id)
        logging.info(f"Recommendation Generated: {response}")
    except IndexError as ie:
        logging.error(ie)
        response = {}["message"]=f"User ID does not exist, no recommendations"
    except Exception as e:
        logging.error(e)
        response = {}["message"]=f"Recommendation Process Failed with exception {e}"

    return json.dumps(response)