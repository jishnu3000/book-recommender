import pickle
import pandas as pd
import numpy as np
from flask import Flask, render_template, request

popular_books = pd.read_pickle('assets/popular_books.pkl')
book_user_rating_matrix = pd.read_pickle('assets/book_user_rating_matrix.pkl')
books = pd.read_pickle('assets/books.pkl')
similarity_scores = pd.read_pickle('assets/similarity_scores.pkl')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(
        'index.html',
        bookNames= list(popular_books['Book-Title'].values),
        authors= list(popular_books['Book-Author'].values),
        bookImages= list(popular_books['Image-URL-M'].values),
        numRatings= list(popular_books['num_ratings'].values),
        avgRatings= list(popular_books['avg_rating'].values)
    )

@app.route('/recommend')
def recommend_page():
    return render_template(
        'recommend.html',
        bookNames= list(book_user_rating_matrix.index),
    )

@app.route('/recommendations', methods=['post'])
def recommend():
    book_input = request.form.get('book_select')

    index = np.where(book_user_rating_matrix.index==book_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x:x[1], reverse=True)[1:9]
    
    recommendations = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == book_user_rating_matrix.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        recommendations.append(item)

    print(recommendations)

    return render_template('recommend.html', data=recommendations, bookNames=list(book_user_rating_matrix.index))

if __name__ == '__main__':
    app.run()