from yahoo_finance import Share
from pprint import pprint

stock_symbols = ['GOOGL', 'YHOO', 'MSFT', 'AMZN', 'TWTR', \
        'FB', 'CSCO', 'BAC', 'AAPL', 'AMD']

def main():
    for symbol in stock_symbols:
        print 'getting data for', symbol
        stock = Share(symbol)
        data = stock.get_historical('2014-01-01', '2016-01-01')
        
        path = 'data/hist_' + symbol + '.csv'
        with open(path, 'w') as f:
            for day_data in data:
                line = []
                line.append(day_data['Date'])
                line.append(day_data['Open'])
                line.append(day_data['High'])
                line.append(day_data['Low'])
                line.append(day_data['Close'])
                line.append(day_data['Volume'])

                f.write(', '.join(line) + '\n')

        print 'data written to', path

if __name__ == '__main__':
    main()
