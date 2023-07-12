DROP TABLE IF EXISTS FamilyMaster;

CREATE TABLE FamilyMaster (
  CustomerId CHAR(20),
  FamilyId CHAR(20),
  MarrDate CHAR(20),
  DivDate CHAR(20),
  PRIMARY KEY (CustomerId, FamilyId)
);

