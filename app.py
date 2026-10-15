import streamlit as st

# Thiết lập giao diện
st.set_page_config(page_title="KAGUTABA - Lời Nguyền Đền Cổ", page_icon="⛩️")

# CSS tạo không gian kinh dị tối tăm
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

# Khởi tạo trạng thái trò chơi (State)
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


# Tiêu đề giao diện chính
st.title("⛩️ KAGUTABA: THỰC THÊ BỊ NGUYỀN")

# Thanh sidebar hiển thị vật phẩm
st.sidebar.markdown("### 🎒 Túi Vật Phẩm Nghi Lễ")
st.sidebar.markdown(
    f"- Chong chóng gió (Pinwheels): **{st.session_state.pinwheels_count}/3**"
)
st.sidebar.markdown(
    f"- Các vật phẩm khác: {', '.join(st.session_state.inventory) if st.session_state.inventory else 'Trống'}"
)


# --- DIỄN BIẾN CÁC CẢNH TRONG GAME ---

# 1. ĐẾN NƠI (ARRIVAL)
if st.session_state.scene == "arrival":
  st.write(
      "Bạn lái xe đến một khu đền thờ hoang vắng sâu trong vùng núi Nhật Bản."
      " Xung quanh sương mù dày đặc và không một bóng người. Mục đích duy nhất"
      " của bạn là hoàn thành nghi lễ phong ấn Kagutaba."
  )
  st.write("Bạn đứng trước lối vào ngôi đền hẻo lánh.")

  if st.button("Khám phá Khu vực Giếng nước (Phải đền)"):
    st.session_state.scene = "well"
    st.rerun()

  if st.button("Khám phá Hộp công đức & Sân sau (Trái đền)"):
    st.session_state.scene = "backyard"
    st.rerun()

  if st.button("Tiến vào khu vực đền chính / Nhà Kamidana"):
    st.session_state.scene = "shrine_main"
    st.rerun()


# 2. KHU VỰC GIẾNG NƯỚC (WELL)
elif st.session_state.scene == "well":
  st.subheader("💧 Khu Vực Giếng Nước Cổ")
  st.write(
      "Một chiếc giếng rêu phong tỏa ra hơi lạnh. Có một Chong chóng gió cắm"
      " ngay cạnh thành giếng."
  )

  if (
      st.session_state.pinwheels_count < 3
      and "Chong chóng 1" not in st.session_state.inventory
  ):
    if st.button("Nhặt Chong chóng gió số 1"):st.session_state.inventory.append("Chong chóng 1")
      st.session_state.pinwheels_count += 1
      st.success("Đã nhận 1 Chong chóng gió!")
      st.rerun()

  if st.button("Quay lại lối vào"):
    st.session_state.scene = "arrival"
    st.rerun()


