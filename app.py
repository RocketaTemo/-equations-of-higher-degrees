# - *- coding: utf- 8 - *-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from decimal import Decimal

from flask import Flask, request, render_template, redirect, session, url_for

from Functions import get_coeff, \
    get_coeff_md_1, \
    get_coeff_md_2, \
    get_coeff_md_3, \
    get_coeff_md_4, \
    get_x_md_1, \
    get_x_md_2, \
    stop, r_f, get_orient

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "2d2c7095b09ea67d3384d8d8c83372b1901f6eb2"


# coeff = [[Decimal(3), Decimal(0), Decimal(5), Decimal(5)]]  # Таблица с коэффицентами
# coeff.append([1, -35, 380, -1350, 1000])
# coeff.append([[1, 0], [-4, 0], [6, 0], [-3, 0], [2, 0], [1, 0]])

# ШАГ 1

@app.route('/e1/step_1/', methods=["GET", "POST"])
def e1_step_1():
    if not "messege" in session:
        session["messege"] = ""
    if request.method == "POST":
        coeff = []
        coeff.append([])

        response = request.form["response"].split(",")
        session["coeff"] = response

        for num in session["coeff"]:
            coeff[0].append(Decimal(num))

        n = len(coeff[0]) - 1
        g = 1
        h = 3

        # ПОЛУЧИТЬ КОЭФФИЦЕНТЫ

        while True:

            coeff.append([])
            for i in range(0, n + 1):
                coeff[g].append(r_f(get_coeff(coeff, g, i, n), h))

            if stop(coeff, g, n, h):  # условия остановки
                break

            g += 1
            # input()

        session["coeff_g"] = g
        # ПОЛУЧИТЬ КОРНИ

        xs = []  # Здесь хранятся действительные корни
        l = 1
        ro_inf = None

        while l < n + 1:
            # ПОЛУЧИТЬ ДЕЙСТВИТЕЛЬНЫЕ КОРНИ
            if coeff[g][l] > 0 and coeff[g][l - 1] > 0 and coeff[g - 1][l] > 0 and coeff[g - 1][l - 1] > 0:

                a = coeff[g][l]
                b = coeff[g][l - 1]

                x = r_f((a / b) ** Decimal(1 / (2 ** g)), h)
                if type(x) == complex:
                    x = x.real

                if get_orient(coeff, x, n):
                    xs.append((round(r_f(x, h), 10)))
                else:
                    xs.append(round(r_f(-x, h - 1), 10))

            else:  # ПОЛУЧИТЬ КОМПЛЕКСНЫЕ КОРНИ
                a = coeff[g][l + 1]
                b = coeff[g][l - 1]
                ro = (a / b) ** Decimal(1 / (2 ** g))

                ro_inf = [l, ro]  # ро и его позиция
                l += 1

            l += 1

        if ro_inf:  # если есть комплексные корни
            alfa = Decimal(-1 / 2) * coeff[0][1] / coeff[0][0]

            for x in xs:
                alfa += Decimal(-1 / 2) * x

            alfa = r_f(alfa, h)

            ro_ = ro_inf[1]

            beta = r_f(abs(ro_ - alfa ** 2) ** Decimal(1 / 2), h)

            xs.append(complex(alfa, -beta))
            xs.append(complex(alfa, beta))

        session["messege"] = "Готово можете перейти к решению"
        return redirect(url_for("restart"))

    return render_template("e1_step_1.html")


# ШАГ 2
@app.route('/e1/step_2/', methods=["GET", "POST"])
def e1_step_2():
    errors = []
    coeff = []
    coeff.append([])

    for num in session["coeff"]:
        coeff[0].append(Decimal(num))

    n = len(coeff[0]) - 1
    g = 1
    h = 3

    # ПОЛУЧИТЬ КОЭФФИЦЕНТЫ

    while True:

        coeff.append([])
        for i in range(0, n + 1):
            coeff[g].append(r_f(get_coeff(coeff, g, i, n), h))

        if stop(coeff, g, n, h):  # условия остановки
            break

        g += 1
        # input()

    if not "k" in session:
        session["k"] = 1
    if not "j" in session:
        session["j"] = 0
    if not "N" in session:
        session["N"] = n + 1

    if request.method == "POST":

        response = r_f(Decimal(request.form["response"].replace(" ", "")), h)

        if r_f(response, 1) == r_f(coeff[session["k"]][session["j"]], 1):
            session["N"] += 1
            session["j"] += 1
            if session["j"] > n:
                session["j"] = 0
                session["k"] += 1

            errors.append("not")
        else:

            if r_f(response, h) == r_f(r_f(get_coeff_md_1(coeff, session["k"], session["j"], n), h), 2):
                errors.append(1)
            elif response == r_f(get_coeff_md_2(coeff, session["k"], session["j"], n), h):
                errors.append(2)
            elif response == r_f(get_coeff_md_3(coeff, session["k"], session["j"], n), h):
                errors.append(3)
            elif response == r_f(get_coeff_md_4(coeff, session["k"], session["j"], n), h):
                errors.append(4)

        # print(get_coeff_md_1(coeff, session["k"], session["j"], n))
        # print(get_coeff_md_2(coeff, session["k"], session["j"], n))
        # print(get_coeff_md_3(coeff, session["k"], session["j"], n))
        # print(get_coeff_md_4(coeff, session["k"], session["j"], n))

    return render_template("e1_step_2.html", coeff=coeff, errors=errors, N=session["N"])


