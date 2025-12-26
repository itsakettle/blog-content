-- LLM
CREATE DATABASE tea_db;

USE tea_db;

CREATE TABLE made_cups_of_tea (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  tea_type VARCHAR(50) NOT NULL,
  person_id BIGINT UNSIGNED NOT NULL,
  made_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (tea_type, person_id, made_at)
);

CREATE TABLE drank_cups_of_tea (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  tea_type VARCHAR(50) NOT NULL,
  person_id BIGINT UNSIGNED NOT NULL,
  drank_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_drank_tea_person (tea_type, person_id)
);


