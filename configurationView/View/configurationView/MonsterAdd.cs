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
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace configurationView
{
    public partial class MonsterAdd : Form
    {
        string monster_path = MainForm.main_path + "monster_list.json";
        JArray array;
        JObject json;
        string path;
        ComboBox comboBox;
        public MonsterAdd(JArray array, JObject json, string path, ComboBox comboBox)
        {
            InitializeComponent();
            StartPosition = FormStartPosition.CenterScreen;
            this.array = array;
            this.json = json;
            this.path = path;
            this.comboBox = comboBox;

            StreamReader stream = File.OpenText(monster_path);
            JsonTextReader reader = new JsonTextReader(stream);
            JObject monster = (JObject)JToken.ReadFrom(reader);
            MonstersName.Items.Clear();
            foreach (var mon in monster["monsters"])
            {
                MonstersName.Items.Add(item: mon.ToString());
            }
            stream.Close();
            reader.Close();
        }

        private void Button1_Click(object sender, EventArgs e)
        {
            try
            {
                string monsters_name = MonstersName.SelectedItem.ToString();
                bool IsAdd = true;
                foreach(var monster in array)
                {
                    if (monsters_name.Equals(monster["enemysPrefString"].ToString()))
                    {
                        IsAdd = false;
                        MessageBox.Show("怪物" + monsters_name + "已经存在配置文件中", "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        break;
                    }
                }
                if (IsAdd)
                {
                    array.Add(JObject.Parse("{'count': " + MonstersNumber.Value.ToString() + ",'enemysPrefString': '" + monsters_name + "'}"));
                    File.WriteAllText(path, json.ToString());
                    comboBox.Items.Add(MonstersName.SelectedItem.ToString());
                    Dispose();
                    MessageBox.Show(text: "怪物添加成功！", caption: "消息提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
            catch
            {
                MessageBox.Show(text: "没有选择怪物类型！", caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void Button2_Click(object sender, EventArgs e)
        {
            Dispose();
        }
    }
}
