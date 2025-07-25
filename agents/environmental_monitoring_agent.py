from adk_local import RuntimeContext
from adk_local import Agent  # optionally alias Agent if needed

from datetime import datetime

class EnvironmentalMonitoringAgent(Agent):
    def __init__(self):
        super().__init__(
            name="EnvironmentalMonitoringAgent",
            description="Monitors environmental data and checks for safety threshold violations.",
            model="gemini-2.0-pro"
        )

        # Define thresholds for alerting
        self.thresholds = {
            "PM2.5": 35,       # μg/m³ (above this is unsafe)
            "noise_dB": 85,    # dB (above this is harmful for hearing)
            "CO_ppm": 50,      # Carbon Monoxide in ppm
            "temperature_C": 45,
            "humidity_%": 90
        }

    async def run(self, context: RuntimeContext) -> None:
        task = context.task
        sensor_data = task.get("sensor_data", {})

        # Required parameters for robust monitoring
        required_params = list(self.thresholds.keys())
        missing_params = [p for p in required_params if p not in sensor_data]
        faulty_params = [p for p, v in sensor_data.items() if not isinstance(v, (int, float)) or v is None or (isinstance(v, (int, float)) and (v < 0 or v > 10000))]

        if not sensor_data:
            context.complete({
                "status": "failed",
                "reason": "No sensor data provided."
            })
            return

        # Parameter-by-parameter breakdown
        breakdown = []
        violations = []
        recommendations = []
        pre_warnings = []
        for param in required_params:
            value = sensor_data.get(param)
            threshold = self.thresholds[param]
            status = "OK"
            recs = []
            if value is None:
                status = "missing"
                recs.append(f"Provide {param} sensor data.")
            elif not isinstance(value, (int, float)) or value < 0 or value > 10000:
                status = "faulty"
                recs.append(f"Check {param} sensor for faulty or out-of-range value: {value}")
            elif value > threshold:
                status = "violation"
                violations.append(f"{param} = {value} exceeds threshold of {threshold}")
                recs.append(self.recommend_action(param, value))
            elif value > 0.9 * threshold:
                status = "pre-warning"
                pre_warnings.append(f"{param} = {value} is close to threshold ({threshold})")
                recs.append(f"Monitor {param} closely; value is approaching unsafe limit.")
            breakdown.append({
                "parameter": param,
                "value": value,
                "threshold": threshold,
                "status": status,
                "recommendations": recs
            })
            recommendations.extend(recs)

        # Check for extra/unexpected parameters
        extra_params = [p for p in sensor_data if p not in required_params]
        if extra_params:
            recommendations.append(f"Unexpected parameters reported: {extra_params}. Check configuration.")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = {
            "timestamp": timestamp,
            "sensor_data": sensor_data,
            "breakdown": breakdown,
            "violations": violations,
            "pre_warnings": pre_warnings,
            "missing_params": missing_params,
            "faulty_params": faulty_params,
            "extra_params": extra_params,
            "recommendations": list(set(recommendations)),
            "compliant": len(violations) == 0 and not missing_params and not faulty_params
        }
        report["rules_summary"] = self.rules_summary()

        if violations or missing_params or faulty_params:
            context.logger.warning(f"🚨 Environmental issues detected: Violations: {violations}, Missing: {missing_params}, Faulty: {faulty_params}")
        elif pre_warnings:
            context.logger.info(f"⚠️ Pre-warning: {pre_warnings}")
        else:
            context.logger.info("✅ All environmental parameters are within safe limits.")

        context.complete({
            "status": "success",
            "report": report
        })

    def recommend_action(self, param, value):
        # Actionable recommendations for each parameter
        actions = {
            "PM2.5": "Increase ventilation, reduce dust sources, or evacuate area if persistent.",
            "noise_dB": "Provide hearing protection, reduce noise at source, or limit exposure time.",
            "CO_ppm": "Evacuate area, increase ventilation, and check for CO sources/leaks.",
            "temperature_C": "Provide cooling, hydration, and limit exposure to high temperatures.",
            "humidity_%": "Use dehumidifiers or increase ventilation to reduce humidity."
        }
        return actions.get(param, f"Take action to reduce {param}.")

    @staticmethod
    def rules_summary():
        return [
            "Checks for missing, faulty, or extra sensor data.",
            "Flags values exceeding or close to safety thresholds.",
            "Provides actionable recommendations for each violation.",
            "Reports parameter-by-parameter breakdown (value, threshold, status, recommendations).",
            "Warns if required parameters are missing or faulty.",
            "Flags unexpected parameters in the input."
        ]

# Support for ADK CLI
async def run_with_adk(task: dict) -> dict:
    agent = EnvironmentalMonitoringAgent()
    return await agent.run_with_adk(task)

def get_agent():
    return EnvironmentalMonitoringAgent()
