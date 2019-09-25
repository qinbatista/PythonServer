'''
lottery.py
'''
import random

from module import common

L = \
{
	"WEAPON" : {
		"cost" : {
			"COIN" : 100
		},
		"tiers" : ["tier1", "tier2"],
		"weights" : {
			"BASIC" : [0.6, 0.4]
		},
		"items" : {
			"tier1" : [1, 2, 3],
			"tier2" : [4, 5, 6, 7]
		}
	}
}

async def random_gift(uid, rewardgroup, tier, **kwarg):
	tier = (random.choices(L[rewardgroup.name]['tiers'], L[rewardgroup.name]['weights'][tier.name]))[0]
	gift = (random.choices(L[rewardgroup.name]['items'][tier]))[0]
	return common.mt(0, 'success', {'tier' : tier, 'gift' : gift})
