# cfn-cross-account-r53-cname
Most AWS customers have more than one account. For example, you might have one account for each business unit.  Typically you have one central account for shared resources. One example is R53. You can only host a specific domain (e.g. example.com) in a single account.

If you use CloudFormation, you cannot create resource records in another account. This is an issue, when you need to create a CNAME for (www.example.com) to alias a ELB (e.g. my-loadbalancer-1234567890.us-west-2.elb.amazonaws.com) or other AWS resource.   

cfn-cross-account-r53-cname is a Cloud Formation Custom Resource that creates a R53 CNAME.  As you can see in diagram.pptx, the Custom Resource sends a meaage to a SNS topic rather than calling LAmbda directly.  This allows you to easily make the cal accross acounts and create the CNAME in another account.    
