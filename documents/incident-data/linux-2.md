### **Incident Root Cause Review / Analysis**

#### **Incident Metadata**

-   **Incident Number:** INC-20241115-002
-   **Incident Name:** RedHat Server Kernel Panic Causing Database Unavailability
-   **Date of Incident:** November 15, 2024
-   **Reported By:** On-call Engineer (PagerDuty Alert)
-   **Priority Level:** P1 (Critical)
-   **Affected Systems:**
    -   Server Name: `db-prod-node03`
    -   Location: On-premise Data Center (Dallas, TX)
    -   Applications Impacted: Centralized Inventory Management System

----------

### **Incident Timeline**

-   **Incident Detected:** 2024-11-15, 03:05 AM CST
-   **First Response:** 2024-11-15, 03:10 AM CST
-   **Resolution Time:** 2024-11-15, 05:45 AM CST
-   **Total Downtime:** 2 hours 40 minutes

----------

### **Root Cause Analysis**

#### **Causes**

1.  **Primary Cause:**
    
    -   A memory leak in the application caused the server to exhaust all memory resources, triggering a kernel panic.
2.  **Contributing Factors:**
    
    -   Memory leak in a custom Python service running on the server, which was not identified during QA.
    -   Swap space was insufficiently configured, leaving the system unable to handle memory exhaustion.
    -   The server was running a legacy RedHat kernel version (7.6), which had known vulnerabilities related to memory management.

----------

### **Incident Details**

-   **Description:**  
    At 03:05 AM CST, the server `db-prod-node03` experienced a kernel panic due to memory exhaustion, leading to the database becoming unavailable. This caused a cascading failure, as the Inventory Management System relies heavily on this database for operations like stock updates and order placements.
    
-   **Impact:**
    
    -   Inventory updates for over 10,000 SKUs were delayed.
    -   Warehouse operations in three regions (USA, EMEA, APAC) were affected, causing delays in order processing.
    -   Financial impact estimated at $25,000 due to penalties from delayed shipments.

----------

### **Resolution Steps**

1.  **Immediate Actions:**
    
    -   Rebooted the server to restore availability.
    -   Redirected database traffic to the secondary node in the cluster.
    -   Stopped the problematic Python service temporarily.
2.  **Post-Incident Actions:**
    
    -   Analyzed core dumps to confirm the memory leak source.
    -   Upgraded the server to RedHat kernel version 7.9 with fixes for memory handling.
    -   Increased swap space configuration from 4GB to 16GB for better resiliency.
    -   Fixed the memory leak issue in the Python service and deployed a patch.

----------

### **Support Teams Involved**

1.  **Infrastructure Team:**
    -   John Doe (Team Lead)
    -   Anna Richards
2.  **Database Administration Team:**
    -   Ravi Sharma
    -   Elena Petrova
3.  **Application Development Team:**
    -   Michael Lee
    -   Maria Gonzalez

----------

### **Preventative Measures**

1.  Conduct periodic kernel upgrades to ensure servers are running stable and secure versions.
2.  Implement memory usage alerts in Prometheus and Grafana for early detection of leaks.
3.  Perform stress testing and memory profiling for all custom application services.
4.  Ensure swap configurations are adequate for all critical servers.

----------

### **Lessons Learned**

-   Custom services need rigorous memory testing before deployment in production.
-   Upgrading to the latest supported versions of operating system kernels is crucial for stability.
-   A well-configured swap space can prevent kernel panics during memory exhaustion events.

----------

### **Follow-Up Actions**

-   **Deadline:** 2024-11-25
-   **Owner:** Infrastructure Team

1.  Upgrade all servers running RedHat 7.6 to the latest kernel versions.
2.  Enhance application deployment pipelines to include memory profiling tools.
3.  Review and optimize swap configurations across all production systems.