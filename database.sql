-- ─────────────────────────────────────────────────────────────────────────────
--  Activity Logs — Database Schema
-- ─────────────────────────────────────────────────────────────────────────────

CREATE DATABASE IF NOT EXISTS activity_logs
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE activity_logs;

CREATE TABLE IF NOT EXISTS user_logs (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  username   VARCHAR(100)                        NOT NULL,
  action     VARCHAR(100)                        NOT NULL,
  source_ip  VARCHAR(50)                         NOT NULL DEFAULT '0.0.0.0',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,

  INDEX idx_action     (action),
  INDEX idx_username   (username),
  INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── Seed data (optional) ────────────────────────────────────────────────────
INSERT INTO user_logs (username, action, source_ip) VALUES
  ('alice_smith',  'login',          '192.168.1.10'),
  ('bob_jones',    'failed_login',   '10.0.0.5'),
  ('carol_white',  'profile_update', '172.16.0.12'),
  ('alice_smith',  'create_order',   '192.168.1.10'),
  ('demo_user',    'login',          '203.0.113.42'),
  ('henry_davis',  'logout',         '198.51.100.7'),
  ('emma_brown',   'login',          '192.168.1.25'),
  ('demo_user',    'create_order',   '203.0.113.42');
