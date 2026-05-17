# 23020246_NguyenTheBang_CaroAI
# Trò chơi Caro AI sử dụng Minimax và Alpha-Beta Pruning

Đây là chương trình trò chơi **Caro AI** được xây dựng bằng Python. Người chơi có thể chơi trực tiếp với máy tính thông qua giao diện đồ họa được lập trình bằng thư viện **Pygame**.

AI trong chương trình sử dụng các thuật toán tìm kiếm như **Minimax** và **Alpha-Beta Pruning** để phân tích trạng thái bàn cờ và lựa chọn nước đi phù hợp.

🔎 Overview
Caro là một trò chơi chiến thuật dành cho hai người chơi. Hai bên lần lượt đánh dấu quân cờ của mình lên bàn cờ. Người chiến thắng là người đầu tiên tạo được một chuỗi liên tiếp gồm **4 quân cờ** theo một trong các hướng:

- Hàng ngang
- Hàng dọc
- Đường chéo chính
- Đường chéo phụ

Trong project này, người chơi sẽ thi đấu với AI. Sau mỗi nước đi của người chơi, AI sẽ tính toán và đưa ra nước đi tiếp theo dựa trên thuật toán được chọn.

Chương trình có giao diện trực quan, hỗ trợ hiển thị:

- Bàn cờ Caro
- Lịch sử nước đi
- Thuật toán AI đang sử dụng
- Thời gian AI suy nghĩ
- Số nút mà thuật toán đã xét
- Kết quả thắng, thua hoặc hòa

📌 Yêu cầu 
Để chạy được chương trình, máy tính cần cài đặt:

- Python 3.x
- Thư viện Pygame: 
> pip install pygame

📂 Cấu trúc thư mục
Project gồm các file chính như sau:

```text
caro-ai/
│
├── .gitignore           # Các file/thư mục được Git bỏ qua
├── alphabeta.py         # Cài đặt thuật toán Alpha-Beta Pruning
├── benchmark.py         # So sánh hiệu suất giữa Minimax và Alpha-Beta
├── board.py             # Xử lý bàn cờ, nước đi, kiểm tra thắng/thua/hòa
├── evaluation.py        # Hàm đánh giá trạng thái bàn cờ
├── gui.py               # Giao diện trò chơi bằng Pygame
├── main.py              # File chạy chính của chương trình
├── minimax.py           # Cài đặt thuật toán Minimax
├── README.md            # File hướng dẫn sử dụng project
├── requirements.txt     # Danh sách thư viện cần cài đặt
└── utils.py             # Các hàm hỗ trợ dùng chung
```

File chính dùng để chạy chương trình là:
```text
main.py
```
🎮 Cách chạy chương trình 
Để chơi Caro với AI, hãy chạy các lệnh sau:
```text
git clone https://github.com/nguyenbang2005tb-eng/23020246_NguyenTheBang_CaroAI.git
cd 23020246_NguyenTheBang_CaroAI
python main.py
```
Sau khi chạy chương trình thành công, giao diện chính của trò chơi Caro AI sẽ xuất hiện. Tại màn hình bắt đầu, người chơi có thể lựa chọn chế độ chơi và thiết lập độ sâu tìm kiếm cho thuật toán AI.

Người chơi có thể chọn một trong các chế độ sau:

- **Minimax**: AI sử dụng thuật toán Minimax để tính toán nước đi.
- **Alpha-Beta**: AI sử dụng thuật toán Alpha-Beta Pruning để tối ưu quá trình tìm kiếm.
- **So sánh Alpha-Beta và Minimax**: chương trình chạy hai thuật toán trên cùng một trạng thái bàn cờ để so sánh thời gian xử lý, số nút đã xét và nước đi được chọn.

Ngoài ra, người chơi có thể chọn **độ sâu tìm kiếm** cho AI. Độ sâu càng lớn thì AI có thể phân tích nhiều nước đi hơn, nhưng thời gian xử lý cũng sẽ lâu hơn.

Sau khi chọn chế độ và độ sâu tìm kiếm, người chơi nhấn nút **PLAY** để bắt đầu ván đấu.

Người chơi thực hiện nước đi trước bằng cách nhấn chuột vào một ô trống trên bàn cờ. Sau khi người chơi đánh, AI sẽ sử dụng thuật toán **Minimax** hoặc **Alpha-Beta Pruning** để tính toán và đưa ra nước đi tiếp theo.

Trong giao diện chơi, người chơi có thể:
- Nhấn chuột vào ô trống trên bàn cờ để đánh quân.
- Theo dõi lượt đi của người chơi và AI.
- Xem lịch sử các nước đi đã thực hiện.
- Xem thời gian suy nghĩ của AI.
- Xem số nút mà thuật toán đã xét.
- Theo dõi kết quả ván đấu khi có người thắng hoặc hòa.
- Nhấn nút **Reset** để chơi lại ván mới từ đầu.
- Nhấn nút **Back to Menu** để quay trở lại màn hình menu chọn chế độ.

Trò chơi diễn ra luân phiên giữa người chơi và AI cho đến khi một trong hai bên tạo được chuỗi 4 quân liên tiếp theo hàng ngang, hàng dọc hoặc đường chéo. Nếu bàn cờ đã được đánh hết nhưng vẫn chưa có bên nào chiến thắng, ván đấu sẽ được tính là hòa. Khi ván đấu kết thúc, chương trình sẽ hiển thị kết quả thắng, thua hoặc hòa.


