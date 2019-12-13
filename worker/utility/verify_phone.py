#!/usr/bin/env python
# coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json

ACCESS_KEY_ID = "LTAI4FvgaWfboqy1bVtAcxmY"
ACCESS_KEY_SECRET = "OarxNMURFi6bu2oQeHHw1UbFPA9dBf"
client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, 'cn-hangzhou')
request = CommonRequest()


def send_verification(to, code):
	"""
	:param to: send phone
	:param code: verification code
	"""
	request.set_accept_format('json')
	request.set_domain('dysmsapi.aliyuncs.com')
	request.set_method('POST')
	request.set_protocol_type('https')  # https | http
	request.set_version('2017-05-25')
	request.set_action_name('SendSms')

	request.add_query_param('RegionId', "cn-hangzhou")
	request.add_query_param('PhoneNumbers', to)
	request.add_query_param('SignName', "陆逊互娱")
	request.add_query_param('TemplateCode', "SMS_180049475")
	request.add_query_param('TemplateParam', "{\"code\":\"%s\"}" % code)
	response = client.do_action(request)
	res = json.loads(response)
	return res["Code"]


if __name__ == '__main__':
	send_verification("18323019610", "123456")
