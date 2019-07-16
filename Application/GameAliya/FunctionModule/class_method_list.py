	async def increase_item_quantity(self, item_id, item_quantity):
		try:
			self.item_list_count += 1
			gasql("UPDATE bag SET " + item_id + "=" + item_id + " +" + item_quantity + " WHERE unique_id='" + self.unique_id + "'")
			result_quantity = gasql("select " + item_id + " from bag where  unique_id='" + self.unique_id + "'")
			dc = {"item" + str(self.item_list_count): [item_id, result_quantity[0][0]]}
			return dc
		except:
			return {"scroll_error": "1"}
	async def increase_supplies(self, message_info):
		message_dic = json.loads(message_info, encoding="utf-8")
		title_list = self.__get_title_list("bag")
		content_list = self.__get_content_list("bag")
		return_dic = {}
		for key in message_dic["data"].keys():
			if key not in title_list:
	async def random_gift(self, message_info):
		print("[BagSystemClass][_random_gift] -> 方法未写！")
	async def get_all_supplies(self, message_info):
		"""
		give all skills' level to client
		"""
		table, result = gasql_t("select * from bag where unique_id='" + self.unique_id + "'")
		data_dic = {}
		for i in range(1, len(result[0])):
			data_dic.update({"item" + str(i): [table[i][0], result[0][i]]})
	async def level_up_scroll(self, unique_id,scroll_id_name):
		print("aaaaa")
		return
		message_dic = eval(message_info)
		scroll_id_name = ""
		level_up_scroll_name = ""
		if "scroll_skill_10" in message_dic["data"].keys():
			scroll_id_name = "scroll_skill_10"
			level_up_scroll_name = "scroll_skill_30"
			quantity = message_dic["data"]["scroll_skill_10"]
		elif "scroll_skill_30" in message_dic["data"].keys():
			scroll_id_name = "scroll_skill_30"
			level_up_scroll_name = "scroll_skill_100"
			quantity = message_dic["data"]["scroll_skill_30"]
		else:
			return mc("2", "illegal scroll level up ")
		sql_result = gasql(
			"select " + scroll_id_name + "," + level_up_scroll_name + " from bag where unique_id='" + self.unique_id + "'")
		current_scroll = sql_result[0][0]
		level_up_scroll = sql_result[0][1]
		if current_scroll < 3 or int(quantity) < 3:
			return mc("1", "scroll is not eought", {"item1": [str(scroll_id_name), str(current_scroll)],
			                                        "item2": [str(level_up_scroll_name), str(level_up_scroll)]})
		else:
			gasql("UPDATE bag SET " + scroll_id_name + "= " + scroll_id_name + "-" + str(
				3) + " WHERE unique_id='" + self.unique_id + "'")
			gasql("UPDATE bag SET " + level_up_scroll_name + "= " + level_up_scroll_name + "+" + str(
				1) + " WHERE unique_id='" + self.unique_id + "'")
			return mc("0", "level up success", {"item1": [str(scroll_id_name), str(current_scroll - 3)],
			                                    "item2": [str(level_up_scroll_name), str(level_up_scroll + 1)]})
	async def get_content_list(self, table_name) -> list:
		sql_result = gasql("select * from " + table_name + " where  unique_id='" + self.unique_id + "'")
		print("[BagSystemClass][__get_table_content] -> sql_result:" + str(sql_result))
		return list(sql_result[0])
	async def get_skill_level(self, skill_id):
		"""
		get skill level
		"""
		sql_result = gasql("select " + skill_id + " from skill where unique_id='" + self.unique_id + "'")
		return sql_result[0][0]
	def sql_str_operating(self, table_name, title_list, content_list) -> str:
		heard_str = "UPDATE %s SET " % table_name
		end_str = " where unique_id='%s'" % self.unique_id
		result_str = ""
		for i in range(len(title_list)):
			if title_list[i] != "unique_id":
				if i != len(title_list) - 1:
					result_str += title_list[i] + "=%s, "
				else:
					result_str += title_list[i] + "=%s"
		result_str = heard_str + result_str + end_str
		print("[BagSystemClass][__sql_str_operating] -> result_str:" + result_str)
		return result_str % tuple(content_list)
	def get_title_list(self, table_name) -> list:
		sql_result = gasql("desc " + table_name + ";")
		col_list = []
		for col in sql_result:
			col_list.append(col[0])
		return col_list
	# It is helpful to define a private method that you can simply pass
	# an SQL command as a string and it will execute. Call this method
	# whenever you issue an SQL statement.
