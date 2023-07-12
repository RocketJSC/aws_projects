DROP TABLE IF EXISTS ObjectMaster;

CREATE TABLE ObjectMaster (
  CustomerId CHAR(20) NOT NULL,
  ObjectId CHAR(20) NOT NULL,
  ObjectType CHAR(20) NOT NULL,
  ObjectValue VARCHAR(256) NOT NULL,
  PRIMARY KEY (CustomerId, ObjectId)
);

