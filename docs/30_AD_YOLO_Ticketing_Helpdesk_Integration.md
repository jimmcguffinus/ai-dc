---
layout: page
title: 30 AD YOLO Ticketing Helpdesk Integration
permalink: /docs/30_AD_YOLO_Ticketing_Helpdesk_Integration/
---
# AD-YOLO Ticketing & Helpdesk Integration

## Overview
AD-YOLO integrates with enterprise ticketing systems, allowing IT teams to track real-time Active Directory (AD) changes and automate responses. This enables seamless incident management, reducing manual effort and enhancing security.

## Features
### 🔥 **Real-Time Ticket Creation**
- Automatic ticket creation based on **critical AD changes**:
  - New privileged users added
  - Service accounts modified
  - Unusual login patterns detected
  - Devices joining or leaving the network
  - GPO modifications
  - Expired or disabled user accounts

### 🤖 **AI-Powered Helpdesk Chatbot**
- Employees and IT staff can ask AD-YOLO:
  - **"Who has been locked out in the last 24 hours?"**
  - **"Which users were added to Domain Admins?"**
  - **"What devices were enrolled today?"**
- Responses are pulled directly from the AD-YOLO database

### 🎯 **Multi-System Integration**
Supports major IT Service Management (ITSM) and helpdesk platforms:
- ServiceNow
- Jira Service Management
- Zendesk
- Freshservice
- ConnectWise
- IT Glue
- Custom REST API integrations

## 🚀 How It Works

### **1️⃣ Change Detection**
AD-YOLO continuously monitors AD changes via:
- **DirSync** control
- **USNChanged** attribute tracking
- **LDAP Change Notifications**
- **Security event log monitoring (Event ID 4720, 4732, etc.)**

### **2️⃣ AD-YOLO Database Updates**
Detected changes are **logged into SQLite/Milvus**, with key attributes:
| Attribute | Example Value |
|-----------|--------------|
| Name | `John Doe` |
| Object Type | `User` |
| Change Type | `Added to Domain Admins` |
| Timestamp | `2025-03-15 14:30:22` |

### **3️⃣ Automated Ticket Creation**
A new ticket is **instantly generated** if the change meets predefined security policies.

Example JSON payload for ServiceNow:
```json
{
  "short_description": "Critical AD Change Detected",
  "description": "User 'John Doe' was added to Domain Admins at 2025-03-15 14:30:22.",
  "priority": "High",
  "assignment_group": "Security Operations",
  "category": "Security Incident"
}
```

### **4️⃣ Chatbot Query Processing**
When a helpdesk agent queries AD-YOLO:

- **"Show all recent admin additions"**
  - AD-YOLO fetches from its vector DB
  - Returns structured data in natural language

- **"Reset password for User X"**
  - AD-YOLO validates user identity
  - Triggers ServiceNow API to reset the password

## 🔌 Integration with Ticketing Systems

### REST API for Ticketing
Example PowerShell script to create a ServiceNow ticket:
```powershell
$Body = @{
    short_description = "Critical AD Change Detected"
    description = "User 'John Doe' was added to Domain Admins at $(Get-Date)."
    priority = "High"
    assignment_group = "Security Operations"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://servicenow.example.com/api/now/table/incident" `
  -Method Post `
  -Headers @{"Authorization"="Bearer $Token"} `
  -Body $Body
```

### GraphQL Query Interface
Instead of SQL, enable GraphQL queries for flexible AI-driven insights:
```graphql
query {
  recentChanges(filter: { objectType: "User", changeType: "Added to Admins" }) {
    name
    timestamp
    changedBy
  }
}
```

### Ticketing Workflow Example
| Event | Action | Ticketing System |
|-------|--------|-----------------|
| User added to Admins | Open critical ticket | ServiceNow, Jira |
| Multiple failed logins | Flag for review | Zendesk, IT Glue |
| GPO modified | Log for compliance | ConnectWise |
| Computer object deleted | Auto-assign IT investigation | Freshservice |

## 🛠️ Future Enhancements

### Firebase App for Live Updates
- Push ticket updates to mobile IT dashboards
- Integrate Firebase Cloud Functions for real-time alerts

### AI-Driven Ticket Prioritization
- Machine learning assigns risk scores to AD changes
- High-risk actions trigger multi-factor authentication (MFA) verification

### Expanded Chatbot Capabilities
- Voice interaction via Google Assistant / Alexa
- Generate automated incident reports from AD-YOLO insights

## 📌 Conclusion
AD-YOLO revolutionizes helpdesk workflows by combining:
- Real-time AD monitoring
- AI-powered chat interfaces
- Automated ticketing
- GraphQL-based query engines

This empowers IT teams with instant incident detection, automated response, and an intelligent helpdesk assistant. 🚀

### 🔥 **Key Features Added**
✔️ **GraphQL query support for AI-enhanced ticketing**  
✔️ **Expanded ITSM integrations (ConnectWise, IT Glue, Freshservice, etc.)**  
✔️ **Chatbot natural language queries**  
✔️ **PowerShell & JSON examples for automation**  
✔️ **REST API triggers for ServiceNow tickets**  

---

💡 **Next Steps:** Connect AD-YOLO to your ITSM system today! 
