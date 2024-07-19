# Cách chạy web
1. `py -m venv moodle_venv` với người lần đầu cài
2. `. moodle_venv/Scripts/activate` để khởi tạo virtual environment. Lưu ý đối với MacOS và Linux có cách cài khác nên tìm kiếm trên google.
3. `git clone https://github.com/hauvanvn/Moodle1.1.git` với người lần đầu tải
4. `cd Moodle1.1`
5. `git pull` với người đã tải
6. `pip install -r requirements.txt` để cài các package cần thiết
7. `py manage.py runserver` để chạy server
# Sau khi coding xong mak có cài thêm những package nào thì sử dụng lệnh này trước khi push lên GitHub
`py -m pip freeze > requirements.txt`
