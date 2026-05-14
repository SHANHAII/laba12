-- ============================================================
-- ЗАДАНИЕ 7: SQL-миграции для банковского приложения
-- Инструмент: Alembic (raw SQL эквиваленты)
-- ============================================================

-- ------------------------------------------------------------
-- Миграция 001: Создание таблицы accounts
-- Alembic revision: 001_create_accounts
-- ------------------------------------------------------------

-- upgrade
CREATE TABLE accounts (
    id          INTEGER      NOT NULL PRIMARY KEY AUTOINCREMENT,
    owner_name  VARCHAR(100) NOT NULL,
    account_number VARCHAR(20) NOT NULL UNIQUE,
    balance     FLOAT        NOT NULL DEFAULT 0.0,
    currency    VARCHAR(3)   NOT NULL DEFAULT 'RUB',
    account_type VARCHAR(20) NOT NULL DEFAULT 'checking',
    is_active   BOOLEAN      NOT NULL DEFAULT 1,
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_accounts_id             ON accounts (id);
CREATE INDEX ix_accounts_account_number ON accounts (account_number);

-- downgrade
-- DROP INDEX ix_accounts_account_number;
-- DROP INDEX ix_accounts_id;
-- DROP TABLE accounts;


-- ------------------------------------------------------------
-- Миграция 002: Создание таблицы transfers (переводы)
-- Alembic revision: 002_create_transfers
-- ------------------------------------------------------------

-- upgrade
CREATE TABLE transfers (
    id              INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
    from_account_id INTEGER  NOT NULL REFERENCES accounts(id),
    to_account_id   INTEGER  NOT NULL REFERENCES accounts(id),
    amount          FLOAT    NOT NULL,
    currency        VARCHAR(3) NOT NULL DEFAULT 'RUB',
    fee             FLOAT    NOT NULL DEFAULT 0.0,
    status          VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_transfers_from_account ON transfers (from_account_id);
CREATE INDEX ix_transfers_to_account   ON transfers (to_account_id);
CREATE INDEX ix_transfers_created_at   ON transfers (created_at);

-- downgrade
-- DROP INDEX ix_transfers_created_at;
-- DROP INDEX ix_transfers_to_account;
-- DROP INDEX ix_transfers_from_account;
-- DROP TABLE transfers;


-- ------------------------------------------------------------
-- Миграция 003: Добавление поля phone к accounts
-- Alembic revision: 003_add_phone_to_accounts
-- ------------------------------------------------------------

-- upgrade
ALTER TABLE accounts ADD COLUMN phone VARCHAR(20);

-- downgrade (SQLite не поддерживает DROP COLUMN до версии 3.35)
-- В PostgreSQL: ALTER TABLE accounts DROP COLUMN phone;


-- ------------------------------------------------------------
-- Миграция 004: Создание таблицы cards (карты, many-to-one к accounts)
-- Alembic revision: 004_create_cards
-- ------------------------------------------------------------

-- upgrade
CREATE TABLE cards (
    id          INTEGER      NOT NULL PRIMARY KEY AUTOINCREMENT,
    account_id  INTEGER      NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    card_number VARCHAR(16)  NOT NULL UNIQUE,
    holder_name VARCHAR(100) NOT NULL,
    expires_at  DATE         NOT NULL,
    is_blocked  BOOLEAN      NOT NULL DEFAULT 0,
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_cards_account_id ON cards (account_id);
CREATE INDEX ix_cards_card_number ON cards (card_number);

-- downgrade
-- DROP INDEX ix_cards_card_number;
-- DROP INDEX ix_cards_account_id;
-- DROP TABLE cards;


-- ============================================================
-- Alembic env.py — конфигурация (фрагмент)
-- ============================================================
--
-- from alembic import context
-- from app.database import Base
-- from app.models import Account  # noqa: импорт нужен для автогенерации
--
-- target_metadata = Base.metadata
--
-- def run_migrations_online():
--     connectable = context.config.attributes.get("connection", None)
--     with connectable.connect() as connection:
--         context.configure(connection=connection, target_metadata=target_metadata)
--         with context.begin_transaction():
--             context.run_migrations()
-- ============================================================
