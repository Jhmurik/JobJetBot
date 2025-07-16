CREATE TABLE IF NOT EXISTS drivers (
    id BIGINT PRIMARY KEY,
    full_name TEXT NOT NULL,
    birth_date TEXT,
    citizenship TEXT,
    residence TEXT,
    license_type TEXT,
    experience TEXT,
    languages TEXT[],
    documents TEXT,
    truck_type TEXT,
    employment_type TEXT,
    ready_to_depart TEXT,  -- исправлено название и тип
    contacts TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
