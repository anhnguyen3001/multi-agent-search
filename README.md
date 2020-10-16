# Pacman-Multi agents
Câu 1: Reflex Agent:
- Hàm evaluation tính dựa vào: score = score của trạng thái game tiếp - min(khoảng cách -> các food) + min(khoảng cách -> các ghost).

Câu 2: Minimax:
- Gồm 3 hàm: minimax, maxValue, minValue.
- Hàm maxValue - pacman, minValue - ghost. Cả hai hàm đều chạy loop trên các actions có thể từ trạng thái hiện tại, lấy giá trị bằng cách gọi đến hàm minimax. Sau đó, với hàm maxValue lấy giá trị max của các actions, với hàm minValue lấy giá trị min của các actions.
- Hàm minimax: Nếu là trạng thái kết thúc -> lấy giá trị bằng hàm self.evaluationFunction(). Tiếp tục, kiểm tra xem là pacman hay ghost. Nếu là pacman -> maxValue còn là ghost -> minValue.

Câu 3: Alpha-Beta Pruning:
- Cũng tương tự với Câu 2. Tuy nhiên ở hàm maxValue, minValue có thêm phần cắt nhánh:
  + maxValue: Sau khi cập nhật maxValue, kiểm tra xem maxValue > beta => cắt nhánh, không thì cập nhật là alpha = maxValue
  + minValue: Sau khi cập nhật minValue, kiểm tra xem minValue < alpha => cắt nhánh, không thì cập nhật là beta = minValue

Câu 4: Expectimax:
- Cũng tương tự với Câu 2. Tuy nhiên ở hàm minValue đổi thành hàm expValue. Trong hàm này, thay vì tìm min của các actions (như Minimax) thì value = sum(value của các actions hợp lệ)/ số actions hợp lệ

Câu 5: Evaluation Function:
- Tính dựa vào với sự ưu tiên giảm dần: 
  + Số viên to còn lại
  + Số food còn lại
  + Ghost sợ gần nhất
  + Food gần nhất
  + Ghost bình thường gần nhất
