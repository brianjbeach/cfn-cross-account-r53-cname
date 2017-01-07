import sys, boto3, json, urllib, urllib2, json
client = boto3.client('route53')
    
def lambda_handler(event, context):
    #SNS events contain a wrapper around the Lambda event. Unpack the
    #lambda event from SNS. Delete this part if calling lambda directly.
    print("SNS Event: " + json.dumps(event))
    event = json.loads(event['Records'][0]['Sns']['Message'])
    print("Lambda Event: " + json.dumps(event))
    processCustomResource(event, context)
    
    
def processCustomResource(event, context): 
    try: 
        type = event['RequestType']
        hostedzone = event['ResourceProperties']['HostedZoneId']
        source = event['ResourceProperties']['Name']
        target = event['ResourceProperties']['Value']
        
        if type == 'Delete':
            action = "DELETE"
            print "Deleting CNAME " + source + "->" + target + " in " + hostedzone
        else:
            action = "UPSERT"
            print "Creating CNAME " + source + "->" + target + " in " + hostedzone
        change_resource_record_sets(action, hostedzone, source, target)
        
        print "Completed successfully"
        responseStatus = 'SUCCESS'
        responseData = {}
        sendResponse(event, context, responseStatus, responseData)
        
    except: 
        print("Error:", sys.exc_info()[0])
        responseStatus = 'FAILED'
        responseData = {'Error': ("Unexpected error: ", sys.exc_info()[0])}
        sendResponse(event, context, responseStatus, responseData)


def change_resource_record_sets(action, hostedzone, source, target):
    response = client.change_resource_record_sets(
		HostedZoneId=hostedzone,
		ChangeBatch= {
			'Comment': 'CNAME %s -> %s' % (source, target),
			'Changes': [{
				'Action': action,
				'ResourceRecordSet': {
					'Name': source,
					'Type': 'CNAME',
					'TTL': 300,
					'ResourceRecords': [{'Value': target}]
				}
			}]
		}
	)

def sendResponse(event, context, responseStatus, responseData):
    data = json.dumps({
        'Status': responseStatus,
        'Reason': 'See the details in CloudWatch Log Stream: ' + context.log_stream_name,
        'PhysicalResourceId': context.log_stream_name,
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
        'Data': responseData
    })
    
    print event['ResponseURL']
    print data
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(url=event['ResponseURL'], data=data)
    request.add_header('Content-Type', '')
    request.get_method = lambda: 'PUT'
    url = opener.open(request)