import streamlit as st


def human_format(num):
    num = float("{:.3g}".format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return "{}{}".format(
        "{:,.2f}".format(num).rstrip("0").rstrip("."),
        ["", "k", "m", "bn", "tn"][magnitude],
    )


st.title("Dial Manipulatoor")
tit1, tit2 = st.columns(2)
tit1.subheader("Market Scale")
tit2.subheader("Power")

set1, set2 = st.columns(2)
m0 = set1.number_input("Current Market Size (bn USD)", min_value=0.0, value=400.0)
g = set2.slider("Discounted growth factor", min_value=0.0, value=10.0)

set3, set4 = st.columns(2)
s = set3.slider("Long-term Market Share", min_value=0.0, max_value=100.0, value=30.0)
m = set4.slider(
    "Long-term Net Profit Margin > Cost of Capital",
    min_value=0.0,
    max_value=20.0,
    value=10.0,
)

val = m0 * 1_000_000_000.0 * g * s / 100 * m / 100
s1, s2, s3 = st.columns(3)
s2.latex(
    r"""
V = M_0 \space g \space \bar{s} \space \bar{m}
"""
)
s2.metric(label="Value", value=human_format(val))
