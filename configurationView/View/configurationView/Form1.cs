using System;
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
        int height = 520;
        StreamReader stream;
        JsonTextReader reader;
        //DirectoryInfo di1 = new DirectoryInfo(Directory.GetCurrentDirectory());
        //public static string main_path = "..//..//..//..//..//configuration//";
        static string main_path = "configuration//";
        string current_version = "0";
        string old_version = "0";
        string new_version;
        public static string view_configuration_path = main_path + "view_configuration.json";
        JObject json;
        string json_version = main_path + "config_timer_setting.json";
        /// <summary>
        /// client configuration
        /// </summary>
        string clien_path = main_path + "client//";
        string public_file_path;
        string level_enemy_layouts_config = main_path + "client//{0}//level_enemy_layouts_config.json";
        JObject public_json_data;
        string level_enemy_layouts_config_tower = main_path + "client//{0}//level_enemy_layouts_config_tower.json";
        string monster_config = main_path + "client//{0}//monster_config.json";
        /// <summary>
        /// sever configuration
        /// </summary>
        string server_path = main_path + "server//";
        string entry_consumables_config = main_path + "server//{0}//entry_consumables_config.json";
        string stage_reward_config = main_path + "server//{0}//stage_reward_config.json";
        string hang_reward_config = main_path + "server//{0}//hang_reward_config.json";
        string lottery_config = main_path + "server//{0}//lottery_config.json";
        string mysql_data_config = main_path + "server//{0}//mysql_data_config.json";
        string player_config = main_path + "server//{0}//player_config.json";
        string skill_level_up_config = main_path + "server//{0}//skill_level_up_config.json";
        string weapon_config = main_path + "server//{0}//weapon_config.json";
        string world_distribution = main_path + "server//{0}//world_distribution.json";
        //string ex = string.Format("{ 0}", "ex");
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

        private void AddVersion_Click(object sender, EventArgs e)
        {
            string version_str = Interaction.InputBox("请输入版本号，将会拷贝最新版本作为当前版本", "输入版本号", "");
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
                        result = MessageBox.Show(text: string.Format("客服端版本{0}已存在，是否添加客服端版本{1}中没有的文件", new_version, current_version), caption: "确认提示", MessageBoxButtons.YesNo, MessageBoxIcon.Information);
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
                        result = MessageBox.Show(text: string.Format("服务端版本{0}已存在，是否添加服务端版本{1}中没有的文件", new_version, current_version), caption: "确认提示", MessageBoxButtons.YesNo, MessageBoxIcon.Information);
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

        private void VersionOption_SelectedIndexChanged(object sender, EventArgs e)
        {
            current_version = VersionOption.SelectedItem.ToString();
        }

        #region Panel1 怪物生成设置
        private void StageType_SelectedIndexChanged(object sender, EventArgs e)
        {
            try
            {
                StageNumber.Items.Clear();
                switch (StageType.SelectedItem.ToString())
                {
                    case "普通关卡":
                        {
                            public_file_path = level_enemy_layouts_config;
                        }
                        break;
                    case "冲塔关卡":
                        {
                            public_file_path = level_enemy_layouts_config_tower;
                        }
                        break;
                }
                stream = File.OpenText(string.Format(public_file_path, current_version));
                reader = new JsonTextReader(stream);
                public_json_data = (JObject)JToken.ReadFrom(reader);
                stream.Close();
                reader.Close();
                int i = 1;  // public_json_data["enemyLayouts"][i-1].ToString()
                foreach (var item in public_json_data["enemyLayouts"])
                {
                    StageNumber.Items.Add(i.ToString());
                    i++;
                }
                old_version = current_version;
            }
            catch
            {
                MessageBox.Show(text: string.Format("不存在版本{0}！", current_version), caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void Panel1DelStage_Click(object sender, EventArgs e)
        {
            // delete
            try
            {
                public_json_data["enemyLayouts"][StageNumber.SelectedIndex].Remove();
                File.WriteAllText(string.Format(public_file_path, current_version), public_json_data.ToString());
                StageNumber.Items.Remove(StageNumber.SelectedItem.ToString());
                MessageBox.Show(text: string.Format("删除成功！", current_version), caption: "提示信息", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch
            {
                MessageBox.Show("未选择关卡，请选择关卡后再删除！", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void Panel1AddStage_Click(object sender, EventArgs e)
        {
            // add
            try
            {
                JArray array = (JArray)public_json_data["enemyLayouts"];
                array.Add(public_json_data["enemyLayouts"][StageNumber.Items.Count - 1]);
                public_json_data["enemyLayouts"] = array;
                File.WriteAllText(string.Format(public_file_path, current_version), public_json_data.ToString());
                StageNumber.Items.Add(StageNumber.Items.Count + 1);
                StageNumber.SelectedIndex = StageNumber.Items.IndexOf(StageNumber.Items.Count);
                MessageBox.Show(text: "关卡添加成功 ！", caption: "消息提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch
            {
                MessageBox.Show(text: string.Format("未选择关卡类型！", current_version), caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void StageNumber_SelectedIndexChanged(object sender, EventArgs e)
        {
            WaveNumber.Items.Clear();
            if (old_version.Equals(current_version))
            {
                JArray array = (JArray)public_json_data["enemyLayouts"][StageNumber.SelectedIndex]["enemyLayout"];
                for(int i=1; i<=array.Count; i++)
                {
                    WaveNumber.Items.Add(i.ToString());
                }
            }
            else
            {
                MessageBox.Show(text: "请重新选择关卡类型 ！", caption: "消息提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
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

            MonsterList.Items.Clear();
            MonsterGenerationPoint.Items.Clear();
            JArray array = (JArray)enemy["enemyList"];
            foreach (var item in array)
            {
                MonsterList.Items.Add(item["enemysPrefString"].ToString());
            }
            array = (JArray)enemy["SpawnPointStrings"];
            foreach (var item in array)
            {
                MonsterGenerationPoint.Items.Add(item.ToString());
            }
        }

        private void WaveNumber_SelectedIndexChanged(object sender, EventArgs e)
        {
            try
            {
                SettingPanel((JObject)public_json_data["enemyLayouts"][StageNumber.SelectedIndex]["enemyLayout"][WaveNumber.SelectedIndex]);
            }
            catch
            {
                MessageBox.Show(text: "未选择关卡类型！暂无波数信息！", caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void MonsterList_SelectedIndexChanged(object sender, EventArgs e)
        {
            JObject enemyLayout = (JObject)public_json_data["enemyLayouts"][StageNumber.SelectedIndex]["enemyLayout"][WaveNumber.SelectedIndex];
            JArray array = (JArray)enemyLayout["enemyList"];
            MonsterAmount.Value = (decimal)array[MonsterList.SelectedIndex]["count"];
        }

        private void Panel1DelMonster_Click(object sender, EventArgs e)
        {
            // delete
            try
            {
                JArray array = (JArray)public_json_data["enemyLayouts"][StageNumber.SelectedIndex]["enemyLayout"][WaveNumber.SelectedIndex]["enemyList"];
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
                    array[MonsterList.SelectedIndex].Remove();
                    public_json_data["enemyLayouts"][StageNumber.SelectedIndex]["enemyLayout"][WaveNumber.SelectedIndex]["enemyList"] = array;
                    File.WriteAllText(string.Format(public_file_path, current_version), public_json_data.ToString());
                    MonsterList.Items.Remove(MonsterList.SelectedItem.ToString());
                    MonsterAmount.Value = 0;
                    MessageBox.Show(text: string.Format("删除怪物成功！", current_version), caption: "提示信息", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
            catch
            {
                MessageBox.Show(text: string.Format("请选择一种怪后再删除！", current_version), caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void Panel1AddMonster_Click(object sender, EventArgs e)
        {
            // add
            try {
                new MonsterAdd((JArray)public_json_data["enemyLayouts"][StageNumber.SelectedIndex]["enemyLayout"][WaveNumber.SelectedIndex]["enemyList"], public_json_data, string.Format(public_file_path, current_version), MonsterList).Show();
            }
            catch
            {
                MessageBox.Show(text: string.Format("未选择关卡数！", current_version), caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void Panel1DelPoint_Click(object sender, EventArgs e)
        {
            // delete
            try
            {
                JArray array = (JArray)public_json_data["enemyLayouts"][StageNumber.SelectedIndex]["enemyLayout"][WaveNumber.SelectedIndex]["SpawnPointStrings"];
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
                    array[MonsterGenerationPoint.SelectedIndex].Remove();
                    public_json_data["enemyLayouts"][StageNumber.SelectedIndex]["enemyLayout"][WaveNumber.SelectedIndex]["SpawnPointStrings"] = array;
                    File.WriteAllText(string.Format(public_file_path, current_version), public_json_data.ToString());
                    MonsterGenerationPoint.Items.Remove(MonsterGenerationPoint.SelectedItem.ToString());
                    MessageBox.Show(text: string.Format("删除成功！", current_version), caption: "提示信息", MessageBoxButtons.OK, MessageBoxIcon.Information);

                }
            }
            catch
            {
                MessageBox.Show(text: string.Format("请选择一个出生点后再删除！", current_version), caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void Panel1AddPoint_Click(object sender, EventArgs e)
        {
            try
            {
                string item = OptionalGenerationPoint.SelectedItem.ToString();
                if (MonsterGenerationPoint.Items.Contains(item))
                {
                    MessageBox.Show(text: string.Format("出生点已添加到该波怪物出生点中！", current_version), caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                else
                {
                    JArray array = (JArray)public_json_data["enemyLayouts"][StageNumber.SelectedIndex]["enemyLayout"][WaveNumber.SelectedIndex]["SpawnPointStrings"];
                    array.Add(item);
                    File.WriteAllText(string.Format(public_file_path, current_version), public_json_data.ToString());
                    MonsterGenerationPoint.Items.Add(item);
                    MessageBox.Show(text: string.Format("出生点{0}添加成功！", item), caption: "提示信息", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
            catch
            {
                MessageBox.Show(text: "请选择一个出生点后再添加！", caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void Panel1DelWave_Click(object sender, EventArgs e)
        {
            try
            {
                public_json_data["enemyLayouts"][StageNumber.SelectedIndex]["enemyLayout"][WaveNumber.SelectedIndex].Remove();
                File.WriteAllText(string.Format(public_file_path, current_version), public_json_data.ToString());
                WaveNumber.Items.Remove(WaveNumber.SelectedItem.ToString());
                TotalTime.Value = 0;
                ColdDownTime.Value = 0;
                IsPreWaveFinish.Checked = false;
                MessageBox.Show(text: string.Format("删除成功！", current_version), caption: "提示信息", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch
            {
                MessageBox.Show("未选择怪物波数，请选择波数后再删除！", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void Panel1AddWave_Click(object sender, EventArgs e)
        {
            // add
            try
            {
                JArray array = (JArray)public_json_data["enemyLayouts"][StageNumber.SelectedIndex]["enemyLayout"];
                array.Add(array[array.Count - 1]);
                public_json_data["enemyLayouts"][StageNumber.SelectedIndex]["enemyLayout"] = array;
                File.WriteAllText(string.Format(public_file_path, current_version), public_json_data.ToString());
                WaveNumber.Items.Add(WaveNumber.Items.Count + 1);
                MessageBox.Show(text: "关卡添加成功 ！", caption: "消息提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch
            {
                MessageBox.Show(text: string.Format("未选择关卡数！", current_version), caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void TotalTime_ValueChanged(object sender, EventArgs e)
        {
            try
            {
                if ((int)TotalTime.Value != 0)
                {
                    public_json_data["enemyLayouts"][StageNumber.SelectedIndex]["enemyLayout"][WaveNumber.SelectedIndex]["totalTime"] = (int)TotalTime.Value;
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
                    public_json_data["enemyLayouts"][StageNumber.SelectedIndex]["enemyLayout"][WaveNumber.SelectedIndex]["coldDownTime"] = (int)ColdDownTime.Value;
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
                public_json_data["enemyLayouts"][StageNumber.SelectedIndex]["enemyLayout"][WaveNumber.SelectedIndex]["isPreWaveFinish"] = IsPreWaveFinish.Checked;
            }
            catch
            {
                MessageBox.Show("没有选择关卡数！", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void MonsterAmount_ValueChanged(object sender, EventArgs e)
        {
            try
            {
                if ((int)MonsterAmount.Value != 0)
                {
                    JArray array = (JArray)public_json_data["enemyLayouts"][StageNumber.SelectedIndex]["enemyLayout"][WaveNumber.SelectedIndex]["enemyList"];
                    array[MonsterList.SelectedIndex]["count"] = (int)MonsterAmount.Value;
                }
            }
            catch
            {
                MessageBox.Show("没有选择怪物！", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void Panel1Save_Click(object sender, EventArgs e)
        {
            File.WriteAllText(string.Format(public_file_path, current_version), public_json_data.ToString());
            MessageBox.Show("保存成功！", "消息提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
        #endregion

        #region Panel2 怪物属性
        private void Panel2MonsterList_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (old_version.Equals(current_version))
            {
                JObject Panel2MonsterData = (JObject)public_json_data[Panel2MonsterList.SelectedItem.ToString()];
                Panel2LV.Value = (decimal)Panel2MonsterData["LV"];
                Panel2HP.Value = (decimal)Panel2MonsterData["HP"];
                Panel2MP.Value = (decimal)Panel2MonsterData["MP"];
                Panel2Attack.Value = (decimal)Panel2MonsterData["Attack"];
                Panel2PhysicalDefend.Value = (decimal)Panel2MonsterData["PhysicalDefend"];
                Panel2Strength.Value = (decimal)Panel2MonsterData["Strength"];
                Panel2Vitality.Value = (decimal)Panel2MonsterData["Vitality"];
                Panel2Mentality.Value = (decimal)Panel2MonsterData["Mentality"];
                Panel2Agility.Value = (decimal)Panel2MonsterData["Agility"];
                Panel2FlameDefend.Value = (decimal)Panel2MonsterData["FlameDefend"];
                Panel2FrozenDefend.Value = (decimal)Panel2MonsterData["FrozenDefend"];
                Panel2PoisonDefend.Value = (decimal)Panel2MonsterData["PoisonDefend"];
                Panel2LightningDefend.Value = (decimal)Panel2MonsterData["LightningDefend"];
                Panel2Flame.Value = (decimal)Panel2MonsterData["Flame"];
                Panel2Frozen.Value = (decimal)Panel2MonsterData["Frozen"];
                Panel2Poison.Value = (decimal)Panel2MonsterData["Poison"];
                Panel2Lightning.Value = (decimal)Panel2MonsterData["Lightning"];
                Panel2Sacredness.Checked = ((int)Panel2MonsterData["Sacredness"] == 0) ? false : true;
                Panel2AttackSpeed.Value = (decimal)Panel2MonsterData["AttackSpeed"];
                Panel2MoveSpeed.Value = (decimal)Panel2MonsterData["MoveSpeed"];
                Panel2RotationSpeed.Value = (decimal)Panel2MonsterData["RotationSpeed"];
                Panel2AttackRange.Value = (decimal)Panel2MonsterData["AttackRange"];
                Panel2CriticalLevel.Value = (decimal)Panel2MonsterData["CriticalLevel"];
                Panel2CriticalDefend.Value = (decimal)Panel2MonsterData["CriticalDefend"];
                Panel2HitRate.Value = (decimal)Panel2MonsterData["HitRate"];
                Panel2CDRate.Value = (decimal)Panel2MonsterData["CDRate"];
            }
            else
            {
                MessageBox.Show("请重新选择此面板，暂未刷新！", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void Panel2Save_Click(object sender, EventArgs e)
        {
            if (old_version.Equals(current_version))
            {
                JObject Panel2MonsterData = (JObject)public_json_data[Panel2MonsterList.SelectedItem.ToString()];
                Panel2MonsterData["LV"] = (int)Panel2LV.Value;
                Panel2MonsterData["HP"] = (int)Panel2HP.Value;
                Panel2MonsterData["MP"] = (int)Panel2MP.Value;
                Panel2MonsterData["Attack"] = (int)Panel2Attack.Value;
                Panel2MonsterData["PhysicalDefend"] = (int)Panel2PhysicalDefend.Value;
                Panel2MonsterData["Strength"] = (int)Panel2Strength.Value;
                Panel2MonsterData["Vitality"] = (int)Panel2Vitality.Value;
                Panel2MonsterData["Mentality"] = (int)Panel2Mentality.Value;
                Panel2MonsterData["Agility"] = (int)Panel2Agility.Value;
                Panel2MonsterData["FlameDefend"] = (int)Panel2FlameDefend.Value;
                Panel2MonsterData["FrozenDefend"] = (int)Panel2FrozenDefend.Value;
                Panel2MonsterData["PoisonDefend"] = (int)Panel2PoisonDefend.Value;
                Panel2MonsterData["LightningDefend"] = (int)Panel2LightningDefend.Value;
                Panel2MonsterData["Flame"] = (int)Panel2Flame.Value;
                Panel2MonsterData["Frozen"] = (int)Panel2Frozen.Value;
                Panel2MonsterData["Poison"] = (int)Panel2Poison.Value;
                Panel2MonsterData["Lightning"] = (int)Panel2Lightning.Value;
                Panel2MonsterData["Sacredness"] = Panel2Sacredness.Checked ? 1 : 0;
                Panel2MonsterData["AttackSpeed"] = (int)Panel2AttackSpeed.Value;
                Panel2MonsterData["MoveSpeed"] = (int)Panel2MoveSpeed.Value;
                Panel2MonsterData["RotationSpeed"] = (int)Panel2RotationSpeed.Value;
                Panel2MonsterData["AttackRange"] = (int)Panel2AttackRange.Value;
                Panel2MonsterData["CriticalLevel"] = (int)Panel2CriticalLevel.Value;
                Panel2MonsterData["CriticalDefend"] = (int)Panel2CriticalDefend.Value;
                Panel2MonsterData["HitRate"] = (int)Panel2HitRate.Value;
                Panel2MonsterData["CDRate"] = (int)Panel2CDRate.Value;
                File.WriteAllText(string.Format(public_file_path, current_version), public_json_data.ToString());
                MessageBox.Show("保存成功！", "消息提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            else
            {
                MessageBox.Show("请重新选择此面板，暂未刷新！", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void Panel2DelMonster_Click(object sender, EventArgs e)
        {
            // delete
            try
            {
                if (public_json_data.Count == 1)
                {
                    MessageBox.Show(text: "最后一种怪，不可删除！", caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                else if (public_json_data.Count == 0)
                {
                    MessageBox.Show(text: "已没有怪物可以删除，可手动增加一种怪物再删除！", caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                else
                {
                    public_json_data.Remove(Panel2MonsterList.SelectedItem.ToString());
                    File.WriteAllText(string.Format(public_file_path, current_version), public_json_data.ToString());
                    Panel2MonsterList.Items.Remove(Panel2MonsterList.SelectedItem.ToString());
                    MessageBox.Show(text: string.Format("删除怪物成功！", current_version), caption: "提示信息", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
            catch
            {
                MessageBox.Show(text: string.Format("请选择一种怪后再删除！", current_version), caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void Panel2AddMonster_Click(object sender, EventArgs e)
        {
            try
            {
                string monsters_name = Panel2OptionalMonsterType.SelectedItem.ToString();
                bool IsAdd = true;
                foreach (var item in public_json_data)
                {
                    if (monsters_name.Equals(item.Key))
                    {
                        IsAdd = false;
                        MessageBox.Show("怪物" + monsters_name + "已经存在配置文件中", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        break;
                    }
                }
                if (IsAdd)
                {
                    string Panel2_monster = Panel2MonsterList.Items[0].ToString();
                    public_json_data.Add(monsters_name, JToken.Parse("{}"));
                    JObject Panel2_object = (JObject)public_json_data[monsters_name];
                    foreach (var item in (JObject)public_json_data[Panel2_monster])
                    {
                        Panel2_object.Add(item.Key, 1);
                    }
                    File.WriteAllText(string.Format(public_file_path, current_version), public_json_data.ToString());
                    Panel2MonsterList.Items.Add(monsters_name);
                    MessageBox.Show(text: "怪物添加成功！", caption: "消息提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
            catch
            {
                MessageBox.Show(text: "没有选择怪物类型！", caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
        #endregion

        #region Panel3
        private void Panel3Save_Click(object sender, EventArgs e)
        {
            try
            {
                JObject consumption_stage = JObject.Parse("{}");
                JObject reward_stage = JObject.Parse("{}");
                JArray reward_stage_list = JArray.Parse("[]");
                int stage_value = int.Parse(Panel3SelectSatge.SelectedItem.ToString());
                switch (Panel3SelectSatgeType.SelectedItem.ToString())
                {
                    case "普通关卡":
                        {
                            consumption_stage = (JObject)public_json_data["consumption"]["stage"][Panel3SelectSatge.SelectedItem.ToString()];
                            reward_stage = (JObject)public_json_data["reward"]["stage"][Panel3SelectSatge.SelectedItem.ToString()];
                            #region consumption
                            if (Panel3Iron.Checked)
                            {
                                if (consumption_stage.Property("iron") == null) // 判断是否存在属性iron
                                {
                                    consumption_stage.Add("iron", (int)Panel3IronValue.Value);
                                }
                                else
                                {
                                    consumption_stage["iron"] = (int)Panel3IronValue.Value;
                                }
                            }
                            else
                            {
                                if (consumption_stage.Property("iron") != null)
                                {
                                    consumption_stage.Remove("iron");
                                }
                            }
                            if (Panel3Coin.Checked)
                            {
                                if (consumption_stage.Property("coin") == null) // 判断是否存在属性
                                {
                                    consumption_stage.Add("coin", (int)Panel3CoinValue.Value);
                                }
                                else
                                {
                                    consumption_stage["coin"] = (int)Panel3CoinValue.Value;
                                }
                            }
                            else
                            {
                                if (consumption_stage.Property("coin") != null)
                                {
                                    consumption_stage.Remove("coin");
                                }
                            }
                            if (Panel3Energy.Checked)
                            {
                                if (consumption_stage.Property("energy") == null) // 判断是否存在属性
                                {
                                    consumption_stage.Add("energy", (int)Panel3EnergyValue.Value);
                                }
                                else
                                {
                                    consumption_stage["energy"] = (int)Panel3EnergyValue.Value;
                                }
                            }
                            else
                            {
                                if (consumption_stage.Property("energy") != null)
                                {
                                    consumption_stage.Remove("energy");
                                }
                            }
                            #endregion
                            #region reward
                            if (Panel3RewardSmallEnergyPotion.Checked)
                            {
                                if (reward_stage.Property("small_energy_potion") == null) // 判断是否存在属性iron
                                {
                                    reward_stage.Add("small_energy_potion", (int)Panel3RewardSmallEnergyPotionValue.Value);
                                }
                                else
                                {
                                    reward_stage["small_energy_potion"] = (int)Panel3RewardSmallEnergyPotionValue.Value;
                                }
                            }
                            else
                            {
                                if (reward_stage.Property("small_energy_potion") != null)
                                {
                                    reward_stage.Remove("small_energy_potion");
                                }
                            }
                            if (Panel3RewardCoin.Checked)
                            {
                                if (reward_stage.Property("coin") == null) // 判断是否存在属性
                                {
                                    reward_stage.Add("coin", (int)Panel3RewardCoinValue.Value);
                                }
                                else
                                {
                                    reward_stage["coin"] = (int)Panel3RewardCoinValue.Value;
                                }
                            }
                            else
                            {
                                if (reward_stage.Property("coin") != null)
                                {
                                    reward_stage.Remove("coin");
                                }
                            }
                            if (Panel3RewardEnergy.Checked)
                            {
                                if (reward_stage.Property("energy") == null) // 判断是否存在属性
                                {
                                    reward_stage.Add("energy", (int)Panel3RewardEnergyValue.Value);
                                }
                                else
                                {
                                    reward_stage["energy"] = (int)Panel3RewardEnergyValue.Value;
                                }
                            }
                            else
                            {
                                if (reward_stage.Property("energy") != null)
                                {
                                    reward_stage.Remove("energy");
                                }
                            }
                            if (Panel3RewardLowScrollZ.Checked)
                            {
                                if (reward_stage.Property("fortune_wheel_ticket_basic") == null) // 判断是否存在属性iron
                                {
                                    reward_stage.Add("fortune_wheel_ticket_basic", (int)Panel3RewardLowScrollZValue.Value);
                                }
                                else
                                {
                                    reward_stage["fortune_wheel_ticket_basic"] = (int)Panel3RewardLowScrollZValue.Value;
                                }
                            }
                            else
                            {
                                if (reward_stage.Property("fortune_wheel_ticket_basic") != null)
                                {
                                    reward_stage.Remove("fortune_wheel_ticket_basic");
                                }
                            }
                            if (Panel3RewardProScrollZ.Checked)
                            {
                                if (reward_stage.Property("fortune_wheel_ticket_pro") == null) // 判断是否存在属性
                                {
                                    reward_stage.Add("fortune_wheel_ticket_pro", (int)Panel3RewardProScrollZValue.Value);
                                }
                                else
                                {
                                    reward_stage["fortune_wheel_ticket_pro"] = (int)Panel3RewardProScrollZValue.Value;
                                }
                            }
                            else
                            {
                                if (reward_stage.Property("fortune_wheel_ticket_pro") != null)
                                {
                                    reward_stage.Remove("fortune_wheel_ticket_pro");
                                }
                            }
                            if (Panel3RewardIron.Checked)
                            {
                                if (reward_stage.Property("iron") == null) // 判断是否存在属性
                                {
                                    reward_stage.Add("iron", (int)Panel3RewardIronValue.Value);
                                }
                                else
                                {
                                    reward_stage["iron"] = (int)Panel3RewardIronValue.Value;
                                }
                            }
                            else
                            {
                                if (reward_stage.Property("iron") != null)
                                {
                                    reward_stage.Remove("iron");
                                }
                            }
                            if (Panel3RewardExperience.Checked)
                            {
                                if (reward_stage.Property("experience") == null) // 判断是否存在属性
                                {
                                    reward_stage.Add("experience", (int)Panel3RewardExperienceValue.Value);
                                }
                                else
                                {
                                    reward_stage["experience"] = (int)Panel3RewardExperienceValue.Value;
                                }
                            }
                            else
                            {
                                if (reward_stage.Property("experience") != null)
                                {
                                    reward_stage.Remove("experience");
                                }
                            }
                            if (Panel3RewardBasicScrollC.Checked)
                            {
                                if (reward_stage.Property("basic_summon_scroll") == null) // 判断是否存在属性
                                {
                                    reward_stage.Add("basic_summon_scroll", (int)Panel3RewardBasicScrollCValue.Value);
                                }
                                else
                                {
                                    reward_stage["basic_summon_scroll"] = (int)Panel3RewardBasicScrollCValue.Value;
                                }
                            }
                            else
                            {
                                if (reward_stage.Property("basic_summon_scroll") != null)
                                {
                                    reward_stage.Remove("basic_summon_scroll");
                                }
                            }
                            if (Panel3RewardProphetScrollC.Checked)
                            {
                                if (reward_stage.Property("prophet_summon_scroll") == null) // 判断是否存在属性
                                {
                                    reward_stage.Add("prophet_summon_scroll", (int)Panel3RewardProphetScrollCValue.Value);
                                }
                                else
                                {
                                    reward_stage["prophet_summon_scroll"] = (int)Panel3RewardProphetScrollCValue.Value;
                                }
                            }
                            else
                            {
                                if (reward_stage.Property("prophet_summon_scroll") != null)
                                {
                                    reward_stage.Remove("prophet_summon_scroll");
                                }
                            }
                            if (Panel3RewardProScrollC.Checked)
                            {
                                if (reward_stage.Property("pro_summon_scroll") == null) // 判断是否存在属性
                                {
                                    reward_stage.Add("pro_summon_scroll", (int)Panel3RewardProScrollCValue.Value);
                                }
                                else
                                {
                                    reward_stage["pro_summon_scroll"] = (int)Panel3RewardProScrollCValue.Value;
                                }
                            }
                            else
                            {
                                if (reward_stage.Property("pro_summon_scroll") != null)
                                {
                                    reward_stage.Remove("pro_summon_scroll");
                                }
                            }
                            if (Panel3RewardExperiencePotion.Checked)
                            {
                                if (reward_stage.Property("experience_potion") == null) // 判断是否存在属性
                                {
                                    reward_stage.Add("experience_potion", (int)Panel3RewardExperiencePotionValue.Value);
                                }
                                else
                                {
                                    reward_stage["experience_potion"] = (int)Panel3RewardExperiencePotionValue.Value;
                                }
                            }
                            else
                            {
                                if (reward_stage.Property("experience_potion") != null)
                                {
                                    reward_stage.Remove("experience_potion");
                                }
                            }
                            if (Panel3Reward10Scroll.Checked)
                            {
                                if (reward_stage.Property("skill_scroll_10") == null) // 判断是否存在属性
                                {
                                    reward_stage.Add("skill_scroll_10", (int)Panel3Reward10ScrollValue.Value);
                                }
                                else
                                {
                                    reward_stage["skill_scroll_10"] = (int)Panel3Reward10ScrollValue.Value;
                                }
                            }
                            else
                            {
                                if (reward_stage.Property("skill_scroll_10") != null)
                                {
                                    reward_stage.Remove("skill_scroll_10");
                                }
                            }
                            if (Panel3Reward30Scroll.Checked)
                            {
                                if (reward_stage.Property("skill_scroll_30") == null) // 判断是否存在属性
                                {
                                    reward_stage.Add("skill_scroll_30", (int)Panel3Reward30ScrollValue.Value);
                                }
                                else
                                {
                                    reward_stage["skill_scroll_30"] = (int)Panel3Reward30ScrollValue.Value;
                                }
                            }
                            else
                            {
                                if (reward_stage.Property("skill_scroll_30") != null)
                                {
                                    reward_stage.Remove("skill_scroll_30");
                                }
                            }
                            if (Panel3Reward100Scroll.Checked)
                            {
                                if (reward_stage.Property("skill_scroll_100") == null) // 判断是否存在属性
                                {
                                    reward_stage.Add("skill_scroll_100", (int)Panel3Reward100ScrollValue.Value);
                                }
                                else
                                {
                                    reward_stage["skill_scroll_100"] = (int)Panel3Reward100ScrollValue.Value;
                                }
                            }
                            else
                            {
                                if (reward_stage.Property("skill_scroll_100") != null)
                                {
                                    reward_stage.Remove("skill_scroll_100");
                                }
                            }
                            #endregion
                        }
                        break;
                    case "冲塔关卡":
                        {
                            consumption_stage = (JObject)public_json_data["consumption"]["tower"][Panel3SelectSatge.SelectedItem.ToString()];
                            #region consumption
                            if (Panel3Iron.Checked)
                            {
                                if (consumption_stage.Property("iron") == null) // 判断是否存在属性iron
                                {
                                    consumption_stage.Add("iron", (int)Panel3IronValue.Value);
                                }
                                else
                                {
                                    consumption_stage["iron"] = (int)Panel3IronValue.Value;
                                }
                            }
                            else
                            {
                                if (consumption_stage.Property("iron") != null)
                                {
                                    consumption_stage.Remove("iron");
                                }
                            }
                            if (Panel3Coin.Checked)
                            {
                                if (consumption_stage.Property("coin") == null) // 判断是否存在属性
                                {
                                    consumption_stage.Add("coin", (int)Panel3CoinValue.Value);
                                }
                                else
                                {
                                    consumption_stage["coin"] = (int)Panel3CoinValue.Value;
                                }
                            }
                            else
                            {
                                if (consumption_stage.Property("coin") != null)
                                {
                                    consumption_stage.Remove("coin");
                                }
                            }
                            if (Panel3Energy.Checked)
                            {
                                if (consumption_stage.Property("energy") == null) // 判断是否存在属性
                                {
                                    consumption_stage.Add("energy", (int)Panel3EnergyValue.Value);
                                }
                                else
                                {
                                    consumption_stage["energy"] = (int)Panel3EnergyValue.Value;
                                }
                            }
                            else
                            {
                                if (consumption_stage.Property("energy") != null)
                                {
                                    consumption_stage.Remove("energy");
                                }
                            }
                            #endregion
                            if (stage_value % 10 == 0) // 整十关卡
                            {
                                foreach (var item in Panel3List.Items)
                                {
                                    reward_stage_list.Add(item.ToString());
                                }
                                public_json_data["reward"]["tower"][Panel3SelectSatge.SelectedItem.ToString()] = reward_stage_list;
                            }
                            else
                            {
                                reward_stage = (JObject)public_json_data["reward"]["tower"][Panel3SelectSatge.SelectedItem.ToString()];
                                #region reward
                                if (Panel3RewardSmallEnergyPotion.Checked)
                                {
                                    if (reward_stage.Property("small_energy_potion") == null) // 判断是否存在属性iron
                                    {
                                        reward_stage.Add("small_energy_potion", (int)Panel3RewardSmallEnergyPotionValue.Value);
                                    }
                                    else
                                    {
                                        reward_stage["small_energy_potion"] = (int)Panel3RewardSmallEnergyPotionValue.Value;
                                    }
                                }
                                else
                                {
                                    if (reward_stage.Property("small_energy_potion") != null)
                                    {
                                        reward_stage.Remove("small_energy_potion");
                                    }
                                }
                                if (Panel3RewardCoin.Checked)
                                {
                                    if (reward_stage.Property("coin") == null) // 判断是否存在属性
                                    {
                                        reward_stage.Add("coin", (int)Panel3RewardCoinValue.Value);
                                    }
                                    else
                                    {
                                        reward_stage["coin"] = (int)Panel3RewardCoinValue.Value;
                                    }
                                }
                                else
                                {
                                    if (reward_stage.Property("coin") != null)
                                    {
                                        reward_stage.Remove("coin");
                                    }
                                }
                                if (Panel3RewardEnergy.Checked)
                                {
                                    if (reward_stage.Property("energy") == null) // 判断是否存在属性
                                    {
                                        reward_stage.Add("energy", (int)Panel3RewardEnergyValue.Value);
                                    }
                                    else
                                    {
                                        reward_stage["energy"] = (int)Panel3RewardEnergyValue.Value;
                                    }
                                }
                                else
                                {
                                    if (reward_stage.Property("energy") != null)
                                    {
                                        reward_stage.Remove("energy");
                                    }
                                }
                                if (Panel3RewardLowScrollZ.Checked)
                                {
                                    if (reward_stage.Property("fortune_wheel_ticket_basic") == null) // 判断是否存在属性iron
                                    {
                                        reward_stage.Add("fortune_wheel_ticket_basic", (int)Panel3RewardLowScrollZValue.Value);
                                    }
                                    else
                                    {
                                        reward_stage["fortune_wheel_ticket_basic"] = (int)Panel3RewardLowScrollZValue.Value;
                                    }
                                }
                                else
                                {
                                    if (reward_stage.Property("fortune_wheel_ticket_basic") != null)
                                    {
                                        reward_stage.Remove("fortune_wheel_ticket_basic");
                                    }
                                }
                                if (Panel3RewardProScrollZ.Checked)
                                {
                                    if (reward_stage.Property("fortune_wheel_ticket_pro") == null) // 判断是否存在属性
                                    {
                                        reward_stage.Add("fortune_wheel_ticket_pro", (int)Panel3RewardProScrollZValue.Value);
                                    }
                                    else
                                    {
                                        reward_stage["fortune_wheel_ticket_pro"] = (int)Panel3RewardProScrollZValue.Value;
                                    }
                                }
                                else
                                {
                                    if (reward_stage.Property("fortune_wheel_ticket_pro") != null)
                                    {
                                        reward_stage.Remove("fortune_wheel_ticket_pro");
                                    }
                                }
                                if (Panel3RewardIron.Checked)
                                {
                                    if (reward_stage.Property("iron") == null) // 判断是否存在属性
                                    {
                                        reward_stage.Add("iron", (int)Panel3RewardIronValue.Value);
                                    }
                                    else
                                    {
                                        reward_stage["iron"] = (int)Panel3RewardIronValue.Value;
                                    }
                                }
                                else
                                {
                                    if (reward_stage.Property("iron") != null)
                                    {
                                        reward_stage.Remove("iron");
                                    }
                                }
                                if (Panel3RewardExperience.Checked)
                                {
                                    if (reward_stage.Property("experience") == null) // 判断是否存在属性
                                    {
                                        reward_stage.Add("experience", (int)Panel3RewardExperienceValue.Value);
                                    }
                                    else
                                    {
                                        reward_stage["experience"] = (int)Panel3RewardExperienceValue.Value;
                                    }
                                }
                                else
                                {
                                    if (reward_stage.Property("experience") != null)
                                    {
                                        reward_stage.Remove("experience");
                                    }
                                }
                                if (Panel3RewardBasicScrollC.Checked)
                                {
                                    if (reward_stage.Property("basic_summon_scroll") == null) // 判断是否存在属性
                                    {
                                        reward_stage.Add("basic_summon_scroll", (int)Panel3RewardBasicScrollCValue.Value);
                                    }
                                    else
                                    {
                                        reward_stage["basic_summon_scroll"] = (int)Panel3RewardBasicScrollCValue.Value;
                                    }
                                }
                                else
                                {
                                    if (reward_stage.Property("basic_summon_scroll") != null)
                                    {
                                        reward_stage.Remove("basic_summon_scroll");
                                    }
                                }
                                if (Panel3RewardProphetScrollC.Checked)
                                {
                                    if (reward_stage.Property("prophet_summon_scroll") == null) // 判断是否存在属性
                                    {
                                        reward_stage.Add("prophet_summon_scroll", (int)Panel3RewardProphetScrollCValue.Value);
                                    }
                                    else
                                    {
                                        reward_stage["prophet_summon_scroll"] = (int)Panel3RewardProphetScrollCValue.Value;
                                    }
                                }
                                else
                                {
                                    if (reward_stage.Property("prophet_summon_scroll") != null)
                                    {
                                        reward_stage.Remove("prophet_summon_scroll");
                                    }
                                }
                                if (Panel3RewardProScrollC.Checked)
                                {
                                    if (reward_stage.Property("pro_summon_scroll") == null) // 判断是否存在属性
                                    {
                                        reward_stage.Add("pro_summon_scroll", (int)Panel3RewardProScrollCValue.Value);
                                    }
                                    else
                                    {
                                        reward_stage["pro_summon_scroll"] = (int)Panel3RewardProScrollCValue.Value;
                                    }
                                }
                                else
                                {
                                    if (reward_stage.Property("pro_summon_scroll") != null)
                                    {
                                        reward_stage.Remove("pro_summon_scroll");
                                    }
                                }
                                if (Panel3RewardExperiencePotion.Checked)
                                {
                                    if (reward_stage.Property("experience_potion") == null) // 判断是否存在属性
                                    {
                                        reward_stage.Add("experience_potion", (int)Panel3RewardExperiencePotionValue.Value);
                                    }
                                    else
                                    {
                                        reward_stage["experience_potion"] = (int)Panel3RewardExperiencePotionValue.Value;
                                    }
                                }
                                else
                                {
                                    if (reward_stage.Property("experience_potion") != null)
                                    {
                                        reward_stage.Remove("experience_potion");
                                    }
                                }
                                if (Panel3Reward10Scroll.Checked)
                                {
                                    if (reward_stage.Property("skill_scroll_10") == null) // 判断是否存在属性
                                    {
                                        reward_stage.Add("skill_scroll_10", (int)Panel3Reward10ScrollValue.Value);
                                    }
                                    else
                                    {
                                        reward_stage["skill_scroll_10"] = (int)Panel3Reward10ScrollValue.Value;
                                    }
                                }
                                else
                                {
                                    if (reward_stage.Property("skill_scroll_10") != null)
                                    {
                                        reward_stage.Remove("skill_scroll_10");
                                    }
                                }
                                if (Panel3Reward30Scroll.Checked)
                                {
                                    if (reward_stage.Property("skill_scroll_30") == null) // 判断是否存在属性
                                    {
                                        reward_stage.Add("skill_scroll_30", (int)Panel3Reward30ScrollValue.Value);
                                    }
                                    else
                                    {
                                        reward_stage["skill_scroll_30"] = (int)Panel3Reward30ScrollValue.Value;
                                    }
                                }
                                else
                                {
                                    if (reward_stage.Property("skill_scroll_30") != null)
                                    {
                                        reward_stage.Remove("skill_scroll_30");
                                    }
                                }
                                if (Panel3Reward100Scroll.Checked)
                                {
                                    if (reward_stage.Property("skill_scroll_100") == null) // 判断是否存在属性
                                    {
                                        reward_stage.Add("skill_scroll_100", (int)Panel3Reward100ScrollValue.Value);
                                    }
                                    else
                                    {
                                        reward_stage["skill_scroll_100"] = (int)Panel3Reward100ScrollValue.Value;
                                    }
                                }
                                else
                                {
                                    if (reward_stage.Property("skill_scroll_100") != null)
                                    {
                                        reward_stage.Remove("skill_scroll_100");
                                    }
                                }
                                #endregion
                            }
                            // Segment
                            JArray segment_list = (JArray)public_json_data["reward"]["tower"]["segment"];
                            segment_list[0] = (int)Panel3WeaponSegmentMin.Value;
                            segment_list[1] = (int)Panel3WeaponSegmentMax.Value;
                        }
                        break;
                }
                File.WriteAllText(string.Format(entry_consumables_config, current_version), public_json_data["consumption"].ToString());
                File.WriteAllText(string.Format(stage_reward_config, current_version), public_json_data["reward"].ToString());
                MessageBox.Show("保存成功！", "消息提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch
            {
                MessageBox.Show("请选择需要保存的关卡，保存失败", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
        #endregion

        #region Panel4
        #endregion

        #region Panel5
        #endregion

        private void FunctionOption_SelectedIndexChanged(object sender, EventArgs e)
        {
            Panel1.Visible = false;
            Panel2.Visible = false;
            VersionOption.SelectedItem = current_version.ToString();
            Height = 520;
            Location = new Point(Location.X, 89);
            switch (FunctionOption.SelectedIndex)
            {
                case 0: // 怪物生成设置
                    {
                        Panel1.Location = new Point(PanelX, PanelY);
                        Panel1.Width = width;
                        Panel1.Height = height;
                        Panel1.Visible = true;
                    } break;
                case 1: // 怪物属性：monster_config
                    {
                        Panel2.Location = new Point(PanelX, PanelY);
                        Panel2.Width = width;
                        Panel2.Height = height;
                        Panel2.Visible = true;
                        //Panel2MonsterList
                        public_file_path = monster_config;
                        stream = File.OpenText(string.Format(public_file_path, current_version));
                        reader = new JsonTextReader(stream);
                        public_json_data = (JObject)JToken.ReadFrom(reader);
                        stream.Close();
                        reader.Close();
                        Panel2MonsterList.Items.Clear();
                        foreach (var item in public_json_data)
                        {
                            Panel2MonsterList.Items.Add(item.Key.ToString());
                        }
                        old_version = current_version;


                        Panel2OptionalMonsterType.Items.Clear();
                        stream = File.OpenText(view_configuration_path);
                        reader = new JsonTextReader(stream);
                        foreach (var item in JToken.ReadFrom(reader)["monsters"])
                        {
                            Panel2OptionalMonsterType.Items.Add(item: item.ToString());
                        }
                    }
                    break;
                case 2: // 关卡配置：entry_consumables_config / stage_reward_config
                    {
                        Panel3.Location = new Point(PanelX, PanelY);
                        Panel3.Width = width;
                        Panel3.Height = height;
                        Panel3.Visible = true;
                        public_json_data = JObject.Parse("{}");
                        // 加载关卡消耗的json数据
                        stream = File.OpenText(string.Format(entry_consumables_config, current_version));
                        reader = new JsonTextReader(stream);
                        public_json_data.Add("consumption", (JObject)JToken.ReadFrom(reader));
                        stream.Close();
                        reader.Close();
                        // 加载关卡奖励的json数据
                        stream = File.OpenText(string.Format(stage_reward_config, current_version));
                        reader = new JsonTextReader(stream);
                        public_json_data.Add("reward", (JObject)JToken.ReadFrom(reader));
                        stream.Close();
                        reader.Close();

                    }
                    break;
                case 3: // 挂机奖励：hang_reward_config
                    {

                    }
                    break;
                case 4: // 抽奖奖励：lottery_config
                    {

                    }
                    break;
                case 5: // 玩家配置表：player_config
                    {

                    }
                    break;
                case 6: // 卷轴升级技能配置信息：skill_level_up_config
                    {

                    }
                    break;
                case 7: // 武器配置：weapon_config
                    {

                    }
                    break;
                case 8: // 世界参数：world_distribution
                    {

                    }
                    break;
            }
        }

        private void Panel3SelectSatgeType_SelectedIndexChanged(object sender, EventArgs e)
        {
            Panel3SelectSatge.Items.Clear();
            Panel3AllList.Items.Clear();
            Panel3Clear();
            Panel3WeaponSegmentMin.Value = 0;
            Panel3WeaponSegmentMax.Value = 0;
            switch (Panel3SelectSatgeType.SelectedItem.ToString())
            {
                case "普通关卡": // 普通关卡
                    {
                        foreach(var item in (JObject)public_json_data["consumption"]["stage"])
                        {
                            Panel3SelectSatge.Items.Add(item.Key);
                        }
                    }
                    break;
                case "冲塔关卡": // 冲塔关卡
                    {
                        foreach (var item in (JObject)public_json_data["consumption"]["tower"])
                        {
                            Panel3SelectSatge.Items.Add(item.Key);
                        }
                        // Segment
                        JArray segment_list = (JArray)public_json_data["reward"]["tower"]["segment"];
                        Panel3WeaponSegmentMax.Value = (decimal)segment_list[1];
                        Panel3WeaponSegmentMin.Value = (decimal)segment_list[0];
                    }
                    break;
            }

            // Panel3AllList
            stream = File.OpenText(view_configuration_path);
            reader = new JsonTextReader(stream);
            JArray all_list = (JArray)JToken.ReadFrom(reader)["panel3"]["reward_stage_10"];
            foreach(var item in all_list)
            {
                Panel3AllList.Items.Add(item.ToString());
            }
        }

        private void Panel3SelectSatge_SelectedIndexChanged(object sender, EventArgs e)
        {
            int stage_value = int.Parse(Panel3SelectSatge.SelectedItem.ToString());
            JObject consumption_stage = JObject.Parse("{}");
            JObject reward_stage = JObject.Parse("{}");
            JArray reward_stage_list = JArray.Parse("[]");
            switch (Panel3SelectSatgeType.SelectedItem.ToString())
            {
                case "普通关卡":
                    {
                        consumption_stage = (JObject)public_json_data["consumption"]["stage"][Panel3SelectSatge.SelectedItem.ToString()];
                        reward_stage = (JObject)public_json_data["reward"]["stage"][Panel3SelectSatge.SelectedItem.ToString()];
                    } break;
                case "冲塔关卡":
                    {
                        consumption_stage = (JObject)public_json_data["consumption"]["tower"][Panel3SelectSatge.SelectedItem.ToString()];
                        if (stage_value % 10 == 0)
                        {
                            reward_stage_list = (JArray)public_json_data["reward"]["tower"][Panel3SelectSatge.SelectedItem.ToString()];
                        }
                        else
                        {
                            reward_stage = (JObject)public_json_data["reward"]["tower"][Panel3SelectSatge.SelectedItem.ToString()];
                        }
                    } break;
            }
            Panel3Clear(); // 清理所有的控件
            // consumption stage and tower
            foreach (var item in consumption_stage)
            {
                switch (item.Key)
                {
                    case "iron":
                        {
                            Panel3Iron.Checked = true;
                            Panel3IronValue.Value = (decimal)item.Value;
                        }
                        break;
                    case "coin":
                        {
                            Panel3Coin.Checked = true;
                            Panel3CoinValue.Value = (decimal)item.Value;
                        }
                        break;
                    case "energy":
                        {
                            Panel3Energy.Checked = true;
                            Panel3EnergyValue.Value = (decimal)item.Value;
                        }
                        break;
                }
            }
            // reward stage and  tower
            foreach (var item in reward_stage_list)
            {
                Panel3List.Items.Add(item.ToString());
            }
            foreach (var item in reward_stage)
            {
                switch (item.Key)
                {
                    case "small_energy_potion":
                        {
                            Panel3RewardSmallEnergyPotion.Checked = true;
                            Panel3RewardSmallEnergyPotionValue.Value = (decimal)item.Value;
                        }
                        break;
                    case "coin":
                        {
                            Panel3RewardCoin.Checked = true;
                            Panel3RewardCoinValue.Value = (decimal)item.Value;
                        }
                        break;
                    case "energy":
                        {
                            Panel3RewardEnergy.Checked = true;
                            Panel3RewardEnergyValue.Value = (decimal)item.Value;
                        }
                        break;
                    case "fortune_wheel_ticket_basic": // 低级转卷轴
                        {
                            Panel3RewardLowScrollZ.Checked = true;
                            Panel3RewardLowScrollZValue.Value = (decimal)item.Value;
                        }
                        break;
                    case "fortune_wheel_ticket_pro": // 高级转卷轴
                        {
                            Panel3RewardProScrollZ.Checked = true;
                            Panel3RewardProScrollZValue.Value = (decimal)item.Value;
                        }
                        break;
                    case "iron":
                        {
                            Panel3RewardIron.Checked = true;
                            Panel3RewardIronValue.Value = (decimal)item.Value;
                        }
                        break;
                    case "experience": // 经验
                        {
                            Panel3RewardExperience.Checked = true;
                            Panel3RewardExperienceValue.Value = (decimal)item.Value;
                        }
                        break;
                    case "basic_summon_scroll": // 基础抽卷轴
                        {
                            Panel3RewardBasicScrollC.Checked = true;
                            Panel3RewardBasicScrollCValue.Value = (decimal)item.Value;
                        }
                        break;
                    case "prophet_summon_scroll": // 先知抽卷轴
                        {
                            Panel3RewardProphetScrollC.Checked = true;
                            Panel3RewardProphetScrollCValue.Value = (decimal)item.Value;
                        }
                        break;
                    case "pro_summon_scroll": // 高级抽卷轴
                        {
                            Panel3RewardProScrollC.Checked = true;
                            Panel3RewardProScrollCValue.Value = (decimal)item.Value;
                        }
                        break;
                    case "experience_potion": // 经验药水
                        {
                            Panel3RewardExperiencePotion.Checked = true;
                            Panel3RewardExperiencePotionValue.Value = (decimal)item.Value;
                        }
                        break;
                    case "skill_scroll_10": // 低级卷轴
                        {
                            Panel3Reward10Scroll.Checked = true;
                            Panel3Reward10ScrollValue.Value = (decimal)item.Value;
                        }
                        break;
                    case "skill_scroll_30": // 中级卷轴
                        {
                            Panel3Reward30Scroll.Checked = true;
                            Panel3Reward30ScrollValue.Value = (decimal)item.Value;
                        }
                        break;
                    case "skill_scroll_100": // 高级卷轴
                        {
                            Panel3Reward100Scroll.Checked = true;
                            Panel3Reward100ScrollValue.Value = (decimal)item.Value;
                        }
                        break;
                }
            }
        }

        private void Panel3Clear()
        {
            // consumption
            Panel3Iron.Checked = false;
            Panel3IronValue.Value = 0;
            Panel3Coin.Checked = false;
            Panel3CoinValue.Value = 0;
            Panel3Energy.Checked = false;
            Panel3EnergyValue.Value = 0;
            // reward
            Panel3RewardSmallEnergyPotion.Checked = false;
            Panel3RewardSmallEnergyPotionValue.Value = 0;
            Panel3RewardCoin.Checked = false;
            Panel3RewardCoinValue.Value = 0;
            Panel3RewardEnergy.Checked = false;
            Panel3RewardEnergyValue.Value = 0;
            Panel3RewardLowScrollZ.Checked = false;
            Panel3RewardLowScrollZValue.Value = 0;
            Panel3RewardProScrollZ.Checked = false;
            Panel3RewardProScrollZValue.Value = 0;
            Panel3RewardIron.Checked = false;
            Panel3RewardIronValue.Value = 0;
            Panel3RewardExperience.Checked = false;
            Panel3RewardExperienceValue.Value = 0;
            Panel3RewardBasicScrollC.Checked = false;
            Panel3RewardBasicScrollCValue.Value = 0;
            Panel3RewardProphetScrollC.Checked = false;
            Panel3RewardProphetScrollCValue.Value = 0;
            Panel3RewardProScrollC.Checked = false;
            Panel3RewardProScrollCValue.Value = 0;
            Panel3RewardExperiencePotion.Checked = false;
            Panel3RewardExperiencePotionValue.Value = 0;
            Panel3Reward10Scroll.Checked = false;
            Panel3Reward10ScrollValue.Value = 0;
            Panel3Reward30Scroll.Checked = false;
            Panel3Reward30ScrollValue.Value = 0;
            Panel3Reward100Scroll.Checked = false;
            Panel3Reward100ScrollValue.Value = 0;
            Panel3List.Items.Clear();
        }

        private void Panel3DelSatge_Click(object sender, EventArgs e)
        {
            try
            {
                JObject panel3_del_data;
                switch (Panel3SelectSatgeType.SelectedItem.ToString())
                {
                    case "普通关卡":
                        {
                            panel3_del_data = (JObject)public_json_data["consumption"]["stage"];
                            panel3_del_data.Remove(Panel3SelectSatge.SelectedItem.ToString());

                            panel3_del_data = (JObject)public_json_data["reward"]["stage"];
                            panel3_del_data.Remove(Panel3SelectSatge.SelectedItem.ToString());
                        }
                        break;
                    case "冲塔关卡":
                        {
                            panel3_del_data = (JObject)public_json_data["consumption"]["tower"];
                            panel3_del_data.Remove(Panel3SelectSatge.SelectedItem.ToString());

                            panel3_del_data = (JObject)public_json_data["reward"]["tower"];
                            panel3_del_data.Remove(Panel3SelectSatge.SelectedItem.ToString());
                        }
                        break;
                }
                Panel3SelectSatge.Items.Remove(Panel3SelectSatge.SelectedItem.ToString());
                Panel3Clear();
                MessageBox.Show(text: string.Format("删除成功！", current_version), caption: "提示信息", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch
            {
                MessageBox.Show("未选择关卡类型或者关卡数，请选择对应关卡后再删除！", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void Panel3AddSatge_Click(object sender, EventArgs e)
        {
            try
            {
                int stage = int.Parse(Interaction.InputBox("请输入需要添加的关卡数，关卡数必须为正整数", "输入关卡数", ""));
                JObject consumption_stage = JObject.Parse("{}");
                JObject reward_stage = JObject.Parse("{}");
                if (stage <= 0)
                {
                    MessageBox.Show("关卡数必须为正整数，关卡添加失败", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                else if (Panel3SelectSatge.Items.Contains(stage.ToString())) // 判断集合中是否存在这个关卡
                {
                    MessageBox.Show("关卡已经存在，不需要重复添加，关卡添加失败", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                else
                {
                    switch (Panel3SelectSatgeType.SelectedItem.ToString())
                    {
                        case "普通关卡":
                            {
                                consumption_stage = (JObject)public_json_data["consumption"]["stage"];
                                reward_stage = (JObject)public_json_data["reward"]["stage"];
                                consumption_stage.Add(stage.ToString(), JObject.Parse("{}"));
                                reward_stage.Add(stage.ToString(), JObject.Parse("{}"));
                            }
                            break;
                        case "冲塔关卡":
                            {
                                consumption_stage = (JObject)public_json_data["consumption"]["tower"];
                                reward_stage = (JObject)public_json_data["reward"]["tower"];
                                consumption_stage.Add(stage.ToString(), JObject.Parse("{}"));
                                if (stage % 10 == 0) // 整10关卡
                                {
                                    reward_stage.Add(stage.ToString(), JArray.Parse("[]"));
                                }
                                else
                                {
                                    reward_stage.Add(stage.ToString(), JObject.Parse("{}"));
                                }
                            }
                            break;
                    }
                    Panel3SelectSatge.Items.Add(stage.ToString());
                    MessageBox.Show("关卡添加成功", "消息提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
            catch
            {
                MessageBox.Show("输入错误，关卡数必须为正整数", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void Panel3WeaponSegmentMax_ValueChanged(object sender, EventArgs e)
        {
            if (Panel3WeaponSegmentMax.Value < Panel3WeaponSegmentMin.Value)
            {
                Panel3WeaponSegmentMax.Value = Panel3WeaponSegmentMin.Value;
            }
        }

        private void Panel3WeaponSegmentMin_ValueChanged(object sender, EventArgs e)
        {
            if (Panel3WeaponSegmentMax.Value < Panel3WeaponSegmentMin.Value)
            {
                Panel3WeaponSegmentMin.Value = Panel3WeaponSegmentMax.Value;
            }
        }

        private void Panel3Del_Click(object sender, EventArgs e)
        {
            try
            {
                int stage_value = int.Parse(Panel3SelectSatge.SelectedItem.ToString());
                int index = Panel3List.SelectedIndex;
                if (stage_value % 10 == 0)
                {
                    Panel3List.Items.Remove(Panel3List.SelectedItem.ToString());
                    if (index < Panel3List.Items.Count)
                    {
                        Panel3List.SelectedIndex = index;
                    }
                    MessageBox.Show("删除成功", "信息提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else
                {
                    MessageBox.Show("选择的关卡非整十关卡", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            catch
            {
                MessageBox.Show("请选择奖励后再执行删除", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void Panel3Add_Click(object sender, EventArgs e)
        {
            try
            {
                int stage_value = int.Parse(Panel3SelectSatge.SelectedItem.ToString());
                if (stage_value % 10 == 0)
                {
                    if (Panel3List.Items.Contains(Panel3AllList.SelectedItem.ToString()))
                    {
                        MessageBox.Show("请不要重复添加", "信息提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                    else
                    {
                        Panel3List.Items.Add(Panel3AllList.SelectedItem.ToString());
                        MessageBox.Show("添加成功", "信息提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                }
                else
                {
                    MessageBox.Show("选择的关卡非整十关卡", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            catch
            {
                MessageBox.Show("请选择奖励后再执行删除", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
