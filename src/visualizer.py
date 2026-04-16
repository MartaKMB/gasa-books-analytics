"""
visualizer build single PNG dashboard
"""

import os
import matplotlib.pyplot as plt

def save_dashboard(
    df_by_product,
    df_by_region,
    df_by_month,
    df_by_quarter,
    kpis: dict,
    n_top: int = 3,
    out_dir: str = "reports/figures",
    filename: str = "dashboard.png"
):
    top = df_by_product.nlargest(n_top, "units_sum").copy()

    fig, axs = plt.subplots(2, 3, figsize=(12,7))

    axs[0, 0].axis("off")

    kpi_lines = [
        "KEY METRICS",
        "-----------",
        f"Total units: {kpis.get("total_units", 0):,}",
        f"Products: {kpis.get("distinct_products", 0)}",
        f"Regions: {kpis.get("distinct_regions", 0)}",
    ]
    kpi_text_block = "\n".join(kpi_lines)

    axs[0, 0].text(
        0.02, 0.98, kpi_text_block,
        va="top", ha="left",
        fontsize=11, family="Monospace"
    )



    

    # axs[1, 0].text(0.02, 0.98, "This dashboard analyzes Amazon book sales data from my seller account, showing key KPIs, top-performing titles, regional performance, and time-based trends. A clear seasonal pattern emerges, with the strongest sales occurring in Q1 and Q4, indicating increased demand during these periods.")
    axs[1, 0].axis("off")

    report_lines = [
        "Amazon books sales dashboard",
        "showing key performance metrics,",
        "top-selling products,",
        "regional distribution,",
        "and sales seasonality ",
        "across months and quarters",
        "based on internal sales data.",
    ]
    report_text_block = "\n".join(report_lines)

    axs[1, 0].text(
        0.02, 0.98, report_text_block,
        va="top", ha="left",
        fontsize=9, family="Monospace"
    )



    axs[0, 1].bar(top["shorttitle"], top["units_sum"])
    axs[0, 1].set_title(f"Top {n_top} sold books")
    axs[0, 1].set_ylabel("units")
    axs[0, 1].tick_params(axis="x")
    axs[0, 1].grid(axis="y", alpha=0.3)

    axs[0, 2].bar(df_by_region["region"], df_by_region["units_sum"])
    axs[0, 2].set_title(f"Sales by region")
    axs[0, 2].set_xlabel("country")
    axs[0, 2].set_ylabel("units")
    axs[0, 2].grid(axis="y", alpha=0.3)

    axs[1, 1].bar(df_by_quarter["quarter"], df_by_quarter["units_sum"])
    axs[1, 1].set_title(f"Sales seasonality per quarter")
    axs[1, 1].set_xlabel("quarter")
    axs[1, 1].set_ylabel("units")
    axs[1, 1].grid(axis="y", alpha=0.3)

    axs[1, 2].plot(df_by_month["month"], df_by_month["units_sum"], marker="o")
    axs[1, 2].bar(df_by_month["month"], df_by_month["units_sum"])
    axs[1, 2].set_title(f"Sales by month")
    axs[1, 2].set_xlabel("month")
    axs[1, 2].set_ylabel("units")
    axs[1, 2].tick_params(axis="x", rotation=90)
    axs[1, 2].grid(axis="y", alpha=0.3)

    fig.suptitle("GaSa books sales dashboard", fontsize=14, y=0.98)
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)

    out_path = os.path.join(out_dir, filename)

    plt.savefig(out_path, dpi=150)

    plt.close(fig)

    print("by month:", df_by_month)
    return out_path

