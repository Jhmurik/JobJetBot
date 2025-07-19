-- 🚚 Таблица: Водители
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
    ready_to_depart TEXT,
    contacts TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    regions TEXT[],  -- 📍 Регион(ы) работы
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 🏢 Таблица: Компании
CREATE TABLE IF NOT EXISTS companies (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    country TEXT,
    city TEXT,
    owner_id BIGINT NOT NULL,
    regions TEXT[],  -- 📍 Регион(ы) деятельности
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 👨‍💼 Таблица: Менеджеры
CREATE TABLE IF NOT EXISTS managers (
    id UUID PRIMARY KEY,
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE, -- ❗️опционально
    user_id BIGINT NOT NULL,
    full_name TEXT,
    position TEXT,
    phone TEXT,
    email TEXT,
    company_name TEXT,       -- 📎 если менеджер без привязки
    company_country TEXT,    -- 🌍 страна фирмы
    company_city TEXT,       -- 🏙️ город фирмы
    is_owner BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT FALSE,
    regions TEXT[],  -- 📍 Регион(ы) работы
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 💳 Таблица: Платежи
CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    role TEXT NOT NULL, -- driver | manager
    amount NUMERIC(10, 2) NOT NULL,
    currency TEXT NOT NULL, -- EUR, TON, etc.
    payment_method TEXT NOT NULL, -- cryptomus, ton, paypal, etc.
    payment_type TEXT NOT NULL, -- premium, resume_unlock, etc.
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
