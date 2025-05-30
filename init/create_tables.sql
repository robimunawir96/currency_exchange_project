-- Drop tables if they exist
DROP TABLE IF EXISTS fact_exchange;
DROP TABLE IF EXISTS dim_base_currency;
DROP TABLE IF EXISTS dim_target_currency;
DROP TABLE IF EXISTS dim_date;

-- DIMENSION: Base Currency
CREATE TABLE dim_base_currency (
    base_currency_id SERIAL PRIMARY KEY,
    currency_code VARCHAR(10) UNIQUE NOT NULL,
    description VARCHAR(100)
);

-- DIMENSION: Target Currency
CREATE TABLE dim_target_currency (
    target_currency_id SERIAL PRIMARY KEY,
    currency_code VARCHAR(10) UNIQUE NOT NULL,
    description VARCHAR(100)
);

-- DIMENSION: Date
CREATE TABLE dim_date (
    date_id DATE PRIMARY KEY,
    year INT,
    month INT,
    day INT,
    day_name VARCHAR(10),
    week INT
);

-- FACT TABLE: Exchange Rates
CREATE TABLE fact_exchange (
    exchange_id SERIAL PRIMARY KEY,
    date_id DATE REFERENCES dim_date(date_id),
    base_currency_id INT REFERENCES dim_base_currency(base_currency_id),
    target_currency_id INT REFERENCES dim_target_currency(target_currency_id),
    exchange_rate FLOAT NOT NULL
);

-- INDEXING
CREATE INDEX idx_exchange_date ON fact_exchange(date_id);
CREATE INDEX idx_exchange_base_target ON fact_exchange(base_currency_id, target_currency_id);
