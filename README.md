# Project Moodle1.1
Đây là đồ án nhóm của môn Nhập môn công nghệ phần mềm(CSC13002). Là một trang web quản lý học tập của trường lấy ý tưởng từ trang quản lý học tập của trường đại học Khoa học Tự Nhiên - DHQGHCM. Trang web có chức năng tạo môn học, tải tài liệu, giao bài tập...

Web được code bằng thml, Bootstrap css framework cho frontend và Django framework cho backend.

Thành viên trong Nhóm:
1. Nguyễn Văn Hậu (22127105), vai trò: Backend Dev
2. Nguyễn Văn Đức (22127073), vai trò: Fullstack Dev
3. Đinh Vũ Gia Hân (22127098), vai trò: Fontend Dev
4. Nguyễn Thị Thu Ngân (22127290), vai trò: Design và Frontend Dev
5. Nguyễn Gia Kiệt - team leader (22127221), vai trò: Design và Frontend Dev

## Cách chạy web
1. `py -m venv moodle_venv` với người lần đầu cài
2. `. moodle_venv/Scripts/activate` để khởi tạo virtual environment. Lưu ý đối với MacOS và Linux có cách cài khác nên tìm kiếm trên google.
3. `git clone https://github.com/hauvanvn/Moodle1.1.git` với người lần đầu tải
4. `cd Moodle1.1`
5. `git pull` với người đã tải
6. `pip install -r requirements.txt` để cài các package cần thiết
7. `py manage.py runserver` để chạy server
## Sau khi coding xong mak có cài thêm những package nào thì sử dụng lệnh này trước khi push lên GitHub
`py -m pip freeze > requirements.txt`
