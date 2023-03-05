from sqlite3 import IntegrityError
from sqlalchemy import Column, Integer, String
from __init__ import db
import random


class FitnessEntry(db.Model):
    __tablename__ = "fitness"
    id = db.Column(db.Integer, primary_key=True)
    _username = Column(db.String(255), nullable=False)
    _diet_name = Column(db.String(255), nullable=False)
    _calories = Column(db.Integer, nullable=False)
    _protein = Column(db.Integer, nullable=False)
    _fat = Column(db.Integer, nullable=False)
    _carbs = Column(db.Integer, nullable=False)
    _extra_notes = Column(db.String(255), nullable=False)


    def __init__(self, username, diet_name, calories, protein, fat, carbs, extra_notes):
        self._username = username
        self._diet_name = diet_name
        self._calories = calories
        self._protein = protein
        self._fat = fat
        self._carbs = carbs
        self._extra_notes = extra_notes

    def __repr__(self):
        return (
            "<FitnessEntry(username='%s', calories='%s', protein='%s', fat='%s', carbs='%s', extra_notes='%s')>"
            % (
                self.username,
                self.calories,
                self.protein,
                self.fat,
                self.carbs,
                self.extra_notes,
            )
        )

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def diet_name(self):
        return self._diet_name

    @diet_name.setter
    def diet_name(self, value):
        self._diet_name = value

    @property
    def calories(self):
        return self._calories

    @calories.setter
    def calories(self, value):
        self._calories = value

    @property
    def protein(self):
        return self._protein

    @protein.setter
    def protein(self, value):
        self._protein = value

    @property
    def fat(self):
        return self._fat

    @fat.setter
    def fat(self, value):
        self._fat = value

    @property
    def carbs(self):
        return self._carbs

    @carbs.setter
    def carbs(self, value):
        self._carbs = value

    @property
    def extra_notes(self):
        return self._extra_notes

    @extra_notes.setter
    def extra_notes(self, value):
        self._extra_notes = value

    def create(self):
        try:
            # creates a player object from Player(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id" : self.id,
            "username": self.username,
            "calories": self.calories,
            "protein": self.protein,
            "fat": self.fat,
            "carbs": self.carbs,
            "extra_notes": self.extra_notes,
            "diet_name": self.diet_name,
        }

    # CRUD update: updates name, uid, password, tokens
    # returns self
    def update(self, dictionary): 
        # {k:v, v:w, x:r}
        """only updates values in dictionary with length"""
        for key in dictionary:
            if key == "name":
                self._diet_name = dictionary[key]
                print("changed " + key)
            if key == "calories":
                self._calories = dictionary[key]
                print("changed " + key)
            if key == "protein":
                self._protein
                print("changed " + key)
            if key == "fat":
                self._fat = dictionary[key]
                print("changed " + key)
            if key == "carbs":
                self._carbs = dictionary[key]
                print("changed " + key)
            if key == "notes":
                self._extra_notes = dictionary[key]
                print("changed " + key)
        db.session.commit()
        return self

    # CRUD delete: remove self
    # return self
    def delete(self):
        player = self
        db.session.delete(self)
        db.session.commit()
        return player




def fitness_table_empty():
    return len(db.session.query(FitnessEntry).all()) == 0


def initDiets():
    if not fitness_table_empty():
        return

    entry1 = FitnessEntry("Martin", "Cutting", 2000, 150, 70, 150, "had a big lunch")
    entry2 = FitnessEntry(
        "Ethan", "Bulking", 1700, 120, 50, 100, "ate a lot of veggies"
    )
    entry3 = FitnessEntry("Derek", "Training", 1500, 200, 80, 200, "had a heavy dinner")

    fitness_entries = [entry1, entry2, entry3]

    for entry in fitness_entries:
        try:
            entry.create()
        except Exception as e:
            print("error while creating entries: " + str(e))
            db.session.rollback()
