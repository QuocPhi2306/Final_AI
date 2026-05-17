import streamlit as st
from matplotlib.figure import Figure

from core.config import BA_PARAMS
from core.data_loader import generate_random_cities
from services.runner import run_algorithm


st.set_page_config(page_title="TSP Solver Dashboard", layout="wide")


def apply_custom_style():
    st.markdown(
        """
        <style>
        html, body, .stApp {
            background: #0c1725;
            color: #f5f7ff;
        }
        .css-1v3fvcr, .css-1v3fvcr span, .css-18ni7ap, .css-1gkd3gj, .css-1d391kg {
            color: #f5f7ff;
        }
        .stButton>button {
            background-color: #0f5df4;
            color: white;
            border-radius: 10px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #1366ff;
            color: white;
        }
        .stAlert {
            background-color: #172a43;
            color: #f5f7ff;
        }
        .metric-container {
            background: #14223b;
            border-radius: 18px;
            padding: 18px 24px;
            margin-bottom: 12px;
        }
        .block-container {
            padding-top: 1rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 1rem;
        }
        .stSidebar {
            background: linear-gradient(180deg, #0a1221 0%, #08101f 100%);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def plot_route_figure(coords, path):
    fig = Figure(figsize=(10, 6), dpi=100)
    ax = fig.add_subplot(111)

    x = [coords[i][0] for i in path] + [coords[path[0]][0]]
    y = [coords[i][1] for i in path] + [coords[path[0]][1]]
    ax.plot(x, y, marker="o", color="#68b3ff", linewidth=2, markersize=8)

    for idx, (xi, yi) in enumerate(coords):
        ax.scatter([xi], [yi], color="#45b295", s=60, zorder=3)
        ax.text(xi, yi, str(idx), fontsize=10, color="#ffffff", ha="right", va="bottom")

    ax.set_facecolor("#0a1630")
    fig.patch.set_facecolor("#0c1725")
    ax.spines["bottom"].set_color("#5f7db5")
    ax.spines["top"].set_color("#5f7db5")
    ax.spines["left"].set_color("#5f7db5")
    ax.spines["right"].set_color("#5f7db5")
    ax.xaxis.label.set_color("#f5f7ff")
    ax.yaxis.label.set_color("#f5f7ff")
    ax.title.set_color("#f5f7ff")
    ax.tick_params(colors="#d6deff")
    ax.grid(True, color="#1f2d54")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    return fig


def plot_convergence_figure(history):
    fig = Figure(figsize=(10, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(range(len(history)), history, marker="o", color="#ffa726", linewidth=2)
    ax.set_facecolor("#0a1630")
    fig.patch.set_facecolor("#0c1725")
    ax.spines["bottom"].set_color("#5f7db5")
    ax.spines["top"].set_color("#5f7db5")
    ax.spines["left"].set_color("#5f7db5")
    ax.spines["right"].set_color("#5f7db5")
    ax.xaxis.label.set_color("#f5f7ff")
    ax.yaxis.label.set_color("#f5f7ff")
    ax.title.set_color("#f5f7ff")
    ax.tick_params(colors="#d6deff")
    ax.grid(True, color="#1f2d54")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Best Cost")
    return fig


def initialize_state():
    if "best_cost" not in st.session_state:
        st.session_state.best_cost = None
    if "best_run" not in st.session_state:
        st.session_state.best_run = None
    if "last_result" not in st.session_state:
        st.session_state.last_result = None
    if "last_coords" not in st.session_state:
        st.session_state.last_coords = None
    if "last_n" not in st.session_state:          
        st.session_state.last_n = None             
    if "last_algorithm" not in st.session_state:  
        st.session_state.last_algorithm = None     


def main():
    apply_custom_style()
    initialize_state()

    st.write("# Giải bài toán Người du lịch")
    st.write("#### (Travelling salesman problem)")

    with st.sidebar:
        st.write("## Cấu hình")
        n = st.slider("Số lượng thành phố", min_value=3, max_value=50, value=15, step=1)
        algorithm_choice = st.selectbox("Thuật toán", ["Bat Algorithm", "Backtracking"])
        run_button = st.button("Chạy thuật toán")

        if st.session_state.best_cost is not None:
            st.markdown("---")
            st.write("### Kỷ lục hiện tại")
            st.write(f"**{st.session_state.best_cost:.3f}**")
            if st.session_state.best_run:
                st.write(f"Thuật toán: {st.session_state.best_run}")

    algorithm = "ba" if algorithm_choice == "Bat Algorithm" else "backtracking"
    if algorithm == "backtracking" and n > 12:
        st.warning("Backtracking có thể chậm với số thành phố lớn hơn 12.")
# Reset khi thay đổi cấu hình
    if st.session_state.last_n != n or st.session_state.last_algorithm != algorithm_choice:
        st.session_state.best_cost = None
        st.session_state.best_run = None
        st.session_state.last_result = None
        st.session_state.last_coords = None
        st.session_state.last_n = n
        st.session_state.last_algorithm = algorithm_choice
    if run_button:
        coords, matrix = generate_random_cities(n, return_coords=True)
        params = BA_PARAMS if algorithm == "ba" else None
        with st.spinner("Đang chạy thuật toán..."):
            result = run_algorithm(algorithm, matrix, params)

        st.session_state.last_result = result
        st.session_state.last_coords = coords
        if st.session_state.best_cost is None or result["cost"] < st.session_state.best_cost:
            st.session_state.best_cost = result["cost"]
            st.session_state.best_run = algorithm_choice

    result = st.session_state.last_result
    coords = st.session_state.last_coords

    if result is not None and coords is not None:
        first_col, second_col, third_col = st.columns([1.5, 1.5, 1.5])
        first_col.metric("Chi phí mới nhất", f"{result['cost']:.4f}")
        second_col.metric("Thời gian (s)", f"{result['time']:.4f}")
        third_col.metric("Chi phí tốt nhất", f"{st.session_state.best_cost:.4f}")

        st.markdown("---")
        plot_col, detail_col = st.columns([2.5, 1])

        with plot_col:
            if algorithm == "ba":
                left_plot, right_plot = st.columns([1, 1])
                with left_plot:
                    st.markdown("### Trực quan hóa")
                    st.pyplot(plot_route_figure(coords, result["path"]))
                with right_plot:
                    st.markdown("### Biểu đồ hội tụ")
                    history = result.get("history", [])
                    if history:
                        st.pyplot(plot_convergence_figure(history))
                    else:
                        st.info("Không có dữ liệu hội tụ để hiển thị.")
            else:
                st.markdown("### Trực quan hóa")
                st.pyplot(plot_route_figure(coords, result["path"]))

        with detail_col:
            st.markdown("### Lần chạy này")
            st.write(f"**Thuật toán:** {algorithm_choice}")
            st.write(f"**Số điểm:** {n}")
            st.write(f"**Chi phí:** {result['cost']:.4f}")
            st.write(f"**Thời gian:** {result['time']:.4f} s")
            st.write("---")
            st.write("**Đường đi**")
            st.write(result["path"])
    else:
        st.info("Chọn cấu hình và nhấn 'Chạy thuật toán' để bắt đầu.")


if __name__ == "__main__":
    main()
