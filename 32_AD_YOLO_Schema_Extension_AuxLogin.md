# AD-YOLO Schema Extension & AuxLogin Attributes

## Overview
AD-YOLO extends the Active Directory schema with custom auxiliary attributes (`auxLogin`) to track and manage additional user and device properties. This extension enables enhanced monitoring, security controls, and asset management capabilities.

## Schema Extension

### Auxiliary Class Definition
```ldif
# auxLogin.ldif
dn: CN=auxLogin,CN=Schema,CN=Configuration,DC=example,DC=com
objectClass: classSchema
governsID: 1.2.840.113556.1.5.9999
lDAPDisplayName: auxLogin
adminDisplayName: Auxiliary Login Class
adminDescription: AD-YOLO auxiliary class for enhanced login tracking
objectClassCategory: 3
subClassOf: top
mayContain: loginInstalledApps
mayContain: loginSecurityCameras
mayContain: login4KTVs
mayContain: loginMetaGlasses
mayContain: loginWorkstations
mayContain: loginLastLocation
mayContain: loginDeviceHealth
mayContain: loginAccessLevel
defaultSecurityDescriptor: D:(A;;RPWPCRCCDCLCLORCWOWDSDDTSW;;;DA)
systemOnly: FALSE
defaultHidingValue: FALSE
objectCategory: CN=Class-Schema,CN=Schema,CN=Configuration,DC=example,DC=com
```

### Attribute Definitions
```ldif
# Installed Applications
dn: CN=loginInstalledApps,CN=Schema,CN=Configuration,DC=example,DC=com
objectClass: attributeSchema
adminDisplayName: Login Installed Applications
adminDescription: List of installed applications on user's devices
attributeID: 1.2.840.113556.1.4.9901
attributeSyntax: 2.5.5.12
isSingleValued: FALSE
lDAPDisplayName: loginInstalledApps
searchFlags: 1
systemOnly: FALSE

# Security Cameras
dn: CN=loginSecurityCameras,CN=Schema,CN=Configuration,DC=example,DC=com
objectClass: attributeSchema
adminDisplayName: Login Security Cameras
adminDescription: Security camera access and permissions
attributeID: 1.2.840.113556.1.4.9902
attributeSyntax: 2.5.5.12
isSingleValued: FALSE
lDAPDisplayName: loginSecurityCameras
searchFlags: 1
systemOnly: FALSE

# 4K TVs
dn: CN=login4KTVs,CN=Schema,CN=Configuration,DC=example,DC=com
objectClass: attributeSchema
adminDisplayName: Login 4K TVs
adminDescription: 4K TV device assignments and configurations
attributeID: 1.2.840.113556.1.4.9903
attributeSyntax: 2.5.5.12
isSingleValued: FALSE
lDAPDisplayName: login4KTVs
searchFlags: 1
systemOnly: FALSE

# Meta Glasses
dn: CN=loginMetaGlasses,CN=Schema,CN=Configuration,DC=example,DC=com
objectClass: attributeSchema
adminDisplayName: Login Meta Glasses
adminDescription: Meta Glasses device assignments
attributeID: 1.2.840.113556.1.4.9904
attributeSyntax: 2.5.5.1
isSingleValued: TRUE
lDAPDisplayName: loginMetaGlasses
searchFlags: 1
systemOnly: FALSE
```

## Schema Management

### Schema Extension Manager
```python
class SchemaManager:
    def __init__(self, ad_client):
        self.ad_client = ad_client
        
    async def install_schema(self):
        """Install AD-YOLO schema extensions"""
        try:
            # Check if schema already exists
            if await self.schema_exists():
                return False
                
            # Install attribute definitions
            await self.install_attributes()
            
            # Install auxiliary class
            await self.install_auxiliary_class()
            
            # Update schema cache
            await self.update_schema_cache()
            
            return True
        except Exception as e:
            logging.error(f"Schema installation error: {e}")
            return False
            
    async def schema_exists(self):
        """Check if schema is already installed"""
        return await self.ad_client.attribute_exists('loginInstalledApps')
```

### Attribute Management
```python
class AttributeManager:
    def __init__(self):
        self.attributes = {
            'loginInstalledApps': {
                'syntax': '2.5.5.12',  # String(Unicode)
                'multi_valued': True,
                'indexed': True
            },
            'loginSecurityCameras': {
                'syntax': '2.5.5.12',  # String(Unicode)
                'multi_valued': True,
                'indexed': True
            },
            'login4KTVs': {
                'syntax': '2.5.5.12',  # String(Unicode)
                'multi_valued': True,
                'indexed': True
            },
            'loginMetaGlasses': {
                'syntax': '2.5.5.1',   # Boolean
                'multi_valued': False,
                'indexed': True
            }
        }
        
    def get_attribute_ldif(self, attr_name):
        """Generate LDIF for attribute"""
        attr = self.attributes[attr_name]
        return f"""
dn: CN={attr_name},CN=Schema,CN=Configuration,DC=example,DC=com
objectClass: attributeSchema
adminDisplayName: {self.get_display_name(attr_name)}
adminDescription: {self.get_description(attr_name)}
attributeID: {self.get_attribute_id(attr_name)}
attributeSyntax: {attr['syntax']}
isSingleValued: {str(not attr['multi_valued']).upper()}
lDAPDisplayName: {attr_name}
searchFlags: {1 if attr['indexed'] else 0}
systemOnly: FALSE
"""
```

## Data Management

