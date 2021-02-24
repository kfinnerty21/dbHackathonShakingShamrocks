Notes on Czech Bank Account Data

There is anonymised Czech bank account data available, originally released in 1999 for a data mining challenge and referred to as the Berka Dataset.

The dataset was later used as part of a data analytics assignment at the University of North Carolina at Charlotte in 2002.

The dataset comprises a number of files, of most interest to us is trans.asc which includes one million transactions for 4500 unique accounts, for the period
between 1/1/93 and 31/12/98.  The data includes Czech words, but a dictionary is available.

I have preprocessed the transaction dataset, translating the Czech to English and creating separate Year, Month and Day columns from the date.
I have uploaded this processed dataset in the repo, along with the zip file of the raw data.

I'm not sure if the data will be of any use, as it is quite old so doesn't really represent contemporary spending patterns (e.g. there will be very little if any
online shopping transactions), and the categories of transaction are quite high-level (Insurance, Payment of Statement, Interest Paid or Charged, Loan Payment,
Pension Payment, Household Payment, etc). But in case it's of use, it's available here.

Links:
Details on the data set, including data model and data dictionary: https://webpages.uncc.edu/mirsad/itcs6265/group1/domain.html
Website discussing the dataset: https://data.world/lpetrocelli/czech-financial-dataset-real-anonymized-transactions
Source of zip file: https://www.researchgate.net/post/Is_there_any_public_database_for_financial_transactions_or_at_least_a_synthetic_generated_data_set

Zip file of raw data (downloaded from the researchgate.net link above): data_berka.zip
CSV file of processed transaction data: czech_bank_data_preprocessed.csv