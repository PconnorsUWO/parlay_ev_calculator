import streamlit as st 
from parlay_value.calculations import (
    moneyline_to_decimal,
    calculate_parlay_probability,
    calculate_ev_of_parlay,
    kelly_fraction,
    american_to_probability,
)

def reset_all():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

def main():
    st.title("Parlay Bet Calculator")
    st.markdown("Insert your bets/legs and the offered parlay odds to dynamically see the metrics.")

    with st.sidebar:
        st.header("Bet Input Options")

        if st.button("Reset Bet"):
            reset_all()

        odds_format = st.radio("Select Offered Parlay Odds Format", ("American", "Decimal"))

        if odds_format == "American":
            offered_odds_input = st.number_input(
                "Offered Parlay Moneyline Odds (American)", value=2236, step=1, key="offered_ml"
            )
            offered_ml = offered_odds_input
            dec_odds = moneyline_to_decimal(offered_ml)
        else:
            offered_odds_input = st.number_input(
                "Offered Parlay Decimal Odds", value=23.36, step=0.01, key="offered_dec"
            )
            dec_odds = offered_odds_input

            def decimal_to_moneyline(dec):
                if dec >= 2:
                    return (dec - 1) * 100
                elif dec > 1:
                    return -100 / (dec - 1)
                else:
                    return 0

            offered_ml = decimal_to_moneyline(dec_odds)

        st.markdown("### Enter Bets (Legs)")
        num_legs = st.number_input("Number of Legs", value=2, min_value=1, step=1, key="num_legs")

        legs = []
        for i in range(int(num_legs)):
            st.markdown(f"**Leg {i+1}**")
            leg_ml = st.number_input(
                f"American Odds for Leg {i+1}",
                value=100,
                step=1,
                key=f"leg_{i}"
            )
            leg_prob = american_to_probability(leg_ml)
            st.write(f"Implied Fair Probability for Leg {i+1}: {leg_prob:.2%}")
            legs.append(leg_prob)


    parlay_prob = calculate_parlay_probability(legs)
    market_prob = 1 / dec_odds if dec_odds > 0 else 0

    ev = calculate_ev_of_parlay(parlay_prob, offered_ml)

    full_kelly = kelly_fraction(dec_odds, parlay_prob)
    quarter_kelly = full_kelly / 4

    st.markdown("## Calculated Metrics")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Odds Format for Parlay", odds_format)
        st.metric("Number of Legs", int(num_legs))
    with col2:
        st.metric("Combined Fair (Parlay) Probability", f"{parlay_prob:.2%}")
        st.metric("Market Implied Probability", f"{market_prob:.2%}")
    with col3:
        st.metric("Offered Decimal Odds", f"{dec_odds:.2f}")
        st.metric("Effective Value (EV per unit stake)", f"{ev:.2f}")

    col_kelly1, col_kelly2 = st.columns(2)
    with col_kelly1:
        st.metric("Full Kelly Fraction", f"{full_kelly:.2%} of bankroll")
    with col_kelly2:
        st.metric("Quarter Kelly Fraction", f"{quarter_kelly:.2%} of bankroll")

if __name__ == "__main__":
    main()
