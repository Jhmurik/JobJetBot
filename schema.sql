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
    regions TEXT[],
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
    regions TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 👨‍💼 Таблица: Менеджеры
CREATE TABLE IF NOT EXISTS managers (
    id UUID PRIMARY KEY,
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL,
    full_name TEXT,
    position TEXT,
    phone TEXT,
    email TEXT,
    company_name TEXT,
    company_country TEXT,
    company_city TEXT,
    is_owner BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT FALSE,
    regions TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 💳 Таблица: Платежи
CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    role TEXT NOT NULL, -- driver | manager
    amount NUMERIC(10, 2) NOT NULL,
    currency TEXT NOT NULL, -- USDT
    payment_method TEXT NOT NULL, -- cryptomus, ton, paypal, etc.
    payment_type TEXT NOT NULL, -- premium, resume_unlock, etc.
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 🕹️ Таблица: Лимиты активации анкет водителей (10/мес)
CREATE TABLE IF NOT EXISTS driver_activations (
    user_id BIGINT,
    month TEXT,
    count INTEGER DEFAULT 0,
    PRIMARY KEY (user_id, month)
);

-- 📢 Таблица: Реклама
CREATE TABLE IF NOT EXISTS ads (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    image_url TEXT,
    button_text TEXT,
    button_url TEXT,
    target_roles TEXT[], -- driver, manager, all
    target_regions TEXT[],
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 👥 Таблица: Реферальная программа
CREATE TABLE IF NOT EXISTS referrals (
    id SERIAL PRIMARY KEY,
    referrer_id BIGINT NOT NULL,
    referred_id BIGINT NOT NULL,
    role TEXT NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    premium BOOLEAN DEFAULT FALSE
);

-- 📣 Подключённые группы и каналы (для новостей и рекламы)
CREATE TABLE IF NOT EXISTS bot_groups (
    id BIGINT PRIMARY KEY,
    title TEXT,
    type TEXT CHECK (type IN ('channel', 'group')),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
