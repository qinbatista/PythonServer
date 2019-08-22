using Microsoft.VisualBasic;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace configurationView
{
    public partial class HangRewardView : Form
    {
        MainForm main;
        JObject public_json_data;
        JArray array;
        string hang_reward_path;
        public HangRewardView(MainForm main, string hang_reward_path, string version_str)
        {
            InitializeComponent();
            StartPosition = FormStartPosition.CenterScreen;
            this.main = main;
            this.hang_reward_path = hang_reward_path;
            title.Text += "(" + version_str + ")";
            StreamReader stream = File.OpenText(hang_reward_path);
            JsonTextReader reader = new JsonTextReader(stream);
            public_json_data = (JObject)JToken.ReadFrom(reader);
            stream.Close();
            reader.Close();
            foreach(var item in public_json_data)
            {
                HangStageSelect.Items.Add(int.Parse(item.Key));
            }
        }

        private void HangRewardView_FormClosing(object sender, FormClosingEventArgs e)
        {
            main.Show();
        }

        private void HangStageSelect_SelectedIndexChanged(object sender, EventArgs e)
        {
            HangClear();
            foreach (var item in (JObject)public_json_data[HangStageSelect.SelectedItem.ToString()])
            {
                switch (item.Key)
                {
                    case "small_energy_potion":
                        {
                            SmallEnergyPotion.Checked = true;
                            SmallEnergyPotionValue.Value = (decimal)item.Value;
                        }
                        break;
                    case "coin":
                        {
                            Coin.Checked = true;
                            CoinValue.Value = (decimal)item.Value;
                        }
                        break;
                    case "iron":
                        {
                            Iron.Checked = true;
                            IronValue.Value = (decimal)item.Value;
                        }
                        break;
                    // 下面的属于特殊类型such as ==> key:[value, probability]
                    case "basic_summon_scroll": // 基础抽卷轴
                        {
                            array = (JArray)item.Value;
                            BasicScrollC.Checked = true;
                            BasicScrollCValue.Value = (decimal)array[0];
                            BasicScrollCProbability.Value = (decimal)array[1];
                        }
                        break;
                    case "pro_summon_scroll": // 高级抽卷轴
                        {
                            array = (JArray)item.Value;
                            ProScrollC.Checked = true;
                            ProScrollCValue.Value = (decimal)array[0];
                            ProScrollCProbability.Value = (decimal)array[1];
                        }
                        break;
                    case "prophet_summon_scroll": // 先知抽卷轴
                        {
                            array = (JArray)item.Value;
                            ProphetScrollC.Checked = true;
                            ProphetScrollCValue.Value = (decimal)array[0];
                            ProphetScrollCProbability.Value = (decimal)array[1];
                        }
                        break;
                    case "skill_scroll_10": // 低级卷轴
                        {
                            array = (JArray)item.Value;
                            Hang10Scroll.Checked = true;
                            Hang10ScrollValue.Value = (decimal)array[0];
                            Hang10ScrollProbability.Value = (decimal)array[1];
                        }
                        break;
                    case "skill_scroll_30": // 中级卷轴
                        {
                            array = (JArray)item.Value;
                            Hang30Scroll.Checked = true;
                            Hang30ScrollValue.Value = (decimal)array[0];
                            Hang30ScrollProbability.Value = (decimal)array[1];
                        }
                        break;
                    case "skill_scroll_100": // 高级卷轴
                        {
                            array = (JArray)item.Value;
                            Hang100Scroll.Checked = true;
                            Hang100ScrollValue.Value = (decimal)array[0];
                            Hang100ScrollProbability.Value = (decimal)array[1];
                        }
                        break;
                }
            }
        }

        private void HangClear()
        {
            SmallEnergyPotion.Checked = false;
            SmallEnergyPotionValue.Value = 0;
            Coin.Checked = false;
            CoinValue.Value = 0;
            Iron.Checked = false;
            IronValue.Value = 0;
            BasicScrollC.Checked = false;
            BasicScrollCValue.Value = 0;
            BasicScrollCProbability.Value = 0;
            ProScrollC.Checked = false;
            ProScrollCValue.Value = 0;
            ProScrollCProbability.Value = 0;
            ProphetScrollC.Checked = false;
            ProphetScrollCValue.Value = 0;
            ProphetScrollCProbability.Value = 0;
            Hang10Scroll.Checked = false;
            Hang10ScrollValue.Value = 0;
            Hang10ScrollProbability.Value = 0;
            Hang30Scroll.Checked = false;
            Hang30ScrollValue.Value = 0;
            Hang30ScrollProbability.Value = 0;
            Hang100Scroll.Checked = false;
            Hang100ScrollValue.Value = 0;
            Hang100ScrollProbability.Value = 0;
        }

        private void DelSatge_Click(object sender, EventArgs e)
        {
            try
            {
                public_json_data.Remove(HangStageSelect.SelectedItem.ToString());
                HangStageSelect.Items.RemoveAt(HangStageSelect.SelectedIndex);
                HangClear();
                MessageBox.Show("删除成功", "消息提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch (NullReferenceException)
            {
                MessageBox.Show("未选择关卡，请选择关卡数", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void AddSatge_Click(object sender, EventArgs e)
        {
            try
            {
                int stage = int.Parse(Interaction.InputBox("请输入需要添加的关卡数，关卡数必须为正整数", "输入关卡数", ""));
                if (stage <= 0)
                {
                    MessageBox.Show("关卡数必须为正整数", "信息提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else if (HangStageSelect.Items.Contains(stage))
                {
                    MessageBox.Show("此关卡已存在", "信息提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else
                {
                    HangStageSelect.Items.Add(stage);
                    public_json_data.Add(stage.ToString(), JObject.Parse("{}"));
                    MessageBox.Show("关卡添加成功", "信息提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
            catch (FormatException)
            {
                MessageBox.Show(text: "请输入正整数", caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void HangSave_Click(object sender, EventArgs e)
        {
            try
            {
                JObject stage_data = JObject.Parse("{}");
                if (SmallEnergyPotion.Checked) { stage_data.Add("small_energy_potion", (int)SmallEnergyPotionValue.Value); }
                if (Coin.Checked) { stage_data.Add("coin", (int)CoinValue.Value); }
                if (Iron.Checked) { stage_data.Add("iron", (int)IronValue.Value); }
                if (BasicScrollC.Checked)
                {
                    array = JArray.Parse(string.Format("[{0}, {1}]", BasicScrollCValue.Value, BasicScrollCProbability.Value));
                    stage_data.Add("basic_summon_scroll", array);
                }
                if (ProScrollC.Checked)
                {
                    array = JArray.Parse(string.Format("[{0}, {1}]", ProScrollCValue.Value, ProScrollCProbability.Value));
                    stage_data.Add("pro_summon_scroll", array);
                }
                if (ProphetScrollC.Checked)
                {
                    array = JArray.Parse(string.Format("[{0}, {1}]", ProphetScrollCValue.Value, ProphetScrollCProbability.Value));
                    stage_data.Add("prophet_summon_scroll", array);
                }
                if (Hang10Scroll.Checked)
                {
                    array = JArray.Parse(string.Format("[{0}, {1}]", Hang10ScrollValue.Value, Hang10ScrollProbability.Value));
                    stage_data.Add("skill_scroll_10", array);
                }
                if (Hang30Scroll.Checked)
                {
                    array = JArray.Parse(string.Format("[{0}, {1}]", Hang30ScrollValue.Value, Hang30ScrollProbability.Value));
                    stage_data.Add("skill_scroll_30", array);
                }
                if (Hang100Scroll.Checked)
                {
                    array = JArray.Parse(string.Format("[{0}, {1}]", Hang100ScrollValue.Value, Hang100ScrollProbability.Value));
                    stage_data.Add("skill_scroll_100", array);
                }
                public_json_data[HangStageSelect.SelectedItem.ToString()] = stage_data;
            }
            catch (NullReferenceException) { }
            File.WriteAllText(hang_reward_path, public_json_data.ToString());
            MessageBox.Show("保存成功", "信息提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void HangClose_Click(object sender, EventArgs e)
        {
            main.Close();
        }
    }
}
