# 649_scrap

The purpose of these scripts is to download the 649 winning from the BCLC playnow.com website with the hope of gaining some insight into the winnings.

The Playnow website requires javascript to be ran in browser in order to get information from the winnings.
For this, I use the [selenium] package to load the javascript in the chrome web driver, then save the html locally.

Once I have all the data, I use [BeautifulSoup] to extract the information and load it into a sqlite database, where I can then export to a csv if needed.

I will not upload the csv file of the data itself, as I'm not sure how much the government wants me posting that to another website, but it should be all publicly available.

