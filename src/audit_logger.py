import json
import os
from datetime import datetime

class AuditLogger:
    def __init__(self, log_dir="data/audit_logs"):
        self.log_dir = log_dir
        self.log_file = os.path.join(log_dir, "audit_trail.json")
        
        # Ensure directory exists
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def log_event(self, event_type, filename, risk_score, status="Success", metadata=None):
        """
        Logs a user action or system event.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,  # e.g., "CONTRACT_ANALYSIS", "TEMPLATE_GENERATION"
            "filename": filename,
            "risk_score": risk_score,
            "status": status,
            "metadata": metadata or {}
        }

        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                json.dump(entry, f)
                f.write("\n") # Newline delimited JSON for easy appending
        except Exception as e:
            print(f"Failed to write audit log: {e}")

    def get_logs(self):
        """
        Reads logs for the dashboard (optional).
        """
        logs = []
        if os.path.exists(self.log_file):
            with open(self.log_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        logs.append(json.loads(line))
                    except:
                        continue
        return logs