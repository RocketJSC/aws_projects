DROP TABLE IF EXISTS IndividualMaster;

CREATE TABLE IndividualMaster (
  CustomerId CHAR(20) NOT NULL,
  IndividualId CHAR(20) NOT NULL,
  IndividualName CHAR(40) NOT NULL,
  IndividualSurname CHAR(20) NOT NULL,
  IndividualGivenname CHAR(20) NOT NULL,
  IndividualSuffix CHAR(10),
  Gender CHAR(1) NOT NULL,
  BirthDate CHAR(20),
  DeathDate CHAR(20),
  ObitUrl VARCHAR(256),
  FindAGraveURL VARCHAR(256),
  CensusFlags CHAR(50),
  TagIds VARCHAR(200),
  PRIMARY KEY (CustomerId, IndividualId)
);

