"""
Permission Policy Engine for AI Company.
Enforces risk classification:
- LOW RISK: Automatic execution (reading files, plans, local unit tests, documentation)
- MEDIUM RISK: Configurable (installing dependencies, modifying source files)
- HIGH RISK: Requires Owner Approval (production deployment, external messaging, financial actions, destructive ops)
"""
from typing import Tuple

class RiskLevel:
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class PermissionPolicy:
    def __init__(self, medium_risk_auto_approve: bool = True):
        self.medium_risk_auto_approve = medium_risk_auto_approve

    def evaluate_action(self, agent: str, action: str, details: str = "") -> Tuple[str, bool, str]:
        """
        Returns (risk_level, requires_approval, reason)
        """
        action_lower = action.lower()
        
        # High Risk operations ALWAYS require owner approval by default
        if any(w in action_lower for w in [
            "deploy production", "production deployment", "deploy_production",
            "send external message", "send email", "financial", "payment",
            "delete database", "drop table", "remove workspace", "destructive"
        ]):
            return (RiskLevel.HIGH, True, "Operation affects production systems or external stakeholders.")

        # Medium Risk operations
        if any(w in action_lower for w in [
            "modify source code", "write file", "edit file", "install dependency", "run local service"
        ]):
            req_approval = not self.medium_risk_auto_approve
            return (RiskLevel.MEDIUM, req_approval, "Modifies project workspace files or environment.")

        # Low Risk operations (Automatic)
        return (RiskLevel.LOW, False, "Safe read-only or analysis operation within project boundary.")
