# cryptospike

## ProLion Cryptospike 3.x and later

Datasource Program/Special Agent for monitoring ProLion Cryptospike 3.x and later
- Monitoring of service status (possible without login details)
- Monitoring of number of blocked users
- Monitoring of health status of storage server connection (*tested with NetApp Storage only*)
- Monitoring of Cryptospike licence

![Cryptospike Example](cryptospike.png)

## Version History:

### 1.2.1:
- Bug fix: Check crashed when not all CS Server are assigned to SVM (Thanks to Github User @Martin-85 for contributing the fix)

### 1.2.0:

- Bug fix: Blocked User Check crashes if no information about quarantined users and/or active users is available.
- Warning message if one of the monitored nodes is not licensed (e.g. after a controller replacement)


### 1.1.0:

- Support for Cryptospike 3.4.x and later
- Blocked User Check also checks for quarantined users

### 1.0.0:

- first release

## Configuration User Role CryptoSpike
create a new role "Monitoring" with the following settings:

- Cluster: Read
- StorageUser: Read
- Dashboard: View
- Audited Users: View
- Audited Users > Users: View
- Audited Users > Users > Reports: View
- Audited Users > Incidents: View
- Landscape: View
- Landscape > Storage Cluster: View 
- Landscape > Storage Cluster > Cluster > Details: View 
- Landscape > Storage Cluster > Server > Details: View 
- Landscape > Storage Cluster > Volume > Details: View 
- System: View
- System > Status: View
- Account Settings: View
- Date and Time: View

create an user and assign the role "Monitoring"

In Checkmk configure the datasource program (Setup > Agents > Other Integrations > Applications > ProLion Cryptospike)
