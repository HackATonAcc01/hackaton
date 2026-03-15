import flask
import pony
from flask import Flask, redirect, render_template
from database.database import Control


from forms.searchform import SearchForm
control = Control()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'FJFEfhegfm>FIYSUebhfgsyekfekhfdbsf'
@app.route('/', methods=['GET', 'POST'])
def index():

    form = SearchForm()
    if form.validate_on_submit():
        print("hrllo")
        age = form.age.data
        print(age)
        theme = form.theme.data

        duration = form.duration.data
        instruments = form.instruments.data

        location = f"/search/{theme}/{age}/{duration}/{instruments}"
        return flask.make_response(redirect(location))
    return render_template("index.html", form=form)



@app.route('/search/<theme>/<age>/<duration>/<instruments>', methods=['GET', 'POST'])
def search(theme, age , duration, instruments):
    scenarios = control.getScenariosPreviewArray(theme, age, duration, instruments)
    return render_template("preview.html", scenarios=scenarios)


@app.route('/view/<id>')
def view(id):
    scenario = control.getById(int(id))
    return render_template("view.html", scenario=scenario)


generated = False
def generateScenarios():
    if generated: return
    ageToR = {"primary": "начальная школа", "middle": "средние классы", "high": "старшеклассники"}
    nameDict = {"costumes": "Национальные костюмы татар", "holidays": "День Сибири"}
    goalDict = {"costumes": "Узнать о национальных костюмах татар", "holidays": "Узнать о Дне Сибири"}
    startCostumes = {"primary": """Загадка: У каждого народа он особый:
Узоры, ленты, яркая отделка.
Его из сундука достать попробуй,
Когда в селе начнется посиделка. (Национальный костюм)
""", "middle": "Короткое видео о истории национальных костюмах татар", "high": "Карта Поволжья и краткий рассказ о культуре татар"}
    startHolidays = {"primary": """Загадка: Веселье, танцы, хоровод,
Подарков много, вкусный торт.
В календаре — особый день,
Работать никому не лень,
А хочется лишь отдыхать.
Как этот день нам называть? (Праздник)""", "middle": "Короткое видео о истории Дня Сибири", "high": "Карта Сибири и краткий рассказ о истории Дня Сибири"}
    mainPartCostumes = {"phones": "Ученики ищут информацию о национальных костюмах татар в интернете, используя свои телефоны и отвечая на вопросы", "computer": "Учитель устраивает викторину, ведя учет на компьютере", "whiteboard": "Ученики подробно рассматривают национальные костюмы татар на интерактивной доске", "quiz": "Ученики прохидят онлайн викторину по материалу рассказанному учителем"}

    mainPartHolidays = {"phones": "Ученики ищут информацию о Дне Сибири в интернете, используя свои телефоны и отвечая на вопросы",
                        "computer": "Учитель устраивает викторину, ведя учет на компьютере",
                        "whiteboard": "Ученики подробно рассматривают карту похода Ермака на интерактивной доске",
                        "quiz": "Ученики прохидят онлайн викторину по материалу рассказанному учителем"}

    reflection = {"primary": "Ученики рассмативают облако слов, встретившихся на уроке", "middle": "Ученики проходят мини-опрос для закрепления пройденной темы", "high": "Ученики рассматривают фотоколлаж, связанный с пройденной темой"}
    result = {"costumes": "Вы узнали о национальных костюмах татар", "holidays": "Вы узнали о Дне Сибири"}
    someExtraPart = {"costumes": "Игра на отгадывание частей костюмов", "holidays": "Игра на составление пути похода Ермака"}
    mainExtraPart = {"costumes": "Подробное обсуждение строения костюмов", "holidays": "Обсуждение на тему слодности похода"}
    for theme in ["costumes", "holidays"]:
        for age in ["primary", "middle", "high"]:
            for duration in ["15min", "30min", "whole"]:
                for instruments in ["phones", "computer", "whiteboard", "quiz"]:
                    array = [nameDict[theme], ageToR[age], goalDict[theme]]
                    if theme == "costumes":
                        array.append(startCostumes[age])
                        main_ = mainPartCostumes[instruments]
                        if duration != "15min":
                            main_ += '<br>' + someExtraPart[theme]
                        if duration != "30min":
                            main_ += '<br>' + mainExtraPart[theme]
                        array.append(main_)
                    else:
                        array.append(startHolidays[age])
                        main_ = mainPartHolidays[instruments]
                        if duration != "15min":
                            main_ += '<br>' + someExtraPart[theme]
                        if duration != "30min":
                            main_ += '<br>' + mainExtraPart[theme]
                        array.append(main_)
                    array.append(reflection[age])
                    array.append(result[theme])
                    if not control.getScenariosPreviewArray(theme, age , duration, instruments):
                        with pony.orm.db_session():
                            control.createCriteria(theme, age, duration, instruments, control.createScenario(name=array[0], age=array[1], goal=array[2], start=array[3], main=array[4], reflection=array[5], result=array[6]))



generateScenarios()
# with pony.orm.db_session():
#     control.createCriteria(theme="a", age="b", duration="c", instruments="d", scenario=control.createScenario(name="aa",age= "bb", goal="cc", start="dd", main="ee", reflection="ff", result="gg"))
app.run(debug=True)