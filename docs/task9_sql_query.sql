-- ============================================================
-- ЗАДАНИЕ 9: Аналитический SQL-запрос
-- Задача: Топ-10 клиентов по суммарному объёму переводов
--         за последние 30 дней с разбивкой по валютам
-- ============================================================

-- Промпт в Claude Code:
-- "На основе таблиц accounts и transfers напиши SQL-запрос,
--  который показывает топ-10 клиентов по суммарному объёму
--  исходящих переводов за последние 30 дней.
--  Включи: имя владельца, номер счёта, общую сумму переводов,
--  количество переводов, среднюю сумму одного перевода.
--  Объясни логику запроса."

-- ============================================================
-- ЗАПРОС
-- ============================================================

SELECT
    a.owner_name                          AS владелец,
    a.account_number                      AS номер_счёта,
    a.currency                            AS валюта,
    COUNT(t.id)                           AS кол_переводов,
    ROUND(SUM(t.amount), 2)               AS сумма_переводов,
    ROUND(AVG(t.amount), 2)               AS средний_перевод,
    ROUND(SUM(t.fee), 2)                  AS сумма_комиссий
FROM accounts a
JOIN transfers t ON t.from_account_id = a.id
WHERE
    t.status   = 'completed'
    AND t.created_at >= datetime('now', '-30 days')
GROUP BY
    a.id, a.owner_name, a.account_number, a.currency
ORDER BY
    сумма_переводов DESC
LIMIT 10;

-- ============================================================
-- ОБЪЯСНЕНИЕ ЛОГИКИ
-- ============================================================
--
-- 1. FROM accounts a JOIN transfers t ON t.from_account_id = a.id
--    Соединяем таблицу счетов с таблицей переводов по полю
--    from_account_id — берём только ИСХОДЯЩИЕ переводы.
--
-- 2. WHERE t.status = 'completed'
--    Учитываем только успешно завершённые переводы.
--    Статус 'pending' или 'failed' не включаем.
--
-- 3. AND t.created_at >= datetime('now', '-30 days')
--    Фильтр по последним 30 дням. В PostgreSQL было бы:
--    t.created_at >= NOW() - INTERVAL '30 days'
--
-- 4. GROUP BY a.id, ...
--    Группируем по каждому счёту. Используем a.id как первичный
--    ключ группировки — это гарантирует уникальность, даже если
--    два клиента имеют одинаковое имя.
--
-- 5. COUNT(t.id) — число переводов
--    SUM(t.amount) — суммарный объём
--    AVG(t.amount) — средний чек одного перевода
--    SUM(t.fee) — сколько заработал банк с этого клиента
--
-- 6. ORDER BY сумма_переводов DESC LIMIT 10
--    Сортируем по убыванию суммы и берём первые 10 строк.
--
-- ============================================================
-- ВАРИАНТ ДЛЯ PostgreSQL
-- ============================================================

/*
SELECT
    a.owner_name,
    a.account_number,
    a.currency,
    COUNT(t.id)             AS transfer_count,
    ROUND(SUM(t.amount)::numeric, 2) AS total_amount,
    ROUND(AVG(t.amount)::numeric, 2) AS avg_amount,
    ROUND(SUM(t.fee)::numeric, 2)    AS total_fee
FROM accounts a
JOIN transfers t ON t.from_account_id = a.id
WHERE
    t.status     = 'completed'
    AND t.created_at >= NOW() - INTERVAL '30 days'
GROUP BY a.id, a.owner_name, a.account_number, a.currency
ORDER BY total_amount DESC
LIMIT 10;
*/
