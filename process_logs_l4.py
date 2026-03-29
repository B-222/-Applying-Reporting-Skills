import json

log_file = "clean_logs_l4.txt"

level_counts = {}
service_counts = {}
error_samples = []

with open(log_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        
        parts = [p.strip() for p in line.split("|")]
        
        if len(parts) == 4:
            ts, level, service, msg = parts
            
            level_counts[level] = level_counts.get(level, 0) + 1
            service_counts[service] = service_counts.get(service, 0) + 1
            
            if level == "ERROR":
                error_samples.append(line)

summary = {
    "level_counts": level_counts,
    "service_counts": service_counts
}

with open("summary_l4.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

print("✓ JSON summary saved to summary_l4.json")

sorted_services = sorted(service_counts.items(), key=lambda x: x[1], reverse=True)

report_text = "INCIDENT MINI-REPORT\n\n"

report_text += "Log Level Summary:\n"
for level in sorted(level_counts.keys()):
    report_text += f"{level}: {level_counts[level]}\n"

report_text += "\n"

report_text += "Top Services by Volume:\n"
for service, count in sorted_services:
    report_text += f"{service}: {count}\n"

report_text += "\n"

report_text += "Sample ERROR Logs:\n"
if error_samples:
    for error_line in error_samples:
        report_text += f"{error_line}\n"
else:
    report_text += "No errors found.\n"

with open("incident_report_l4.txt", "w", encoding="utf-8") as f:
    f.write(report_text)

print("✓ Incident report saved to incident_report_l4.txt")
print("\nReport Preview:\n")
print(report_text)
