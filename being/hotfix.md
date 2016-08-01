GET /hotfix/{device}?version=1.0.1 
device = ios or android

{
	md5: xxxx,
	url: http://s0.nihao.com/hotfix/{md5}
}

list:

version
filename
device
note
created_at
updated_at

form:

ver
file


GET　/v1/user/brief-list?id[]=1&id[]=2

response:
{
	"10" : {
		'uid' : 10
		'avatar' : 'http://xxx.png',
		'fullname': 'xxx',
		'intro' : 'xxx',
		'sex' : 1,
		'age' : 23,
		'truthful': 1
	},

	"11" : {...}
｝

----------


GET /v1/components

response:
[
	{
		name: "itinerary",
		type: "native", // or "html"
		link: "being:/xxx"
		title: "xxx"
		subtitle: "yyyy"
		icon: "http://s0.nihao.com/components/itinerary.png"
	},
	{...}
]

POST /v1/blacklist?uid=123