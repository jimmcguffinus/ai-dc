# AD-YOLO Schema Extension (auxLogin)

## Overview
AD-YOLO extends Active Directory schema with auxiliary attributes (`auxLogin`) to track modern enterprise assets and user properties. This extension enables granular tracking of devices, vehicles, security equipment, and employee-specific data while maintaining AD's core functionality.

## Extended Attributes

### Core Attributes
```powershell
# Base auxLogin attributes
$attributes = @{
    'auxLoginInstalledApps' = 'List of installed applications'
    'auxLoginSecurityCameras' = 'Assigned security camera IDs'
    'auxLogin4KTVs' = 'Managed 4K display assets'
    'auxLoginMetaGlasses' = 'AR/VR device assignments'
}
```

### New Extended Attributes
```powershell
# Additional tracking attributes
$newAttributes = @{
    'auxLoginIMEINumber' = 'Mobile device IMEI tracking'
    'auxLoginFleetVehicle' = 'Company vehicle assignments'
    'auxLoginGunRegistry' = 'Security weapon tracking'
    'auxLoginProjects' = 'Active project assignments'
    'auxLoginHandicap' = 'Golf handicap for perks program'
    'auxLoginBadgeLevel' = 'Security clearance level'
    'auxLoginParkingSpot' = 'Assigned parking location'
    'auxLoginCertifications' = 'Professional certifications'
}
```

## Schema Extension

### PowerShell Deployment
```powershell
# Import AD Schema module
Import-Module ActiveDirectory

# Create new auxiliary class
$schemaPath = "CN=Schema,CN=Configuration,DC=login,DC=local"
$auxLoginClass = "CN=auxLogin,$schemaPath"

New-ADObject -Name "auxLogin" -Type "classSchema" -Path $schemaPath -OtherAttributes @{
    objectClass = "classSchema"
    ldapDisplayName = "auxLogin"
    governsID = "1.2.840.113556.1.5.9999"
    objectClassCategory = 3
    systemOnly = $false
    defaultObjectCategory = $auxLoginClass
    mayContain = @(
        "auxLoginIMEINumber",
        "auxLoginFleetVehicle",
        "auxLoginGunRegistry",
        "auxLoginProjects",
        "auxLoginHandicap"
    )
}
```

## Bulk Import Support

### LDIF Import Example
```ldif
dn: CN=Schema,CN=Configuration,DC=login,DC=local
changetype: modify
add: attributeTypes
attributeTypes: (
    1.2.840.113556.1.4.9001
    NAME 'auxLoginIMEINumber'
    SYNTAX '1.3.6.1.4.1.1466.115.121.1.15'
    SINGLE-VALUE
)
-
add: attributeTypes
attributeTypes: (
    1.2.840.113556.1.4.9002
    NAME 'auxLoginFleetVehicle'
    SYNTAX '1.3.6.1.4.1.1466.115.121.1.15'
    SINGLE-VALUE
)
```

### CSV Bulk Import Tool
```python
import csv
import ldap3
from typing import Dict, List

class AuxLoginBulkImporter:
    def __init__(self, ldap_server: str, admin_dn: str, password: str):
        self.server = ldap3.Server(ldap_server)
        self.conn = ldap3.Connection(
            self.server, 
            admin_dn, 
            password, 
            auto_bind=True
        )

    def import_from_csv(self, csv_path: str):
        """Import auxLogin attributes from CSV"""
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self._update_user_attributes(row)

    def _update_user_attributes(self, data: Dict):
        """Update user with auxLogin attributes"""
        user_dn = f"CN={data['username']},OU=Users,DC=login,DC=local"
        
        attributes = {
            'auxLoginIMEINumber': data.get('imei', ''),
            'auxLoginFleetVehicle': data.get('vehicle', ''),
            'auxLoginProjects': data.get('projects', '').split(','),
            'auxLoginHandicap': data.get('handicap', '')
        }

        self.conn.modify(user_dn, 
            {attr: [(ldap3.MODIFY_REPLACE, [val])] 
             for attr, val in attributes.items() if val}
        )

# Usage Example
importer = AuxLoginBulkImporter(
    'ldap://dc.login.local',
    'CN=Admin,DC=login,DC=local',
    'password'
)
importer.import_from_csv('aux_login_data.csv')
```

## Enhanced Audit Tracking

### Attribute Change Logging
```python
from datetime import datetime
import sqlite3
from typing import Dict

class AuxLoginAuditor:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.setup_database()

    def setup_database(self):
        """Create audit tables"""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS attribute_changes (
                id INTEGER PRIMARY KEY,
                user_dn TEXT NOT NULL,
                attribute TEXT NOT NULL,
                old_value TEXT,
                new_value TEXT,
                changed_by TEXT NOT NULL,
                change_time TIMESTAMP,
                source_ip TEXT,
                change_location TEXT
            )
        """)

    def log_change(self, change_data: Dict):
        """Log attribute modification"""
        self.conn.execute("""
            INSERT INTO attribute_changes (
                user_dn, attribute, old_value, new_value,
                changed_by, change_time, source_ip, change_location
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            change_data['user_dn'],
            change_data['attribute'],
            change_data['old_value'],
            change_data['new_value'],
            change_data['changed_by'],
            datetime.now(),
            change_data['source_ip'],
            change_data['location']
        ))
        self.conn.commit()

    def get_audit_trail(self, user_dn: str) -> List[Dict]:
        """Retrieve audit history for a user"""
        cursor = self.conn.execute("""
            SELECT * FROM attribute_changes
            WHERE user_dn = ?
            ORDER BY change_time DESC
        """, (user_dn,))
        
        return [dict(row) for row in cursor.fetchall()]
```

