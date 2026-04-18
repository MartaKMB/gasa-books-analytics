"""
visualizer builds PNG dashboard (modular version)
"""

import os
import matplotlib.pyplot as plt

# KPI BLOCK
def plot_kpis(ax, kpis: dict):
    ax.axis("off")

    kpi_lines = [
        "KEY METRICS",
        "-----------",
        f"Total units: {kpis.get('total_units', 0):,}",
        f"Products: {kpis.get('distinct_products', 0)}",
        f"Regions: {kpis.get('distinct_regions', 0)}",
        f"JDG active months: {kpis.get('active_months', 0)}",
        f"JDG suspended months: {kpis.get('suspended_months', 0)}",
        f"Amazon coverage: {kpis.get('amazon_coverage', 0):.2%}",

        # FIXED KEY
        f"Cannibalization impact: {kpis.get('cannibalization_impact', 0):.2%}"
    ]

    ax.text(
        0.02, 0.98,
        "\n".join(kpi_lines),
        va="top",
        ha="left",
        fontsize=11,
        family="Monospace"
    )

# TOP PRODUCTS
def plot_top_products(ax, df_by_product, n_top: int):
    top = df_by_product.nlargest(n_top, "total_units")

    ax.bar(top["book"], top["total_units"])
    ax.set_title(f"Top {n_top} sold books")
    ax.set_ylabel("units")
    ax.grid(axis="y", alpha=0.3)

# REGION
def plot_region(ax, df_by_region):
    ax.bar(df_by_region["region"], df_by_region["total_units"])

    ax.set_title("Sales by region")
    ax.set_xlabel("country")
    ax.set_ylabel("units")
    ax.grid(axis="y", alpha=0.3)

# MONTHLY TREND
def plot_monthly(ax, df_by_month):
    ax.plot(df_by_month["month"], df_by_month["total_units"], marker="o")

    ax.set_title("Sales by month")
    ax.set_xlabel("month")
    ax.set_ylabel("units")
    ax.tick_params(axis="x", rotation=90)
    ax.grid(axis="y", alpha=0.3)

# SEASONALITY
def plot_seasonality(ax, df_seasonality):
    """
    FIX: seasonal view is now pure Amazon aggregation:
    quarter -> avg_units (no JDG split anymore)
    """

    df = df_seasonality.copy()

    # ensure correct order
    df = df.sort_values("quarter")

    ax.bar(
        df["quarter"],
        df["avg_units"]
    )

    ax.set_xticks([1, 2, 3, 4])
    ax.set_xlabel("Quarter")
    ax.set_title("Amazon sales seasonality (by quarter)")
    ax.set_ylabel("Average units")
    ax.grid(axis="y", alpha=0.3)

# CHANNEL IMPACT
def plot_channel_impact(ax, df_own_impact):
    ax.bar(df_own_impact["channel_status"], df_own_impact["total_units"])

    ax.set_title("JDG status vs sales on Amazon")
    ax.set_xlabel("channel status")
    ax.set_ylabel("units")
    ax.grid(axis="y", alpha=0.3)


# ======================
# MAIN DASHBOARD
# ======================
def save_dashboard(
    df_by_product,
    df_by_region,
    df_by_month,
    df_own_impact,
    df_seasonality,
    kpis: dict,
    n_top: int = 3,
    out_dir: str = "reports/figures",
    filename: str = "dashboard.png"
):
    fig, axs = plt.subplots(2, 3, figsize=(12, 7))

    # Row 1
    plot_kpis(axs[0, 0], kpis)
    plot_top_products(axs[0, 1], df_by_product, n_top)
    plot_region(axs[0, 2], df_by_region)

    # Row 2
    plot_monthly(axs[1, 0], df_by_month)
    plot_seasonality(axs[1, 1], df_seasonality)
    plot_channel_impact(axs[1, 2], df_own_impact)

    fig.suptitle("GaSa books sales dashboard", fontsize=14, y=0.98)

    plt.tight_layout()
    plt.subplots_adjust(top=0.92)

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)

    plt.savefig(out_path, dpi=150)
    plt.close(fig)

    return out_path
