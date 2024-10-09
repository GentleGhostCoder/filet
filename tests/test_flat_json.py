# import json
# from time import perf_counter
#
# import orjson
# import pandas as pd
#
# from filet.boto3.recursive_explode_table import recursive_explode_flatten_dataframe
# from filet.cpputils import FlatJsonHandler
#
#
# def test_flat_json_speed():
#     test_json = """
#     {
#       "header": {
#         "version": 1.0
#       },
#       "data": [ 1,  2 ]
#     }
#     """
#
#     time_custom_handler = perf_counter()
#     for _ in range(100):
#         handler = FlatJsonHandler()
#         data = handler.loads(test_json)
#         df = pd.DataFrame(data)
#     print(perf_counter() - time_custom_handler)
#
#     time_pandas_normalize = perf_counter()
#     for _ in range(100):
#         df2 = recursive_explode_flatten_dataframe(pd.json_normalize(orjson.loads(test_json)))
#     print(perf_counter() - time_pandas_normalize)
#
#     assert time_pandas_normalize > time_custom_handler
#     assert df.shape == df2.shape
#
#
# def test_complex_flat_json():
#     test_json = """
#     {
#     "status": "success",
#     "data": {
#     "resultType": "matrix",
#     "result": [
#             {
#             "metric": {
#               "id": "1",
#               "__name__": "node_memory_MemTotal_bytes",
#               "alias": "datacenteraggregation",
#               "cluster": "F1C20",
#               "datacenter": "de-kae-bs-kvm-live",
#               "instance": "onode012035.server.lan:9100",
#               "job": "clusters"
#             },
#             "values": [
#               [
#                 1698678900,
#                 "809772896256"
#               ],
#               [
#                 1698678960,
#                 "809772896256"
#               ],
#               [
#                 1698679020,
#                 "809772896256"
#               ],
#               [
#                 1698679080,
#                 "809772896256"
#               ],
#               [
#                 1698679140,
#                 "809772896256"
#               ],
#               [
#                 1698679200,
#                 "809772896256"
#               ]
#             ]
#           },
#           {
#             "metric": {
#               "id": "2",
#               "__name__": "node_memory_MemTotal_bytes",
#               "alias": "datacenteraggregation",
#               "cluster": "F1C3",
#               "datacenter": "de-kae-bs-esxi-live",
#               "instance": "localhost:9100",
#               "job": "self",
#               "recordings": "clusters"
#             },
#             "values": [
#               [
#                 1698678900,
#                 "6216773632"
#               ],
#               [
#                 1698678960,
#                 "6216773632"
#               ],
#               [
#                 1698679020,
#                 "6216773632"
#               ],
#               [
#                 1698679080,
#                 "6216773632"
#               ],
#               [
#                 1698679140,
#                 "6216773632"
#               ],
#               [
#                 1698679200,
#                 "6216773632"
#               ]
#             ]
#          },
#           {
#             "metric": {
#               "id": "3",
#               "__name__": "node_memory_MemTotal_bytes",
#               "alias": "datacenteraggregation",
#               "cluster": "F1C3",
#               "datacenter": "de-kae-bs-esxi-live",
#               "instance": "localhost:9100",
#               "job": "self",
#               "recordings": "clusters"
#             },
#             "values": [
#               [
#                 1698678900,
#                 "6216773632"
#               ],
#               [
#                 1698678960,
#                 "6216773632"
#               ],
#               [
#                 1698679020,
#                 "6216773632"
#               ],
#               [
#                 1698679080,
#                 "6216773632"
#               ],
#               [
#                 1698679140,
#                 "6216773632"
#               ],
#               [
#                 1698679200,
#                 "6216773632"
#               ]
#             ]
#          },
#           {
#             "metric": {
#               "id": "4",
#               "__name__": "node_memory_MemTotal_bytes",
#               "alias": "datacenteraggregation",
#               "cluster": "F1C3",
#               "datacenter": "de-kae-bs-esxi-live",
#               "instance": "localhost:9100"
#             },
#             "values": [
#               [
#                 1698678900,
#                 "6216773632"
#               ],
#               [
#                 1698678960,
#                 "6216773632"
#               ],
#               [
#                 1698679020,
#                 "6216773632"
#               ],
#               [
#                 1698679080,
#                 "6216773632"
#               ],
#               [
#                 1698679140,
#                 "6216773632"
#               ],
#               [
#                 1698679200,
#                 "6216773632"
#               ]
#             ]
#          }
#         ]
#       }
#     }
#     """
#
#     handler = FlatJsonHandler()
#     data = handler.loads(test_json)
#     df = pd.DataFrame(data)
#     assert df.shape == (24, 12)
#
#     assert df.shape[0] == df.drop_duplicates().shape[0]
#
#
# # def test_incomplete_json():
# #     test_json = '{"HostingJira::12255":{"expand":"names,schema","issues":[{"expand":"operations,versionedRepresentations,editmeta,changelog,renderedFields","fields":{"created":"2023-01-13T12:22:07.000+0000","priority":{"iconUrl":"https://hosting-jira.1and1.org/images/icons/help_16.gif","id":"10000","name":"Undefined","self":"https://hosting-jira.1and1.org/rest/api/2/priority/10000"},"resolution":null,"resolutiondate":null,"status":{"description":"Yeswewilldoit!","iconUrl":"https://hosting-jira.1and1.org/images/icons/statuses/generic.png","id":"10302","name":"Selected","self":"https://hosting-jira.1and1.org/rest/api/2/status/10302","statusCategory":{"colorName":"inprogress","id":4,"key":"indeterminate","name":"InProgress","self":"https://hosting-jira.1and1.org/rest/api/2/statuscategory/4"}},"summary":"OSdetailsnotstoredinDaveifaDIMcallfails","updated":"2024-01-15T10:07:01.000+0000"},"id":"1577404","key":"ITOVC-286","self":"https://hosting-jira.1and1.org/rest/api/2/issue/1577404"}],"maxResults":50,"startAt":0,"total":1},"HostingJira::16286":{"expand":"schema,names","issues":[{"expand":"operations,versionedRepresentations,editmeta,changelog,renderedFields","fields":{"created":"2024-01-31T21:37:53.000+0000","priority":{"iconUrl":"https://hosting-jira.1and1.org/images/icons/priorities/minor.svg","id":"4","name":"Minor","self":"https://hosting-jira.1and1.org/rest/api/2/priority/4"},"resolution":{"description":"Theproblemisaduplicateofanexistingissue.","id":"10002","name":"Duplicate","self":"https://hosting-jira.1and1.org/rest/api/2/resolution/10002"},"resolutiondate":"2024-02-01T11:03:02.000+0000","status":{"description":"Aresolutionhasbeentaken,anditisawaitingverificationbyreporter.Fromhereissuesareeitherreopened,orareclosed.","iconUrl":"https://hosting-jira.1and1.org/images/icons/statuses/resolved.png","id":"5","name":"Resolved","self":"https://hosting-jira.1and1.org/rest/api/2/status/5","statusCategory":{"colorName":"success","id":3,"key":"done","name":"Done","self":"https://hosting-jira.1and1.org/rest/api/2/statuscategory/3"}},"summary":"UnabletosetupemailasIMAPinemailclients","updated":"2024-02-01T11:08:48.000+0000"},"id":"3599566","key":"BUG-127758","self":"https://hosting-jira.1and1.org/rest/api/2/issue/3599566"},{"expand":"operations,versionedRepresentations,editmeta,changelog,renderedFields","fields":{"created":"2024-01-31T19:16:59.000+0000","priority":{"iconUrl":"https://hosting-jira.1and1.org/images/icons/priorities/minor.svg","id":"4","name":"Minor","self":"https://hosting-jira.1and1.org/rest/api/2/priority/4"},"resolution":{"description":"Theproblemisaduplicateofanexistingissue.","id":"10002","name":"Duplicate","self":"https://hosting-jira.1and1.org/rest/api/2/resolution/10002"},"resolutiondate":"2024-02-01T11:07:31.000+0000","status":{"description":"Theissueisconsideredfinished,theresolutioniscorrect.Issueswhichareclosedcanbereopened.","iconUrl":"https://hosting-jira.1and1.org/images/icons/statuses/closed.png","id":"6","name":"Closed","self":"https://hosting-jira.1and1.org/rest/api/2/status/6","statusCategory":{"colorName":"success","id":3,"key":"done","name":"Done","self":"https://hosting-jira.1and1.org/rest/api/2/statuscategory/3"}},"summary":"IMAPconfigurationdoesn\'tworkwithamailbox","updated":"2024-02-02T12:21:56.000+0000"},"id":"3599545","key":"BUG-127745","self":"https://hosting-jira.1and1.org/rest/api/2/issue/3599545"},{"expand":"operations,versionedRepresentations,editmeta,changelog,renderedFields","fields":{"created":"2024-01-31T19:11:19.000+0000","priority":{"iconUrl":"https://hosting-jira.1and1.org/images/icons/priorities/minor.svg","id":"4","name":"Minor","self":"https://hosting-jira.1and1.org/rest/api/2/priority/4"},"resolution":{"description":"Workhasbeencompletedonthisissue.Afixforthisissueischeckedintothetreeandtested.","id":"10000","name":"Done/Fixed","self":"https://hosting-jira.1and1.org/rest/api/2/resolution/10000"},"resolutiondate":"2024-02-01T08:34:32.000+0000","status":{"description":"Theissueisconsideredfinished,theresolutioniscorrect.Issueswhichareclosedcanbereopened.","iconUrl":"https://hosting-jira.1and1.org/images/icons/statuses/closed.png","id":"6","name":"Closed","self":"https://hosting-jira.1and1.org/rest/api/2/status/6","statusCategory":{"colorName":"success","id":3,"key":"done","name":"Done","self":"https://hosting-jira.1and1.org/rest/api/2/statuscategory/3"}},"summary":"Customercannotdeletemailbox","updated":"2024-02-01T09:10:44.000+0000"},"id":"3599542","key":"BUG-127742","self":"https://hosting-jira.1and1.org/rest/api/2/issue/3599542"},{"expand":"operations,versionedRepresentations,editmeta,changelog,renderedFields","fields":{"created":"2024-01-31T18:01:16.000+0000","priority":{"iconUrl":"https://hosting-jira.1and1.org/images/icons/priorities/minor.svg","id":"4","name":"Minor","self":"https://hosting-jira.1and1.org/rest/api/2/priority/4"},"resolution":{"description":"Workhasbeencompletedonthisissue.Afixforthisissueischeckedintothetreeandtested.","id":"10000","name":"Done/Fixed","self":"https://hosting-jira.1and1.org/rest/api/2/resolution/10000"},"resolutiondate":"2024-02-02T09:25:28.000+0000","status":{"description":"Theissueisconsideredfinished,theresolutioniscorrect.Issueswhichareclosedcanbereopened.","iconUrl":"https://hosting-jira.1and1.org/images/icons/statuses/closed.png","id":"6","name":"Closed","self":"https://hosting-jira.1and1.org/rest/api/2/status/6","statusCategory":{"colorName":"success","id":3,"key":"done","name":"Done","self":"https://hosting-jira.1and1.org/rest/api/2/statuscategory/3"}},"summary":"Spoofingmailing-pleasesetanexception","updated":"2024-02-02T09:51:13.000+0000"},"id":"3599642","key":"BUG-127728","self":"https://hosting-jira.1and1.org/rest/api/2/issue/3599642"},{"expand":"operations,versionedRepresentations,editmeta,changelog,renderedFields","fields":{"created":"2024-01-31T17:56:10.000+0000","priority":{"iconUrl":"https://hosting-jira.1and1.org/images/icons/priorities/minor.svg","id":"4","name":"Minor","self":"https://hosting-jira.1and1.org/rest/api/2/priority/4"},"resolution":{"description":"Workhasbeencompletedonthisissue.Afixforthisissueischeckedintothetreeandtested.","id":"10000","name":"Done/Fixed","self":"https://hosting-jira.1and1.org/rest/api/2/resolution/10000"},"resolutiondate":"2024-02-01T10:34:33.000+0000","status":{"description":"Theissueisconsideredfinished,theresolutioniscorrect.Issueswhichareclosedcanbereopened.","iconUrl":"https://hosting-jira.1and1.org/images/icons/statuses/closed.png","id":"6","name":"Closed","self":"https://hosting-jira.1and1.org/rest/api/2/status/6","statusCategory":{"colorName":"success","id":3,"key":"done","name":"Done","self":"https://hosting-jira.1and1.org/rest/api/2/statuscategory/3"}},"summary":"Reminder:UpdateyouremailsettingsbyJanuary28,2024","updated":"2024-02-01T15:37:58.000+0000"},"id":"3599638","key":"BUG-127724","self":"https://hosting-jira.1and1.org/rest/api/2/issue/3599638"},{"expand":"operations,versionedRepresentations,editmeta,changelog,renderedFields","fields":{"created":"2024-01-31T17:28:37.000+0000","priority":{"iconUrl":"https://hosting-jira.1and1.org/images/icons/priorities/minor.svg","id":"4","name":"Minor","self":"https://hosting-jira.1and1.org/rest/api/2/priority/4"},"resolution":{"description":"Workhasbeencompletedonthisissue.Afixforthisissueischeckedintothetreeandtested.","id":"10000","name":"Done/Fixed","self":"https://hosting-jira.1and1.org/rest/api/2/resolution/10000"},"resolutiondate":"2024-02-02T09:25:56.000+0000","status":{"description":"Theissueisconsideredfinished,theresolutioniscorrect.Issueswhichareclosedcanbereopened.","iconUrl":"https://hosting-jira.1and1.org/images/icons/statuses/closed.png","id":"6","name":"Closed","self":"https://hosting-jira.1and1.org/rest/api/2/status/6","statusCategory":{"colorName":"success","id":3,"key":"done","name":"Done","self":"https://hosting-jira.1and1.org/rest/api/2/statuscategory/3"}},"summary":"Addmailaliasesforspoofingchange","updated":"2024-02-07T09:50:24.000+0000"},"id":"3599616","key":"BUG-127719","self":"https://hosting-jira.1and1.org/rest/api/2/issue/3599616"},{"expand":"operations,versionedRepresentations,editmeta,changelog,renderedFields","fields":{"created":"2024-01-31T16:56:56.000+0000","priority":{"iconUrl":"https://hosting-jira.1and1.org/images/icons/help_16.gif","id":"10000","name":"Undefined","self":"https://hosting-jira.1and1.org/rest/api/2/priority/10000"},"resolution":{"description":"Workhasbeencompletedonthisissue.Afixforthisissueischeckedintothetreeandtested.","id":"10000","name":"Done/Fixed","self":"https://hosting-jira.1and1.org/rest/api/2/resolution/10000"},"resolutiondate":"2024-02-02T09:24:26.000+0000","status":{"description":"Theissueisconsideredfinished,theresolutioniscorrect.Issueswhichareclosedcanbereopened.","iconUrl":"https://hosting-jira.1and1.org/images/icons/statuses/closed.png","id":"6","name":"Closed","self":"https://hosting-jira.1and1.org/rest/api/2/status/6","statusCategory":{"colorName":"success","id":3,"key":"done","name":"Done","self":"https://hosting-jira.1and1.org/rest/api/2/statuscategory/3"}},"summary":"[MailSpoofing]Exception/whitelistingrequested","updated":"2024-02-02T09:44:27.000+0000"},"id":"3599296","key":"BUG-127706","self":"https://hosting-jira.1and1.org/rest/api/2/issue/3599296"},{"expand":"operations,versionedRepresentations,editmeta,changelog,renderedFields","fields":{"created":"2024-01-31T15:59:56.000+0000","priority":{"iconUrl":"https://hosting-jira.1and1.org/images/icons/priorities/minor.svg","id":"4","name":"Minor","self":"https://hosting-jira.1and1.org/rest/api/2/priority/4"},"resolution":{"description":"Workhasbeencompletedonthisissue.Afixforthisissueischeckedintothetreeandtested.","id":"10000","name":"Done/Fixed","self":"https://hosting-jira.1and1.org/rest/api/2/resolution/10000"},"resolutiondate":"2024-02-02T09:29:01.000+0000","status":{"description":"Theissueisconsideredfinished,theresolutioniscorrect.Issueswhichareclosedcanbereopened.","iconUrl":"https://hosting-jira.1and1.org/ima'
# #     handler = FlatJsonHandler()
# #     data = handler.loads(test_json)
# #     df = pd.DataFrame(data)
#
# def test_flat_json_array():
#     # test_json = open("vuln-scorecard-2023-11-29.json").read()
#     test_json = open("node_memory_MemTotal_bytes_20231030_151500.json").read()
#     test_json = open("HostingJira-2024-02-12.json").read()
#     # test_json = json.dumps([{"pluginID": "20007", "severity": {"id": "4", "name": "Critical", "description": "Critical Severity"}, "hasBeenMitigated": "0", "acceptRisk": "0", "recastRisk": "0", "ip": "10.4.129.140", "uuid": "", "port": "443", "protocol": "TCP", "pluginName": "SSL Version 2 and 3 Protocol Detection", "firstSeen": "1678967240", "lastSeen": "1701257088", "exploitAvailable": "No", "exploitEase": "", "exploitFrameworks": "", "synopsis": "The remote service encrypts traffic using a protocol with known weaknesses.", "description": "The remote service accepts connections encrypted using SSL 2.0 and/or SSL 3.0. These versions of SSL are affected by several cryptographic flaws, including:\n\n  - An insecure padding scheme with CBC ciphers.\n\n  - Insecure session renegotiation and resumption schemes.\n\nAn attacker can exploit these flaws to conduct man-in-the-middle attacks or to decrypt communications between the affected service and clients.\n\nAlthough SSL/TLS has a secure means for choosing the highest supported version of the protocol (so that these versions will be used only if the client or server support nothing better), many web browsers implement this in an unsafe way that allows an attacker to downgrade a connection (such as in POODLE). Therefore, it is recommended that these protocols be disabled entirely.\n\nNIST has determined that SSL 3.0 is no longer acceptable for secure communications. As of the date of enforcement found in PCI DSS v3.1, any version of SSL will not meet the PCI SSC's definition of 'strong cryptography'.", "solution": "Consult the application's documentation to disable SSL 2.0 and 3.0.\nUse TLS 1.2 (with approved cipher suites) or higher instead.", "seeAlso": "https://www.schneier.com/academic/paperfiles/paper-ssl.pdf\nhttp://www.nessus.org/u?b06c7e95\nhttp://www.nessus.org/u?247c4540\nhttps://www.openssl.org/~bodo/ssl-poodle.pdf\nhttp://www.nessus.org/u?5d15ba70\nhttps://www.imperialviolet.org/2014/10/14/poodle.html\nhttps://tools.ietf.org/html/rfc7507\nhttps://tools.ietf.org/html/rfc7568", "riskFactor": "Critical", "stigSeverity": "", "vprScore": "", "vprContext": "[]", "baseScore": "10.0", "temporalScore": "", "cvssVector": "AV:N/AC:L/Au:N/C:C/I:C/A:C", "cvssV3BaseScore": "9.8", "cvssV3TemporalScore": "", "cvssV3Vector": "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", "cpe": "", "vulnPubDate": "-1", "patchPubDate": "-1", "pluginPubDate": "1129118400", "pluginModDate": "1649073600", "checkType": "remote", "version": "1.34", "cve": "", "bid": "", "xref": "", "pluginText": "<plugin_output>\n- SSLv3 is enabled and the server supports at least one cipher.\n\tExplanation: TLS 1.0 and SSL 3.0 cipher suites may be used with SSLv3\n\n\n  Medium Strength Ciphers (&gt; 64-bit and &lt; 112-bit key, or 3DES)\n\n    Name                          Code             KEX           Auth     Encryption             MAC\n    ----------------------        ----------       ---           ----     ---------------------  ---\n    EDH-RSA-DES-CBC3-SHA                           DH            RSA      3DES-CBC(168)          SHA1\n    ECDHE-RSA-DES-CBC3-SHA                         ECDH          RSA      3DES-CBC(168)          SHA1\n    DES-CBC3-SHA                                   RSA           RSA      3DES-CBC(168)          SHA1\n\n  High Strength Ciphers (&gt;= 112-bit key)\n\n    Name                          Code             KEX           Auth     Encryption             MAC\n    ----------------------        ----------       ---           ----     ---------------------  ---\n    DHE-RSA-AES128-SHA                             DH            RSA      AES-CBC(128)           SHA1\n    DHE-RSA-AES256-SHA                             DH            RSA      AES-CBC(256)           SHA1\n    DHE-RSA-CAMELLIA128-SHA                        DH            RSA      Camellia-CBC(128)      SHA1\n    DHE-RSA-CAMELLIA256-SHA                        DH            RSA      Camellia-CBC(256)      SHA1\n    DHE-RSA-SEED-SHA                               DH            RSA      SEED-CBC(128)          SHA1\n    ECDHE-RSA-AES128-SHA                           ECDH          RSA      AES-CBC(128)           SHA1\n    ECDHE-RSA-AES256-SHA                           ECDH          RSA      AES-CBC(256)           SHA1\n    AES128-SHA                                     RSA           RSA      AES-CBC(128)           SHA1\n    AES256-SHA                                     RSA           RSA      AES-CBC(256)           SHA1\n    CAMELLIA128-SHA                                RSA           RSA      Camellia-CBC(128)      SHA1\n    CAMELLIA256-SHA                                RSA           RSA      Camellia-CBC(256)      SHA1\n    IDEA-CBC-SHA                                   RSA           RSA      IDEA-CBC(128)          SHA1\n    SEED-SHA                                       RSA           RSA      SEED-CBC(128)          SHA1\n    DHE-RSA-AES128-SHA256                          DH            RSA      AES-CBC(128)           SHA256\n    DHE-RSA-AES256-SHA256                          DH            RSA      AES-CBC(256)           SHA256\n    ECDHE-RSA-AES128-SHA256                        ECDH          RSA      AES-CBC(128)           SHA256\n    ECDHE-RSA-AES256-SHA384                        ECDH          RSA      AES-CBC(256)           SHA384\n    RSA-AES128-SHA256                              RSA           RSA      AES-CBC(128)           SHA256\n    RSA-AES256-SHA256                              RSA           RSA      AES-CBC(256)           SHA256\n\nThe fields above are :\n\n  {Tenable ciphername}\n  {Cipher ID code}\n  Kex={key exchange}\n  Auth={authentication}\n  Encrypt={symmetric encryption method}\n  MAC={message authentication code}\n  {export flag}\n</plugin_output>", "dnsName": "et-0.es-lgr-lpng1cs19.oneandone.net", "macAddress": "", "netbiosName": "", "operatingSystem": "Linux Kernel 2.6", "ips": "10.4.129.140", "recastRiskRuleComment": "", "acceptRiskRuleComment": "", "hostUniqueness": "repositoryID,ip,dnsName", "hostUUID": "", "acrScore": "", "keyDrivers": "", "assetExposureScore": "", "uniqueness": "repositoryID,ip,dnsName", "family": {"id": "24", "name": "Service detection", "type": "active"}, "repository": {"id": "136", "name": "9921436084", "description": "Updated by Tenable script at 2023-11-22 05:13:41.650692", "dataFormat": "IPv4"}, "pluginInfo": "20007 (443/6) SSL Version 2 and 3 Protocol Detection"}])
#     time_custom_handler = perf_counter()
#     for _ in range(10):
#         handler = FlatJsonHandler()
#         data = handler.loads(test_json)
#         df = pd.DataFrame(data)
#     print(perf_counter() - time_custom_handler)
#
#     time_pandas_normalize = perf_counter()
#     for _ in range(10):
#         df2 = recursive_explode_flatten_dataframe(pd.json_normalize(orjson.loads(test_json)))
#     print(perf_counter() - time_pandas_normalize)
