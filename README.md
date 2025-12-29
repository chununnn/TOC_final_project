# TOC_final_project
## environment setup
Make sure Python 3 is installed on your system before setting up the crawler environment.
This crawler also requires Google Chrome to be installed, since Selenium will launch Chrome through ChromeDriver.
Install the required Python packages:


```bash

py -m pip install selenium
py -m pip install webdriver-manager

py -m pip install flask
py -m pip install flask-cors

```
## Usage
Run fortune.py.
Open index.html which you can find in "fronted".

## Crawler Module Usage
Below is an example showing how to use the dispatcher to call different crawler modules:
```bash

from crawler.dispatcher import selectWeb


print("=== web1 test ===")
result = selectWeb("constellation", ["2000","5","15"])
print(result)

print("=== web2 test ===")
result = selectWeb("name", ["王","小民"])
print(result)

```
