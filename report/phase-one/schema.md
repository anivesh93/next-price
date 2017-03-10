# Database Schema
## Schema

### Stock
```
CREATE TABLE stock (
    symbol TEXT PRIMARY KEY,
    name TEXT
);
```

### Historical
```
CREATE TABLE historical (
    symbol TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    date TEXT,
    volume INTEGER,
    FOREIGN KEY (symbol) REFERENCES stock (symbol)
);
```

### RealTime
```
CREATE TABLE realtime (
    symbol TEXT,
    price REAL,
    date TEXT,
    time TEXT,
    volume INTEGER,
    FOREIGN KEY (symbol) REFERENCES stock (symbol)
);
```
\pagebreak

## Diagram
![Database Schema Diagram](schema.png)


