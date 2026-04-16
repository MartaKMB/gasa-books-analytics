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

    fig, axs = plt.subplots(2,2, figsize=(12,7))

    axs[0, 0].bar(top["shorttitle"], top["units_sum"])
    axs[0, 0].set_title(f"Top {n_top} sold books")
    axs[0, 0].set_xlabel("book title")
    axs[0, 0].set_ylabel("units")
    axs[0, 0].tick_params(axis="x", rotation=45)
    axs[0, 0].grid(axis="y", alpha=0.3)

    axs[0, 1].bar(df_by_region["region"], df_by_region["units_sum"])
    axs[0, 1].set_title(f"Sales by region")
    axs[0, 1].set_xlabel("country")
    axs[0, 1].set_ylabel("units")
    axs[0, 1].grid(axis="y", alpha=0.3)

    axs[1, 0].plot(df_by_month["month"], df_by_month["units_sum"], marker="o")
    axs[1, 0].set_title(f"Sales by month")
    axs[1, 0].set_xlabel("month")
    axs[1, 0].set_ylabel("units")
    axs[1, 0].grid(axis="y", alpha=0.3)

    axs[1, 1].axis("off")

    lines = [
        "KEY METRICS",
        "-----------",
        f"Total units: {kpis.get("total_units", 0):,}",
        f"Products: {kpis.get("distinct_products", 0)}",
        f"Regions: {kpis.get("distinct_regions", 0)}",
    ]
    text_block = "\n".join(lines)

    axs[1, 1].text(
        0.02, 0.98, text_block,
        va="top", ha="left",
        fontsize=11, family="Monospace"
    )

    fig.suptitle("GaSa books sales dashboard", fontsize=14, y=0.98)
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)

    out_path = os.path.join(out_dir, filename)

    plt.savefig(out_path, dpi=150)

    plt.close(fig)

    print("VIZ:", df_by_quarter)
    return out_path

