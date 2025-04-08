from flask import Flask, request, render_template
from models.recommender import AssessmentRecommender

app = Flask(__name__)
recommender = AssessmentRecommender()

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        query = request.form['query']
        results = recommender.get_recommendations(query)
    return render_template('index.html', results=results)
if __name__ == "__main__":
    app.run(debug=True)