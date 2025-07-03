from typing import TypedDict, Optional, Dict, Any, Annotated
from langgraph.graph import END, Graph
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.prebuilt import ToolNode
from enum import Enum


class State(TypedDict):
    business_data: dict
    metrics: Optional[Dict[str, float]]
    alerts: Optional[list]
    recommendations: Optional[list]


class Metrics(str, Enum):
    PROFIT = "profit"
    REVENUE_CHANGE = "revenue_change"
    COST_CHANGE = "cost_change"
    CAC = "cac"
    CAC_CHANGE = "cac_change"


def calculate_metrics(state: State) -> Dict[str, Any]:
    data = state["business_data"]
    metrics = {}

    # base calculate
    metrics[Metrics.PROFIT] = data["revenue"] - data["cost"]

    # calculate CAC
    metrics[Metrics.CAC] = (
        data["cost"] / data["customers"] if data["customers"] > 0 else 0
    )

    # Calculate the percentage of changes
    if "previous_revenue" in data and data["previous_revenue"] != 0:
        metrics[Metrics.REVENUE_CHANGE] = (
            (data["revenue"] - data["previous_revenue"])
            / data["previous_revenue"]
            * 100
        )

    if "previous_cost" in data and data["previous_cost"] != 0:
        metrics[Metrics.COST_CHANGE] = (
            (data["cost"] - data["previous_cost"]) / data["previous_cost"] * 100
        )

    if "previous_customers" in data and data["previous_customers"] != 0:
        previous_cac = data["previous_cost"] / data["previous_customers"]
        metrics[Metrics.CAC_CHANGE] = (
            (metrics[Metrics.CAC] - previous_cac) / previous_cac * 100
        )

    return {"metrics": metrics}


def generate_alerts(state: State) -> Dict[str, Any]:
    metrics = state["metrics"]
    alerts = []

    if metrics[Metrics.PROFIT] < 0:
        alerts.append({"type": "warning", "message": "A negative profit was recognized"})

    if Metrics.CAC_CHANGE in metrics and metrics[Metrics.CAC_CHANGE] > 20:
        alerts.append(
            {
                "type": "warning",
                "message": f"Customer acquisition costs have increased by.{metrics[Metrics.CAC_CHANGE]:.2f}% ",
            }
        )

    return {"alerts": alerts}


def generate_recommendations(state: State) -> Dict[str, Any]:
    metrics = state["metrics"]
    recommendations = []

    if metrics[Metrics.PROFIT] < 0:
        recommendations.append("Reduce operating costs")
    elif metrics[Metrics.PROFIT] > 0:
        recommendations.append("Reinvest profits to grow the business")

    if Metrics.REVENUE_CHANGE in metrics:
        if metrics[Metrics.REVENUE_CHANGE] > 10:
            recommendations.append("Increase the scalability of operations")
        elif metrics[Metrics.REVENUE_CHANGE] < -5:
            recommendations.append("Review sales strategies.")

    if Metrics.CAC_CHANGE in metrics:
        if metrics[Metrics.CAC_CHANGE] > 20:
            recommendations.append("Optimize marketing channels")
        elif metrics[Metrics.CAC_CHANGE] < -10:
            recommendations.append("Increase your marketing budget.")

    return {"recommendations": recommendations}


def prepare_final_output(state: State) -> Dict[str, Any]:
    return {
        "metrics": state["metrics"],
        "alerts": state["alerts"],
        "recommendations": state["recommendations"],
    }


# create graph
workflow = Graph()

# define nodes
workflow.add_node("calculate_metrics", calculate_metrics)
workflow.add_node("generate_alerts", generate_alerts)
workflow.add_node("generate_recommendations", generate_recommendations)
workflow.add_node("final_output", prepare_final_output)

# define edge
workflow.add_edge("calculate_metrics", "generate_alerts")
workflow.add_edge("calculate_metrics", "generate_recommendations")
workflow.add_edge("generate_alerts", "final_output")
workflow.add_edge("generate_recommendations", "final_output")
workflow.add_edge("final_output", END)


workflow.set_entry_point("calculate_metrics")


app = workflow.compile()
