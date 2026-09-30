CREATE TABLE dwh.users_business_data_s (
    user_id varchar NOT NULL,
    effective_from DATE NOT NULL,
    effective_to DATE NOT NULL,
    actual_flag BOOLEAN not null,
    load_date TIMESTAMP(0) NOT NULL,
    available_balance NUMERIC not null,
    admin_flag BOOLEAN not null,
    job_insert int not null,
    job_update int not null
);
COMMENT ON TABLE dwh.users_business_data_s IS 'История изменений бизнес-данных пользователей. Unique: (user_id, effective_from)';
COMMENT ON COLUMN dwh.users_business_data_s.user_id IS 'Уникальный идентификатор пользователя';
COMMENT ON COLUMN dwh.users_business_data_s.effective_from IS 'Дата начала действия записи';
COMMENT ON COLUMN dwh.users_business_data_s.effective_to IS 'Дата окончания действия записи';
COMMENT ON COLUMN dwh.users_business_data_s.actual_flag IS 'Признак актуальности записи (true - текущая версия)';
COMMENT ON COLUMN dwh.users_business_data_s.load_date IS 'Дата и время загрузки данных в систему';
COMMENT ON COLUMN dwh.users_business_data_s.available_balance IS 'Доступный баланс пользователя на момент записи';
COMMENT ON COLUMN dwh.users_business_data_s.admin_flag IS 'Флаг наличия прав администратора';
COMMENT ON COLUMN dwh.users_business_data_s.admin_flag IS 'Флаг наличия прав администратора';
COMMENT ON COLUMN dwh.users_business_data_s.job_insert IS 'ID процесса, создавшего запись';
COMMENT ON COLUMN dwh.users_business_data_s.job_update IS 'ID процесса, закрывшего версию записи';



CREATE TABLE dwh.users_telegram_data_s (
    user_id varchar NOT NULL,
    effective_from DATE NOT NULL,
    effective_to date not null,
    actual_flag BOOLEAN not null,
    load_date TIMESTAMP(0) NOT NULL,
    username varchar not null,
    first_name varchar null,
    last_name varchar null,
    premium_status BOOLEAN not null,
    job_insert int not null,
    job_update int not null
);
COMMENT ON TABLE dwh.users_telegram_data_s IS 'История изменений профилей пользователей Telegram. Unique: (user_id, effective_from)';
COMMENT ON COLUMN dwh.users_telegram_data_s.user_id IS 'Уникальный идентификатор пользователя';
COMMENT ON COLUMN dwh.users_telegram_data_s.effective_from IS 'Дата начала действия версии записи';
COMMENT ON COLUMN dwh.users_telegram_data_s.effective_to IS 'Дата окончания действия версии записи';
COMMENT ON COLUMN dwh.users_telegram_data_s.actual_flag IS 'Признак актуальности записи (true - текущая версия)';
COMMENT ON COLUMN dwh.users_telegram_data_s.load_date IS 'Дата и время загрузки данных в систему';
COMMENT ON COLUMN dwh.users_telegram_data_s.username IS 'Никнейм пользователя в Telegram (@username)';
COMMENT ON COLUMN dwh.users_telegram_data_s.first_name IS 'Имя пользователя';
COMMENT ON COLUMN dwh.users_telegram_data_s.last_name IS 'Фамилия пользователя';
COMMENT ON COLUMN dwh.users_telegram_data_s.premium_status IS 'Наличие подписки Telegram Premium';
COMMENT ON COLUMN dwh.users_telegram_data_s.job_insert IS 'ID процесса, создавшей запись';
COMMENT ON COLUMN dwh.users_telegram_data_s.job_update IS 'ID процесса, обновившей (закрывшей) версию';



CREATE TABLE dwh.users_h (
    user_id varchar NOT NULL,
    telegram_id varchar NOT NULL,
    load_date TIMESTAMP(0) NOT NULL,
    job_insert INT NOT NULL
);
COMMENT ON TABLE dwh.users_h IS 'Хаб пользователей. Unique: user_id.';
COMMENT ON COLUMN dwh.users_h.user_id IS 'Уникальный идентификатор пользователя';
COMMENT ON COLUMN dwh.users_h.telegram_id IS 'Уникальный идентификатор пользователя в Telegram';
COMMENT ON COLUMN dwh.users_h.load_date IS 'Дата и время загрузки данных в систему';
COMMENT ON COLUMN dwh.users_h.job_insert IS 'ID процесса, создавшей запись';