# ШАГ 3
@app.route('/e1/step_3/', methods=["GET", "POST"])
def e1_step_3():
    errors = []

    coeff = []
    coeff.append([])

    for num in session["coeff"]:
        coeff[0].append(Decimal(num))

    n = len(coeff[0]) - 1
    g = 1
    h = 3
    # ПОЛУЧИТЬ КОЭФФИЦЕНТЫ

    while True:

        coeff.append([])
        for i in range(0, n + 1):
            coeff[g].append(r_f(get_coeff(coeff, g, i, n), h))

        if stop(coeff, g, n, h):  # условия остановки
            break

        g += 1
        # input()

    # ПОЛУЧИТЬ КОРНИ

    xs = []  # Здесь хранятся действительные корни
    l = 1
    ro_inf = None

    while l < n + 1:
        # ПОЛУЧИТЬ ДЕЙСТВИТЕЛЬНЫЕ КОРНИ

        if coeff[g][l] > 0 and coeff[g][l - 1] > 0 and coeff[g - 1][l] > 0 and coeff[g - 1][l - 1] > 0:

            a = coeff[g][l]
            b = coeff[g][l - 1]

            x = r_f((a / b) ** Decimal(1 / (2 ** g)), h)
            if type(x) == complex:
                x = x.real

            if get_orient(coeff, x, n):
                xs.append(r_f(x, h))
            else:
                xs.append(round(r_f(-x, h - 1), 10))

        else:  # ПОЛУЧИТЬ КОМПЛЕКСНЫЕ КОРНИ
            a = coeff[g][l + 1]
            b = coeff[g][l - 1]
            ro = (a / b) ** Decimal(1 / (2 ** g))

            ro_inf = [l, ro]  # ро и его позиция
            l += 1

        l += 1
    if ro_inf:  # если есть комплексные корни
        alfa = Decimal(-1 / 2) * coeff[0][1] / coeff[0][0]

        for x in xs:
            alfa += Decimal(-1 / 2) * x

        alfa = r_f(alfa, h)

        ro_ = ro_inf[1]

        beta = r_f(abs(ro_ - alfa ** 2) ** Decimal(1 / 2), h)
        beta_md_1 = r_f(abs(ro_ ** 2 - alfa ** 2) ** Decimal(1 / 2), h)

        xs.append(complex(alfa, +beta))
        xs.append(complex(alfa, -beta))

    if not "l3" in session:
        session["l3"] = 0
    if not "N3" in session:
        session["N3"] = 1

    if not "resp" in session:
        session["resp"] = []
        for x in xs:
            if type(x) != complex:
                a = n
                sum = 0
                for c in coeff[0]:
                    sum += c * x ** a
                    a -= 1
                session["resp"].append(float(sum))
            else:
                session["resp"].append("0.0023-1.7i")
                session["resp"].append("0.010+0.541i")
    xsm = []
    for x in xs:
        if type(x) != complex:
            xsm.append(x.normalize())
        else:
            xsm.append(x)

    # cвязь с сайтом
    if request.method == "POST":
        if not "i" in request.form["response"]:
            response = r_f(Decimal(request.form["response"].replace(" ", "")), h)

            if response == r_f(xs[session["l3"]], h):
                session["l3"] += 1
                session["N3"] += 1
                errors.append("not")

            elif response == r_f(get_x_md_1(coeff, g, session["l3"], n, h), 10):
                errors.append(1)
            elif response == r_f(get_x_md_2(coeff, g, session["l3"], n, h), 10):
                errors.append(2)




        else:
            response = request.form["response"].replace("-", "$-") \
                .replace("+", "$+") \
                .replace("i", "") \
                .replace(" ", "") \
                .split("$")

            if complex(Decimal(response[0]), Decimal(response[1])) in xs:
                session["l3"] += 1
                session["N3"] += 1
                errors.append("not")
            elif Decimal(response[1]) == beta_md_1:
                errors.append(10)

    return render_template("e1_step_3.html", xs=xsm, errors=errors)


