DROP DATABASE IF EXISTS gedcomdb;

CREATE DATABASE gedcomdb;

CONNECT gedcomdb;

DROP TABLE IF EXISTS TagMaster;

CREATE TABLE TagMaster (
  CustomerId Char(20) NOT NULL,
  TagId CHAR(20) NOT NULL,
  TagDesc CHAR(40) NOT NULL,
  PRIMARY KEY (CustomerId, TagId)
);

DROP TABLE IF EXISTS ObjectMaster;

CREATE TABLE ObjectMaster (
  CustomerId CHAR(20) NOT NULL,
  ObjectId CHAR(20) NOT NULL,
  ObjectType CHAR(20) NOT NULL,
  ObjectValue VARCHAR(256) NOT NULL,
  PRIMARY KEY (CustomerId, ObjectId)
);

DROP TABLE IF EXISTS FamilyMaster;

CREATE TABLE FamilyMaster (
  CustomerId CHAR(20),
  FamilyId CHAR(20),
  MarrDate CHAR(20),
  DivDate CHAR(20),
  PRIMARY KEY (CustomerId, FamilyId)
);

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

DROP TABLE IF EXISTS FamIndDtl;

CREATE TABLE FamIndDtl (
  CustomerId CHAR(20) NOT NULL,
  FamilyId CHAR(20) NOT NULL,
  IndividualId CHAR(20) NOT NULL,
  Position CHAR(20) NOT NULL,
  FAdopted CHAR (01),
  MAdopted CHAR (01),
  FStep CHAR (01),
  MStep CHAR (01),
  PRIMARY KEY (CustomerId, FamilyId, IndividualId),
  FOREIGN KEY (CustomerId, IndividualId) REFERENCES IndividualMaster(CustomerId, IndividualId)
);

