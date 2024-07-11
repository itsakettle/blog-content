CREATE DATABASE treasure_api;

USE treasure_api;

CREATE TABLE treasure_location (
  what3words NVARCHAR(100) NOT NULL,
  feather_code NVARCHAR(100) NOT NULL
);

INSERT INTO treasure_location VALUES 
  ("what3words 1", "sparrow_123"),
  ("what3words 2", "owl_123");
