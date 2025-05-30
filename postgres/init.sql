-- DIMENSION TABLES

-- Currency Dimension
CREATE TABLE IF NOT EXISTS dim_currency (
    currency_code VARCHAR(3) PRIMARY KEY,
    currency_name VARCHAR(50) -- bisa ditambah dari mapping jika diperlukan
);

-- Time Dimension
CREATE TABLE IF NOT EXISTS dim_time (
    time_id SERIAL PRIMARY KEY,
    fetch_date DATE,
    fetch_time TIME,
    UNIQUE(fetch_date, fetch_time)
);

-- FACT TABLE

CREATE TABLE IF NOT EXISTS fact_exchange_rate (
    id SERIAL PRIMARY KEY,
    base_currency VARCHAR(3) REFERENCES dim_currency(currency_code),
    target_currency VARCHAR(3) REFERENCES dim_currency(currency_code),
    rate FLOAT,
    time_id INT REFERENCES dim_time(time_id),
    fetch_timestamp TIMESTAMP
);

-- Tabel Prediksi Nilai Tukar IDR
CREATE TABLE IF NOT EXISTS forecast_exchange_rate (
    base_currency TEXT NOT NULL,
    target_currency TEXT NOT NULL,
    forecast_date DATE NOT NULL,
    forecast_rate FLOAT NOT NULL,
    PRIMARY KEY (base_currency, target_currency, forecast_date)
);

-- INDEXING
CREATE INDEX IF NOT EXISTS idx_fact_exchange_rate_time
ON fact_exchange_rate(time_id);

CREATE INDEX IF NOT EXISTS idx_fact_exchange_rate_target
ON fact_exchange_rate(target_currency);

-- Optional Index untuk analitik lebih cepat
CREATE INDEX IF NOT EXISTS idx_fact_exchange_rate_base
ON fact_exchange_rate(base_currency);
