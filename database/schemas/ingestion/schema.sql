-- Your existing table creation code
CREATE TABLE IF NOT EXISTS stock_data_raw (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10),
    price DECIMAL,
    size INT,
    timestamp TIMESTAMPTZ
);
