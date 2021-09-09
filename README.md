# Cloud Guru Bulk Course Downloader
The [Cloud Guru](https://acloudguru.com/) course downloader uses selenium instances to responsively load pages, crawl backend links, and download videos in bulk. It is NOT for pirating and will not work unless you have a valid cloud guru account.



## Prerequestites
Python3 and the following python libraries must be installed before execution: ['requests', 'colorama', 'beautifulsoup4', 'selenium']

`pip install -r requirements.txt`


## Operation
This script allows a user to login through the command line (preferred and much faster) or copy an instance of the user's current Firefox browser profile upon execution to mitigate sign-in issues. Make sure you have the latest version of Firefox installed and you are signed into the website. Download the geckodriver executable from [Mozilla github](https://github.com/mozilla/geckodriver/releases).


Modify the defined variables at the top of the script:

 1 : THREADS - Number Of Threads To Run At Once.
 
 2 : WEBDRIVER_PATH - Point to geckodriver executable.
 
 3 : PROFILE_PATH - Point to Firefox profile <C:/Users/User/AppData/Roaming/Mozilla/Firefox/Profiles/xxxx.default-release>.

![](https://github.com/dragoneyeintel/Linux-Academy-Course-Rip/blob/main/Link%20Example.png)

Navigate to the course in a broser and copy the course name, in this case <introduction-to-python-scripting>. Execute the python script and insert this course name when prompted.
 
 ![.](https://github.com/dragoneyeintel/Linux-Academy-Course-Rip/blob/main/Example%20Operation.gif)

`sudo python3 CourseRip_v2-3.py`


## Archive
Archive contains all previous versions of the python script through development.


## Author

[@nootsploit](https://twitter.com/nootsploit)

https://dragoneyeintel.com
