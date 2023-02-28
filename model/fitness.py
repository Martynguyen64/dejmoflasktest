from sqlalchemy import Column, Integer, String
from __init__ import db
import random


class FitnessEntry(db.Model):
    __tablename__ = "diets"

    id = Column(Integer, primary_key=True)
    _username = Column(String(255), nullable=False)
    _diet_name = Column(String(255), nullable=False)
    _calories = Column(Integer, nullable=False)
    _protein = Column(Integer, nullable=False)
    _fat = Column(Integer, nullable=False)
    _carbs = Column(Integer, nullable=False)
    _extra_notes = Column(String(255), nullable=False)

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
            "<FitnessEntry(id='%s', username='%s', calories='%s', protein='%s', fat='%s', carbs='%s', extra_notes='%s')>"
            % (
                self.id,
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

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "calories": self.calories,
            "protein": self.protein,
            "fat": self.fat,
            "carbs": self.carbs,
            "extra_notes": self.extra_notes,
            "diet_name": self.diet_name,
        }


def fitness_table_empty():
    return len(db.session.query(FitnessEntry).all()) == 0


def init_diets():
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
            db.session.add(entry)
            db.session.commit()
        except Exception as e:
            print("error while creating entries: " + str(e))
            db.session.rollback()
