from jinja2 import Template
from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader('./J2_temps')
env = Environment(loader=file_loader)

template1 = env.get_template('Post_staging_template.j2')
PS_dict = {}
PS_dict['PS_TEMPLATE_NAME'] = 'SASASASA'
PS_dict['LAN_INTF'] = 'vni-0/4'

print template1.render(PS = PS_dict)


# abc = {
#     'dg_name' : "sadadsad",
#     'org_name' : "12324",
#     'xycvc' : "999"
# }



# DG_template_body = """{
# 	"device-group": {
# 		"name": {{ dg.dg_name }},
# 		"dg:organization": {{ dg.org_name }},
# 		"dg:enable-2factor-auth": false,
# 		"dg:enable-staging-url": false,
# 		"dg:poststaging-template": {{ dg.ps_name }}
# 	}
# }"""
#
#
# T = Template(DG_template_body)
# print T.render(dg=abc)