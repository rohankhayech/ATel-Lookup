param (
    [Parameter(Mandatory = $true)][string]$Container,
    [Parameter(Mandatory = $true)][string]$Password
)

Get-Content backup.sql | docker exec -i $Container /usr/bin/mysql -u root --password=$Password db
