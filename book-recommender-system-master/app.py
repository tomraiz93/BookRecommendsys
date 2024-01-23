from flask import Flask, render_template, request
import pickle
import numpy as np

# Load danh sách tác giả từ file pickle
with open('authors.pkl', 'rb') as file:
    author_list = pickle.load(file)

popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)
recommendations = []
temporary_recommendations = []

def process_recommendations(recommendations):
    global temporary_recommendations
    temporary_recommendations.extend(recommendations[:10])
    
    # In các đường dẫn ảnh để kiểm tra
    for rec in recommendations[:10]:
        print("Image URL:", rec[0][2])

# Hàm tìm kiếm sách và tác giả dựa trên phần tên
def search_books_partial(user_input):
    # Kiểm tra và xử lý NaN trong cột 'Book-Author'
    books['Book-Author'] = books['Book-Author'].fillna('')  # Thay thế NaN bằng chuỗi trống

    # Tìm kiếm sách hoặc tác giả dựa trên phần của tên nhập vào
    matching_items = books[books['Book-Title'].str.lower().str.contains(user_input.lower()) |
                          books['Book-Author'].str.lower().str.contains(user_input.lower())]

    if matching_items.empty:
        return []

    return matching_items[['Book-Title', 'Book-Author', 'Image-URL-M']]

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values),
                           temporary_recommendations=temporary_recommendations,
                           recommendations=recommendations
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend_books():
    user_input = request.form.get('user_input')

    # Tìm kiếm sách và tác giả dựa trên phần tên
    matching_books = search_books_partial(user_input)

    if matching_books.empty:
        return render_template('recommend.html', data=[])

    # Lấy gợi ý cho sách và tác giả phù hợp
    
    seen_items = set()

    for _, item in matching_books.iterrows():
        book_title = item['Book-Title']

        # Kiểm tra xem cuốn sách hoặc tác giả đã được thêm vào gợi ý chưa
        if book_title not in seen_items:
            item_data = [
                book_title,
                item['Book-Author'],
                item['Image-URL-M']
            ]

            recommendations.append([item_data])
            seen_items.add(book_title)

    process_recommendations(recommendations)

    return render_template('recommend.html', data=recommendations, user_input=user_input)

@app.route('/recommend_by_author', methods=['POST'])
def recommend_by_author():
    author_input = request.form.get('author_input')

    # Tìm kiếm sách và tác giả dựa trên phần tên tác giả
    matching_items = search_books_partial(author_input)

    if matching_items.empty:
        return render_template('recommend.html', data=[])

    # Lấy gợi ý cho sách và tác giả phù hợp
    recommendations = []
    seen_items = set()

    for _, item in matching_items.iterrows():
        book_title = item['Book-Title']

        # Kiểm tra xem cuốn sách hoặc tác giả đã được thêm vào gợi ý chưa
        if book_title not in seen_items:
            item_data = [
                book_title,
                item['Book-Author'],
                item['Image-URL-M']
            ]

            recommendations.append([item_data])
            seen_items.add(book_title)

    process_recommendations(recommendations)
    return render_template('recommend.html', data=recommendations, author_input=author_input)


if __name__ == '__main__':
    app.run(debug=True)