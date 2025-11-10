Mấy ông đọc từ file main dòng if __name__ == "__main__" rồi đọc theo hướng code để hiểu hết nha
Một số thay đổi so với code tham khảo:
- Trong hàm main
+ Anh sử dụng biến layout để lấy dữ liệu file txt
--> Tui sửa thành biến level để nữa mình sẽ chọn 10 map cố định cho level từ 1-10
+ Các thông số về Mummy của anh chứa trong list gồm nhiều Mummy
--> Tui sửa thành các biến đơn quản lý 1 Mummy. Khi tới phần nâng cao mình sẽ sửa lại
- Hàm graphics
+ Ở phần Vẽ Stair tui có chỉnh lại điều kiện cho nó đơn giản và sắp xếp lại thứ tự dễ nhìn (Phần này mấy ông check lại cùng với tui)
+ Ở phần Vẽ Wall anh for (i,j) tui sửa lại for (x,y) cho nó dễ hiểu là tọa độ luôn
