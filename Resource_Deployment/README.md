# Deployment Guide  
  
We are currently working on an automated deployment process for this solution accelerator. Until this becomes available, here is the Manual Deployment Guide for deploying this Solution Accelerator.  

## Step 1: Get the data required for this Accelerator 
We are using the data provided by [this Kaggle Open Dataset](https://www.kaggle.com/mkechinov/ecommerce-behavior-data-from-multi-category-store), and you will need to download the data to your local machine. You will need the following CSVs/Datasets (download them):  
    - 2019-Oct.csv  
    - 2019-Nov.csv  
    - 2019-Dec.csv.gz (available [here](https://drive.google.com/drive/folders/1Nan8X33H8xrXS5XhCKZmSpClFTCJsSpE))   
    - 2020-Jan.csv.gz (available [here](https://drive.google.com/drive/folders/1Nan8X33H8xrXS5XhCKZmSpClFTCJsSpE))  


## Step 2: Create Azure Synapse Analytics (workspace preview)
In this step you will deploy an Azure Synapse Analytics (workspace preview), a SQL Pool and a Spark Pool in the Azure Synapse Analytics (workspace preview) and an Azure Data Lake (Gen2) Storage Account into your Azure Subscription that you are using for this solution accelerator. 

**Parameters**

Below are paramaters you will use to create the necessary resources for this solution accelerator. 
- **Subscription**: Azure Subscription Id 
- **Resource Group**: Name of the resource group to create 
- **Resource Name**: a globally unique name for creating the resources (must be 3-10 characters)
- **Username**: SQL user for Synapse workspace 
- **Password**: SQL user for Synapse workspace (must be at least 8 characters)
- **Location**: the location to deploy all the resources  
- **Directory Path**: the directory path where the dataset is located locally on your computer  
- **Cosmos DB Account Name**: the name of the Cosmos DB Account that will be used to store the User Recommendations and Product Details  


**Note:** You will be installing the Azure CLI extension for Azure Synapse 
1. Open Powershell as Administrator  
2. Navigate to this folder `0. Resource Deployment\deployment\backend\`  
3. Run the following command: 
    `./deployment_script.ps1`

## Step 3: Upload Assets and Data to the Synapse Workspace  
1. Launch the Synapse Studio:  
    - Go to the resource page in the portal and click the "Launch Synapse Studio"
2. Go to "Develop", click the "+", and click Import:  
    - In the demo's repository, go to `1. Analytics Deployment\synapse-studio\notebooks` to select all of the the Spark Notebooks  
3. Click Publish and confirm the assets to be published  
4. Go to the "Manage" tab in the Studio and click on the Apache Spark pools  
5. Click on the Spark Pool that you deployed and click "Packages, then click "Upload environment config file"  
    - Go to `1. Analytics Deployment\synapse-studio\cluster_config` to get the requirements.txt for upload  
6. Ensure that you give yourself and any other user admin privilages for this accelerator by going to the `Manage` tab, then `Access control` underneath `Security` and click "+ Add"
    - ![Manage, Access Control](./imgs/manage_access_control.png)  
7. Now click the Role dropdown and select all three roles, and search for your username and the other user's usernames to be added by using the search bar underneath the Role dropdown  
    - ![Add Roles](./imgs/add_roles.png)  
    - ![Add Users](./imgs/add_users.png)  
8. Click Apply at the bottom of the window.  
9. Now the environment should be ready to go for the execution of the scripts  
  
## Step 4: Setting Up the Cosmos DB and Azure Synapse Link  
### Create Containers for Recommendations and Product Details  
1. Go to the Cosmos DB service that was created in Step 2  
2. Follow the directions [here](https://docs.microsoft.com/en-us/azure/synapse-analytics/synapse-link/how-to-connect-synapse-link-cosmos-db#connect-an-azure-cosmos-db-database-to-a-synapse-workspace) to link your Cosmos DB to your Azure Synapse Analytics Workspace  
    - **NOTE**: Make sure to create a Linked Service in Synapse for the Cosmos DB connection and name it `retail_ai_cosmos_synapse_link`  
2. Go to the Data Explorer and create a database named `product_data` with the configurations below  
    - ![Add Database](./imgs/cdb_database.png)  
3. Underneath the database, create two containers with the following configurations  
    - ![Add Container for Product Details](./imgs/cdb_prod_detail.png)  
    - ![Add Container for User Recommendations](./imgs/cdb_user_recs.png)  
  
## Step 5: Running of the Notebooks and SQL Scripts  
1. Go to the Azure Portal and deploy a Azure Machine Learning Services resource into the resource group that you are using for this Solution Accelerator.  
    - You can search for `Machine Learning` after clicking on `Create a resource` to get the correct resource.  
    - **NOTE**: Along with the service comes the following:  
        - Azure Key Vault  
        - Azure Storage  
        - Azure Application Insights  
        - Azure Container Registry (**ATTENTION**: The name of this service will be needed in the deployment of the Azure Kubernetes Service)  
            - You can find the name of the associated Container Registry in the resource page of the deployed Azure Machine Learning Service  
2. Configure / Fill out the Parameters and then Run the following notebooks and scripts in order:  
    1. `01_CreateOrUpdateProductDetails`  
    2. `02_Clean_Training_Data`  
    3. `03_ALS_Model_Training`  
    4. `04_RecommendationRefresh`  
3. After all of these have been run successfully, the recommendations will have been generated for the User-Based Recommendations, and the model will be ready for deployment for the Item-Based Recommender served on Azure Kubernetes Service.  
  
## Step 6: Set Up the Item-Based Recommendation Web Service  
> In this section we will set up the Item-Based Recommendation Web Service by using Azure Machine Learning Service to package and deploy the model and Azure Kubernetes Service to host the model.  
### Deploy the resources  
> You will need the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) for this part, install it [from here](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest).  
> You will also need Python 3.7+ installed on your local mahcine.  
1. Go to the Azure Portal and deploy a Azure Machine Learning Services resource into the resource group that you are using for this Solution Accelerator.  
    - You can search for `Machine Learning` after clicking on `Create a resource` to get the correct resource.  
    - **NOTE**: Along with the service comes the following:  
        - Azure Key Vault  
        - Azure Storage  
        - Azure Application Insights  
        - Azure Container Registry (**ATTENTION**: The name of this service will be needed in the deployment of the Azure Kubernetes Service)  
            - You can find the name of the associated Container Registry in the resource page of the deployed Azure Machine Learning Service  
2. **After the Azure Machine Learning Service is deployed,** Use the Azure CLI steps below to deploy the Azure Kubernetes Service  
    ```sh
    # After running this, it will prompt you to login to the portal or enter in a device code
    az login  
      
    # Set the subscription context, you will need the subscription ID which can be found in the resource page for the resource group that you are using for this Solution Accelerator  
    az account set --subscription <enter-subscription-id>  
      
    # Now run the following to deploy the Azure Kubernetes Cluster  
    # NOTE: You will need to replace the following:  
        # - <insert-resource-group-name>: Name of the resource group you are using for this Solution Accelerator  
        # - <insert-desired-cluster-name>: Desired name for the AKS cluster  
        # - <insert-name-of-acr>: Name of the Azure Container Resitry that was deployed along with the Azure Machine Learning Service in the previous step  
    az aks create --resource-group <insert-resource-group-name> --name <insert-desired-cluster-name> --node-count 3 --enable-addons monitoring --generate-ssh-keys --attach-acr <insert-name-of-acr>  
      
    # Now you will need to create a Service Principal and give it Contributor access to your Azure Machine Learning Service  
    # Enter in your subscription ID, resource group name and the name of your Azure Machine Learning Service  
    az ad sp create-for-rbac -n "sp_synapse_accelerator" --role contributor
    --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group-name}/providers/Microsoft.MachineLearningServices/workspaces/{amls-name}  
    ```  
    - **NOTE**: Save the details of this Service Principal for future steps  
      
3. In the repository on your local machine, open `1. Analytics Deployment\amls\model_deployment\` in an IDE like VS Code  
4. Run `pip install -r requirements.txt`  
5. Edit the `download_model.py` file:  
    -  In the file `download_model.py`, edit the following:  
        ```python
        # Enter the name of the Azure Data Lake Storage Gen2 Account
        DATA_LAKE_NAME=""
        # Enter the name of the filesystem
        DATA_LAKE_FILE_SYSTEM_NAME=""
        # Enter the Primary Key of the Data Lake Account
        DATA_LAKE_PRIMARY_KEY=""
        ```  
    - Now run `python download_model.py`  
        - This should create a ZIP of the model on your local machine.  
6. Before deploying the model, edit the `score.py` file and the `deploy_model.py` file.  
    - `score.py` at the top of the file in the `init()` function:   
        ```python
        def init():
            ## Add in your Data Lake Details Here
            
            ## The DATA_LAKE_NAME should be the attached Data Lake to your Synapse Studio where the saved ALS Model is
            DATA_LAKE_NAME=""
            ## DATA_LAKE_FILE_SYSTEM_NAME should be the filesystem that is attached to the Synapse Studio where the Model is saved
            DATA_LAKE_FILE_SYSTEM_NAME=""
            ## DATA_LAKE_PRIMARY_KEY is the Primary Key of the Azure Data Lake Storage Gen2 that can be found in the portal
            DATA_LAKE_PRIMARY_KEY=""
        ```  
    - `deploy_model.py`  
        ```python
        # Subscription ID for the Solution Accelerator
        SUBSCRIPTION_ID=""
        # Resource Group that you are using for the Solution Accelerator
        RESOURCE_GROUP=""
        # Found in the output of the Service Principal created earlier
        TENANT_ID=""
        # Found in the output of the Service Principal created earlier
        APP_ID=""
        # Found in the output of the Service Principal created earlier
        SP_PASSWORD=""
        # Name of the Azure Machine Learning Service that you deployed
        WORKSPACE_NAME=""
        # Name of the Azure Kubernetes Service that you deployed
        AKS_CLUSTER_NAME=""
        ```  
7. Now run `python deploy_model.py` and the model will be registered with AMLS and deployed to the AKS cluster  
    
## Step 7: Setting Up the API Infrastructure  

### Set Up the Azure Function  

#### VS Code Instructions  
  
> **Note**: Ensure that you have the pre-requisities to develop and locally debug Python Azure functions. [See here](https://docs.microsoft.com/en-us/azure/developer/python/tutorial-vs-code-serverless-python-01#visual-studio-code-python-and-the-azure-functions-extension) for details.  
1. Deploy a Azure Function App with Python as the Runtime Stack  
    - Record the value for `AzureWebJobsStorage`  
2. Open a VS Code at the following filepath of this repository: `1. Analytics Deployment\api-layer\az_func\__app__`  
3. Edit the `local.settings.json` to fill in the following values:  
    ```
        {
            "IsEncrypted": false,
            "Values": {
                "FUNCTIONS_WORKER_RUNTIME": "python",
                "COSMOS_DB_ACCOUNT_NAME": "", // Account Name is the name of the actual Cosmos DB resource
                "COSMOS_DB_DATABASE_NAME": "product_data",
                "DETAIL_COLLECTION": "product_details",
                "USER_REC_COLLECTION": "user_recommendations",
                "COSMOS_KEY": "", // Primary Key found in Azure Portal in the Cosmos DB Resource Blade
                "AMLS_SERVICE_KEY": "", // Web Service Key Found in Azure Machine Learning Studio under Deployments
                "AzureWebJobsStorage": "", // Connection String found in Configuration blade of Function App
                "SCORING_URL": "" // URL of the Scoring Endpoint Found in Azure Machine Learning Studio under Deployments
            }
        }
    ```
4. Go to the Azure Function Extension and publish the function to the Function App deployed in Step 1 of this section.  
5. Go to the Function App in the Extension menu of VS Code and right click on the `Application Settings` and choose `Upload Local Settings`  
    - ![Index Setup](./imgs/app_setting.png)  
  
### Set Up Azure API Management  
  
1. Deploy Azure API Management in the resource group that you are using for this Solution Accelerator  
2. In Azure API Management, go to `APIs` and choose `Function App`  
    - ![Indexer Setup](./imgs/import_function_menu.png)  
3. Choose the Function App that you deployed and import all the functions.  
4. Configure the name of your API and click Create  
  
> Now you are ready to integrate the API with your front-end by utilizing the API you built in Azure API Managment.  
  
#### Example Recommendation Call  

```https://{ENTER_YOUR_APIM_NAME}.net/{VERSION_NUM_OF_API}/get_shopper_recommendations?subscription-key={APIM_SUBSCRIPTION_KEY}&user_id=568778435```

    