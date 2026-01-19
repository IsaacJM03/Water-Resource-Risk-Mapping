def generate_summary(risk, primary, trend):
    base = f"Risk is {risk:.1f}%, driven mainly by {primary}."

    if trend == "rising":
        base += " The situation is worsening over time."
    elif trend == "falling":
        base += " Conditions are improving gradually."
    else:
        base += " The situation is stable."

    return base
