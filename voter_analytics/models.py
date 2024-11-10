# voter_analytics/models.py

from django.db import models
from django.urls import reverse
from datetime import datetime
import csv


# Create your models here.
class Voter(models.Model):
    """
        Encapsulate the idea of a registered voter

        *    Last Name
        *    First Name
        *    Residential Address - Street Number
        *    Residential Address - Street Name
        *    Residential Address - Apartment Number
        *    Residential Address - Zip Code
        *    Date of Birth
        *    Date of Registration
        *    Party Affiliation
        *    Precinct Number

        These fields indicate whether or not a given voter participated in several recent elections:
        *    v20state
        *    v21town
        *    v21primary
        *    v22general
        *    v23town

        The voter_score is a numeric value, indicating how many of the past 5 elections the voter participated in.
    """
    
    # attributes of a registered voter
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    street_number = models.TextField(blank=False)
    street_name = models.TextField(blank=False)
    apartment_number = models.TextField(blank=True, null=True)
    zip_code = models.TextField(blank=False)
    dob = models.DateField(blank=False)
    dor = models.DateField(blank=False)
    party_affiliation = models.TextField(blank=False)
    precinct_number = models.TextField(blank=False)

    # fields to indicate whether or not a given voter participated in several recent elections
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    # voter_score is a numeric value, indicating how many of the past 5 elections the voter participated in
    voter_score = models.IntegerField(default=0)


    def __str__(self):
        """
            Return a string representation of the Voter object
        """
        return f"Personal Information: first_name = {self.first_name}, last_name = {self.last_name}, dob = ({self.dob}), \n\
                 Political Information: party = {self.party_affiliation}, precinct_number = {self.precinct_number}, voter_score = {self.voter_score}\n\
                 Address: {self.street_number}, {self.street_name}, {self.apartment_number}, {self.zip_code}\n\
                 Election Participation: v20state = {self.v20state}, v21town = {self.v21town}, v21primary = {self.v21primary}, v22general = {self.v22general}, v23town = {self.v23town}"


def load_data():
    """
        Function to load data records from CSV file into Django model instances
    """

    def parse_bool(value):
        """
            helper to parse a string value to a boolean
        """
        return value.strip().lower() in ['true', '1', 'yes']

    Voter.objects.all().delete() # clear the database

    filename = "/Users/jackywtk/BU-CS412/voter_analytics/newton_voters.csv"
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row

        for fields in reader:
            try:
                # Create Voter instance from CSV row
                voter = Voter(
                    first_name=fields[2].strip(),
                    last_name=fields[1].strip(),
                    street_number=fields[3].strip(),
                    street_name=fields[4].strip(),
                    apartment_number=fields[5].strip() if fields[5].strip() else None,
                    zip_code=fields[6].strip(),
                    dob=datetime.strptime(fields[7].strip(), "%Y-%m-%d").date(),
                    dor=datetime.strptime(fields[8].strip(), "%Y-%m-%d").date(),
                    party_affiliation=fields[9].strip(),
                    precinct_number=fields[10].strip(),
                    v20state=parse_bool(fields[11]),
                    v21town=parse_bool(fields[12]),
                    v21primary=parse_bool(fields[13]),
                    v22general=parse_bool(fields[14]),
                    v23town=parse_bool(fields[15]),
                    voter_score=int(fields[16].strip())
                )
                voter.save()
                print(f"Created voter: {voter}")

            except Exception as e:
                print(f"Skipped: {fields} due to error: {e}")
        
        print(f"Done. Created {Voter.objects.count()} records.")