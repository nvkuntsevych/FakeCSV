# FakeCSV  

Online service for generating CSV files with fake (dummy) data using Python and Django.  

Endpoints:  
/users/login/ - log in user;  
/users/logout/ - log out user;  
/schemas/list/ - get list of schemas of current user;  
/schemas/create/ - create new schema;  
/schemas/update/\<pk>/ - update existing schema by id;  
/schemas/delete/\<pk>/ - delete existing schema by id;  
/schemas/retrieve/\<pk>/ - retrieve existing schema by id;  
/schemas/generate/\<pk>/ - generate new dataset by schema id;  
/schemas/download/\<pk>/ - download existing dataset by schema id.  
