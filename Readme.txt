-----------------Requirements-----------------
Only compatible with python 2.7

In case that you don't have python and you are on Windows, there is a video that could help
https://www.youtube.com/watch?v=gD4eulxGNok

You can check your python version using:
	python --version

If your python by default is V.2.7
	sudo pip install scrapy
	sudo pip install argparse

If your python by default is V.3.5
	sudo pip2 install scrapy
	sudo pip2 install argparse

-----------------How to run it?-----------------
If your python by default is V.2.7

	-To get the CSV of http://www.myairlease.com/available/fleetintel_list.
	 It gerenates the "FleetIntel_List.csv" with the information
		python myairlease_scraper.py 1 
	
	-To get the CSV of http://www.myairlease.com/available/available_for_lease.
	 It gerenates the "Available_assets_list.csv" with the information
		python myairlease_scraper.py 2
	
	-To build it all just
		python myairlease_scraper.py 3
		
-----------------How to run it?-----------------
If your python by default is V.3.5

	-To get the CSV of http://www.myairlease.com/available/fleetintel_list.
	 It gerenates the "FleetIntel_List.csv" with the information
		python2.7 myairlease_scraper.py 1 
	
	-To get the CSV of http://www.myairlease.com/available/available_for_lease.
	 It gerenates the "Available_assets_list.csv" with the information
		python2.7 myairlease_scraper.py 2
	
	-To build it all just
		python2.7 myairlease_scraper.py 3
