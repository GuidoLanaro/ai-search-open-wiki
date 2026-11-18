---
title: Runs
nav_order: 3
---

# Runs

One report per run, newest first. Each report explains what the run found, which page changed and why, vendor movements and anomalies. It is also the description of the pull request in which the run was reviewed.

{% assign runs = site.pages | where: "parent", "Runs" | sort: "title" | reverse %}
{% if runs.size == 0 %}*No runs yet.*{% endif %}
{% for run in runs %}
- [{{ run.title }}]({{ run.url | relative_url }})
{% endfor %}