# 3. SÂN SAU & HỘP CÔNG ĐỨC (BACKYARD & DONATION BOX)
elif st.session_state.scene == "backyard":
  st.subheader("🏡 Sân Sau & Hộp Công Đức")
  st.write(
      "Bạn tìm thấy một chiếc bàn có đặt một đồng xu cũ, và một chiếc hộp công"
      " đức. Phía sau nhà kho có kìm cắt dây."
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
    if st.button("Bỏ đồng xu vào Hộp công đức để đổi lấy Chong chóng gió"):
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


# 4. ĐỀN CHÍNH / NHÀ KAMIDANA (SHRINE MAIN)
elif st.session_state.scene == "shrine_main":
  st.subheader("⛩️ Khu Vực Đền Chính")
  st.write(
      "Cánh cửa đền bị xích khóa chặt bằng ổ khóa lớn. Bên trong văng vẳng"
      " tiếng động lạ."
  )

  if st.session_state.has_pliers:
    if st.button("Dùng kìm bẻ khóa cửa đền"):
      st.session_state.scene = "inside_shrine"
      st.rerun()
  else:
    st.info("Cửa bị khóa xích kiên cố. Bạn cần tìm kìm ở sân sau.")

  if st.button("Quay lại lối vào"):
    st.session_state.scene = "arrival"
    st.rerun()


# 5. BÊN TRONG ĐỀN & KHU VỰC NGHI LỄ (INSIDE SHRINE)
elif st.session_state.scene == "inside_shrine":
  st.subheader("🕯️ Phòng Nghi Lễ Cốt Lõi")
  st.write(
      "Bên trong đền tối tăm, có thêm một Chong chóng gió thứ 3 ở góc phòng,"
      " cùng vải trắng và muối."
  )

  if (
      st.session_state.pinwheels_count < 3
      and "Chong chóng 3" not in st.session_state.inventory
  ):
    if st.button("Nhặt Chong chóng gió cuối cùng"):
      st.session_state.inventory.append("Chong chóng 3")
      st.session_state.pinwheels_count += 1
      st.success("Đã thu thập đủ 3 Chong chóng gió!")
      st.rerun()st.markdown("---")
  st.write("### Thực hiện Nghi Lễ phong ấn:")

  if st.button("Làm ĐÚNG quy trình (1 Bái - 4 Vỗ tay - 1 Bái - Cắt dây)"):
    if st.session_state.pinwheels_count == 3:
      st.session_state.scene = (
          "ending_4"  # Spirit They're Gone (Đủ đồ, đúng lễ)
      )
    else:
      st.session_state.scene = "ending_3"  # Bottomless Pit (Thiếu chong chóng)
    st.rerun()

  if st.button("Làm SAI quy trình (Cắt dây trước hoặc lạy sai)"):
    st.session_state.scene = "ending_1"  # My Shadow
    st.rerun()

  if st.button("Thực hiện quy trình dị biệt (2 Bái - 2 Vỗ tay - 1 Bái)"):
    st.session_state.scene = "special_ritual_choice"
    st.rerun()


# 6. LỰA CHỌN ĐẶC BIỆT CHO ENDING 5 & 6
elif st.session_state.scene == "special_ritual_choice":
  st.subheader("🌀 Không Gian Khác Sau Hố Sâu")
  st.write(
      "Sau khi thực hiện quy trình dị biệt, bạn rơi xuống một không gian tối"
      " đen và gặp một đứa trẻ đeo mặt nạ kỳ quái đang đứng chờ."
  )

  if st.button("Nói chuyện và NHẬN lấy chiếc mặt nạ từ đứa trẻ"):
    st.session_state.scene = "ending_5"  # Cold Cold Cold
    st.rerun()

  if st.button("Từ chối nhận mặt nạ và bỏ chạy"):
    st.session_state.scene = "ending_6"  # Hole
    st.rerun()


# --- CÁC KẾT THÚC (6 ENDINGS ĐẦY ĐỦ) ---

elif st.session_state.scene == "ending_1":
  st.error("🌑 ENDING 1: MY SHADOW (Bóng Ma Đeo Bám)")
  st.write(
      "Vì thực hiện sai quy trình nghi lễ, lời nguyền không được giải tỏa mà"
      " ngược lại đã triệu hồi thực thể. Một cái bóng đen kịt bám theo bạn đến"
      " tận cùng thế giới."
  )
  if st.button("Chơi lại"):
    reset_game()
    st.rerun()

elif st.session_state.scene == "ending_2":
  st.warning("🏃 ENDING 2: RUN BOY RUN (Chạy Ngay Đi)")
  st.write(
      "Bạn đã hoàn thành chính xác các bước phong ấn. Tuy nhiên, năng lượng"
      " hắc ám bùng nổ, bạn phải lập tức cắm cổ chạy thục mạng ra xe ô tô để"
      " thoát thân khỏi ngọn núi trước khi quá muộn."
  )
  if st.button("Chơi lại"):
    reset_game()
    st.rerun()

elif st.session_state.scene == "ending_3":
  st.error("🕳️ ENDING 3: BOTTOMLESS PIT (Hố Sâu Vô Tận)")
  st.write(
      "Bạn thiếu các vật phẩm quan trọng (như thu thập chưa đủ chong chóng gió)"
      " nhưng vẫn cố thực hiện nghi lễ. Sàn nhà sụp xuống, kéo bạn rơi thẳng"
      " vào một hố sâu tối tăm không bao giờ thấy đáy."
  )
  if st.button("Chơi lại"):
    reset_game()
    st.rerun()

elif st.session_state.scene == "ending_4":
  st.error("👻 ENDING 4: SPIRIT THEY'RE GONE (Linh Hồn Tan Biến)")
  st.write("Bạn đã thu thập đủ 3 chong chóng gió và làm hoàn hảo mọi bước nghi lễ."
      " Dù phong ấn thành công ác thần, nhưng sức mạnh tâm linh quá lớn đã hòa"
      " tan thể xác lẫn linh hồn bạn vào hư vô."
  )
  if st.button("Chơi lại"):
    reset_game()
    st.rerun()

elif st.session_state.scene == "ending_5":
  st.info("❄️ ENDING 5: COLD COLD COLD (Lạnh Lẽo Tột Cùng)")
  st.write(
      "Bạn đi theo nhánh nghi lễ ẩn, gặp đứa trẻ và chấp nhận nhận chiếc mặt"
      " nạ tế lễ. Ý thức của bạn chìm vào băng giá vĩnh cửu, trở thành một phần"
      " của đền thờ."
  )
  if st.button("Chơi lại"):
    reset_game()
    st.rerun()

elif st.session_state.scene == "ending_6":
  st.error("🕳️ ENDING 6: HOLE (Cái Hố Định Mệnh)")
  st.write(
      "Bạn thực hiện nghi lễ đặc biệt nhưng kiên quyết từ chối chiếc mặt nạ từ"
      " đứa trẻ. Bạn bị nuốt chửng vào một cái hố không lối thoát, mắc kẹt trong"
      " vòng lặp vô tận của sự sợ hãi."
  )
  if st.button("Chơi lại"):
    reset_game()
    st.rerun()
