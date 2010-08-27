19.08.2010

	Full text search imporovement.
	Full text search only on Club model. 

	New application - keywords.
		It saves every keyword if referer if one of the 
		most popular search engine. The max length of the stack where the keywords are saved
		is settings.MAX_STACK_LENGTH. 

	Installation:
		manage.py syncdb
			- will create tables for keywords application, and fill initial keywords (3 for each site)

		manage.py migrate directory 0013
			- will create the full text index for directory.Club model.
			fields are:  name, description, address, phone, email, homepage

27.08.2010
	Keywords application in pluggable now. Enable it for some site with adding site id to the 
	KEYWORDS_ON_SITES tuple in the settings.py
