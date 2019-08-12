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
        JArray array;
        JObject json;
        string path;
        ComboBox comboBox;
        public MonsterAdd(JArray array, JObject json, string path, ComboBox comboBox)
        {
            InitializeComponent();
            this.array = array;
            this.json = json;
            this.path = path;
            this.comboBox = comboBox;
        }

        private void Button1_Click(object sender, EventArgs e)
        {
            try
            {
                array.Add(JObject.Parse("{'count': " + MonstersNumber.Value.ToString() + ",'enemysPrefString': '" + MonstersName.SelectedItem.ToString() + "'}" ));
                File.WriteAllText(path, json.ToString());
                comboBox.Items.Add(MonstersName.SelectedItem.ToString());
                Close();
                MessageBox.Show(text: "关卡添加成功！", caption: "消息提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch
            {
                MessageBox.Show(text: "没有选择怪物类型！", caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void Button2_Click(object sender, EventArgs e)
        {
            Close();
        }
    }
}
