from fastapi import FastAPI
from business_agent import app as business_agent

app = FastAPI(
    title="Business Analytics Agent",
    description="یک عامل هوش مصنوعی برای تحلیل داده‌های کسب‌وکار"
)

@app.post("/analyze")
async def analyze_business_data(data: dict):
    """Analyze business data and return insights"""
    result = business_agent.invoke({"business_data": data})
    return {
        "status": "success",
        "data": result
    }

#For local execution
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)