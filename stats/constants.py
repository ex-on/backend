MALE_STANDARD_BMI = 22
FEMALE_STANDARD_BMI = 21

MALE_STANDARD_BODY_FAT_PERCENTAGE = 15
FEMALE_STANDARD_BODY_FAT_PERCENTAGE = 23

def getStandardBmi(gender):
  if gender == 0:
    return MALE_STANDARD_BMI
  else:
    return FEMALE_STANDARD_BMI

def getStandardBodyFatPercentage(gender):
  if gender == 0:
    return MALE_STANDARD_BODY_FAT_PERCENTAGE
  else:
    return FEMALE_STANDARD_BODY_FAT_PERCENTAGE