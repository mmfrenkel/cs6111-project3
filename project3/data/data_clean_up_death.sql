SELECT *
FROM nyc_leading_cause_of_death_adj;

ALTER TABLE `cs6111`.`nyc_leading_cause_of_death_adj` 
CHANGE COLUMN `Leading Cause` `Cause` TEXT NULL DEFAULT NULL ,
CHANGE COLUMN `Race Ethnicity` `Race-Ethnicity` TEXT NULL DEFAULT NULL ;

ALTER TABLE nyc_leading_cause_of_death_adj
ADD COLUMN Cleaned_Cause TEXT;

UPDATE nyc_leading_cause_of_death_adj
SET CLEANED_CAUSE = SUBSTRING_INDEX(CAUSE,'(',1);

UPDATE nyc_leading_cause_of_death_adj
SET SEX = "Male" WHERE SEX = "M";

UPDATE nyc_leading_cause_of_death_adj
SET SEX = "Female" WHERE SEX = "F";