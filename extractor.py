import json
import re
from datetime import date

def extract_structured_data(summary_text: str) -> dict:
    """Extract structured data from summary text without API call"""

    result = {
        "meeting_date": str(date.today()),
        "participants": [],
        "action_items": [],
        "key_decisions": [],
        "discussion_points": [],
        "overall_summary": ""
    }

    lines = summary_text.split("\n")
    current_section = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if "Meeting Summary" in line:
            current_section = "summary"
        elif "Action Items" in line:
            current_section = "actions"
        elif "Key Decisions" in line:
            current_section = "decisions"
        elif "Key Discussion" in line:
            current_section = "discussion"
        elif "Participants" in line:
            current_section = "participants"
        elif line.startswith("-") or line.startswith("•"):
            content = line.lstrip("-•").strip()
            if current_section == "participants":
                result["participants"].append(content)
            elif current_section == "decisions":
                result["key_decisions"].append(content)
            elif current_section == "discussion":
                result["discussion_points"].append(content)
            elif current_section == "actions":
                # Try to parse "Person: Task by Deadline"
                if ":" in content:
                    parts = content.split(":", 1)
                    owner = parts[0].strip()
                    task_part = parts[1].strip()
                    deadline = "Not specified"
                    if " by " in task_part.lower():
                        idx = task_part.lower().index(" by ")
                        deadline = task_part[idx+4:].strip()
                        task_part = task_part[:idx].strip()
                    result["action_items"].append({
                        "owner": owner,
                        "task": task_part,
                        "deadline": deadline
                    })
        elif current_section == "summary" and line and not line.startswith("#"):
            result["overall_summary"] += line + " "

    result["overall_summary"] = result["overall_summary"].strip()
    return result

def save_json(data: dict, path: str = "outputs/meeting_data.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"💾 Structured data saved to {path}")