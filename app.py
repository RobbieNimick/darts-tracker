from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "darts_secret_key"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        player1 = request.form["player1"]
        player2 = request.form["player2"]
        starting_score = int(request.form["starting_score"])

        session["player1"] = player1
        session["player2"] = player2
        session["score1"] = starting_score
        session["score2"] = starting_score
        session["current_player"] = player1

        return redirect(url_for("game"))

    return render_template("index.html")


@app.route("/game", methods=["GET", "POST"])
def game():
    if "player1" not in session:
        return redirect(url_for("index"))

    message = ""

    if request.method == "POST":
        dart_score = int(request.form["dart_score"])
        current = session["current_player"]

        if current == session["player1"]:
            new_score = session["score1"] - dart_score
            if new_score < 0 or new_score == 1:
                message = f"Bust! {current} scores nothing this round."
                session["current_player"] = session["player2"]
            elif new_score == 0:
                session["score1"] = 0
                return redirect(url_for("winner"))
            else:
                session["score1"] = new_score
                session["current_player"] = session["player2"]
        else:
            new_score = session["score2"] - dart_score
            if new_score < 0 or new_score == 1:
                message = f"Bust! {current} scores nothing this round."
                session["current_player"] = session["player1"]
            elif new_score == 0:
                session["score2"] = 0
                return redirect(url_for("winner"))
            else:
                session["score2"] = new_score
                session["current_player"] = session["player1"]

    return render_template("game.html",
        player1=session["player1"],
        player2=session["player2"],
        score1=session["score1"],
        score2=session["score2"],
        current_player=session["current_player"],
        message=message
    )


@app.route("/winner")
def winner():
    if "player1" not in session:
        return redirect(url_for("index"))

    if session["score1"] == 0:
        winning_player = session["player1"]
    else:
        winning_player = session["player2"]

    return render_template("winner.html", winner=winning_player)


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)