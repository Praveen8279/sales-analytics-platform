import plotly.express as px


# ------------------------------------------
# Line Chart
# ------------------------------------------

def create_line_chart(
    df,
    x,
    y,
    title,
    color="#1F77B4"
):
    fig = px.line(
        df,
        x=x,
        y=y,
        title=title,
        markers=True
    )

    fig.update_traces(
        line=dict(color=color, width=3)
    )

    fig.update_layout(
        template="plotly_white",
        height=450
    )

    return fig


# ------------------------------------------
# Bar Chart
# ------------------------------------------

def create_bar_chart(
    df,
    x,
    y,
    title,
    color="#1F77B4"
):
    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        color_discrete_sequence=[color]
    )

    fig.update_layout(
        template="plotly_white",
        height=450
    )

    return fig


# ------------------------------------------
# Horizontal Bar Chart
# ------------------------------------------

def create_horizontal_bar_chart(
    df,
    x,
    y,
    title,
    color="#2CA02C"
):
    fig = px.bar(
        df,
        x=x,
        y=y,
        orientation="h",
        title=title,
        color_discrete_sequence=[color]
    )

    fig.update_layout(
        template="plotly_white",
        height=500
    )

    return fig


# ------------------------------------------
# Pie Chart
# ------------------------------------------

def create_pie_chart(
    df,
    names,
    values,
    title
):
    fig = px.pie(
        df,
        names=names,
        values=values,
        title=title,
        hole=0.45
    )

    fig.update_layout(
        template="plotly_white",
        height=450
    )

    return fig