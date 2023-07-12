DROP TABLE IF EXISTS TagMaster;

CREATE TABLE TagMaster (
  CustomerId Char(20) NOT NULL,
  TagId CHAR(20) NOT NULL,
  TagDesc CHAR(40) NOT NULL,
  PRIMARY KEY (CustomerId, TagId)
);

