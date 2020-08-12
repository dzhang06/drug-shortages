# drug-shortages

Purpose of this script is to script the ASHP All Drug Shortages page and compile it into a database? from here: 
https://www.ashp.org/Drug-Shortages/Current-Shortages/Drug-Shortages-List?page=All

### What Works

Script can scrape and save to csv the overall list information capturing generic name, shortage status, 
revision date, link to page with more details, and also the drug id found in the url. 
Also, can generate new csv with all drug details stored within drug specific url.

### What's broken

nothing at the moment

### Currently in progress

Working on way to make something useful out of recent updates

### Planned for future

Eventually hope to build out a continuously running script (or would work with a task scheduler) to check the
website daily and update the database with new updates and also send a notification of updates.

Also maybe incorporate the FDA's drug shortage information as well.

# Changelog

8/10/20
- added ability to send email of current day's changes

8/8/20
- created method to filter main drugs table by date
- completed method to create drug details csv
- started changelog