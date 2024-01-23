// recommend.js

// Hàm để lưu số lần bấm submit gợi ý vào localStorage
function saveRecommendCount() {
    // Lấy số lần từ localStorage, nếu không có thì mặc định là 0
    let count = parseInt(localStorage.getItem('recommendCount')) || 0;

    // Tăng biến đếm lên 1
    count++;

    // Lưu số lần vào localStorage
    localStorage.setItem('recommendCount', count);
}

// Hàm để lấy số lần bấm submit gợi ý từ localStorage
function getRecommendCount() {
    return parseInt(localStorage.getItem('recommendCount')) || 0;
}

// Hàm để hiển thị sách và lưu số lần bấm submit gợi ý khi người dùng xem sách
function viewBook(book) {
    // Hiển thị sách
    console.log("Viewing Book: ", book);

    // Lưu số lần bấm submit gợi ý
    saveRecommendCount();
}

// Hàm để kiểm tra xem nên hiển thị sách gợi ý hay không
function shouldDisplayRecommendedBooks() {
    // Kiểm tra số lần bấm submit gợi ý
    const recommendCount = getRecommendCount();

    // Trả về true nếu có ít nhất một lần bấm submit, ngược lại là false
    return recommendCount > 0;
}
