DROP TABLE IF EXISTS FamIndDtl;

CREATE TABLE FamIndDtl (
  CustomerId CHAR(20) NOT NULL,
  FamilyId CHAR(20) NOT NULL,
  IndividualId CHAR(20) NOT NULL,
  Position CHAR(20) NOT NULL,
  PRIMARY KEY (CustomerId, FamilyId, IndividualId),
  FOREIGN KEY (CustomerId, IndividualId) REFERENCES IndividualMaster(CustomerId, IndividualId)
);

