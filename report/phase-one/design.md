# ECE568 Software Engineering of Web Applications
**Project Phase 1 - System Design Report**

* Sanjay Bharadhwaj Vijayaraghava - sv453
* Shreyas Ujjappa Megalamane - sm1717
* Mayank - um45
* Ashish Behl - acb228
* Soundarajan Thiagarajan - st694
* Anivesh Baratam - ab1517

## System Design

### Stocks Considered
1. Google - GOOGL
2. Yahoo - YHOO
3. Microsoft - MSFT
4. Amazon - AMZN
5. Twitter - TWTR

### Real Time Data

![Real Time data collection system design](real_time_design.png)

The above system flow design shows how the real-time finance data is extracted.

1. The real-time stock market data API is provided by *Yahoo Finance*.
2. The Python script requests data for various stock symbols from the API and reads the response.
3. The extracted data is raw, so the data is processed.
4. The raw data is converted to the required schema and stored in the *sqlite* database.

\pagebreak

### Historical Data
![Historical data collection system design](historical_design.png)

The above system flow design shows how the historical finance data is extracted.

1. The historical stock data is stored in *Yahoo Finance API* and it is to be queried using *Yahoo Query Language* (*YQL*).
2. A Python API (*yahoo_finance*) is used which retrieves the data from those repositories and presents in JSON format.
3. Then, the data is read and stored in the *sqlite* database.

## Submission Files
* Please find `schema.pdf` and `README.pdf` for the database schema and instructions to run respectively.
* Code for Phase 1 is present in `real_time.py` and `historical.py`.
* Please find the data for the stocks considered in the `data` folder. It contains both historical and real-time data which are given by the postfix `_hist` and `_real` respectively.

## Contributions
Equal Contributions
