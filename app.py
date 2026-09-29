import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from simulation import HospitalSimulation


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI-Assisted Hospital Capacity Simulation",
    page_icon="🏥",
    layout="wide"
)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.block-container {
    padding-top: 1.5rem;
}

[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #E5EAF2;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.04);
}

.simulation-box {
    padding: 20px;
    border-radius: 16px;
    background: linear-gradient(
        135deg,
        #edf6ff,
        #ffffff
    );
    border: 1px solid #d9e8f7;
}

.flow-box {
    text-align: center;
    padding: 18px;
    border-radius: 18px;
    color: white;
    font-weight: bold;
    font-size: 18px;
}

.arrival {
    background: #3b82f6;
}

.queue {
    background: #f4b942;
}

.doctor {
    background: #2db99c;
}

.finish {
    background: #9b51e0;
}

.ai-box {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    padding: 20px;
    border-radius: 14px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.title("🏥 AI-Assisted Hospital Capacity Simulation")

st.caption(
    "Simulasi Antrean Poli • Better Planning • Shorter Queue • Better Service"
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Parameter Simulasi")

    simulation_time = st.number_input(
        "Durasi Simulasi (menit)",
        min_value=60,
        max_value=1440,
        value=480,
        step=30
    )

    arrival_time = st.number_input(
        "Rata-rata Waktu Kedatangan (menit)",
        min_value=1.0,
        value=5.0,
        step=1.0
    )

    service_time = st.number_input(
        "Rata-rata Waktu Pelayanan (menit)",
        min_value=1.0,
        value=10.0,
        step=1.0
    )

    num_doctors = st.number_input(
        "Jumlah Dokter",
        min_value=1,
        max_value=20,
        value=2
    )

    st.divider()

    run_simulation = st.button(
        "▶ Mulai Simulasi",
        type="primary",
        use_container_width=True
    )

    st.subheader("Opsi Tambahan")

    animation = st.checkbox(
        "Tampilkan animasi pasien",
        value=True
    )

    automatic_report = st.checkbox(
        "Buat laporan otomatis"
    )

    fast_mode = st.checkbox(
        "Mode cepat (lebih ringan)"
    )


# =========================================================
# RUN SIMULATION
# =========================================================

if run_simulation:

    simulation = HospitalSimulation(
        simulation_time=simulation_time,
        arrival_time=arrival_time,
        service_time=service_time,
        num_doctors=num_doctors
    )

    df, metrics = simulation.run()

    st.session_state["df"] = df
    st.session_state["metrics"] = metrics


# =========================================================
# DISPLAY RESULTS
# =========================================================

if "df" in st.session_state:

    df = st.session_state["df"]
    metrics = st.session_state["metrics"]

    if df.empty:

        st.warning("Tidak ada pasien pada simulasi.")

    else:

        # =================================================
        # METRICS
        # =================================================

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "👥 Total Pasien",
                metrics["total_patients"]
            )

        with col2:
            st.metric(
                "⏱️ Rata-rata Waiting Time",
                f'{metrics["average_waiting"]:.2f} menit'
            )

        with col3:
            st.metric(
                "🩺 Utilization Dokter",
                f'{metrics["doctor_utilization"]:.1f}%'
            )

        with col4:
            st.metric(
                "✅ Pasien Selesai",
                metrics["completed"]
            )

        st.divider()


        # =================================================
        # PATIENT FLOW
        # =================================================

        st.subheader("🔄 Alur Simulasi")

        flow1, arrow1, flow2, arrow2, flow3, arrow3, flow4 = st.columns(
            [3, 1, 3, 1, 3, 1, 3]
        )

        with flow1:
            st.markdown(
                """
                <div class="flow-box arrival">
                📥 Arrival<br>
                Pasien Datang
                </div>
                """,
                unsafe_allow_html=True
            )

        with arrow1:
            st.markdown("## →")

        with flow2:
            st.markdown(
                """
                <div class="flow-box queue">
                ⏱ Queue<br>
                Antrean
                </div>
                """,
                unsafe_allow_html=True
            )

        with arrow2:
            st.markdown("## →")

        with flow3:
            st.markdown(
                """
                <div class="flow-box doctor">
                👨‍⚕️ Doctor<br>
                Pelayanan
                </div>
                """,
                unsafe_allow_html=True
            )

        with arrow3:
            st.markdown("## →")

        with flow4:
            st.markdown(
                """
                <div class="flow-box finish">
                ✓ Finish<br>
                Selesai
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")


        # =================================================
        # HOSPITAL VISUALIZATION
        # =================================================

        st.subheader("🏥 Visualisasi Poli")

        hospital1, hospital2, hospital3 = st.columns(3)

        with hospital1:

            st.info(
                f"""
                ### 🪑 Ruang Tunggu

                Pasien datang dan menunggu nomor antrean.

                **Total pasien:** {len(df)}
                """
            )

        with hospital2:

            st.success(
                f"""
                ### 🩺 Ruang Dokter

                Dokter aktif:

                **{num_doctors} dokter**
                """
            )

        with hospital3:

            st.success(
                f"""
                ### 🚪 Selesai

                Pasien telah menyelesaikan pelayanan.

                **{metrics["completed"]} pasien**
                """
            )


        st.divider()


        # =================================================
        # CHARTS
        # =================================================

        st.subheader("📊 Analytics")

        chart1, chart2 = st.columns(2)

        # Waiting time
        with chart1:

            fig_wait = px.bar(
                df,
                x="ID",
                y="Waiting Time",
                title="Waiting Time per Pasien",
                labels={
                    "ID": "ID Pasien",
                    "Waiting Time": "Waktu Tunggu (menit)"
                }
            )

            st.plotly_chart(
                fig_wait,
                use_container_width=True
            )


        # Service time
        with chart2:

            fig_service = px.histogram(
                df,
                x="Service Time",
                nbins=20,
                title="Distribusi Waktu Pelayanan",
                labels={
                    "Service Time":
                    "Waktu Pelayanan (menit)"
                }
            )

            st.plotly_chart(
                fig_service,
                use_container_width=True
            )


        # =================================================
        # TIMELINE
        # =================================================

        st.subheader("⏱ Timeline Pelayanan Pasien")

        timeline_df = df.copy()

        fig_timeline = go.Figure()

        for _, row in timeline_df.iterrows():

            # Waiting
            fig_timeline.add_trace(
                go.Bar(
                    x=[
                        row["Start Service"]
                        - row["Arrival"]
                    ],
                    y=[
                        f'Pasien {int(row["ID"])}'
                    ],
                    base=row["Arrival"],
                    orientation="h",
                    name="Menunggu",
                    legendgroup="waiting",
                    showlegend=False
                )
            )

            # Service
            fig_timeline.add_trace(
                go.Bar(
                    x=[
                        row["End Service"]
                        - row["Start Service"]
                    ],
                    y=[
                        f'Pasien {int(row["ID"])}'
                    ],
                    base=row["Start Service"],
                    orientation="h",
                    name="Pelayanan",
                    legendgroup="service",
                    showlegend=False
                )
            )

        fig_timeline.update_layout(
            title="Timeline Antrean dan Pelayanan",
            xaxis_title="Waktu Simulasi (menit)",
            yaxis_title="Pasien",
            barmode="overlay",
            height=max(
                500,
                len(df) * 25
            )
        )

        st.plotly_chart(
            fig_timeline,
            use_container_width=True
        )


        # =================================================
        # DATA TABLE
        # =================================================

        st.subheader("📋 Data Pasien (Real-time Simulation Result)")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


        # =================================================
        # AI INSIGHT
        # =================================================

        utilization = metrics["doctor_utilization"]
        waiting = metrics["average_waiting"]

        if utilization > 90:

            insight = (
                "Utilisasi dokter sangat tinggi. "
                "Pertimbangkan menambah dokter untuk "
                "mengurangi antrean."
            )

        elif utilization > 70:

            insight = (
                "Utilisasi dokter berada pada tingkat tinggi "
                "namun masih cukup terkendali."
            )

        elif utilization > 40:

            insight = (
                "Utilisasi dokter berada dalam rentang moderat "
                "dan kapasitas pelayanan relatif memadai."
            )

        else:

            insight = (
                "Utilisasi dokter relatif rendah. "
                "Kapasitas dokter mungkin lebih besar "
                "dibanding kebutuhan pasien."
            )

        if waiting > 15:

            insight += (
                " Rata-rata waktu tunggu cukup tinggi sehingga "
                "penyesuaian kapasitas pelayanan perlu dipertimbangkan."
            )

        st.markdown(
            f"""
            <div class="ai-box">

            <h3>💡 AI Insight</h3>

            {insight}

            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.info(
        "👈 Atur parameter simulasi pada sidebar kemudian "
        "tekan **Mulai Simulasi**."
    )