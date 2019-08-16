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
        public HangRewardView(MainForm main, string hang_reward_path)
        {
            InitializeComponent();
            StartPosition = FormStartPosition.CenterScreen;
            this.main = main;
            StreamReader stream = File.OpenText(hang_reward_path);
            JsonTextReader reader = new JsonTextReader(stream);
            public_json_data = (JObject)JToken.ReadFrom(reader);
            stream.Close();
            reader.Close();
            foreach(var item in public_json_data)
            {
                HangStageSelect.Items.Add(item.Key);
            }
        }

        private void HangRewardView_FormClosing(object sender, FormClosingEventArgs e)
        {
            main.Show();
        }

        private void HangStageSelect_SelectedIndexChanged(object sender, EventArgs e)
        {
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

        private void DelSatge_Click(object sender, EventArgs e)
        {
            try
            {
                public_json_data.Remove(HangStageSelect.SelectedItem.ToString());
                HangStageSelect.Items.Remove(HangStageSelect.SelectedItem.ToString());
                MessageBox.Show("删除成功", "消息提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch (NullReferenceException)
            {
                MessageBox.Show("未选择关卡，请选择关卡数", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
