import os
import matplotlib.pyplot as plt


def plot_kpis(ax, kpis: dict):
    ax.axis("off")

    kpi_lines = [
        "KEY METRICS",
        "-----------",
        f"Total units: {kpis.get('total_units', 0):,}",
        f"Products: {kpis.get('distinct_products', 0)}",
        f"Regions: {kpis.get('distinct_regions', 0)}",
        "-----------",
        f"JDG active months: {kpis.get('active_months', 0)}",
        f"JDG suspended months: {kpis.get('suspended_months', 0)}",
        f"Amazon active months: {kpis.get('amazon_active_months', 0)}",
        f"Amazon coverage: {kpis.get('amazon_coverage', 0):.2%}",
        "-----------",
        f"Cannibalization impact: {kpis.get("cannibalization_pct"):.1%} ",
        f"({kpis.get('cannibalization_impact')})"
    ]

    ax.text(
        0.02, 0.98,
        "\n".join(kpi_lines),
        va="top",
        ha="left",
        fontsize=10,
        family="Monospace"
    )

def plot_top_products(ax, df, n_top):
    top = df.nlargest(n_top, "total_units")

    ax.bar(top["book"], top["total_units"])
    ax.set_title("Top products")
    ax.set_ylabel("units")


def plot_region(ax, df):
    ax.bar(df["region"], df["total_units"])
    ax.set_title("Region")


def plot_monthly(ax, df):
    ax.plot(df["month"], df["units"], marker="o", label="Monthly units")

    if "rolling_units" in df.columns:
        ax.plot(df["month"], df["rolling_units"], label="3M rolling avg")

    ax.set_title("Monthly sales")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)


def plot_seasonality(ax, df):
    ax.bar(df["quarter"], df["avg_units"])
    ax.set_title("Seasonality")


def plot_channel(ax, df):

    ax.plot(df["month"], df["units"], label="Units")
    ax.plot(df["month"], df["rolling_3m"], label="Trend (3M avg)")

    # zaznaczenie okresów zawieszenia JDG
    for i in range(len(df)):
        if df.iloc[i]["own_channel_active"] == 0:
            ax.axvspan(
                df.iloc[i]["month"],
                df.iloc[i]["month"],
                alpha=0.2
            )

    ax.set_title("Sales trend with JDG status")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

def plot_channel_bar(ax, df):

    grouped = df.groupby("own_channel_active")["units"].mean()

    ax.bar(
        ["Active", "Suspended"],
        [grouped.get(1, 0), grouped.get(0, 0)]
    )

    ax.set_title("Avg sales: JDG active vs suspended")


def save_dashboard(
    df_by_product,
    df_by_region,
    df_by_month,
    df_own_impact,
    df_seasonality,
    kpis,
    n_top,
    out_dir,
    filename
):

    fig, axs = plt.subplots(2, 3, figsize=(12, 6))

    plot_kpis(axs[0, 0], kpis)
    plot_top_products(axs[0, 1], df_by_product, n_top)
    plot_region(axs[0, 2], df_by_region)

    plot_monthly(axs[1, 0], df_by_month)
    plot_seasonality(axs[1, 1], df_seasonality)
    plot_channel_bar(axs[1, 2], df_own_impact)

    plt.tight_layout()

    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, filename)

    plt.savefig(path)
    plt.close()

    return path
