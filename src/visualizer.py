import os
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

plt.style.use("seaborn-v0_8-whitegrid")

def plot_kpis(ax, kpis: dict):
    ax.axis("off")

    kpi_lines = [
        "KEY METRICS",
        "-----------",
        f"Total units: {kpis.get('total_units', 0):,}",
        f"Products: {kpis.get('distinct_products', 0)}",
        f"Regions: {kpis.get('distinct_regions', 0)}",
        "-----------",
        f"JDG total months: {kpis.get('jdg_total_months', 0)}",
        f"Amazon total months: {kpis.get('amazon_observed_months', 0)}",
        f"Overlap (used in analysis): {kpis.get('overlap_months', 0)}",
        "-----------",
        f"JDG active months: {kpis.get('active_months', 0)}",
        f"JDG suspended months: {kpis.get('suspended_months', 0)}",
        f"Impact: {kpis.get('cannibalization_pct', 0):.2%}",
        f"({kpis.get('cannibalization_impact', '')})"
    ]

    ax.text(
        0.02, 0.98,
        "\n".join(kpi_lines),
        va="top",
        ha="left",
        fontsize=10,
        family="Monospace",
        color="white",
        bbox=dict(
            boxstyle="round,pad=1.0",
            facecolor="#1F77B4",
            edgecolor="#FF871E",
            linewidth=1.2
        )
    )

def plot_top_products(ax, df, n_top):
    top = df.nlargest(n_top, "total_units")

    ax.bar(top["book"], top["total_units"])
    ax.set_title("Top products")
    ax.set_ylabel("units")


def plot_region(ax, df):
    ax.bar(df["region"], df["total_units"])
    ax.set_title("Top regions")
    ax.set_ylabel("units")


def plot_monthly(ax, df):
    ax.plot(df["month"], df["units"], marker="o", label="Monthly units")

    if "rolling_units" in df.columns:
        ax.plot(df["month"], df["rolling_units"], label="Underlying trend") # Sales trend (3-month avg) / 3M rolling avg

    ax.set_title("Monthly sales")
    ax.set_ylabel("units")
    ax.legend()
    ax.tick_params(axis="x", rotation=90)
    ax.grid(axis="y", alpha=0.3)


def plot_seasonality(ax, df):
    ax.bar(df["quarter"], df["avg_share"])

    ax.set_title("Seasonality (quarter share of annual sales)")
    ax.set_ylabel("share (%)")
    ax.set_xlabel("quarters")

    ax.yaxis.set_major_formatter(PercentFormatter(1.0))

def plot_channel_bar(ax, df):
    grouped = df.groupby("own_channel_active")["units"].mean()

    ax.bar(
        ["Active", "Suspended"],
        [grouped.get(1, 0), grouped.get(0, 0)]
    )

    ax.set_title("Amazon avg sales vs JDG status")
    ax.set_ylabel("units")
    ax.set_xlabel("JDG activity")

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
    fig, axs = plt.subplots(2, 3, figsize=(12,7))

    plot_kpis(axs[0, 0], kpis)
    plot_top_products(axs[0, 1], df_by_product, n_top)
    plot_region(axs[0, 2], df_by_region)

    plot_monthly(axs[1, 0], df_by_month)
    plot_seasonality(axs[1, 1], df_seasonality)
    plot_channel_bar(axs[1, 2], df_own_impact)

    fig.suptitle("BOOKS SALES ON AMAZON", fontsize=14, y=0.98, fontweight="bold")
    plt.tight_layout(pad=3.0)
    plt.subplots_adjust(top=0.92)

    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, filename)

    plt.savefig(path, dpi=150)
    plt.close()

    return path
