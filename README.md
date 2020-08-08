# drug-shortages

Purpose of this script is to script the ASHP All Drug Shortages page and compile it into a database? from here: 
https://www.ashp.org/Drug-Shortages/Current-Shortages/Drug-Shortages-List?page=All

### What Works

Script can scrape and save to csv the overall list information capturing generic name, shortage status, 
revision date, link to page with more details, and also the drug id found in the url

### What's broken

Does not work on the most basic level besides what's mentioned above. Still in progress..

### Currently in progress

Working on logic to scrape each individual drug's detail page to extract information about products 
affected, reason for shortage, available products, estimated resupply date, references, and last updated information

### Planned for future

Eventually hope to build out a continuously running script (or would work with a task scheduler) to check the
website daily and update the database with new updates and also send a notification of updates.

Also maybe incorporate the FDA's drug shortage information as well.
