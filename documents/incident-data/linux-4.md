### **Incident Root Cause Review / Analysis**

#### **Incident Metadata**

-   **Incident Number:** INC-20241201-004
-   **Incident Name:** RedHat Server Time Drift Causing Authentication Failures
-   **Date of Incident:** December 1, 2024
-   **Reported By:** User Support Team (via Helpdesk Tickets)
-   **Priority Level:** P1 (Critical)
-   **Affected Systems:**
    -   Server Name: `auth-prod-node01`
    -   Location: GCP us-central1 Region
    -   Applications Impacted: Single Sign-On (SSO) Authentication Service

----------

### **Incident Timeline**

-   **Incident Detected:** 2024-12-01, 09:20 AM UTC
-   **First Response:** 2024-12-01, 09:30 AM UTC
-   **Resolution Time:** 2024-12-01, 11:15 AM UTC
-   **Total Downtime:** 1 hour 55 minutes

----------

### **Root Cause Analysis**

#### **Causes**

1.  **Primary Cause:**
    
    -   The `auth-prod-node01` server had an NTP (Network Time Protocol) misconfiguration, causing a time drift of 5 minutes. This led to token validation failures in the SSO authentication service.
2.  **Contributing Factors:**
    
    -   NTP servers in the configuration file were outdated and unreachable.
    -   No monitoring alerts were set up for time synchronization issues.
    -   The application did not gracefully handle minor time drifts and treated them as hard failures.

----------

### **Incident Details**

-   **Description:**  
    At 09:20 AM UTC, users reported being unable to log in through the Single Sign-On (SSO) service. Investigation revealed that the `auth-prod-node01` server, which hosts the authentication service, had a time drift of 5 minutes. This mismatch caused token expiration times to appear invalid, leading to authentication failures.
    
-   **Impact:**
    
    -   Over 5,000 users were unable to access enterprise applications during the downtime.
    -   Customer-facing portals experienced degraded service as internal teams couldn't log in for troubleshooting.
    -   Incident escalated to executive leadership due to its widespread impact.

----------

### **Resolution Steps**

1.  **Immediate Actions:**
    
    -   Re-synchronized the server’s clock using a manual `ntpdate` command.
    -   Updated the SSO service configuration to temporarily relax token expiration validation thresholds.
2.  **Post-Incident Actions:**
    
    -   Configured the server to use reliable NTP servers (`time.google.com`).
    -   Enabled real-time monitoring for clock synchronization issues via Prometheus and Grafana.
    -   Fixed the SSO application logic to tolerate minor time mismatches (up to 10 seconds).

----------

### **Support Teams Involved**

1.  **Infrastructure Team:**
    -   Mark Taylor (Team Lead)
    -   Olivia Adams
2.  **Application Development Team:**
    -   Kevin Chen
    -   Deepa Kumar
3.  **User Support Team:**
    -   Amanda Williams

----------

### **Preventative Measures**

1.  Use robust and reliable NTP servers with redundancy in configuration (`time.google.com`, `pool.ntp.org`).
2.  Set up monitoring and alerting for time synchronization issues on all production servers.
3.  Update the SSO service to gracefully handle small time drifts without failing authentication.
4.  Conduct periodic audits of NTP configurations and ensure all servers are synchronized correctly.

----------

### **Lessons Learned**

-   Reliable time synchronization is critical for services dependent on timestamp-based validations.
-   Monitoring for system-level metrics like time drift can prevent widespread outages.
-   Applications must be designed with fault tolerance for minor system-level inconsistencies.

----------

### **Follow-Up Actions**

-   **Deadline:** 2024-12-10
-   **Owner:** Infrastructure Team

1.  Audit NTP configurations across all production servers and standardize them.
2.  Deploy and test a patch for the SSO service to handle minor time discrepancies.
3.  Create a runbook for troubleshooting time synchronization issues.