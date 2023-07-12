DROP TABLE IF EXISTS SourceMaster;

CREATE TABLE SourceMaster (
  CustomerId Char(20) NOT NULL,
  SourceId CHAR(20) NOT NULL,
  SourceDesc VARCHAR(256) NOT NULL,
  PRIMARY KEY (CustomerId, SourceId)
);

