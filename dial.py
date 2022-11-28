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
st.text("Source: 7 Powers - Hamilton Helmer")
st.latex(
    r"""
V = M_0 \space g \space \bar{s} \space \bar{m}
"""
)
st.text("Where g is the terminal value factor (1+g)/(r-g)")
col_left, col_right = st.columns(2)
col_left.subheader("Inputs to Market Scale")
col_right.subheader("Inputs to Power")

m0 = col_left.number_input("Current Market Size (bn USD)", min_value=0.0, value=400.0)
coc = col_left.slider("Cost of capital", min_value=0.0, max_value=100.0, value=20.0)
eta = col_left.slider(
    "Long-term revenue growth", min_value=0.0, max_value=coc, value=5.0
)
g = (1 + eta / 100.0) / (coc / 100.0 - eta / 100.0)
# g = col_right.slider("Discounted growth factor", min_value=0.0, value=10.0)

s = col_right.slider(
    "Long-term Market Share", min_value=0.0, max_value=100.0, value=30.0
)
m = col_right.slider(
    "Long-term Net Profit Margin > Cost of Capital",
    min_value=0.0,
    max_value=20.0,
    value=10.0,
)

col_left2, col_right2 = st.columns(2)
col_left2.subheader("Market Scale")
col_left2.metric(
    "Contribution to market scale growth over inf",
    value=human_format(m0 * 1_000_000_000.0 * g),
)
col_right2.subheader("Power")
col_right2.metric(
    "Long-term market extractive power", value="{:.1%}".format(s / 100 * m / 100)
)


val = m0 * 1_000_000_000.0 * g * s / 100 * m / 100
s1, s2, s3 = st.columns(3)
s2.subheader("Value")
s2.metric(label="Long-term value accretion potential", value=human_format(val))
