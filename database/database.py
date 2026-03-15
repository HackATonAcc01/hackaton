import json

from pony.orm import *
from typing import cast
db = Database("sqlite", "database.sqlite", create_db=True)


class Scenario(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    age = Required(str)
    goal = Required(str)
    start = Required(str)
    main = Required(str)
    reflection = Required(str)
    result = Required(str)
    criteria = Optional('Criteria', reverse='scenario')



class Criteria(db.Entity):
    id = PrimaryKey(int, auto=True)
    theme = Required(str)
    age = Required(str)
    duration = Required(str)
    instruments = Required(str)
    criteriaArray = [theme, age, duration, instruments]
    scenario = Required(Scenario, reverse='criteria')


db.generate_mapping(create_tables=True)

class Control():

    def createScenario(self, name, age, goal, start, main, reflection, result):
        scenario = Scenario(name=name, age=age, goal=goal, start=start, main=main, reflection=reflection, result=result)
        return scenario


    def createCriteria(self, theme, age, duration, instruments, scenario):
        criteria = Criteria(theme=theme, age=age, duration=duration, instruments=instruments, scenario=scenario)

        return criteria


    def getCriteria(self, theme, age, duration, instruments):
        criteria = Criteria.select().filter(theme=theme, age=age, duration=duration, instruments=instruments)[:]
        return criteria


    def getScenario(self, criteria):
        return criteria.scenario


    def processCriteria(self, criteria):
        scenarios = []
        for c in criteria:
            scenarios.append(self.getScenario(c))

        return scenarios


    def searchScenario(self, theme, age, duration, instruments):
        return self.processCriteria(self.getCriteria(theme, age, duration, instruments))

    @db_session
    def getScenariosPreviewArray(self, theme, age , duration, instruments):
        previewArray = []
        for s in self.searchScenario(theme, age, duration, instruments):
            previewArray.append([s.id, s.name])
        return previewArray


    def getScenarioById(self, id):
        return list(Scenario.select(lambda s: s.id == id))[0]


    def getAllScenarioValues(self, scenario):
        return [scenario.name, scenario.age, scenario.goal ,scenario.start, scenario.main, scenario.reflection, scenario.result]


    @db_session
    def getById(self, id):
        return self.getAllScenarioValues(self.getScenarioById(id))