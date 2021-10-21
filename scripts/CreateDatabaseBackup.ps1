param (
    [Parameter(Mandatory = $true)][string]$Container,
    [Parameter(Mandatory = $true)][string]$Password
)

docker exec $Container /usr/bin/mysqldump -u root --password="$Password" db | Set-Content backup.sql
