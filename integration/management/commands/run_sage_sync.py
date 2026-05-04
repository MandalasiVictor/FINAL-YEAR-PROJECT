import os
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = "The command for running sage integration."

    def add_arguments(self, parser):
        parser.add_argument('--test', action='store_true', help='Load test data')

    def handle(self, *args, **options):
        from integration.helpers import load_employee_data
        from integration.models import Integration
        test_flag = options['test']
        integration = Integration.objects.first()
        if test_flag:
            data = [
                {
                    "empID": 1175,
                    "employeeCode": "001_10993",
                    "displayName": "Mrs J Test",
                    "lastName": "test",
                    "firstName": "test",
                    "leaveStartDate": "2003-01-27T00:00:00",
                    "leaveTypeCode": "SICK_LVE",
                    "totalTypeEntitlement": 30.0,
                    "balanceCarriedForward": 52.375,
                    "hierarchyNameA": "D490 - Warehousing",
                    "jobTitleLongDescription": "Team Leader Stores"
                    
                },
                {
                    "empID": 1176,
                    "employeeCode": "001_10994",
                    "displayName": "Mr K Test",
                    "lastName": "test",
                    "firstName": "test",
                    "leaveStartDate": "2003-02-14T00:00:00",
                    "leaveTypeCode": "ANNUAL_LVE",
                    "totalTypeEntitlement": 25.0,
                    "balanceCarriedForward": 15.0,
                    "hierarchyNameA": "D490 - Warehousing",
                    "jobTitleLongDescription": "Warehouse Operative"
                    
                },
                {
                    "empID": 1177,
                    "employeeCode": "001_10995",
                    "displayName": "Ms L Test",
                    "lastName": "test",
                    "firstName": "test",
                    "leaveStartDate": "2003-03-01T00:00:00",
                    "leaveTypeCode": "SICK_LVE",
                    "totalTypeEntitlement": 30.0,
                    "balanceCarriedForward": 45.0,
                    "hierarchyNameA": "D490 - Warehousing",
                    "jobTitleLongDescription": "Warehouse Operative"
                    
                },
                {
                    "empID": 1178,
                    "employeeCode": "001_10996",
                    "displayName": "Mr M Test",
                    "lastName": "test",
                    "firstName": "test",
                    "leaveStartDate": "2003-04-10T00:00:00",
                    "leaveTypeCode": "ANNUAL_LVE",
                    "totalTypeEntitlement": 25.0,
                    "balanceCarriedForward": 10.0,
                    "hierarchyNameA": "D490 - Warehousing",
                    "jobTitleLongDescription": "Warehouse Operative"
                    
                },
                {
                    "empID": 1179,
                    "employeeCode": "001_10997",
                    "displayName": "Ms N Test",
                    "lastName": "test",
                    "firstName": "test",
                    "leaveStartDate": "2003-05-20T00:00:00",
                    "leaveTypeCode": "SICK_LVE",
                    "totalTypeEntitlement": 10.0,
                    "balanceCarriedForward": 20.0,
                    "hierarchyNameA": "D490 - Warehousing",
                    "jobTitleLongDescription": "Warehouse Operative"
                    
                },

                {
                    "empID": 1180,
                    "employeeCode": "001_10998",
                    "displayName": "Mr O Test",
                    "lastName": "test",
                    "firstName": "test",
                    "leaveStartDate": "2003-06-05T00:00:00",
                    "leaveTypeCode": "ANNUAL_LVE",
                    "totalTypeEntitlement": 25.0,
                    "balanceCarriedForward": 35.0,
                    "hierarchyNameA": "D490 - Warehousing",
                    "jobTitleLongDescription": "Warehouse Operative"
                    
                },
                {
                    "empID": 1181,
                    "employeeCode": "001_10999",
                    "displayName": "Mrs P Test",
                    "lastName": "test",
                    "firstName": "test",
                    "leaveStartDate": "2003-07-15T00:00:00",
                    "leaveTypeCode": "SICK_LVE",
                    "totalTypeEntitlement": 20.0,
                    "balanceCarriedForward": 25.0,
                    "hierarchyNameA": "D490 - Warehousing",
                    "jobTitleLongDescription": "Warehouse Operative"
                    
                },
                ]
            load_employee_data(data=data, integration=integration)
        else:
            load_employee_data(integration=integration)