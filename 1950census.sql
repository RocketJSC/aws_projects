SELECT CustomerId, IndividualId, IndividualName, IndividualSurname, IndividualGivenname, IndividualSuffix,
       Gender,
       CASE WHEN SUBSTRING(BirthDate, 2, 1) <> '_' AND SUBSTRING(BirthDate, 1, 4) > '1950' THEN STR_TO_DATE(BirthDate, '%Y-%m-%d') ELSE BirthDate END AS BirthDate,
       CASE WHEN SUBSTRING(DeathDate, 2, 1) <> '_' AND (DeathDate IS NULL OR SUBSTRING(DeathDate, 1, 4) > '1959') THEN STR_TO_DATE(DeathDate, '%Y-%m-%d') ELSE DeathDate END AS DeathDate,
       ObitUrl, FindAGraveURL, CensusFlags, TagIds
FROM IndividualMaster
WHERE (SUBSTRING(BirthDate, 2, 1) <> '_' AND SUBSTRING(BirthDate, 1, 4) < '1950' AND (DeathDate IS NULL OR SUBSTRING(DeathDate, 1, 4) > '1959'))
      AND (CensusFlags NOT LIKE '%1950%') limit 20;
