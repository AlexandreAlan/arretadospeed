-- Execute como superusuário postgres:
--   sudo -u postgres psql -f /var/www/arretadospeed/sql/init.sql

-- Cria usuário (ignora se já existir)
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'arretado') THEN
    CREATE ROLE arretado WITH LOGIN PASSWORD 'arretado123';
  END IF;
END
$$;

-- Cria banco (ignora se já existir)
SELECT 'CREATE DATABASE arretadospeed OWNER arretado ENCODING ''UTF8'''
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'arretadospeed')\gexec

-- Conecta ao banco e cria a tabela
\c arretadospeed

-- Garante permissões
GRANT ALL PRIVILEGES ON DATABASE arretadospeed TO arretado;
GRANT ALL ON SCHEMA public TO arretado;

-- Tabela principal de resultados
CREATE TABLE IF NOT EXISTS speed_tests (
    test_id       VARCHAR(36)  PRIMARY KEY,
    ip_address    VARCHAR(45)  NOT NULL,
    isp           VARCHAR(255),
    city          VARCHAR(100),
    country       VARCHAR(100),
    latency_min   FLOAT,
    latency_avg   FLOAT,
    latency_max   FLOAT,
    jitter        FLOAT,
    download_mbps FLOAT,
    upload_mbps   FLOAT,
    user_agent    TEXT,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- Índices para consultas mais rápidas
CREATE INDEX IF NOT EXISTS idx_speed_tests_created_at  ON speed_tests (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_speed_tests_ip_address  ON speed_tests (ip_address);

-- Confirma
SELECT 'Banco arretadospeed e tabela speed_tests criados com sucesso.' AS status;
