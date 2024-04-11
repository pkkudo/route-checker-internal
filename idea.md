# What to setup?

- periodical monitor log of a routing table from interesting network node(s)
- a tool to search through the saved log files for any changes in the routing table for a specified subnet
- setup a report that runs every 6 hours to give you the route table summary with detailed report for certain interesting routes
  - like what?
  - dmz subnets, server farm subnets
  - important peering - interface, physical or virtual (not routing)

# How to setup a job to run periodically?

- systemd service unit file for the job, a script/program to run, and systemd timer unit to trigger the service unit per the schedule
  - or crontab for old system
  - or build application image and deploy it as a CronJob on Kubernetes
