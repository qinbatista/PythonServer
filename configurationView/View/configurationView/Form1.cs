﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.IO;
using Microsoft.VisualBasic;
using System.Collections;

namespace configurationView
{
    public partial class MainForm : Form
    {
        #region 配置信息
        int PanelX = 0;
        int PanelY = 141;
        int width = 1178;
        int height = 505;
        StreamReader stream;
        JsonTextReader reader;
        //DirectoryInfo di1 = new DirectoryInfo(Directory.GetCurrentDirectory());
        static string main_path = "..//..//..//..//..//configuration//";
        string current_version = "0";
        string old_version = "0";
        string new_version;
        JObject json;
        string json_version = main_path + "//config_timer_setting.json";
        /// <summary>
        /// client configuration
        /// </summary>
        string clien_path = main_path + "client//";
        string level_enemy_layouts_config = main_path + "client//{0}//level_enemy_layouts_config.json";
        JObject client_stage_json;
        string level_enemy_layouts_config_tower = main_path + "client//{0}//level_enemy_layouts_config_tower.json";
        string monster_config = main_path + "client//{0}//monster_config.json";
        /// <summary>
        /// sever configuration
        /// </summary>
        string server_path = main_path + "server//";
        string entry_consumables_config = main_path + "server//{0}//entry_consumables_config.json";
        string hang_reward_config = main_path + "server//{0}//hang_reward_config.json";
        string lottery_config = main_path + "server//{0}//lottery_config.json";
        string mysql_data_config = main_path + "server//{0}//mysql_data_config.json";
        string player_config = main_path + "server//{0}//player_config.json";
        string skill_level_up_config = main_path + "server//{0}//skill_level_up_config.json";
        string stage_reward_config = main_path + "server//{0}//stage_reward_config.json";
        string weapon_config = main_path + "server//{0}//weapon_config.json";
        string world_distribution = main_path + "server//{0}//world_distribution.json";
        //string ex = String.Format("{ 0}", "ex");
        #endregion
        public MainForm()
        {
            InitializeComponent();
            Height = 200;
            StartPosition = FormStartPosition.CenterScreen;
            stream = File.OpenText(json_version);
            reader = new JsonTextReader(stream);
            json = (JObject)JToken.ReadFrom(reader);
            stream.Close();
            reader.Close();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            foreach (var date in json)
            {
                if (float.Parse(date.Value["server"].ToString()) > float.Parse(current_version))
                {
                    current_version = date.Value["server"].ToString();
                }
                //this.VersionOption.Items.Add(date.Key + ":" + date.Value);
                VersionOption.Items.Add(date.Value["server"]);
            }
        }

