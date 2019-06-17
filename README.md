# check_ncpa_disk
Script to monitor all disks, using NCPA (check_ncpa.py)

**Prequisites**

1. Download script check_ncpa (https://github.com/NagiosEnterprises/ncpa/blob/master/client/check_ncpa.py)

**Installation**

1. Download and copy the script to your nagios script directory (ex /usr/local/nagios/libexec)


**Configuration**

	-H", "--srvip" : Define IP hostame
    -t", "--keyncpa": Define your NCPA key
    -p", "--port": Define your NCPA port (ex. 5693)
    -w", "--warning": Define your Warning thresholds;
    -c", "--critical": Define your Critical thresholds;
    -v", "--versionso": Define your S.O. (linux|windows)
    -x", "--exclude": to exclude units (ex: D:|D:,E:|/boot) 

Examples:

- Monitoring All Disks Linux, exclude /mnt/resource
```
/usr/local/nagios/libexec/check_ncpa_disk.py -H 192.168.0.1 -t my_ncpa_key -p 5693 -w 80 -c 95 -v linux -x /mnt/resource
```

- Monitoring All Disks Windows, exclude D: and F:
```
/usr/local/nagios/libexec/check_ncpa_disk.py -H 192.168.0.1 -t my_ncpa_key -p 5693 -w 80 -c 95 -v windows -x D:, F:
```