## Schema Validation

### Health Check Tool
```python
from typing import List, Dict
import ldap3

class SchemaHealthChecker:
    def __init__(self, ldap_server: str, admin_dn: str, password: str):
        self.server = ldap3.Server(ldap_server)
        self.conn = ldap3.Connection(
            self.server, 
            admin_dn, 
            password, 
            auto_bind=True
        )

    def check_schema_health(self) -> Dict[str, List]:
        """Perform comprehensive schema health check"""
        results = {
            'missing_attributes': [],
            'conflicts': [],
            'invalid_syntax': [],
            'recommendations': []
        }

        # Check required attributes
        required_attrs = [
            'auxLoginIMEINumber',
            'auxLoginFleetVehicle',
            'auxLoginGunRegistry',
            'auxLoginProjects',
            'auxLoginHandicap'
        ]

        schema_attrs = self._get_schema_attributes()
        
        for attr in required_attrs:
            if attr not in schema_attrs:
                results['missing_attributes'].append(attr)

        # Check for conflicts
        for attr in schema_attrs:
            if attr.startswith('auxLogin'):
                conflicts = self._check_attribute_conflicts(attr)
                if conflicts:
                    results['conflicts'].extend(conflicts)

        # Validate syntax
        for attr in schema_attrs:
            if not self._validate_attribute_syntax(attr):
                results['invalid_syntax'].append(attr)

        return results

    def _get_schema_attributes(self) -> List[str]:
        """Get all schema attributes"""
        self.conn.search(
            'CN=Schema,CN=Configuration,DC=login,DC=local',
            '(objectClass=attributeSchema)',
            attributes=['lDAPDisplayName']
        )
        return [entry.lDAPDisplayName.value for entry in self.conn.entries]

    def _check_attribute_conflicts(self, attr: str) -> List[str]:
        """Check for attribute naming conflicts"""
        conflicts = []
        self.conn.search(
            'CN=Schema,CN=Configuration,DC=login,DC=local',
            f'(&(objectClass=attributeSchema)(!(lDAPDisplayName={attr}))(name=*{attr}*))',
            attributes=['lDAPDisplayName']
        )
        return [entry.lDAPDisplayName.value for entry in self.conn.entries]

    def _validate_attribute_syntax(self, attr: str) -> bool:
        """Validate attribute syntax"""
        self.conn.search(
            'CN=Schema,CN=Configuration,DC=login,DC=local',
            f'(lDAPDisplayName={attr})',
            attributes=['attributeSyntax', 'oMSyntax']
        )
        if not self.conn.entries:
            return False
        
        entry = self.conn.entries[0]
        return all([
            entry.attributeSyntax.value,
            entry.oMSyntax.value
        ])

# Usage Example
checker = SchemaHealthChecker(
    'ldap://dc.login.local',
    'CN=Admin,DC=login,DC=local',
    'password'
)

health_report = checker.check_schema_health()
print("Schema Health Report:")
for category, issues in health_report.items():
    print(f"\n{category.upper()}:")
    for issue in issues:
        print(f"- {issue}")
```

## Deployment Validation

### Pre-deployment Checks
```powershell
# Validate schema before deployment
function Test-AuxLoginSchema {
    param(
        [string]$Domain = "login.local",
        [string[]]$RequiredAttributes
    )
    
    $results = @{
        Success = $true
        Messages = @()
    }
    
    # Check Schema Admin rights
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($identity)
    if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        $results.Success = $false
        $results.Messages += "Error: Must run as Schema Admin"
    }
    
    # Check Schema Master availability
    try {
        $schemaNC = (Get-ADRootDSE).schemaNamingContext
        Get-ADObject $schemaNC
    } catch {
        $results.Success = $false
        $results.Messages += "Error: Cannot access Schema Master"
    }
    
    # Validate attribute names
    foreach ($attr in $RequiredAttributes) {
        if ($attr -notmatch '^auxLogin[A-Z]') {
            $results.Success = $false
            $results.Messages += "Error: Invalid attribute name format: $attr"
        }
    }
    
    return $results
}

# Example usage
$checkResults = Test-AuxLoginSchema -RequiredAttributes @(
    'auxLoginIMEINumber',
    'auxLoginFleetVehicle',
    'auxLoginGunRegistry'
)

if ($checkResults.Success) {
    Write-Host "Schema validation passed!"
} else {
    Write-Host "Schema validation failed:"
    $checkResults.Messages | ForEach-Object { Write-Host "- $_" }
}
```

## Future Enhancements
✅ **Additional tracking attributes**  
✅ **Enhanced audit logging**  
✅ **Bulk import tools**  
✅ **Schema validation**  
✅ **Health monitoring**  

## Next Steps
1. Deploy new attributes using LDIF or PowerShell
2. Import existing data using CSV tool
3. Enable enhanced audit logging
4. Run schema health check
5. Monitor attribute usage and performance

---

*AD-YOLO Schema Extension provides a robust framework for tracking modern enterprise assets while maintaining AD compatibility and security.* 🎯 