# What to setup?

- periodical monitor log of a routing table from interesting network node(s)
- a tool to search through the saved log files for any changes in the routing table for a specified subnet
  - generate and send report
  - send alert
  - compress and clean up saved log files
- setup a report that runs every 6 hours to give you the route table summary with detailed report for certain interesting routes
  - like what?
  - dmz subnets, server farm subnets
  - important peering - interface, physical or virtual (not routing)

# How to setup a job to run periodically?

- systemd service unit file for the job, a script/program to run, and systemd timer unit to trigger the service unit per the schedule
  - or crontab for old system
  - or build application image and deploy it as a CronJob on Kubernetes

# example

## subnet for a certain destination

- `show ip route` every 1 hour on a backbone network device
- run a script to search for 10.20.192.0/21 in all the stored log files for past n hours/days
  - `uptime` of the route
  - brief stats
    - is the route available on all the stored log files for past n hours (100%)?
- optionally, run an additional script using timer to send alert email to a DL or message to Slack/Discord/etc. to pay close attention to a certain important subnets

## peering between primary data center and public cloud

- `show interfaces` or `show ip bgp neighbor {peer}` or ... every 1 hour on each edge devices to watch
- generate a report of the interesting interface - look for changes by comparing interesting fields with the previous report generated
  - description
  - link_status
  - protocol_status
  - mtu
  - duplex
  - speed
  - bandwidth
  - media_type
  - last_input
  - last_output
  - input_errors
  - output_errors
  - crc
  - abort
