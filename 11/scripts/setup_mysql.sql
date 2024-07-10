CREATE TABLE treasure_locations (
  location NVARCHAR(100) NOT NULL,
  feather_code NVARCHAR(100) NOT NULL
);

INSERT INTO treasure_locations VALUES 
  ("what3words 1", "sparrow_123"),
  ("what3words 2", "owl_123");
