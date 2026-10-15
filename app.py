import streamlit as st

# Thiết lập giao diện
st.set_page_config(page_title="KAGUTABA - Lời Nguyền Đền Cổ", page_icon="⛩️")

# CSS tạo không gian kinh dị
st.markdown(
    """
    <style>
    .stApp {
        background-color: #080808;
        color: #cccccc;
    }
    h1, h2, h3 {
        color: #990000 !important;
        font-family: monospace;
    }
    .stButton>button {
        background-color: #1a1a1a;
        color: #ff3333;
        border: 1px solid #7a0000;
        width: 100%;
        margin-bottom: 8px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #7a0000;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Khởi tạo trạng thái trò chơi
if "scene" not in st.session_state:
  st.session_state.scene = "arrival"
  st.session_state.inventory = []
  st.session_state.pinwheels_count = 0
  st.session_state.has_pliers = False
  st.session_state.has_coin = False


def reset_game():
  st.session_state.scene = "arrival"
  st.session_state.inventory = []
  st.session_state.pinwheels_count = 0
  st.session_state.has_pliers = False
  st.session_state.has_coin = False


# Tiêu đề chính
st.title("⛩️ KAGUTABA: THỰC THỂ BỊ NGUYỀN")

# Sidebar
st.sidebar.markdown("### 🎒 Túi Vật Phẩm Nghi Lễ")
st.sidebar.markdown(
    f"- Chong chóng gió: **{st.session_state.pinwheels_count}/3**"
)
st.sidebar.markdown(
    f"- Vật phẩm khác: {', '.join(st.session_state.inventory) if st.session_state.inventory else 'Trống'}"
)


# --- DIỄN BIẾN GAME ---

# 1. ĐẾN NƠI
if st.session_state.scene == "arrival":
  st.write(
      "Bạn lái xe đến một khu đền thờ hoang vắng sâu trong vùng núi Nhật Bản."
      " Xung quanh sương mù dày đặc. Mục đích duy nhất của bạn là hoàn thành"
      " nghi lễ phong ấn Kagutaba."
  )
  st.write("Bạn đứng trước lối vào ngôi đền hẻo lánh.")

  if st.button("Khám phá Khu vực Giếng nước (Bên phải)"):
    st.session_state.scene = "well"
    st.rerun()

  if st.button("Khám phá Hộp công đức & Sân sau (Bên trái)"):
    st.session_state.scene = "backyard"
    st.rerun()

  if st.button("Tiến vào khu vực đền chính"):
    st.session_state.scene = "shrine_main"
    st.rerun()

# 2. GIẾNG NƯỚC
elif st.session_state.scene == "well":
  st.subheader("💧 Khu Vực Giếng Nước Cổ")
  st.write(
      "Chiếc giếng rêu phong tỏa ra hơi lạnh. Có một Chong chóng gió cắm ngay"
      " cạnh thành giếng."
  )

  if (
      st.session_state.pinwheels_count < 3
      and "Chong chóng 1" not in st.session_state.inventory
  ):
    if st.button("Nhặt Chong chóng gió số 1"):
      st.session_state.inventory.append("Chong chóng 1")
      st.session_state.pinwheels_count += 1
      st.success("Đã nhận 1 Chong chóng gió!")
      st.rerun()

  if st.button("Quay lại lối vào"):st.session_state.scene = "arrival"
    st.rerun()

# 3. SÂN SAU & HỘP CÔNG ĐỨC
elif st.session_state.scene == "backyard":
  st.subheader("🏡 Sân Sau & Hộp Công Đức")
  st.write(
      "Bạn tìm thấy một chiếc bàn có đặt đồng xu cũ và một hộp công đức. Phía"
      " sau nhà kho có kìm cắt dây."
  )

  if (
      not st.session_state.has_coin
      and "Đồng xu" not in st.session_state.inventory
  ):
    if st.button("Nhặt Đồng xu cũ trên bàn"):
      st.session_state.inventory.append("Đồng xu")
      st.session_state.has_coin = True
      st.success("Đã nhặt đồng xu!")
      st.rerun()

  if (
      "Đồng xu" in st.session_state.inventory
      and "Chong chóng 2" not in st.session_state.inventory
  ):
    if st.button("Bỏ đồng xu vào Hộp công đức để đổi Chong chóng gió"):
      st.session_state.inventory.append("Chong chóng 2")
      st.session_state.pinwheels_count += 1
      st.success("Hộp công đức nhả ra Chong chóng gió số 2!")
      st.rerun()

  if not st.session_state.has_pliers:
    if st.button("Nhặt kìm cắt dây ở sân sau"):
      st.session_state.has_pliers = True
      st.session_state.inventory.append("Kìm cắt")
      st.success("Đã lấy kìm!")
      st.rerun()

  if st.button("Quay lại lối vào"):
    st.session_state.scene = "arrival"
    st.rerun()

# 4. ĐỀN CHÍNH
elif st.session_state.scene == "shrine_main":
  st.subheader("⛩️ Khu Vực Đền Chính")
  st.write("Cánh cửa đền bị xích khóa chặt bằng ổ khóa lớn.")

  if st.session_state.has_pliers:
    if st.button("Dùng kìm bẻ khóa cửa đền"):
      st.session_state.scene = "inside_shrine"
      st.rerun()
  else:
    st.info("Cửa bị khóa xích kiên cố. Bạn cần tìm kìm ở sân sau.")

  if st.button("Quay lại lối vào"):
    st.session_state.scene = "arrival"
    st.rerun()

# 5. BÊN TRONG ĐỀN & NGHI LỄ
elif st.session_state.scene == "inside_shrine":
  st.subheader("🕯️ Phòng Nghi Lễ Cốt Lõi")
  st.write("Bên trong đền tối tăm, có thêm một Chong chóng gió ở góc phòng.")

  if (
      st.session_state.pinwheels_count < 3
      and "Chong chóng 3" not in st.session_state.inventory
  ):
    if st.button("Nhặt Chong chóng gió cuối cùng"):
      st.session_state.inventory.append("Chong chóng 3")
      st.session_state.pinwheels_count += 1
      st.success("Đã thu thập đủ 3 Chong chóng gió!")
      st.rerun()

  st.markdown("---")
  st.write("### Thực hiện Nghi Lễ phong ấn:")

  if st.button("Làm ĐÚNG quy trình (1 Bái - 4 Vỗ tay - 1 Bái - Cắt dây)"):
    if st.session_state.pinwheels_count == 3:
      st.session_state.scene = "ending_4"
    else:
      st.session_state.scene = "ending_3"
    st.rerun()

  if st.button("Làm SAI quy trình (Cắt dây trước hoặc lạy sai)"):
    st.session_state.scene = "ending_1"
    st.rerun()if st.button("Thực hiện quy trình dị biệt (2 Bái - 2 Vỗ tay - 1 Bái)"):
    st.session_state.scene = "special_ritual_choice"
    st.rerun()

# 6. LỰA CHỌN ENDING 5 & 6
elif st.session_state.scene == "special_ritual_choice":
  st.subheader("🌀 Không Gian Khác Sau Hố Sâu")
  st.write(
      "Sau khi thực hiện quy trình dị biệt, bạn rơi xuống một không gian tối"
      " đen và gặp một đứa trẻ đeo mặt nạ kỳ quái đang đứng chờ."
  )

  if st.button("Nói chuyện và NHẬN lấy chiếc mặt nạ từ đứa trẻ"):
    st.session_state.scene = "ending_5"
    st.rerun()

  if st.button("Từ chối nhận mặt nạ và bỏ chạy"):
    st.session_state.scene = "ending_6"
    st.rerun()

# --- 6 ENDINGS ---
elif st.session_state.scene == "ending_1":
  st.error("🌑 ENDING 1: MY SHADOW (Bóng Ma Đeo Bám)")
  st.write(
      "Vì làm sai nghi lễ, một cái bóng đen kịt đã bám theo bạn đến tận cùng"
      " thế giới."
  )
  if st.button("Chơi lại"):
    reset_game()
    st.rerun()

elif st.session_state.scene == "ending_2":
  st.warning("🏃 ENDING 2: RUN BOY RUN (Chạy Ngay Đi)")
  st.write(
      "Năng lượng hắc ám bùng nổ, bạn phải lập tức cắm cổ chạy thục mạng ra xe"
      " ô tô để thoát thân!"
  )
  if st.button("Chơi lại"):
    reset_game()
    st.rerun()

elif st.session_state.scene == "ending_3":
  st.error("🕳️ ENDING 3: BOTTOMLESS PIT (Hố Sâu Vô Tận)")
  st.write(
      "Bạn thiếu vật phẩm chong chóng gió! Sàn nhà sụp xuống kéo bạn rơi xuống"
      " hố sâu không đáy."
  )
  if st.button("Chơi lại"):
    reset_game()
    st.rerun()

elif st.session_state.scene == "ending_4":
  st.error("👻 ENDING 4: SPIRIT THEY'RE GONE (Linh Hồn Tan Biến)")
  st.write(
      "Bạn đã thu thập đủ 3 chong chóng và thực hiện hoàn hảo! Nhưng sức mạnh"
      " tâm linh quá lớn đã hòa tan linh hồn bạn vào hư vô."
  )
  if st.button("Chơi lại"):
    reset_game()
    st.rerun()

elif st.session_state.scene == "ending_5":
  st.info("❄️ ENDING 5: COLD COLD COLD (Lạnh Lẽo Tột Cùng)")
  st.write(
      "Bạn nhận chiếc mặt nạ. Ý thức của bạn chìm vào băng giá vĩnh cửu, trở"
      " thành một phần của đền thờ."
  )
  if st.button("Chơi lại"):
    reset_game()
    st.rerun()

elif st.session_state.scene == "ending_6":
  st.error("🕳️ ENDING 6: HOLE (Cái Hố Định Mệnh)")
  st.write(
      "Bạn từ chối chiếc mặt nạ và bị nuốt chửng vào một cái hố không lối"
      " thoát."
  )
  if st.button("Chơi lại"):
    reset_game()
    st.rerun()
