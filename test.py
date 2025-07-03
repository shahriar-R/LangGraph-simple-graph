import unittest
from agents.business_agent import app as business_agent

class TestBusinessAgent(unittest.TestCase):
    def setUp(self):
        # Sample test data
        self.valid_data = {
            "revenue": 12000,
            "cost": 8000,
            "customers": 100,
            "previous_revenue": 10000,
            "previous_cost": 7000,
            "previous_customers": 90
        }
        
        self.negative_profit_data = {
            "revenue": 5000,
            "cost": 6000,
            "customers": 50,
            "previous_revenue": 4000,
            "previous_cost": 3000,
            "previous_customers": 40
        }

    def test_profit_calculation(self):
        """Test correct profit calculation"""
        result = business_agent.invoke({"business_data": self.valid_data})
        self.assertEqual(
            result["metrics"]["profit"],
            self.valid_data["revenue"] - self.valid_data["cost"]
        )

    def test_negative_profit_alert(self):
        """Test alert generation for negative profit"""
        result = business_agent.invoke({"business_data": self.negative_profit_data})
        alerts = [a["message"] for a in result["alerts"]]
        self.assertTrue(any("Negative profit" in alert for alert in alerts))

    def test_revenue_change_calculation(self):
        """Test revenue change percentage calculation"""
        result = business_agent.invoke({"business_data": self.valid_data})
        expected_change = (self.valid_data["revenue"] - self.valid_data["previous_revenue"]) / self.valid_data["previous_revenue"] * 100
        self.assertAlmostEqual(
            result["metrics"]["revenue_change"],
            expected_change,
            places=2
        )

    def test_output_structure(self):
        """Test output contains all required fields"""
        result = business_agent.invoke({"business_data": self.valid_data})
        self.assertIn("metrics", result)
        self.assertIn("alerts", result)
        self.assertIn("recommendations", result)
        self.assertIsInstance(result["recommendations"], list)

    def test_cac_calculation(self):
        """Test Customer Acquisition Cost calculation"""
        result = business_agent.invoke({"business_data": self.valid_data})
        expected_cac = self.valid_data["cost"] / self.valid_data["customers"]
        self.assertEqual(result["metrics"]["cac"], expected_cac)

if __name__ == "__main__":
    unittest.main()