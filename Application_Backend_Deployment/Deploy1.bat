@REM Copyright (c) Microsoft Corporation.
@REM Licensed under the MIT license.

Powershell.exe -executionpolicy remotesigned -File ^
    Deploy1.ps1 ^
    --location "westus2" ^
    --subscriptionID "584b6f20-2dee-4f11-a030-af9877a27492" ^
    --CertificateEamil "dongbum@outlook.com" ^
    --existingresourceGroupName "contosoretail" ^
    --existingstorageAccountName "contosoretailstorage" ^
    --existingcosmosDBName "contosocosmos-sql" ^
    --recommendMLServiceURL "http://20.190.8.243:80/api/v1/service/retail-ai-item-recommenderv4/score" ^
    --recommendMLServiceBearerToken "qUIwse3yarzaXNSoeXap0t5LQCGSAJIk"




    @REM --location "westus2" ^
    @REM --subscriptionID "{put your subscriptionID for deployment}" ^
    @REM --CertificateEamil "{put you real email address}" ^
    @REM --existingresourceGroupName "{put your resource group name}" ^
    @REM --existingstorageAccountName "{put your storage account name}" ^
    @REM --existingcosmosDBName "{put your CosmosDB Name}" ^
    @REM --recommendMLServiceURL "{put recommendation ml service endpoint URL from MLStudio}" ^
    @REM --recommendMLServiceBearerToken "{put service BearerToken from MLStudio}"