import boto3, json, urllib, urllib2, json
client = boto3.client('route53')
    
def lambda_handler(event, context):
    
    hostedzone = event['ResourceProperties']['HostedZoneId']
    source = event['ResourceProperties']['Name']
    target = event['ResourceProperties']['Value']
  
    try:               
        response = client.change_resource_record_sets(
    		HostedZoneId=hostedzone,
    		ChangeBatch= {
    			'Comment': 'add %s -> %s' % (source, target),
    			'Changes': [{
    				'Action': 'UPSERT',
    				'ResourceRecordSet': {
    					'Name': source,
    					'Type': 'CNAME',
    					'TTL': 300,
    					'ResourceRecords': [{'Value': target}]
    				}
    			}]
    		}
    	)
        responseStatus = 'SUCCESS'
        responseData = {}
        sendResponse(event, context, responseStatus, responseData)
    except: 
        responseStatus = 'FAILED'
        responseData = {'Error': 'Something bad happened'}
        sendResponse(event, context, responseStatus, responseData)
	

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