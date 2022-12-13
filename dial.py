import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


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
st.markdown("Source: 7 Powers - Hamilton Helmer")
st.subheader("Fundamental Market Power Equation")
with st.expander("Fundamental Market Power Equation"):
    st.latex(
        r"""
    V = M_0 \space g \space \bar{s} \space \bar{m}
    """
    )
    st.markdown("Where g is the terminal value growth factor (1+g)/(r-g)")
    col_left, col_right = st.columns(2)
    col_left.subheader("Inputs to Market Scale")
    col_right.subheader("Inputs to Power")

    m0 = col_left.number_input(
        "Current Market Size (bn USD)", min_value=0.0, value=400.0
    )
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

st.subheader("2. Network economies")
with st.expander("2. Network economies"):
    st.latex(
        r"""
    SLM = 1-1/[\frac{\delta}{c}(N_s-N_w)+1]
    """
    )
    st.markdown(
        "Where SLM is the surplus leader margin [%]. Ns and Nm are the user bases of the leader and follower [Q]. Delta is the marginal benefit to all users from one more joiner. c is the variable cost per unit [$/Q]."
    )
    st.markdown(
        "Delta is the increase in value per user (+$/Q) for each new user (1/Q). This formulation only works with pure variable costs."
    )

    vc = st.slider(
        "c: $ variable cost per each unit", min_value=0.01, max_value=100.0, value=50.0
    )
    delta = st.slider(
        "δ: $ Value per user increase for each new user",
        min_value=0.01,
        max_value=10.0,
        value=0.01,
    )
    lowshare = st.number_input(
        "Lowest possible share of underdog in a two player market",
        min_value=0.01,
        max_value=0.49,
        value=0.01,
    )
    hishare = st.number_input(
        "Highest possible share of underdog in a two player market",
        min_value=lowshare,
        max_value=0.50,
        value=0.50,
    )
    nw = st.number_input(
        "Nw: Quantity of users in underdog", min_value=0.0, value=100.0
    )

    df = pd.DataFrame({"nw": np.repeat(nw, 1000)})
    share = np.arange(lowshare, hishare, (hishare - lowshare) / (df.shape[0]))
    df["ns"] = df["nw"] / share - df["nw"]
    df["diff"] = df["ns"] - df["nw"]
    df["slm"] = 1 - 1 / (((delta / vc) * df["diff"]) + 1)

    network1 = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X(
                "diff",
                axis=alt.Axis(
                    title="Difference between incumbent and challenger in absolute users (lin)"
                ),
            ),
            y=alt.Y(
                "slm", axis=alt.Axis(format="%", title="Surplus Leader Margin (%)")
            ),
        )
    )

    network2 = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X(
                "diff",
                scale=alt.Scale(type="log"),
                axis=alt.Axis(
                    title="Difference between incumbent and challenger in absolute users (log)"
                ),
            ),
            y=alt.Y(
                "slm", axis=alt.Axis(format="%", title="Surplus Leader Margin (%)")
            ),
        )
    )
    st.altair_chart(network1, use_container_width=True)
    st.altair_chart(network2, use_container_width=True)

st.subheader("5. Branding")
with st.expander("5. Branding"):
    st.latex(
        r"""
        B(t)=\frac{Z}{(1+(z-1)e^{-Ft}}*D_t*U_t
        """
    )
    st.markdown(
        "Branding multiple for the price of a product over another, dynamically over time. Z: Maximum potential pricing multiple for a specific good Z>2. F: brand cycle time compression factor F>0. Brand dilution function over time t 0<D<1. Brand underinvestment at time t 0<U<1"
    )
    st.latex(
        r"""
        SLM = 1 - \frac{1}{B(t)}
        """
    )
    st.markdown(
        "The SLM is expressed as a function of the price premium extractable from brand value."
    )

    mul = st.slider(
        "Z: Maximum potential branding multiple for a specific good",
        min_value=2.0,
        max_value=10.0,
        value=2.0,
    )
    compr = st.slider(
        "F: Brand cycle compression time (slope of the logistic function)",
        min_value=0.0,
        max_value=5.0,
        value=1.0,
    )
    dilut = st.slider(
        "D: Brand dilution function over time (assumed constant for simplicity, 1=no dilution)",
        min_value=0.0,
        max_value=1.0,
        value=1.0,
    )
    under = st.slider(
        "U: Brand underinvestment function over time (assumed constant for simplicity, 1=no underinvestment)",
        min_value=0.0,
        max_value=1.0,
        value=1.0,
    )

    dfb = pd.DataFrame({"t": np.arange(0.0, 10, 0.1)})
    dfb["b_t"] = (mul / (1 + (mul - 1) * np.exp(-compr * dfb["t"]))) * dilut * under
    dfb["slm"] = 1 - 1 / dfb["b_t"]

    brand1 = (
        alt.Chart(dfb)
        .mark_line()
        .encode(
            x=alt.X(
                "t",
                axis=alt.Axis(title="Arbitrary time period t"),
            ),
            y=alt.Y("b_t", axis=alt.Axis(title="Branding Price Multiplier")),
        )
    )

    brand2 = (
        alt.Chart(dfb)
        .mark_line()
        .encode(
            x=alt.X(
                "t",
                axis=alt.Axis(title="Arbitrary time period t"),
            ),
            y=alt.Y(
                "slm", axis=alt.Axis(format="%", title="Surplus Leader Margin (%)")
            ),
        )
    )

    st.altair_chart(brand1, use_container_width=True)
    st.altair_chart(brand2, use_container_width=True)
