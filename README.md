RenameAndroidPackage
====================

Usage
-----

Works with Python 2.7. 

	renamePackage.py [ -p <project_path> ] [ -o <old_name> ] [ -n <new_name> ] 

	Options:
	  -h, --help            show this help message and exit
	  -p PROJECT_PATH, --project_path=PROJECT_PATH
	  -o OLD_PACKAGE_NAME, --old_package_name=OLD_PACKAGE_NAME
	  -n NEW_PACKAGE_NAME, --new_package_name=NEW_PACKAGE_NAME

Example:
	renamePackage.py -p ~/dev/myApp -o com.example.myapp -n com.awesome.superapp