        private void Add_Click(object sender, EventArgs e)
        {
            String version_str = Interaction.InputBox("请输入版本号，将会拷贝最新版本作为当前版本", "输入密码", "");
            try
            {
                float version = float.Parse(version_str);
                DialogResult result = MessageBox.Show(text: "是否确定使用版本号：" + version_str, caption: "确认提示", MessageBoxButtons.YesNo, MessageBoxIcon.Information);
                if (result.ToString().Equals("Yes"))
                {
                    new_version = version_str;
                    // client 操作的代码
                    if (!Directory.Exists(clien_path + new_version))
                    {
                        Directory.CreateDirectory(clien_path + new_version);
                        string[] fileList = Directory.GetFileSystemEntries(clien_path + current_version);
                        foreach (string file in fileList)
                        {
                            File.Copy(file, clien_path + new_version + "//" + Path.GetFileName(file));
                        }
                    }
                    else
                    {
                        result = MessageBox.Show(text: String.Format("客服端版本{0}已存在，是否添加客服端版本{1}中没有的文件", new_version, current_version), caption: "确认提示", MessageBoxButtons.YesNo, MessageBoxIcon.Information);
                        if (result.ToString().Equals("Yes"))
                        {
                            string[] fileList = Directory.GetFileSystemEntries(clien_path + current_version);
                            foreach (string file in fileList)
                            {
                                if (!File.Exists(clien_path + new_version + "//" + Path.GetFileName(file)))
                                {
                                    File.Copy(file, clien_path + new_version + "//" + Path.GetFileName(file));
                                }
                            }
                        }
                    }
                    // server 操作的代码
                    if (!Directory.Exists(server_path + new_version))
                    {
                        Directory.CreateDirectory(server_path + new_version);
                        string[] fileList = Directory.GetFileSystemEntries(server_path + current_version);
                        foreach (string file in fileList)
                        {
                            File.Copy(file, server_path + new_version + "//" + Path.GetFileName(file));
                        }
                    }
                    else
                    {
                        result = MessageBox.Show(text: String.Format("服务端版本{0}已存在，是否添加服务端版本{1}中没有的文件", new_version, current_version), caption: "确认提示", MessageBoxButtons.YesNo, MessageBoxIcon.Information);
                        if (result.ToString().Equals("Yes"))
                        {
                            string[] fileList = Directory.GetFileSystemEntries(server_path + current_version);
                            foreach (string file in fileList)
                            {
                                if (!File.Exists(server_path + new_version + "//" + Path.GetFileName(file)))
                                {
                                    File.Copy(file, server_path + new_version + "//" + Path.GetFileName(file));
                                }
                            }
                        }
                    }
                    //修改config_timer_setting.json文件的代码
                    try
                    {
                        JObject temp_json = new JObject();
                        temp_json.Add("client", new_version);
                        temp_json.Add("server", new_version);
                        json.Add(dateTimePicker.Value.ToString("yyyy-MM-dd"), temp_json);
                        File.WriteAllText(json_version, json.ToString());
                        MessageBox.Show(text: "添加成功！", caption: "提示信息", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                    catch
                    {
                        json[DateTime.Now.ToString("yyyy-MM-dd")]["client"] = new_version;
                        json[DateTime.Now.ToString("yyyy-MM-dd")]["server"] = new_version;
                        File.WriteAllText(json_version, json.ToString());
                        MessageBox.Show(text: "json文件中已存在此版本！", caption: "提示信息", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                    current_version = new_version;
                    VersionOption.Items.Add(new_version);
                    //this.FunctionOption.Items.Add(json.ToString());
                }
            }
            catch
            {
                MessageBox.Show(text: "版本信息输入错误！", caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        #region Panel1
        private void ComboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            try
            {
                comboBox2.Items.Clear();
                switch (comboBox1.SelectedItem.ToString())
                {
                    case "普通关卡":
                        {
                            stream = File.OpenText(String.Format(level_enemy_layouts_config, current_version));
                            reader = new JsonTextReader(stream);
                            client_stage_json = (JObject)JToken.ReadFrom(reader);
                            stream.Close();
                            reader.Close();
                            int i = 1;  // client_stage_json["enemyLayouts"][i-1].ToString()
                            foreach (var item in client_stage_json["enemyLayouts"])
                            {
                                comboBox2.Items.Add(i.ToString());
                                i++;
                            }
                        }
                        break;
                    case "冲塔关卡":
                        {
                            stream = File.OpenText(String.Format(level_enemy_layouts_config_tower, current_version));
                            reader = new JsonTextReader(stream);
                            client_stage_json = (JObject)JToken.ReadFrom(reader);
                            stream.Close();
                            reader.Close();
                            int i = 1;  // client_stage_json["enemyLayouts"][i-1].ToString()
                            foreach (var item in client_stage_json["enemyLayouts"])
                            {
                                comboBox2.Items.Add(i.ToString());
                                i++;
                            }
                        }
                        break;
                }
                old_version = current_version;
            }
            catch
            {
                MessageBox.Show(text: String.Format("不存在版本{0}！", current_version), caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void VersionOption_SelectedIndexChanged(object sender, EventArgs e)
        {
            current_version = VersionOption.SelectedItem.ToString();
        }

        private void Button1_Click(object sender, EventArgs e)
        {
            // delete
            try
            {
                client_stage_json["enemyLayouts"][comboBox2.SelectedIndex].Remove();
                File.WriteAllText(String.Format(level_enemy_layouts_config, current_version), client_stage_json.ToString());
                comboBox2.Items.Remove(comboBox2.SelectedItem.ToString());
                MessageBox.Show(text: String.Format("删除成功！", current_version), caption: "提示信息", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch
            {
                MessageBox.Show("未选择关卡，请选择关卡后再删除！", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void Button2_Click(object sender, EventArgs e)
        {
            // add
            try
            {
                JArray array = (JArray)client_stage_json["enemyLayouts"];
                array.Add(client_stage_json["enemyLayouts"][comboBox2.Items.Count - 1]);
                client_stage_json["enemyLayouts"] = array;
                File.WriteAllText(String.Format(level_enemy_layouts_config, current_version), client_stage_json.ToString());
                comboBox2.Items.Add(comboBox2.Items.Count + 1);
                comboBox2.SelectedIndex = comboBox2.Items.IndexOf(comboBox2.Items.Count);
                MessageBox.Show(text: "关卡添加成功 ！", caption: "消息提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch
            {
                MessageBox.Show(text: String.Format("未选择关卡类型！", current_version), caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
        private void ComboBox2_SelectedIndexChanged(object sender, EventArgs e)
        {
            if(old_version.Equals(current_version))
            {
                SettingWaveNumber();
                SettingPanel((JObject)client_stage_json["enemyLayouts"][comboBox2.SelectedIndex]["enemyLayout"][0]);
            }
            else
            {
                MessageBox.Show(text: "请重新选择关卡类型 ！", caption: "消息提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }
        private void SettingWaveNumber()
        {
            JArray array = (JArray)client_stage_json["enemyLayouts"][comboBox2.SelectedIndex]["enemyLayout"];
            WaveNumber.Maximum = array.Count;
        }
        /// <summary>
        /// 设置panel下所有的控件属性
        /// </summary>
        /// <param name="enemy"></param>
        private void SettingPanel(JObject enemy)
        {
            TotalTime.Value = (decimal)enemy["totalTime"];
            ColdDownTime.Value = (decimal)enemy["coldDownTime"];
            IsPreWaveFinish.Checked = (bool)enemy["isPreWaveFinish"];

            comboBox3.Items.Clear();
            comboBox4.Items.Clear();
            JArray array = (JArray)enemy["enemyList"];
            foreach (var item in array)
            {
                comboBox3.Items.Add(item["enemysPrefString"].ToString());
            }
            array = (JArray)enemy["SpawnPointStrings"];
            foreach (var item in array)
            {
                comboBox4.Items.Add(item.ToString());
            }
        }

        private void WaveNumber_ValueChanged(object sender, EventArgs e)
        {
            try
            {
                SettingPanel((JObject)client_stage_json["enemyLayouts"][comboBox2.SelectedIndex]["enemyLayout"][int.Parse(WaveNumber.Value.ToString()) - 1]);
            }
            catch
            {
                MessageBox.Show(text: "未选择关卡类型！暂无波数信息！", caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void ComboBox3_SelectedIndexChanged(object sender, EventArgs e)
        {
            JObject enemyLayout = (JObject)client_stage_json["enemyLayouts"][comboBox2.SelectedIndex]["enemyLayout"][int.Parse(WaveNumber.Value.ToString()) - 1];
            JArray array = (JArray)enemyLayout["enemyList"];
            numericUpDown3.Value = (decimal)array[comboBox3.SelectedIndex]["count"];
        }

        private void Button4_Click(object sender, EventArgs e)
        {
            // delete
            try
            {
                JArray array = (JArray)client_stage_json["enemyLayouts"][comboBox2.SelectedIndex]["enemyLayout"][int.Parse(WaveNumber.Value.ToString()) - 1]["enemyList"];
                if (array.Count == 1)
                {
                    MessageBox.Show(text: "最后一种怪，不可删除！", caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                else if (array.Count == 0)
                {
                    MessageBox.Show(text: "已没有怪物可以删除，可手动增加一种怪物再删除！", caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                else
                {
                    array[comboBox3.SelectedIndex].Remove();
                    client_stage_json["enemyLayouts"][comboBox2.SelectedIndex]["enemyLayout"][int.Parse(WaveNumber.Value.ToString()) - 1]["enemyList"] = array;
                    File.WriteAllText(String.Format(level_enemy_layouts_config, current_version), client_stage_json.ToString());
                    comboBox3.Items.Remove(comboBox3.SelectedItem.ToString());
                    numericUpDown3.Value = 0;
                    MessageBox.Show(text: String.Format("删除怪物成功！", current_version), caption: "提示信息", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
            catch
            {
                MessageBox.Show(text: String.Format("请选择一种怪后再删除！", current_version), caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
        private void Button3_Click(object sender, EventArgs e)
        {
            // add
            try {
                new MonsterAdd((JArray)client_stage_json["enemyLayouts"][comboBox2.SelectedIndex]["enemyLayout"][int.Parse(WaveNumber.Value.ToString()) - 1]["enemyList"], client_stage_json, String.Format(level_enemy_layouts_config, current_version), comboBox3).Show();
            }
            catch
            {
                MessageBox.Show(text: String.Format("未选择关卡数！", current_version), caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void Button6_Click(object sender, EventArgs e)
        {
            // delete
            try
            {
                JArray array = (JArray)client_stage_json["enemyLayouts"][comboBox2.SelectedIndex]["enemyLayout"][int.Parse(WaveNumber.Value.ToString()) - 1]["SpawnPointStrings"];
                if (array.Count == 1)
                {
                    MessageBox.Show(text: "最后一个出生点，不可删除！", caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                else if (array.Count == 0)
                {
                    MessageBox.Show(text: "已没有出生的可以删除，可手动增加一个出生点再删除！", caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                else
                {
                    array[comboBox4.SelectedIndex].Remove();
                    client_stage_json["enemyLayouts"][comboBox2.SelectedIndex]["enemyLayout"][int.Parse(WaveNumber.Value.ToString()) - 1]["SpawnPointStrings"] = array;
                    File.WriteAllText(String.Format(level_enemy_layouts_config, current_version), client_stage_json.ToString());
                    comboBox4.Items.Remove(comboBox4.SelectedItem.ToString());
                    MessageBox.Show(text: String.Format("删除成功！", current_version), caption: "提示信息", MessageBoxButtons.OK, MessageBoxIcon.Information);

                }
            }
            catch
            {
                MessageBox.Show(text: String.Format("请选择一个出生点后再删除！", current_version), caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void Button5_Click(object sender, EventArgs e)
        {
            try
            {
                string item = comboBox5.SelectedItem.ToString();
                if (comboBox4.Items.Contains(item))
                {
                    MessageBox.Show(text: String.Format("出生点已添加到该波怪物出生点中！", current_version), caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                else
                {
                    JArray array = (JArray)client_stage_json["enemyLayouts"][comboBox2.SelectedIndex]["enemyLayout"][int.Parse(WaveNumber.Value.ToString()) - 1]["SpawnPointStrings"];
                    array.Add(item);
                    File.WriteAllText(String.Format(level_enemy_layouts_config, current_version), client_stage_json.ToString());
                    comboBox4.Items.Add(item);
                    MessageBox.Show(text: String.Format("出生点{0}添加成功！", item), caption: "提示信息", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
            catch
            {
                MessageBox.Show(text: "请选择一个出生点后再添加！", caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void TotalTime_ValueChanged(object sender, EventArgs e)
        {
            try
            {
                if ((int)TotalTime.Value != 0)
                {
                    client_stage_json["enemyLayouts"][comboBox2.SelectedIndex]["enemyLayout"][int.Parse(WaveNumber.Value.ToString()) - 1]["totalTime"] = (int)TotalTime.Value;
                }
            }
            catch
            {
                MessageBox.Show("没有选择关卡数！", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void ColdDownTime_ValueChanged(object sender, EventArgs e)
        {
            try
            {
                if ((int)ColdDownTime.Value != 0)
                {
                    client_stage_json["enemyLayouts"][comboBox2.SelectedIndex]["enemyLayout"][int.Parse(WaveNumber.Value.ToString()) - 1]["coldDownTime"] = (int)ColdDownTime.Value;
                }
            }
            catch
            {
                MessageBox.Show("没有选择关卡数！", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void IsPreWaveFinish_CheckedChanged(object sender, EventArgs e)
        {
            try
            {
                client_stage_json["enemyLayouts"][comboBox2.SelectedIndex]["enemyLayout"][int.Parse(WaveNumber.Value.ToString()) - 1]["isPreWaveFinish"] = IsPreWaveFinish.Checked;
            }
            catch
            {
                MessageBox.Show("没有选择关卡数！", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void NumericUpDown3_ValueChanged(object sender, EventArgs e)
        {
            try
            {
                if ((int)numericUpDown3.Value != 0)
                {
                    JArray array = (JArray)client_stage_json["enemyLayouts"][comboBox2.SelectedIndex]["enemyLayout"][int.Parse(WaveNumber.Value.ToString()) - 1]["enemyList"];
                    array[comboBox3.SelectedIndex]["count"] = (int)numericUpDown3.Value;
                }
            }
            catch
            {
                MessageBox.Show("没有选择关卡数或怪物类型！", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void Btn_save_Click(object sender, EventArgs e)
        {
            File.WriteAllText(String.Format(level_enemy_layouts_config, current_version), client_stage_json.ToString());
            MessageBox.Show("保存成功！", "消息提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
        #endregion

        #region Panel2
        #endregion

        #region Panel3
        #endregion

        #region Panel4
        #endregion

        #region Panel5
        #endregion

        private void FunctionOption_SelectedIndexChanged(object sender, EventArgs e)
        {
            VersionOption.SelectedItem = current_version.ToString();
            Height = 500;
            Location = new Point(Location.X, 89);
            switch (FunctionOption.SelectedIndex)
            {
                case 0: // 普通关卡怪物生成：level_enemy_layouts_config
                    {
                        panel1.Location = new Point(PanelX, PanelY);
                        panel1.Width = width;
                        panel1.Height = height;
                        panel1.Visible = true;
                    } break;
                case 1: // 塔怪物生成：level_enemy_layouts_config_tower
                    {

                    }
                    break;
                case 2: // 怪物属性：monster_config
                    {

                    }
                    break;
                case 3: // 进关消耗：entry_consumables_config
                    {

                    }
                    break;
                case 4: // 挂机奖励：hang_reward_config
                    {

                    }
                    break;
                case 5: // 抽奖奖励：lottery_config
                    {

                    }
                    break;
                case 6: // 玩家配置表：player_config
                    {

                    }
                    break;
                case 7: // 卷轴升级技能配置信息：skill_level_up_config
                    {

                    }
                    break;
                case 8: // 通关奖励：stage_reward_config
                    {

                    }
                    break;
                case 9: // 武器配置：weapon_config
                    {

                    }
                    break;
                case 10: // 世界参数：world_distribution
                    {

                    }
                    break;
            }
            
        }
    }
}
