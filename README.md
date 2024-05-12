# FDM_FILE_Rule

This python script demonstrates how to use FMD File Rules. 


# How to install  

Please update the FDM hostname, credential, policy name and filetype in the script!


# How to run  

```py
python3 fdm-block-file.py  
Token Received.  
File Policy Found.  
Policy Content: [  
    {
        "version": "lf36zc4oirwpq",  
        "name": "Block PDF Files",  
        "description": "Block PDF Files",  
        "fileTypeCategories": [],  
        "fileTypes": [  
...  
```



```py
python3 fdm-create-file-policy.py -n test1  
Token Received.  
Policy Content: [  
    {  
        "version": "jpxgk244krer5",  
        "name": "Block Malware All",  
        "description": "Block Malware in all file categories",  
        "firstTimeAnalysis": true,  
     
```


```py 
python3 fdm-delete-file-policy.py -n test1  
Token Received.  
ID: 4a2e48cb-1075-11ef-944b-57fb5d896911  
Deleting File Policy: test1  
Done: <Response [204]>  
```




More info:  


File Policy:  
https://developer.cisco.com/docs/ftd-api-reference-v6-ftd-v6-7/addfilepolicy/    
FileType:  
https://developer.cisco.com/docs/ftd-api-reference-v6-ftd-v6-7/getfiletype/  
Rule:  
https://developer.cisco.com/docs/ftd-api-reference-v6-ftd-v6-7/addfilerule/#filetypecategory  
