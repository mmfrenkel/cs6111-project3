
SET SQL_SAFE_UPDATES = 0;

UPDATE restaurant_inspection_data2
	SET SCORE = CONCAT("Score: ", SCORE - MOD(SCORE, 10), "-", SCORE - MOD(SCORE, 10) + 10);

UPDATE restaurant_inspection_data2
SET CRITICAL_FLAG = 
	CASE
        WHEN CRITICAL_FLAG = 'Y' THEN "CRITICAL"
        ELSE "NOT_CRITICAL"
	END;

UPDATE restaurant_inspection_data2
SET INSPECTION_TYPE = CONCAT("Inspection_Type: ", INSPECTION_TYPE);

UPDATE restaurant_inspection_data2
SET ACTION_ITEM = 
	CASE
        WHEN ACTION_ITEM = 'Violations were cited in the following area(s).' THEN "Action: Violations were cited."
        WHEN ACTION_ITEM = 'No violations were recorded at the time of this inspection.' THEN "Action: No violations recorded."
        WHEN ACTION_ITEM = 'Establishment Closed by DOHMH.  Violations were cited in the following area(s) and those requiring immediate action were addressed.' THEN 'Action: Establishment Closed by DOHMH.'
		ELSE CONCAT("Action: ", ACTION_ITEM)
    END;

UPDATE restaurant_inspection_data2
SET VIOLATION_DESCRIPTION = 
	CASE WHEN VIOLATION_DESCRIPTION = "" THEN CONCAT("Violation ", VIOLATION_CODE, ": Unknown Description")
    ELSE CONCAT("Violation ", VIOLATION_CODE, ": ", VIOLATION_DESCRIPTION)
    END;

UPDATE restaurant_inspection_data2
SET INSPECTION_DATE = 
	CASE 
		WHEN INSPECTION_DATE LIKE "%/18" THEN "Inspection Year: 2018"
		WHEN INSPECTION_DATE LIKE "%/19" THEN "Inspection Year: 2019"
		WHEN INSPECTION_DATE LIKE "%/20" THEN "Inspection Year: 2020"
		WHEN INSPECTION_DATE LIKE "%/21" THEN "Inspection Year: 2021"
	ELSE "-"
    END;

ALTER TABLE restaurant_inspection_data2
DROP COLUMN CAMIS;

ALTER TABLE restaurant_inspection_data2
DROP COLUMN VIOLATION_CODE;

ALTER TABLE restaurant_inspection_data2
DROP COLUMN SCORE;

DELETE FROM restaurant_inspection_data2 WHERE DBA IS NULL OR DBA = "";

UPDATE restaurant_inspection_data2
SET GRADE = "-"
WHERE GRADE IS NULL OR GRADE = "";