@app.route('/e1/step_4/', methods=["GET", "POST"])
def e1_step_4():
    errors = []

    coeff = []
    coeff.append([])

    for num in session["coeff"]:
        coeff[0].append(Decimal(num))

    n = len(coeff[0]) - 1
    g = 1
    h = 3
    # ПОЛУЧИТЬ КОЭФФИЦЕНТЫ

    while True:

        coeff.append([])
        for i in range(0, n + 1):
            coeff[g].append(r_f(get_coeff(coeff, g, i, n), h))

        if stop(coeff, g, n, h):  # условия остановки
            break

        g += 1
        # input()

    # ПОЛУЧИТЬ КОРНИ

    xs = []  # Здесь хранятся действительные корни
    l = 1
    ro_inf = None

    while l < n + 1:
        # ПОЛУЧИТЬ ДЕЙСТВИТЕЛЬНЫЕ КОРНИ

        if coeff[g][l] > 0 and coeff[g][l - 1] > 0 and coeff[g - 1][l] > 0 and coeff[g - 1][l - 1] > 0:

            a = coeff[g][l]
            b = coeff[g][l - 1]

            x = r_f((a / b) ** Decimal(1 / (2 ** g)), h)
            if type(x) == complex:
                x = x.real

            if get_orient(coeff, x, n):
                xs.append(r_f(x, h))
            else:
                xs.append(round(r_f(-x, h - 1), 10))

        else:  # ПОЛУЧИТЬ КОМПЛЕКСНЫЕ КОРНИ
            a = coeff[g][l + 1]
            b = coeff[g][l - 1]
            ro = (a / b) ** Decimal(1 / (2 ** g))

            ro_inf = [l, ro]  # ро и его позиция
            l += 1

        l += 1
    if ro_inf:  # если есть комплексные корни
        alfa = Decimal(-1 / 2) * coeff[0][1] / coeff[0][0]

        for x in xs:
            alfa += Decimal(-1 / 2) * x

        alfa = r_f(alfa, h)

        ro_ = ro_inf[1]

        beta = r_f(abs(ro_ - alfa ** 2) ** Decimal(1 / 2), h)
        beta_md_1 = r_f(abs(ro_ ** 2 - alfa ** 2) ** Decimal(1 / 2), h)

        xs.append(complex(alfa, +beta))
        xs.append(complex(alfa, -beta))

    if not "l3" in session:
        session["l3"] = 0
    if not "N3" in session:
        session["N3"] = 1

    if not "resp" in session:
        session["resp"] = []
        for x in xs:
            if type(x) != complex:
                a = n
                sum = 0
                for c in coeff[0]:
                    sum += c * x ** a
                    a -= 1
                session["resp"].append(float(sum))
            else:
                session["resp"].append("0.0023-1.7i")
                session["resp"].append("0.010+0.541i")
    xsm = []
    for x in xs:
        if type(x) != complex:
            xsm.append(x.normalize())
        else:
            xsm.append(x)

    # cвязь с сайтом
    if request.method == "POST":
        if not "i" in request.form["response"]:
            response = r_f(Decimal(request.form["response"].replace(" ", "")), h)

            if response == r_f(xs[session["l3"]], h):
                session["l3"] += 1
                session["N3"] += 1
                errors.append("not")

            elif response == r_f(get_x_md_1(coeff, g, session["l3"], n, h), 10):
                errors.append(1)
            elif response == r_f(get_x_md_2(coeff, g, session["l3"], n, h), 10):
                errors.append(2)




        else:
            response = request.form["response"].replace("-", "$-") \
                .replace("+", "$+") \
                .replace("i", "") \
                .replace(" ", "") \
                .split("$")

            if complex(Decimal(response[0]), Decimal(response[1])) in xs:
                session["l3"] += 1
                session["N3"] += 1
                errors.append("not")
            elif Decimal(response[1]) == beta_md_1:
                errors.append(10)

    return render_template("e1_step_4.html", xs=xsm, errors=errors)

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route('/restart/', methods=["GET", "POST"])
def restart():
    session.pop("k", None)
    session.pop("j", None)
    session.pop("N", None)
    session.pop("N3", None)
    session.pop("l3", None)
    session.pop("resp", None)

    return redirect(request.referrer)


if __name__ == '__main__':
    app.run()