### Attribute Access
```python
class AuxLoginManager:
    def __init__(self, ad_client):
        self.ad_client = ad_client
        
    async def get_aux_login(self, user_dn):
        """Get auxLogin attributes for user"""
        attributes = [
            'loginInstalledApps',
            'loginSecurityCameras',
            'login4KTVs',
            'loginMetaGlasses'
        ]
        
        result = await self.ad_client.get_attributes(
            user_dn, 
            attributes
        )
        
        return {
            attr: result.get(attr, [])
            for attr in attributes
        }
        
    async def update_aux_login(self, user_dn, updates):
        """Update auxLogin attributes"""
        await self.ad_client.modify_attributes(
            user_dn,
            updates,
            operation='REPLACE'
        )
```

### Data Validation
```python
class AuxLoginValidator:
    def __init__(self):
        self.validators = {
            'loginInstalledApps': self.validate_apps,
            'loginSecurityCameras': self.validate_cameras,
            'login4KTVs': self.validate_tvs,
            'loginMetaGlasses': self.validate_glasses
        }
        
    def validate_attribute(self, attr_name, value):
        """Validate attribute value"""
        validator = self.validators.get(attr_name)
        if validator:
            return validator(value)
        return True
        
    def validate_apps(self, apps):
        """Validate installed apps list"""
        if not isinstance(apps, list):
            return False
        return all(isinstance(app, str) for app in apps)
```

## Query & Search

### Advanced Queries
```python
class AuxLoginQuery:
    def __init__(self, ad_client):
        self.ad_client = ad_client
        
    async def find_users_with_app(self, app_name):
        """Find users with specific installed app"""
        filter_str = f"(loginInstalledApps=*{app_name}*)"
        return await self.ad_client.search(
            base_dn="DC=example,DC=com",
            filter_str=filter_str,
            attributes=['cn', 'loginInstalledApps']
        )
        
    async def find_camera_access(self, camera_id):
        """Find users with access to specific camera"""
        filter_str = f"(loginSecurityCameras=*{camera_id}*)"
        return await self.ad_client.search(
            base_dn="DC=example,DC=com",
            filter_str=filter_str,
            attributes=['cn', 'loginSecurityCameras']
        )
```

### Search Templates
```python
class SearchTemplates:
    @staticmethod
    def get_template(search_type):
        """Get search template by type"""
        templates = {
            'apps': {
                'filter': '(loginInstalledApps=*{value}*)',
                'attributes': ['cn', 'loginInstalledApps']
            },
            'cameras': {
                'filter': '(loginSecurityCameras=*{value}*)',
                'attributes': ['cn', 'loginSecurityCameras']
            },
            'tvs': {
                'filter': '(login4KTVs=*{value}*)',
                'attributes': ['cn', 'login4KTVs']
            },
            'glasses': {
                'filter': '(loginMetaGlasses=TRUE)',
                'attributes': ['cn', 'loginMetaGlasses']
            }
        }
        return templates.get(search_type)
```

## Integration Examples

### PowerShell Integration
```powershell
# Get auxLogin attributes
function Get-ADUserAuxLogin {
    param(
        [string]$Identity
    )
    
    Get-ADUser -Identity $Identity -Properties @(
        'loginInstalledApps',
        'loginSecurityCameras',
        'login4KTVs',
        'loginMetaGlasses'
    )
}

# Update auxLogin attributes
function Set-ADUserAuxLogin {
    param(
        [string]$Identity,
        [hashtable]$AuxLoginAttributes
    )
    
    $params = @{
        Identity = $Identity
        Replace = $AuxLoginAttributes
    }
    
    Set-ADUser @params
}
```

### Python Integration
```python
from adyolo.schema import AuxLoginManager

# Initialize manager
aux_login = AuxLoginManager()

# Get user attributes
async def get_user_devices(user_dn):
    aux_data = await aux_login.get_aux_login(user_dn)
    return {
        'installed_apps': aux_data['loginInstalledApps'],
        'security_cameras': aux_data['loginSecurityCameras'],
        '4k_tvs': aux_data['login4KTVs'],
        'meta_glasses': aux_data['loginMetaGlasses']
    }
```

## Security & Compliance

### Access Control
```python
class AuxLoginSecurity:
    def __init__(self):
        self.acl_manager = ACLManager()
        
    def get_attribute_security(self, attr_name):
        """Get security descriptor for attribute"""
        return {
            'loginInstalledApps': 'D:(A;;RPWPCRCCDCLCLORCWOWDSDDTSW;;;DA)',
            'loginSecurityCameras': 'D:(A;;RPWPCRCCDCLCLORCWOWDSDDTSW;;;DA)',
            'login4KTVs': 'D:(A;;RPWPCRCCDCLCLORCWOWDSDDTSW;;;DA)',
            'loginMetaGlasses': 'D:(A;;RPWPCRCCDCLCLORCWOWDSDDTSW;;;DA)'
        }.get(attr_name)
```

### Audit Logging
```python
class AuxLoginAuditor:
    def __init__(self):
        self.logger = self.setup_logger()
        
    def audit_change(self, change):
        """Log attribute change"""
        self.logger.info('AuxLogin Change', extra={
            'timestamp': datetime.now().isoformat(),
            'user_dn': change.user_dn,
            'attribute': change.attribute,
            'old_value': change.old_value,
            'new_value': change.new_value,
            'modified_by': change.modified_by
        })
```

## Future Enhancements
✅ **Additional device attributes**  
✅ **Enhanced security controls**  
✅ **Automated attribute updates**  
✅ **Integration with asset management**  

---

*AD-YOLO's schema extension enables comprehensive tracking and management of user devices and access permissions through custom auxiliary attributes.* 📝 